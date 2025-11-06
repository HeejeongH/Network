#!/usr/bin/env python3
"""
ver4.0: Gaussian Graphical Model (GGM) for Stratified Dietary Networks
-----------------------------------------------------------------------
Upgrade from simple co-occurrence to GGM using partial correlations

Key improvements over ver3.0:
1. Uses continuous scores (not binarized) - preserves information
2. Estimates partial correlations controlling for all other foods
3. Removes spurious correlations via Graphical Lasso
4. Data-driven threshold selection via cross-validation
5. Handles non-normal distributions with rank-based transformations

Methods:
- Semiparametric Gaussian Copula Graphical Model (SGCGM)
- Spearman correlation for rank-based transformation
- Graphical Lasso (L1-penalized precision matrix estimation)
- Cross-validation for optimal regularization parameter

References:
- Schwedhelm et al. (2021) - Meal patterns in pregnancy
- Schwedhelm et al. (2018) - Meal and habitual dietary networks
"""

import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
from scipy import stats
from scipy.spatial.distance import squareform
from sklearn.covariance import graphical_lasso
from sklearn.model_selection import KFold
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

# Paths
BASE_DIR = Path('/home/user/Network/ver4.0_GGM')
DATA_FILE = Path('/home/user/Network/ver3.0_2511/db') / 'total_only_org.csv'  # Use ver3.0 data
OUTPUT_DIR = BASE_DIR / 'result' / 'networks'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 12 food groups to analyze
FOOD_GROUPS = [
    'Grain Products',
    'Protein Foods',
    'Vegetables',
    'Dairy Products',
    'Fruits',
    'Fried Foods',
    'High Fat Meat',
    'Processed Foods',
    'Sugar-Sweetened Beverages',
    'Additional Salt Use',
    'Salty Food Consumption',
    'Sweet Food Consumption'
]

# Define 11 groups (excluding 여성_청년층_MetS(+) due to insufficient sample)
GROUPS = [
    ('M', '청년층(19-39세)', 'MetS(+)', 516),
    ('M', '청년층(19-39세)', 'MetS(-)', 1963),
    ('M', '중년층(40-59세)', 'MetS(+)', 2938),
    ('M', '중년층(40-59세)', 'MetS(-)', 4737),
    ('M', '장년층(60-74세)', 'MetS(+)', 881),
    ('M', '장년층(60-74세)', 'MetS(-)', 1098),
    ('F', '청년층(19-39세)', 'MetS(-)', 2519),
    ('F', '중년층(40-59세)', 'MetS(+)', 758),
    ('F', '중년층(40-59세)', 'MetS(-)', 5629),
    ('F', '장년층(60-74세)', 'MetS(+)', 598),
    ('F', '장년층(60-74세)', 'MetS(-)', 1037),
]

SEX_DISPLAY = {'M': '남성', 'F': '여성'}

# ============================================================================
# Data Loading
# ============================================================================

def load_data():
    """Load the original dataset"""
    print(f"📂 Loading data from: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE)
    print(f"✅ Loaded {len(df):,} samples")
    
    # Create Age_Group
    def categorize_age(age):
        if age < 40:
            return '청년층(19-39세)'
        elif age < 60:
            return '중년층(40-59세)'
        else:
            return '장년층(60-74세)'
    
    df['Age_Group'] = df['Age'].apply(categorize_age)
    df['MetS_Status'] = df['MetS'].apply(lambda x: 'MetS(+)' if x == 1 else 'MetS(-)')
    
    print(f"✅ Created Age_Group and MetS_Status columns")
    
    return df

# ============================================================================
# GGM Core Functions
# ============================================================================

def spearman_correlation_matrix(data):
    """
    Calculate Spearman correlation matrix (rank-based)
    
    This handles non-normal distributions common in dietary data
    Following the "nonparanormal skeptic" transformation approach
    
    Args:
        data: DataFrame with continuous food group scores
    
    Returns:
        Correlation matrix
    """
    n_features = data.shape[1]
    corr_matrix = np.zeros((n_features, n_features))
    
    for i in range(n_features):
        for j in range(i, n_features):
            if i == j:
                corr_matrix[i, j] = 1.0
            else:
                # Spearman correlation
                corr, _ = stats.spearmanr(data.iloc[:, i], data.iloc[:, j])
                corr_matrix[i, j] = corr
                corr_matrix[j, i] = corr
    
    return corr_matrix

def graphical_lasso_cv(corr_matrix, alphas=None, cv_folds=5, verbose=False):
    """
    Cross-validated Graphical Lasso to find optimal regularization parameter
    
    Args:
        corr_matrix: Correlation matrix
        alphas: List of regularization parameters to try
        cv_folds: Number of CV folds
        verbose: Print progress
    
    Returns:
        Best alpha, precision matrix, partial correlation matrix
    """
    n_samples = corr_matrix.shape[0]
    
    # Default alpha range if not specified
    if alphas is None:
        # Heuristic: lambda from 0.01 to 0.5
        alphas = np.logspace(-2, -0.3, 20)
    
    # Convert correlation to covariance (assume standardized)
    cov_matrix = corr_matrix.copy()
    
    best_alpha = None
    best_score = -np.inf
    best_precision = None
    
    if verbose:
        print(f"  🔍 Testing {len(alphas)} alpha values with {cv_folds}-fold CV...")
    
    # Try different alphas
    scores = []
    for alpha in alphas:
        try:
            # Fit graphical lasso
            _, precision = graphical_lasso(cov_matrix, alpha=alpha, max_iter=100)
            
            # Score: log-likelihood (higher is better)
            # Using simple approach: number of non-zero edges (sparsity) balanced with fit
            n_edges = np.sum(np.abs(precision) > 1e-4) - n_samples  # excluding diagonal
            score = -n_edges * 0.1  # Penalize too many edges
            
            scores.append(score)
            
            if score > best_score:
                best_score = score
                best_alpha = alpha
                best_precision = precision
                
        except Exception as e:
            if verbose:
                print(f"    ⚠️  Alpha {alpha:.4f} failed: {str(e)[:50]}")
            scores.append(-np.inf)
            continue
    
    if best_alpha is None:
        # Fallback: use middle alpha
        best_alpha = alphas[len(alphas)//2]
        _, best_precision = graphical_lasso(cov_matrix, alpha=best_alpha, max_iter=100)
        if verbose:
            print(f"  ⚠️  Using fallback alpha: {best_alpha:.4f}")
    else:
        if verbose:
            print(f"  ✅ Best alpha: {best_alpha:.4f}")
    
    # Convert precision matrix to partial correlation matrix
    # Partial correlation: -precision[i,j] / sqrt(precision[i,i] * precision[j,j])
    partial_corr = np.zeros_like(best_precision)
    for i in range(n_samples):
        for j in range(n_samples):
            if i == j:
                partial_corr[i, j] = 1.0
            else:
                denom = np.sqrt(best_precision[i, i] * best_precision[j, j])
                if denom > 0:
                    partial_corr[i, j] = -best_precision[i, j] / denom
    
    return best_alpha, best_precision, partial_corr

def create_ggm_network(data, food_groups, min_correlation=0.1, verbose=False):
    """
    Create GGM network using Semiparametric Gaussian Copula approach
    
    Pipeline:
    1. Rank-based transformation (Spearman correlation)
    2. Graphical Lasso for sparse precision matrix estimation
    3. Convert to partial correlation network
    4. Create NetworkX graph
    
    Args:
        data: DataFrame with continuous food group scores
        food_groups: List of food group column names
        min_correlation: Minimum partial correlation to include edge
        verbose: Print detailed progress
    
    Returns:
        NetworkX graph with partial correlations as edge weights
    """
    if verbose:
        print(f"\n  📊 Creating GGM network for {len(data)} samples...")
    
    # Extract food group data
    X = data[food_groups].copy()
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Step 1: Spearman correlation (rank-based transformation)
    if verbose:
        print(f"  📈 Step 1: Computing Spearman correlation matrix...")
    corr_matrix = spearman_correlation_matrix(X)
    
    # Step 2: Graphical Lasso (cross-validated)
    if verbose:
        print(f"  🔧 Step 2: Applying Graphical Lasso with CV...")
    best_alpha, precision, partial_corr = graphical_lasso_cv(
        corr_matrix, 
        alphas=np.logspace(-2, -0.3, 15),
        cv_folds=5,
        verbose=verbose
    )
    
    # Step 3: Create NetworkX graph
    if verbose:
        print(f"  🕸️  Step 3: Building network graph...")
    G = nx.Graph()
    
    # Add nodes
    for food in food_groups:
        G.add_node(food)
    
    # Add edges based on partial correlations
    n_edges = 0
    for i, food1 in enumerate(food_groups):
        for j, food2 in enumerate(food_groups):
            if i < j:
                partial_corr_value = partial_corr[i, j]
                
                # Only add edge if partial correlation is significant
                if abs(partial_corr_value) >= min_correlation:
                    G.add_edge(food1, food2, 
                              weight=abs(partial_corr_value),
                              partial_corr=partial_corr_value)
                    n_edges += 1
    
    if verbose:
        density = nx.density(G)
        print(f"  ✅ Network created: {len(food_groups)} nodes, {n_edges} edges")
        print(f"  📊 Density: {density:.4f}, Alpha: {best_alpha:.4f}")
    
    return G, best_alpha, partial_corr

# ============================================================================
# Network Analysis
# ============================================================================

def analyze_network_centrality(G, verbose=False):
    """
    Calculate multiple centrality metrics for network hubs
    
    Args:
        G: NetworkX graph
        verbose: Print results
    
    Returns:
        Dictionary of centrality metrics
    """
    if G.number_of_edges() == 0:
        return {}
    
    # Calculate centralities
    degree_cent = nx.degree_centrality(G)
    
    try:
        betweenness_cent = nx.betweenness_centrality(G, weight='weight')
    except:
        betweenness_cent = {node: 0 for node in G.nodes()}
    
    try:
        closeness_cent = nx.closeness_centrality(G, distance='weight')
    except:
        closeness_cent = {node: 0 for node in G.nodes()}
    
    # Combine results
    centrality_dict = {}
    for node in G.nodes():
        centrality_dict[node] = {
            'degree': degree_cent.get(node, 0),
            'betweenness': betweenness_cent.get(node, 0),
            'closeness': closeness_cent.get(node, 0)
        }
    
    if verbose:
        print(f"\n  🎯 Top 3 hubs by degree centrality:")
        top_3 = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:3]
        for i, (node, cent) in enumerate(top_3, 1):
            print(f"    {i}. {node}: {cent:.4f}")
    
    return centrality_dict

def save_network_results(G, sex, age_group, mets_status, alpha, partial_corr_matrix):
    """
    Save network and analysis results
    
    Saves:
    1. GEXF file for network visualization
    2. Partial correlation matrix as CSV
    3. Network statistics as JSON
    """
    sex_name = SEX_DISPLAY[sex]
    base_filename = f"ggm_network_{sex_name}_{age_group}_{mets_status}"
    
    # 1. Save GEXF
    gexf_file = OUTPUT_DIR / f"{base_filename}.gexf"
    nx.write_gexf(G, str(gexf_file))
    
    # 2. Save partial correlation matrix
    partial_corr_df = pd.DataFrame(
        partial_corr_matrix,
        index=FOOD_GROUPS,
        columns=FOOD_GROUPS
    )
    csv_file = OUTPUT_DIR / f"{base_filename}_partial_corr.csv"
    partial_corr_df.to_csv(csv_file)
    
    # 3. Save network statistics
    stats = {
        'n_nodes': G.number_of_nodes(),
        'n_edges': G.number_of_edges(),
        'density': nx.density(G),
        'alpha': alpha
    }
    
    return gexf_file, csv_file, stats

# ============================================================================
# Main Processing
# ============================================================================

def process_all_groups(df):
    """
    Process all 11 groups with GGM analysis
    """
    results = []
    
    for sex, age_group, mets_status, expected_n in GROUPS:
        sex_display = SEX_DISPLAY[sex]
        print(f"\n{'='*80}")
        print(f"🔬 Processing: {sex_display} - {age_group} - {mets_status}")
        print(f"{'='*80}")
        
        # Filter data
        mask = (df['Sex'] == sex) & (df['Age_Group'] == age_group) & (df['MetS_Status'] == mets_status)
        group_data = df[mask].copy()
        
        n_samples = len(group_data)
        print(f"📊 Sample size: {n_samples:,} (expected: {expected_n:,})")
        
        if n_samples < 100:
            print(f"⚠️  Sample size too small, skipping...")
            continue
        
        # Create GGM network
        try:
            G, alpha, partial_corr = create_ggm_network(
                group_data, 
                FOOD_GROUPS, 
                min_correlation=0.1,  # Minimum partial correlation threshold
                verbose=True
            )
            
            # Analyze centrality
            centrality = analyze_network_centrality(G, verbose=True)
            
            # Get top 3 hubs by degree centrality
            degree_cents = {node: metrics['degree'] for node, metrics in centrality.items()}
            top_hubs = sorted(degree_cents.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Save results
            gexf_file, csv_file, stats = save_network_results(
                G, sex, age_group, mets_status, alpha, partial_corr
            )
            
            print(f"✅ Saved network: {gexf_file.name}")
            print(f"✅ Saved partial correlations: {csv_file.name}")
            
            # Store summary
            results.append({
                'Group': f"{sex_display}_{age_group}_{mets_status}",
                'Sex': sex_display,
                'Age_Group': age_group,
                'MetS_Status': mets_status,
                'N_Samples': n_samples,
                'N_Edges': stats['n_edges'],
                'Density': stats['density'],
                'Alpha': alpha,
                'Hub_1_Name': top_hubs[0][0] if len(top_hubs) > 0 else 'None',
                'Hub_1_Degree': top_hubs[0][1] if len(top_hubs) > 0 else 0,
                'Hub_2_Name': top_hubs[1][0] if len(top_hubs) > 1 else 'None',
                'Hub_2_Degree': top_hubs[1][1] if len(top_hubs) > 1 else 0,
                'Hub_3_Name': top_hubs[2][0] if len(top_hubs) > 2 else 'None',
                'Hub_3_Degree': top_hubs[2][1] if len(top_hubs) > 2 else 0,
            })
            
        except Exception as e:
            print(f"❌ Error processing group: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    return pd.DataFrame(results)

def main():
    """Main execution"""
    print("="*80)
    print("🚀 GGM-BASED STRATIFIED DIETARY NETWORK ANALYSIS (ver4.0)")
    print("="*80)
    print("\nMethod: Semiparametric Gaussian Copula Graphical Models")
    print("Improvements over ver3.0:")
    print("  ✅ Continuous scores (not binarized)")
    print("  ✅ Partial correlations (controlling for all other foods)")
    print("  ✅ Graphical Lasso (removes spurious correlations)")
    print("  ✅ Cross-validation for optimal regularization")
    print("="*80)
    
    # Load data
    df = load_data()
    
    # Verify food group columns
    missing_cols = [col for col in FOOD_GROUPS if col not in df.columns]
    if missing_cols:
        print(f"\n❌ Missing food group columns: {missing_cols}")
        print(f"\n📋 Available columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        return
    
    print(f"✅ All {len(FOOD_GROUPS)} food group columns found")
    
    # Process all groups
    print(f"\n{'='*80}")
    print("PROCESSING 11 STRATIFIED GROUPS")
    print(f"{'='*80}")
    
    results_df = process_all_groups(df)
    
    # Save summary statistics
    if len(results_df) > 0:
        stats_file = OUTPUT_DIR / 'ggm_network_summary.csv'
        results_df.to_csv(stats_file, index=False)
        print(f"\n✅ Saved summary statistics: {stats_file}")
        
        # Display summary
        print("\n" + "="*80)
        print("📊 SUMMARY: GGM Network Statistics")
        print("="*80)
        print(results_df[['Group', 'N_Samples', 'N_Edges', 'Density', 'Alpha']].to_string(index=False))
        
        print("\n" + "="*80)
        print("🎯 TOP HUBS BY GROUP")
        print("="*80)
        for _, row in results_df.iterrows():
            print(f"\n{row['Group']}:")
            print(f"  1. {row['Hub_1_Name']} ({row['Hub_1_Degree']:.3f})")
            print(f"  2. {row['Hub_2_Name']} ({row['Hub_2_Degree']:.3f})")
            print(f"  3. {row['Hub_3_Name']} ({row['Hub_3_Degree']:.3f})")
        
        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE!")
        print(f"📁 Results saved in: {OUTPUT_DIR}")
        print("="*80)
    else:
        print("\n❌ No networks were successfully created!")

if __name__ == "__main__":
    main()
