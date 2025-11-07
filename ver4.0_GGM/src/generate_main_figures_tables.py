#!/usr/bin/env python3
"""
Generate Main Figures and Tables for ver4.0 GGM Analysis
- Same structure as ver3.0 but with GGM methodology
- Table 1: Sample Characteristics Summary
- Figure 1: Representative Network Comparison (4 key groups)
- Figure 2: Hub Food Centrality Comparison
- Table 2: Network Metrics Summary
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path('/home/user/webapp/ver4.0_GGM')
NETWORK_DIR = BASE_DIR / 'result' / 'networks'
DATA_DIR = Path('/home/user/webapp/ver3.0_2511/db/processed_data')  # Use ver3.0 data for demographics
OUTPUT_DIR = BASE_DIR / 'result'
FIGURES_DIR = OUTPUT_DIR / 'figures'
TABLES_DIR = OUTPUT_DIR / 'tables'

# Create directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10

# Key representative groups for main figures
KEY_GROUPS = [
    ('남성', '청년층(19-39세)', 'MetS(+)'),
    ('남성', '장년층(60-74세)', 'MetS(-)'),
    ('여성', '중년층(40-59세)', 'MetS(+)'),
    ('여성', '중년층(40-59세)', 'MetS(-)'),
]

KEY_GROUP_LABELS = [
    'Male Young MetS(+)',
    'Male Older MetS(-)',
    'Female Middle MetS(+)',
    'Female Middle MetS(-)',
]

def load_network(sex, age_group, mets_status):
    """Load GGM network file"""
    filename = f"ggm_network_{sex}_{age_group}_{mets_status}.gexf"
    filepath = NETWORK_DIR / filename
    if filepath.exists():
        return nx.read_gexf(str(filepath))
    return None

def load_statistics():
    """Load GGM network statistics"""
    stats_file = NETWORK_DIR / 'ggm_network_summary.csv'
    if stats_file.exists():
        return pd.read_csv(stats_file)
    return None

# ============================================================================
# TABLE 1: Sample Characteristics (Main Text Version)
# ============================================================================

def generate_table_1():
    """Generate Table 1: Sample Characteristics Summary"""
    print("\n📋 Generating Table 1: Sample Characteristics...")
    
    stats_df = load_statistics()
    if stats_df is None:
        print("⚠️  Cannot load statistics")
        return
    
    # Aggregate by demographic groups
    summary_data = []
    
    # Overall
    total_n = stats_df['N_Samples'].sum()
    
    # By Sex
    for sex in ['남성', '여성']:
        sex_data = stats_df[stats_df['Sex'] == sex]
        n = sex_data['N_Samples'].sum()
        pct = n / total_n * 100
        summary_data.append({
            'Characteristic': f'{sex}',
            'N': int(n),
            'Percentage': f'{pct:.1f}'
        })
    
    # By Age Group
    for age in ['청년층(19-39세)', '중년층(40-59세)', '장년층(60-74세)']:
        age_data = stats_df[stats_df['Age_Group'] == age]
        n = age_data['N_Samples'].sum()
        pct = n / total_n * 100
        summary_data.append({
            'Characteristic': age.replace('청년층', 'Young adults ').replace('중년층', 'Middle-aged ').replace('장년층', 'Older adults '),
            'N': int(n),
            'Percentage': f'{pct:.1f}'
        })
    
    # By MetS Status
    for mets in ['MetS(+)', 'MetS(-)']:
        mets_data = stats_df[stats_df['MetS_Status'] == mets]
        n = mets_data['N_Samples'].sum()
        pct = n / total_n * 100
        summary_data.append({
            'Characteristic': mets,
            'N': int(n),
            'Percentage': f'{pct:.1f}'
        })
    
    # By detailed groups (top 3 and bottom 3)
    stats_df_sorted = stats_df.sort_values('N_Samples', ascending=False)
    
    for idx, row in stats_df_sorted.head(3).iterrows():
        group_name = f"{row['Sex']} {row['Age_Group']} {row['MetS_Status']}"
        summary_data.append({
            'Characteristic': f'  {group_name}',
            'N': int(row['N_Samples']),
            'Percentage': f"{row['N_Samples']/total_n*100:.1f}"
        })
    
    summary_data.append({
        'Characteristic': '  ...',
        'N': '...',
        'Percentage': '...'
    })
    
    for idx, row in stats_df_sorted.tail(3).iterrows():
        group_name = f"{row['Sex']} {row['Age_Group']} {row['MetS_Status']}"
        summary_data.append({
            'Characteristic': f'  {group_name}',
            'N': int(row['N_Samples']),
            'Percentage': f"{row['N_Samples']/total_n*100:.1f}"
        })
    
    # Total
    summary_data.append({
        'Characteristic': 'Total',
        'N': int(total_n),
        'Percentage': '100.0'
    })
    
    df = pd.DataFrame(summary_data)
    
    # Save as CSV
    output_csv = TABLES_DIR / 'Table_1_Sample_Characteristics.csv'
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}")
    
    # Save as formatted text
    output_txt = TABLES_DIR / 'Table_1_Sample_Characteristics.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(f"TABLE 1. Sample Characteristics of Study Population (N={int(total_n):,})\n")
        f.write("=" * 70 + "\n\n")
        f.write(df.to_string(index=False))
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("\nData from Korea National Health and Nutrition Examination Survey (KNHANES)\n")
        f.write("11 stratified groups based on sex, age, and metabolic syndrome status\n")
        f.write("Network analysis using Gaussian Graphical Models (GGM)\n")
    
    print(f"✅ Saved: {output_txt}")
    print(f"\n{df.to_string(index=False)}\n")

# ============================================================================
# FIGURE 1: Representative Network Comparison
# ============================================================================

def generate_figure_1():
    """Generate Figure 1: Representative Network Visualizations (GGM)"""
    print("\n📊 Generating Figure 1: Representative Networks (GGM)...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    axes = axes.flatten()
    
    last_nodes = None  # Store the last nodes collection for colorbar
    all_centralities = []  # Collect all centrality values for vmin/vmax
    
    # First pass: collect all centrality values
    for sex, age_group, mets_status in KEY_GROUPS:
        G = load_network(sex, age_group, mets_status)
        if G is not None and G.number_of_nodes() > 0:
            centrality = nx.degree_centrality(G)
            all_centralities.extend(centrality.values())
    
    # Calculate vmin/vmax from actual data
    vmin = min(all_centralities) if all_centralities else 0
    vmax = max(all_centralities) if all_centralities else 1
    
    print(f"  📊 Centrality range: {vmin:.3f} - {vmax:.3f}")
    
    for idx, (sex, age_group, mets_status) in enumerate(KEY_GROUPS):
        ax = axes[idx]
        G = load_network(sex, age_group, mets_status)
        
        if G is None or G.number_of_nodes() == 0:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center')
            ax.set_title(KEY_GROUP_LABELS[idx], fontsize=12, fontweight='bold')
            ax.axis('off')
            continue
        
        # Layout
        pos = nx.spring_layout(G, k=0.7, iterations=50, seed=42)
        
        # Node properties
        degrees = dict(G.degree())
        node_sizes = [degrees[node] * 150 + 200 for node in G.nodes()]
        
        centrality = nx.degree_centrality(G)
        node_colors = [centrality[node] for node in G.nodes()]
        
        # Draw edges with varying widths based on partial correlation
        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 1.0)
            nx.draw_networkx_edges(
                G, pos, [(u, v)], 
                ax=ax, 
                alpha=0.6, 
                width=weight * 5,  # Scale edge width by partial correlation
                edge_color='gray'
            )
        
        # Draw nodes with adjusted vmin/vmax
        nodes = nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_size=node_sizes,
            node_color=node_colors,
            cmap='YlOrRd',
            vmin=vmin, vmax=vmax,  # Use actual data range
            alpha=0.9,
            edgecolors='black',
            linewidths=1.5
        )
        last_nodes = nodes  # Save for colorbar
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight='bold')
        
        # Panel title (centered at top)
        ax.text(0.5, 0.98, KEY_GROUP_LABELS[idx], transform=ax.transAxes,
                fontsize=10, fontweight='bold', 
                horizontalalignment='center', verticalalignment='top',
                color='black')
        
        ax.axis('off')
    
    # Add colorbar (using last nodes collection)
    if last_nodes is not None:
        cbar = plt.colorbar(last_nodes, ax=axes, fraction=0.02, pad=0.02)
        cbar.set_label('Degree Centrality', fontsize=11)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'Figure_1_Representative_Networks_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    print(f"✅ Saved: {output_file}")
    plt.close()

# ============================================================================
# FIGURE 2: Hub Food Centrality Comparison
# ============================================================================

def generate_figure_2():
    """Generate Figure 2: Hub Food Centrality Across Groups (GGM)"""
    print("\n📊 Generating Figure 2: Hub Centrality Comparison (GGM)...")
    
    # Collect centrality data for all foods
    all_groups = [
        ('남성', '청년층(19-39세)', 'MetS(+)', 'M Young\nMetS+'),
        ('남성', '청년층(19-39세)', 'MetS(-)', 'M Young\nMetS-'),
        ('남성', '중년층(40-59세)', 'MetS(+)', 'M Middle\nMetS+'),
        ('남성', '중년층(40-59세)', 'MetS(-)', 'M Middle\nMetS-'),
        ('남성', '장년층(60-74세)', 'MetS(+)', 'M Older\nMetS+'),
        ('남성', '장년층(60-74세)', 'MetS(-)', 'M Older\nMetS-'),
        ('여성', '청년층(19-39세)', 'MetS(-)', 'F Young\nMetS-'),
        ('여성', '중년층(40-59세)', 'MetS(+)', 'F Middle\nMetS+'),
        ('여성', '중년층(40-59세)', 'MetS(-)', 'F Middle\nMetS-'),
        ('여성', '장년층(60-74세)', 'MetS(+)', 'F Older\nMetS+'),
        ('여성', '장년층(60-74세)', 'MetS(-)', 'F Older\nMetS-'),
    ]
    
    # Collect data
    data = []
    all_foods = set()
    
    for sex, age_group, mets_status, label in all_groups:
        G = load_network(sex, age_group, mets_status)
        if G is None:
            continue
        
        centrality = nx.degree_centrality(G)
        for food, cent_value in centrality.items():
            all_foods.add(food)
            data.append({
                'Group': label,
                'Food': food,
                'Centrality': cent_value
            })
    
    df = pd.DataFrame(data)
    
    # Get top hub foods across all groups
    food_avg_centrality = df.groupby('Food')['Centrality'].mean().sort_values(ascending=False)
    top_hub_foods = food_avg_centrality.head(6).index.tolist()
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    
    df_top_hubs = df[df['Food'].isin(top_hub_foods)]
    
    # Grouped bar chart
    x = np.arange(len(all_groups))
    width = 0.13  # Width for 6 bars
    
    for i, food in enumerate(top_hub_foods):
        food_data = df_top_hubs[df_top_hubs['Food'] == food].sort_values('Group')
        values = [food_data[food_data['Group'] == g]['Centrality'].values[0] 
                  if len(food_data[food_data['Group'] == g]) > 0 else 0 
                  for _, _, _, g in all_groups]
        ax.bar(x + i*width, values, width, label=food, alpha=0.8)
    
    ax.set_xlabel('Stratified Groups', fontsize=11, fontweight='bold')
    ax.set_ylabel('Degree Centrality', fontsize=11, fontweight='bold')
    ax.set_title('Top Hub Foods Centrality Across Groups (GGM-based)', fontsize=12, fontweight='bold', pad=10)
    ax.set_xticks(x + width * 2.5)
    ax.set_xticklabels([g[3] for g in all_groups], rotation=45, ha='right', fontsize=9)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(df_top_hubs['Centrality']) * 1.1)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'Figure_2_Hub_Centrality_Comparison_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    print(f"✅ Saved: {output_file}")
    plt.close()

# ============================================================================
# TABLE 2: Network Metrics Summary
# ============================================================================

def generate_table_2():
    """Generate Table 2: GGM Network Metrics Summary"""
    print("\n📋 Generating Table 2: Network Metrics Summary (GGM)...")
    
    stats_df = load_statistics()
    if stats_df is None:
        print("⚠️  Cannot load statistics")
        return
    
    # Calculate additional metrics for each network
    metrics_data = []
    
    for _, row in stats_df.iterrows():
        sex = row['Sex']
        age_group = row['Age_Group']
        mets_status = row['MetS_Status']
        
        # Load network
        G = load_network(sex, age_group, mets_status)
        if G is None:
            continue
        
        # Calculate metrics
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        density = nx.density(G)
        
        try:
            avg_clustering = nx.average_clustering(G)
        except:
            avg_clustering = 0.0
            
        avg_degree = sum(dict(G.degree()).values()) / n_nodes if n_nodes > 0 else 0
        
        # Diameter and path length (if connected)
        try:
            if nx.is_connected(G):
                diameter = nx.diameter(G)
                avg_path = nx.average_shortest_path_length(G)
            else:
                diameter = np.nan
                avg_path = np.nan
        except:
            diameter = np.nan
            avg_path = np.nan
        
        metrics_data.append({
            'Group': f"{sex[0]} {age_group.split('(')[0][:2]} {mets_status}",
            'N': int(row['N_Samples']),
            'Nodes': n_nodes,
            'Edges': n_edges,
            'Density': f"{density:.3f}",
            'Clustering': f"{avg_clustering:.3f}",
            'Avg Degree': f"{avg_degree:.2f}",
            'Alpha': f"{row['Alpha']:.4f}",
            'Top Hub 1': row['Hub_1_Name'],
            'Top Hub 2': row['Hub_2_Name'],
            'Top Hub 3': row['Hub_3_Name']
        })
    
    df = pd.DataFrame(metrics_data)
    
    # Save as CSV
    output_csv = TABLES_DIR / 'Table_2_Network_Metrics_GGM.csv'
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}")
    
    # Save as formatted text
    output_txt = TABLES_DIR / 'Table_2_Network_Metrics_GGM.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("TABLE 2. GGM Network Structural Metrics and Hub Foods\n")
        f.write("=" * 150 + "\n\n")
        f.write(df.to_string(index=False))
        f.write("\n\n" + "=" * 150 + "\n")
        f.write("\nNote: Networks constructed using Gaussian Graphical Models (GGM)\n")
        f.write("Alpha: Regularization parameter from cross-validated Graphical Lasso\n")
        f.write("Density varies by group (data-driven edge selection)\n")
        f.write("Top hubs ranked by degree centrality\n")
    
    print(f"✅ Saved: {output_txt}")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Generate all main figures and tables"""
    print("=" * 80)
    print("GENERATING MAIN FIGURES AND TABLES - VER4.0 GGM")
    print("=" * 80)
    
    # Generate tables
    print("\n" + "=" * 80)
    print("TABLES")
    print("=" * 80)
    generate_table_1()
    generate_table_2()
    
    # Generate figures
    print("\n" + "=" * 80)
    print("FIGURES")
    print("=" * 80)
    generate_figure_1()
    generate_figure_2()
    
    print("\n" + "=" * 80)
    print("✅ ALL MAIN FIGURES AND TABLES GENERATED!")
    print("=" * 80)
    
    print("\n📊 Generated Files:")
    print("\nTables:")
    print("  - Table_1_Sample_Characteristics.csv/.txt")
    print("  - Table_2_Network_Metrics_GGM.csv/.txt")
    
    print("\nFigures:")
    print("  - Figure_1_Representative_Networks_GGM.png (300 DPI)")
    print("  - Figure_2_Hub_Centrality_Comparison_GGM.png (300 DPI)")
    
    print(f"\n📁 Output Directories:")
    print(f"  - Tables: {TABLES_DIR}")
    print(f"  - Figures: {FIGURES_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
