#!/usr/bin/env python3
"""
Create 11 stratified networks from total_only_org.csv
Based on Sex × Age Group × MetS Status stratification
"""

import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path('/home/user/webapp')
DATA_FILE = BASE_DIR / 'db' / 'processed_data' / 'total_only_org.csv'
OUTPUT_DIR = BASE_DIR / 'db' / 'processed_data'

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
# Sex values: M (Male), F (Female)
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

# Mapping for display names
SEX_DISPLAY = {'M': '남성', 'F': '여성'}

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
    
    # Create MetS_Status
    df['MetS_Status'] = df['MetS'].apply(lambda x: 'MetS(+)' if x == 1 else 'MetS(-)')
    
    print(f"✅ Created Age_Group and MetS_Status columns")
    
    return df

def create_cooccurrence_network(data, food_groups, threshold_percentile=70):
    """
    Create co-occurrence network from food group data
    
    Args:
        data: DataFrame with food group columns
        food_groups: List of food group column names
        threshold_percentile: Percentile threshold for edge creation
    
    Returns:
        NetworkX graph
    """
    # Binarize: 1 if score >= 3 (high consumption), 0 otherwise
    # Note: Food groups use 3- or 4-point scales, but binarization threshold is consistent (>=3)
    data_binary = (data[food_groups] >= 3).astype(int)
    
    # Calculate co-occurrence matrix
    n_samples = len(data_binary)
    cooccur_matrix = data_binary.T.dot(data_binary) / n_samples
    
    # Set diagonal to 0
    np.fill_diagonal(cooccur_matrix.values, 0)
    
    # Calculate threshold
    threshold = np.percentile(cooccur_matrix.values[cooccur_matrix.values > 0], threshold_percentile)
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes
    for food in food_groups:
        G.add_node(food)
    
    # Add edges above threshold
    for i, food1 in enumerate(food_groups):
        for j, food2 in enumerate(food_groups):
            if i < j:
                weight = cooccur_matrix.iloc[i, j]
                if weight >= threshold:
                    G.add_edge(food1, food2, weight=weight)
    
    return G

def save_network(G, sex, age_group, mets_status):
    """Save network as GEXF file"""
    # Create filename with display names
    sex_name = SEX_DISPLAY[sex]
    filename = f"network_{sex_name}_{age_group}_{mets_status}.gexf"
    filepath = OUTPUT_DIR / filename
    
    # Save
    nx.write_gexf(G, str(filepath))
    
    return filepath

def process_all_groups(df):
    """Process all 11 groups and create networks"""
    results = []
    
    for sex, age_group, mets_status, expected_n in GROUPS:
        sex_display = SEX_DISPLAY[sex]
        print(f"\n{'='*80}")
        print(f"Processing: {sex_display} ({sex}) - {age_group} - {mets_status}")
        print(f"{'='*80}")
        
        # Filter data
        mask = (df['Sex'] == sex) & (df['Age_Group'] == age_group) & (df['MetS_Status'] == mets_status)
        group_data = df[mask].copy()
        
        n_samples = len(group_data)
        print(f"📊 Sample size: {n_samples:,} (expected: {expected_n:,})")
        
        if n_samples < 100:
            print(f"⚠️  WARNING: Sample size too small ({n_samples}), skipping...")
            continue
        
        # Check if food group columns exist
        missing_cols = [col for col in FOOD_GROUPS if col not in group_data.columns]
        if missing_cols:
            print(f"⚠️  WARNING: Missing columns: {missing_cols}")
            continue
        
        # Create network
        G = create_cooccurrence_network(group_data, FOOD_GROUPS, threshold_percentile=70)
        
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        density = nx.density(G)
        
        print(f"📈 Network: {n_nodes} nodes, {n_edges} edges, density={density:.4f}")
        
        # Calculate top hubs
        if n_edges > 0:
            degree_cent = nx.degree_centrality(G)
            top_hubs = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"🎯 Top 3 hubs: {', '.join([f'{h[0]} ({h[1]:.3f})' for h in top_hubs])}")
        else:
            top_hubs = [('None', 0)] * 3
            print(f"⚠️  No edges in network")
        
        # Save network
        filepath = save_network(G, sex, age_group, mets_status)
        print(f"💾 Saved: {filepath.name}")
        
        # Store results
        sex_display = SEX_DISPLAY[sex]
        results.append({
            'Group': f"{sex_display}_{age_group}_{mets_status}",
            'Sex': sex_display,
            'Age_Group': age_group,
            'MetS_Status': mets_status,
            'N_Samples': n_samples,
            'N_Edges': n_edges,
            'Density': density,
            'Top_Hub_1': top_hubs[0][0] if len(top_hubs) > 0 else 'None',
            'Top_Hub_2': top_hubs[1][0] if len(top_hubs) > 1 else 'None',
            'Top_Hub_3': top_hubs[2][0] if len(top_hubs) > 2 else 'None',
        })
    
    return pd.DataFrame(results)

def main():
    """Main execution"""
    print("=" * 80)
    print("CREATING 11 STRATIFIED NETWORKS")
    print("=" * 80)
    
    # Load data
    df = load_data()
    
    # Check columns
    print(f"\n📋 Available columns: {df.columns.tolist()[:10]}...")
    print(f"📋 Looking for food groups: {FOOD_GROUPS[:3]}...")
    
    # Verify food group columns exist
    food_cols_present = [col for col in FOOD_GROUPS if col in df.columns]
    print(f"✅ Found {len(food_cols_present)}/{len(FOOD_GROUPS)} food group columns")
    
    if len(food_cols_present) < len(FOOD_GROUPS):
        missing = [col for col in FOOD_GROUPS if col not in df.columns]
        print(f"⚠️  Missing columns: {missing}")
        print(f"\n📋 All columns in dataset:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        return
    
    # Process all groups
    results_df = process_all_groups(df)
    
    # Save statistics
    stats_file = OUTPUT_DIR / 'stratified_network_statistics.csv'
    results_df.to_csv(stats_file, index=False)
    print(f"\n✅ Saved statistics: {stats_file}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total groups processed: {len(results_df)}")
    print(f"Total networks created: {len(results_df)}")
    print(f"\nNetwork files saved in: {OUTPUT_DIR}")
    print("=" * 80)
    
    # Display summary table
    if len(results_df) > 0:
        print("\n📊 Network Statistics Summary:")
        print(results_df[['Group', 'N_Samples', 'N_Edges', 'Density']].to_string(index=False))
    else:
        print("\n⚠️  No networks created!")

if __name__ == "__main__":
    main()
