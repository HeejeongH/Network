#!/usr/bin/env python3
"""
Alternative Analysis: Create networks using total_only.csv (1-3-5 transformed scale)

Key difference:
- total_only_org.csv: Original scores (higher = more/frequent consumption)
- total_only.csv: Transformed scores (higher = BETTER dietary quality)
  * 1 = Poor
  * 3 = Intermediate  
  * 5 = Ideal

For this analysis:
- Use threshold ≥3 to identify "Intermediate or better" consumption
- All food groups now have unified scale (1, 3, 5)
"""

import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path('/home/user/webapp/paper2_alternative_analysis')
DATA_FILE = BASE_DIR / 'total_only.csv'
OUTPUT_DIR = BASE_DIR / 'networks'

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

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

# Define 11 groups
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

def load_data():
    """Load the transformed dataset (1-3-5 scale)"""
    print(f"📂 Loading TRANSFORMED data from: {DATA_FILE}")
    print("   (1=Poor, 3=Intermediate, 5=Ideal)")
    df = pd.read_csv(DATA_FILE, index_col=0)
    print(f"✅ Loaded {len(df):,} samples")
    
    # Verify the transformed scale
    print(f"\n🔍 Verifying transformed scale:")
    for food in FOOD_GROUPS[:3]:  # Check first 3
        unique_vals = sorted(df[food].unique())
        print(f"   {food}: {unique_vals}")
    
    # Create Age_Group
    def categorize_age(age):
        if age < 40:
            return '청년층(19-39세)'
        elif age < 60:
            return '중년층(40-59세)'
        else:
            return '장년층(60-74세)'
    
    df['Age_Group'] = df['Age'].apply(categorize_age)
    
    # Create MetS_Status
    df['MetS_Status'] = df['MetS'].apply(lambda x: 'MetS(+)' if x == 1 else 'MetS(-)')
    
    print(f"✅ Created Age_Group and MetS_Status columns\n")
    
    return df

def create_cooccurrence_network(data, food_groups, threshold_percentile=70):
    """
    Create co-occurrence network
    
    IMPORTANT: Since this uses transformed data where higher = BETTER,
    threshold ≥3 means "Intermediate or Ideal quality" (good consumption)
    """
    # Binarize: 1 if score >= 3 (Intermediate or Ideal), 0 if score = 1 (Poor)
    # This captures "adequate or better" dietary quality
    data_binary = (data[food_groups] >= 3).astype(int)
    
    # Calculate co-occurrence matrix
    n_samples = len(data_binary)
    cooccur_matrix = data_binary.T.dot(data_binary) / n_samples
    
    # Set diagonal to 0
    np.fill_diagonal(cooccur_matrix.values, 0)
    
    # Calculate threshold
    non_zero = cooccur_matrix.values[cooccur_matrix.values > 0]
    if len(non_zero) == 0:
        print("   ⚠️  Warning: No co-occurrences found")
        threshold = 0
    else:
        threshold = np.percentile(non_zero, threshold_percentile)
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes
    for food in food_groups:
        G.add_node(food)
    
    # Add edges above threshold
    edge_count = 0
    for i, food1 in enumerate(food_groups):
        for j, food2 in enumerate(food_groups):
            if i < j:
                weight = cooccur_matrix.iloc[i, j]
                if weight >= threshold:
                    G.add_edge(food1, food2, weight=weight)
                    edge_count += 1
    
    return G, edge_count

def calculate_centrality(G):
    """Calculate centrality metrics"""
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    closeness_cent = nx.closeness_centrality(G)
    
    return {
        'degree': degree_cent,
        'betweenness': betweenness_cent,
        'closeness': closeness_cent
    }

def main():
    """Main analysis pipeline"""
    print("=" * 70)
    print("🔄 ALTERNATIVE ANALYSIS: Using Transformed Scale (1-3-5)")
    print("=" * 70)
    print("\n📌 Key difference:")
    print("   - Original: Higher score = more/frequent consumption")
    print("   - Transformed: Higher score = BETTER dietary quality")
    print("   - Threshold ≥3 = Intermediate or Ideal (adequate quality)\n")
    
    # Load data
    df = load_data()
    
    # Store results
    all_results = []
    
    # Create networks for each group
    print("=" * 70)
    print("🔨 Creating Networks for 11 Groups")
    print("=" * 70)
    
    for sex, age_group, mets_status, expected_n in GROUPS:
        # Filter data
        group_data = df[
            (df['Sex'] == sex) & 
            (df['Age_Group'] == age_group) & 
            (df['MetS_Status'] == mets_status)
        ]
        
        n_samples = len(group_data)
        sex_display = SEX_DISPLAY[sex]
        group_name = f"{sex_display}_{age_group}_{mets_status}"
        
        print(f"\n📊 {group_name}")
        print(f"   Sample size: {n_samples:,}")
        
        # Create network
        G, edge_count = create_cooccurrence_network(group_data, FOOD_GROUPS)
        
        # Calculate centrality
        centrality = calculate_centrality(G)
        
        # Network metrics
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        density = nx.density(G)
        
        print(f"   Network: {n_nodes} nodes, {n_edges} edges, density={density:.3f}")
        
        # Top hubs by degree centrality
        top_hubs = sorted(centrality['degree'].items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"   Top 3 hubs:")
        for i, (food, cent) in enumerate(top_hubs, 1):
            print(f"      {i}. {food} (degree={cent:.3f})")
        
        # Save network
        output_file = OUTPUT_DIR / f"network_{group_name}.gexf"
        nx.write_gexf(G, output_file)
        
        # Store results
        all_results.append({
            'Group': group_name,
            'Sex': sex_display,
            'Age': age_group,
            'MetS': mets_status,
            'N': n_samples,
            'Nodes': n_nodes,
            'Edges': n_edges,
            'Density': density,
            'Hub1': top_hubs[0][0] if len(top_hubs) > 0 else '',
            'Hub1_Degree': top_hubs[0][1] if len(top_hubs) > 0 else 0,
            'Hub2': top_hubs[1][0] if len(top_hubs) > 1 else '',
            'Hub2_Degree': top_hubs[1][1] if len(top_hubs) > 1 else 0,
            'Hub3': top_hubs[2][0] if len(top_hubs) > 2 else '',
            'Hub3_Degree': top_hubs[2][1] if len(top_hubs) > 2 else 0,
        })
    
    # Save summary
    results_df = pd.DataFrame(all_results)
    results_file = BASE_DIR / 'network_summary_alternative.csv'
    results_df.to_csv(results_file, index=False)
    
    print("\n" + "=" * 70)
    print("✅ ALTERNATIVE ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print(f"📊 Summary file: {results_file}")
    print(f"🔢 Networks created: 11")
    
    # Display summary statistics
    print("\n📈 Summary Statistics:")
    print(f"   Average edges: {results_df['Edges'].mean():.1f}")
    print(f"   Edge range: {results_df['Edges'].min()} - {results_df['Edges'].max()}")
    print(f"   Average density: {results_df['Density'].mean():.3f}")
    
    # Most common hub foods
    print("\n🌟 Most Common Hub Foods (Rank #1):")
    hub1_counts = results_df['Hub1'].value_counts()
    for food, count in hub1_counts.head(3).items():
        print(f"   {food}: {count}/11 groups")
    
    print("\n" + "=" * 70)
    print("💡 Next steps:")
    print("   1. Compare with original analysis results")
    print("   2. Check if hub foods changed")
    print("   3. Analyze differences in network structure")
    print("=" * 70)

if __name__ == "__main__":
    main()
