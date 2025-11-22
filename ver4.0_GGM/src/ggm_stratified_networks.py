import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
from scipy import stats
from scipy.spatial.distance import squareform
from sklearn.covariance import graphical_lasso
from sklearn.model_selection import KFold
from networkx.algorithms import community as nx_community
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

# Paths
BASE_DIR = Path('/Users/heejeong/Library/CloudStorage/GoogleDrive-hhj2831@gmail.com/내 드라이브/#인력양성/3. 식이_SNUH/#Network/ver4.0_GGM')
DATA_FILE = BASE_DIR / 'db' / 'total_only_org.csv'
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
    df = pd.read_csv(DATA_FILE)
    print(f"Loaded {len(df):,} samples")
    
    def categorize_age(age):
        if age < 40:
            return '청년층(19-39세)'
        elif age < 60:
            return '중년층(40-59세)'
        else:
            return '장년층(60-74세)'
    
    df['Age_Group'] = df['Age'].apply(categorize_age)
    df['MetS_Status'] = df['MetS'].apply(lambda x: 'MetS(+)' if x == 1 else 'MetS(-)')
    
    print(f"Created Age_Group and MetS_Status columns")    
    return df

# ============================================================================
# GGM Core Functions
# ============================================================================

def nonparanormal_skeptic_transform(X):
    n_samples, n_features = X.shape
    Z = np.zeros_like(X, dtype=float)
    
    for j in range(n_features):
        # Step 1: Rank transformation
        ranks = np.argsort(np.argsort(X[:, j])) + 1
        
        # Step 2: Empirical CDF with Winsorization
        F_hat = (ranks - 0.5) / n_samples
        
        # Step 3: Quantile transformation
        Z[:, j] = stats.norm.ppf(F_hat)
    
    return Z

def nonparanormal_correlation_matrix(data):
    X = data.values

    Z = nonparanormal_skeptic_transform(X)
    corr_matrix = np.corrcoef(Z.T)

    return corr_matrix

def graphical_lasso_cv_loglik(X, corr_matrix, alphas=None, cv_folds=5):
    n_samples, n_features = X.shape    
    kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
    cv_scores = np.zeros(len(alphas))
    
    for alpha_idx, alpha in enumerate(alphas):
        fold_scores = []
        
        for fold_idx, (train_idx, test_idx) in enumerate(kf.split(X)):
            try:
                X_train = X[train_idx]
                X_test = X[test_idx]
                
                # Train: Compute Spearman correlation on training data
                train_corr = np.corrcoef(X_train.T)
                
                # Ensure positive definite
                train_corr = train_corr + np.eye(n_features) * 1e-6
                
                # Fit Graphical Lasso on training data
                _, precision_train = graphical_lasso(train_corr, alpha=alpha, max_iter=100)
                
                # Test: Compute log-likelihood on test data
                test_corr = np.corrcoef(X_test.T)
                test_corr = test_corr + np.eye(n_features) * 1e-6
                
                # Log-likelihood: log det(Θ) - tr(S_test * Θ)
                sign, logdet = np.linalg.slogdet(precision_train)
                if sign > 0:
                    log_lik = logdet - np.trace(test_corr @ precision_train)
                    fold_scores.append(log_lik)
                
            except Exception as e:
                continue
        
        # Average log-likelihood across folds
        if len(fold_scores) > 0:
            cv_scores[alpha_idx] = np.mean(fold_scores)
        else:
            cv_scores[alpha_idx] = -np.inf
    
    # Select alpha with best (highest) log-likelihood
    valid_indices = np.where(np.isfinite(cv_scores))[0]
    
    if len(valid_indices) == 0:
        best_alpha = alphas[0]
    else:
        best_idx = valid_indices[np.argmax(cv_scores[valid_indices])]
        best_alpha = alphas[best_idx]
            
    # Fit final model on full data
    cov_matrix = corr_matrix.copy()
    try:
        _, best_precision = graphical_lasso(cov_matrix, alpha=best_alpha, max_iter=100)
    except:
        # Fallback
        best_alpha = 0.01
        _, best_precision = graphical_lasso(cov_matrix, alpha=best_alpha, max_iter=100)
    
    # Count edges
    n_edges = (np.sum(np.abs(best_precision) > 1e-4) - n_features) // 2
    
    print(f"   Final model: {n_edges} edges")
    
    # Convert precision matrix to partial correlation matrix
    partial_corr = np.zeros_like(best_precision)
    for i in range(n_features):
        for j in range(n_features):
            if i == j:
                partial_corr[i, j] = 1.0
            else:
                denom = np.sqrt(best_precision[i, i] * best_precision[j, j])
                if denom > 0:
                    partial_corr[i, j] = -best_precision[i, j] / denom
    
    return best_alpha, best_precision, partial_corr

def graphical_lasso_stars(X, corr_matrix, alphas=None, n_subsample=20, subsample_ratio=0.8, beta=0.1):
    n_samples, n_features = X.shape
    subsample_size = int(n_samples * subsample_ratio)
    
    print(f"  🔍 StARS with {n_subsample} subsamples, testing {len(alphas)} alphas...")
    
    instabilities = []
    
    for alpha_idx, alpha in enumerate(alphas):
        edge_matrices = []
        
        for subsample_idx in range(n_subsample):
            try:
                # Random subsample without replacement
                np.random.seed(42 + subsample_idx)
                subsample_indices = np.random.choice(n_samples, size=subsample_size, replace=False)
                X_sub = X[subsample_indices]
                
                # Compute correlation on subsample
                sub_corr = np.corrcoef(X_sub.T)
                sub_corr = sub_corr + np.eye(n_features) * 1e-6
                
                # Fit Graphical Lasso
                _, precision_sub = graphical_lasso(sub_corr, alpha=alpha, max_iter=100)
                
                # Extract edge presence (binary matrix)
                edges = (np.abs(precision_sub) > 1e-4).astype(int)
                np.fill_diagonal(edges, 0)  # Exclude diagonal
                edge_matrices.append(edges)
                
            except Exception as e:
                print(f"      Alpha {alpha:.4f} subsample {subsample_idx+1} failed")
                continue
        
        if len(edge_matrices) == 0:
            instabilities.append(np.inf)
            continue
        
        # Calculate instability
        edge_matrices = np.array(edge_matrices)  # (n_subsample, p, p)
        edge_probs = np.mean(edge_matrices, axis=0)  # Probability of each edge
        edge_variability = 2 * edge_probs * (1 - edge_probs)
        
        # Total instability: average variability over all edges (upper triangle)
        upper_tri_indices = np.triu_indices(n_features, k=1)
        total_instability = np.mean(edge_variability[upper_tri_indices])
        
        instabilities.append(total_instability)
    
    instabilities = np.array(instabilities)
    
    # Select largest alpha (most sparse) with instability ≤ beta
    valid_indices = np.where(instabilities <= beta)[0]
    
    if len(valid_indices) == 0:
        # If all too unstable, select alpha with minimum instability
        best_idx = np.argmin(instabilities)
        best_alpha = alphas[best_idx]
        print(f"    No stable solution (β={beta}), using min instability: {best_alpha:.4f}")
    else:
        # Select largest alpha (most regularization) that is stable
        best_idx = valid_indices[-1]  # Largest alpha among valid ones
        best_alpha = alphas[best_idx]
        
        print(f"  Best alpha by StARS: {best_alpha:.4f} (instability={instabilities[best_idx]:.4f})")
    
    # Fit final model on full data
    cov_matrix = corr_matrix.copy()
    try:
        _, best_precision = graphical_lasso(cov_matrix, alpha=best_alpha, max_iter=100)
    except:
        best_alpha = 0.01
        _, best_precision = graphical_lasso(cov_matrix, alpha=best_alpha, max_iter=100)
    
    # Count edges
    n_edges = (np.sum(np.abs(best_precision) > 1e-4) - n_features) // 2
    
    print(f"   Final model: {n_edges} edges")
    
    # Convert to partial correlation
    partial_corr = np.zeros_like(best_precision)
    for i in range(n_features):
        for j in range(n_features):
            if i == j:
                partial_corr[i, j] = 1.0
            else:
                denom = np.sqrt(best_precision[i, i] * best_precision[j, j])
                if denom > 0:
                    partial_corr[i, j] = -best_precision[i, j] / denom
    
    return best_alpha, best_precision, partial_corr


def create_ggm_network(data, food_groups, min_correlation=0.1, cv_method='5fold'):
    print(f"\n   Creating GGM network for {len(data)} samples...")
    
    # Extract food group data
    X = data[food_groups].copy()
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Convert to numpy array
    X_array = X.values
    
    # Step 1: Nonparanormal transformation
    corr_matrix = nonparanormal_correlation_matrix(X)
    
    # Step 2: Graphical Lasso (cross-validated)
    alphas = np.logspace(-3.5, -1, 20) 
    if cv_method == 'stars':
        best_alpha, _, partial_corr = graphical_lasso_stars(
            X_array,
            corr_matrix, 
            alphas=alphas,
            n_subsample=50,
            subsample_ratio=0.8,
            beta=0.15,
        )
    else:
        best_alpha, _, partial_corr = graphical_lasso_cv_loglik(
            X_array,
            corr_matrix, 
            alphas=alphas,
            cv_folds=5,
        )
    
    # Step 3: Create NetworkX graph
    G = nx.Graph()
    
    for food in food_groups:
        G.add_node(food)
    
    n_edges = 0
    for i, food1 in enumerate(food_groups):
        for j, food2 in enumerate(food_groups):
            if i < j:
                partial_corr_value = partial_corr[i, j]
                
                if abs(partial_corr_value) >= min_correlation:
                    G.add_edge(food1, food2, weight=abs(partial_corr_value), partial_corr=partial_corr_value)
                    n_edges += 1
    
    density = nx.density(G)

    return G, best_alpha, partial_corr

# ============================================================================
# Network Analysis
# ============================================================================

def detect_communities(G, method='louvain'):
    if G.number_of_edges() == 0:
        return [{node} for node in G.nodes()], 0.0
    
    try:
        if method == 'louvain':
            communities = nx_community.louvain_communities(G, weight='weight', seed=42)
        elif method == 'label_propagation':
            communities = list(nx_community.label_propagation_communities(G))
        else:
            raise ValueError(f"Unknown method: {method}")
        
        modularity = nx_community.modularity(G, communities, weight='weight')
        
        return communities, modularity
        
    except Exception as e:
        print(f"      Community detection failed: {str(e)}")
        return [{node} for node in G.nodes()], 0.0

def analyze_communities(G, communities, modularity):
    n_communities = len(communities)
    
    print(f"\n    Community Detection Results:")
    print(f"    Number of communities: {n_communities}")
    print(f"    Modularity: {modularity:.4f}")
    
    # Analyze each community
    community_info = []
    for i, comm in enumerate(communities, 1):
        comm_size = len(comm)
        comm_nodes = sorted(list(comm))
        
        # Calculate internal edges (within community)
        internal_edges = 0
        for u in comm:
            for v in comm:
                if u < v and G.has_edge(u, v):
                    internal_edges += 1
        
        # Calculate internal density
        max_internal_edges = comm_size * (comm_size - 1) / 2
        internal_density = internal_edges / max_internal_edges if max_internal_edges > 0 else 0
        
        print(f"    Community {i}: {comm_size} nodes, {internal_edges} edges (density: {internal_density:.3f})")
        print(f"    Foods: {', '.join(comm_nodes)}")
        
        community_info.append({
            'community_id': i,
            'size': comm_size,
            'nodes': comm_nodes,
            'internal_edges': internal_edges,
            'internal_density': internal_density
        })
    
    return {
        'n_communities': n_communities,
        'modularity': modularity,
        'communities': community_info
    }

def analyze_network_centrality(G):
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
    
    print(f"\n  🎯 Top 3 hubs by degree centrality:")
    top_3 = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (node, cent) in enumerate(top_3, 1):
        print(f"    {i}. {node}: {cent:.4f}")
    
    return centrality_dict

def save_network_results(G, sex, age_group, mets_status, alpha, partial_corr_matrix, community_stats=None):
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
    
    # 3. Save community information if available
    if community_stats is not None:
        community_file = OUTPUT_DIR / f"{base_filename}_communities.csv"
        community_df = pd.DataFrame(community_stats['communities'])
        community_df['nodes'] = community_df['nodes'].apply(lambda x: '; '.join(x))
        community_df.to_csv(community_file, index=False)
    
    # 4. Save network statistics
    stats = {
        'n_nodes': G.number_of_nodes(),
        'n_edges': G.number_of_edges(),
        'density': nx.density(G),
        'alpha': alpha
    }
    
    if community_stats is not None:
        stats['n_communities'] = community_stats['n_communities']
        stats['modularity'] = community_stats['modularity']
    
    return gexf_file, csv_file, stats

# ============================================================================
# Main Processing
# ============================================================================

def process_all_groups(df, cv_method='5fold'):
    results = []
    
    for sex, age_group, mets_status, expected_n in GROUPS:
        sex_display = SEX_DISPLAY[sex]
        print(f" Processing: {sex_display} - {age_group} - {mets_status}")
        
        mask = (df['Sex'] == sex) & (df['Age_Group'] == age_group) & (df['MetS_Status'] == mets_status)
        group_data = df[mask].copy()
        
        n_samples = len(group_data)
        if n_samples < 100:
            print(f"  Sample size too small, skipping...")
            continue
        
        # Create GGM network
        G, alpha, partial_corr = create_ggm_network(
            group_data, 
            FOOD_GROUPS, 
            min_correlation=0.05,
            cv_method=cv_method,
        )
        
        # Analyze centrality
        centrality = analyze_network_centrality(G)
        
        # Get top 3 hubs by degree centrality
        degree_cents = {node: metrics['degree'] for node, metrics in centrality.items()}
        top_hubs = sorted(degree_cents.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Detect communities
        communities, modularity = detect_communities(G, method='louvain')
        community_stats = analyze_communities(G, communities, modularity)
        
        # Save results
        gexf_file, csv_file, stats = save_network_results(
            G, sex, age_group, mets_status, alpha, partial_corr, community_stats
        )
        
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
            'N_Communities': stats.get('n_communities', 0),
            'Modularity': stats.get('modularity', 0),
            'Hub_1_Name': top_hubs[0][0] if len(top_hubs) > 0 else 'None',
            'Hub_1_Degree': top_hubs[0][1] if len(top_hubs) > 0 else 0,
            'Hub_2_Name': top_hubs[1][0] if len(top_hubs) > 1 else 'None',
            'Hub_2_Degree': top_hubs[1][1] if len(top_hubs) > 1 else 0,
            'Hub_3_Name': top_hubs[2][0] if len(top_hubs) > 2 else 'None',
            'Hub_3_Degree': top_hubs[2][1] if len(top_hubs) > 2 else 0,
        })
        
    return pd.DataFrame(results)

def main(cv_method='5fold'):
    df = load_data()
    
    results_df = process_all_groups(df, cv_method=cv_method)
    
    if len(results_df) > 0:
        stats_file = OUTPUT_DIR / 'ggm_network_summary.csv'
        results_df.to_csv(stats_file, index=False)
        print(f"\nSaved summary statistics: {stats_file}")
        
    else:
        print("\n❌ No networks were successfully created!")

if __name__ == "__main__":
    cv_method = 'stars'  # Options: '5fold' or 'stars'
    main(cv_method=cv_method)
