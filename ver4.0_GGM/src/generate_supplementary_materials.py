#!/usr/bin/env python3
"""
Generate Supplementary Materials for ver4.0 GGM Analysis
- Figure S1: Network visualizations (11 networks)
- Figure S2: Hub transition flowcharts
- Figure S3: Partial Correlation heatmaps (GGM-specific)
- Table S1: Sample characteristics
- Tables S2-S4: Network metrics, edges, centrality
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up paths
BASE_DIR = Path('/home/user/webapp/ver4.0_GGM')
NETWORK_DIR = BASE_DIR / 'result' / 'networks'
OUTPUT_DIR = BASE_DIR / 'result'
FIGURES_DIR = OUTPUT_DIR / 'supplementary_figures'
TABLES_DIR = OUTPUT_DIR / 'supplementary_tables'

# Create directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Set matplotlib style
plt.style.use('default')
sns.set_palette("husl")

# Define 11 groups (excluding 여성_청년층_MetS(+) - insufficient sample)
GROUPS = [
    ('남성', '청년층(19-39세)', 'MetS(+)'),
    ('남성', '청년층(19-39세)', 'MetS(-)'),
    ('남성', '중년층(40-59세)', 'MetS(+)'),
    ('남성', '중년층(40-59세)', 'MetS(-)'),
    ('남성', '장년층(60-74세)', 'MetS(+)'),
    ('남성', '장년층(60-74세)', 'MetS(-)'),
    ('여성', '청년층(19-39세)', 'MetS(-)'),
    ('여성', '중년층(40-59세)', 'MetS(+)'),
    ('여성', '중년층(40-59세)', 'MetS(-)'),
    ('여성', '장년층(60-74세)', 'MetS(+)'),
    ('여성', '장년층(60-74세)', 'MetS(-)'),
]

# Group labels
GROUP_LABELS = [
    '남성_청년층_MetS(+)',
    '남성_청년층_MetS(-)',
    '남성_중년층_MetS(+)',
    '남성_중년층_MetS(-)',
    '남성_장년층_MetS(+)',
    '남성_장년층_MetS(-)',
    '여성_청년층_MetS(-)',
    '여성_중년층_MetS(+)',
    '여성_중년층_MetS(-)',
    '여성_장년층_MetS(+)',
    '여성_장년층_MetS(-)',
]

def load_network_file(sex, age_group, mets_status):
    """Load GEXF network file for specific group"""
    filename = f"ggm_network_{sex}_{age_group}_{mets_status}.gexf"
    filepath = NETWORK_DIR / filename
    
    if filepath.exists():
        return nx.read_gexf(str(filepath))
    else:
        print(f"⚠️  File not found: {filename}")
        return None

def load_stratified_statistics():
    """Load stratified network statistics"""
    stats_file = NETWORK_DIR / 'ggm_network_summary.csv'
    if stats_file.exists():
        return pd.read_csv(stats_file)
    return None

def load_partial_corr_matrix(sex, age_group, mets_status):
    """Load partial correlation matrix for a group"""
    filename = f"ggm_network_{sex}_{age_group}_{mets_status}_partial_corr.csv"
    filepath = NETWORK_DIR / filename
    
    if filepath.exists():
        return pd.read_csv(filepath, index_col=0)
    return None

# ============================================================================
# FIGURE S1: Network Visualizations (11 networks)
# ============================================================================

def generate_figure_s1():
    """Generate Figure S1: 11 GGM network visualizations"""
    print("\n📊 Generating Figure S1: Network Visualizations (GGM)...")
    
    fig, axes = plt.subplots(4, 3, figsize=(18, 24))
    axes = axes.flatten()
    
    last_nodes = None  # Store last nodes collection for colorbar
    all_centralities = []  # Collect all centrality values
    
    # First pass: collect all centrality values
    for sex, age_group, mets_status in GROUPS:
        G = load_network_file(sex, age_group, mets_status)
        if G is not None and G.number_of_nodes() > 0:
            centrality = nx.degree_centrality(G)
            all_centralities.extend(centrality.values())
    
    # Calculate vmin/vmax from actual data
    vmin = min(all_centralities) if all_centralities else 0
    vmax = max(all_centralities) if all_centralities else 1
    
    print(f"  📊 Centrality range: {vmin:.3f} - {vmax:.3f}")
    
    for idx, (sex, age_group, mets_status) in enumerate(GROUPS):
        ax = axes[idx]
        G = load_network_file(sex, age_group, mets_status)
        
        if G is None or G.number_of_nodes() == 0:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', fontsize=12)
            ax.set_title(GROUP_LABELS[idx], fontsize=10, fontweight='bold')
            ax.axis('off')
            continue
        
        # Force-directed layout
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
        
        # Node sizes based on degree
        degrees = dict(G.degree())
        node_sizes = [degrees[node] * 100 + 100 for node in G.nodes()]
        
        # Node colors based on degree centrality
        centrality = nx.degree_centrality(G)
        node_colors = [centrality[node] for node in G.nodes()]
        
        # Draw edges with varying widths based on partial correlation
        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 1.0)
            nx.draw_networkx_edges(
                G, pos, [(u, v)], 
                ax=ax, 
                alpha=0.5, 
                width=weight * 8,  # Scale edge width
                edge_color='gray'
            )
        
        # Draw nodes with adjusted vmin/vmax
        nodes = nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_size=node_sizes,
            node_color=node_colors,
            cmap='YlOrRd',
            vmin=vmin, vmax=vmax,  # Use actual data range
            alpha=0.8,
            edgecolors='black',
            linewidths=1.5
        )
        last_nodes = nodes  # Save for colorbar
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=6, font_weight='bold')
        
        # Title
        title = GROUP_LABELS[idx].replace('_', ' ')
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        density = nx.density(G)
        
        ax.set_title(
            f"{title}\n(N={n_nodes}, E={n_edges}, D={density:.3f})",
            fontsize=9,
            fontweight='bold'
        )
        ax.axis('off')
    
    # Hide unused subplots
    for idx in range(len(GROUPS), len(axes)):
        axes[idx].axis('off')
    
    # Add colorbar (using last nodes collection)
    if last_nodes is not None:
        cbar = plt.colorbar(last_nodes, ax=axes[-1], fraction=0.046, pad=0.04)
        cbar.set_label('Degree Centrality', fontsize=10)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'Figure_S1_Network_Visualizations_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    print(f"✅ Saved: {output_file}")
    plt.close()

# ============================================================================
# FIGURE S2: Hub Transition Flowcharts
# ============================================================================

def generate_figure_s2():
    """Generate Figure S2: Hub transition flowcharts across age groups"""
    print("\n📊 Generating Figure S2: Hub Transition Flowcharts (GGM)...")
    
    stats_df = load_stratified_statistics()
    if stats_df is None:
        print("⚠️  Cannot load statistics file")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Define groups by sex and MetS status
    conditions = [
        ('남성', 'MetS(+)'),
        ('남성', 'MetS(-)'),
        ('여성', 'MetS(+)'),
        ('여성', 'MetS(-)'),
    ]
    
    age_order = ['청년층(19-39세)', '중년층(40-59세)', '장년층(60-74세)']
    
    for idx, (sex, mets) in enumerate(conditions):
        ax = axes[idx // 2, idx % 2]
        
        # Filter data
        mask = (stats_df['Sex'] == sex) & (stats_df['MetS_Status'] == mets)
        group_data = stats_df[mask].copy()
        
        if len(group_data) == 0:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center')
            ax.set_title(f"{sex} - {mets}", fontsize=12, fontweight='bold')
            ax.axis('off')
            continue
        
        # Sort by age
        group_data['age_order'] = group_data['Age_Group'].map({
            age: i for i, age in enumerate(age_order)
        })
        group_data = group_data.sort_values('age_order')
        
        # Create flowchart
        y_positions = list(range(len(group_data), 0, -1))
        
        for i, (_, row) in enumerate(group_data.iterrows()):
            y = y_positions[i]
            
            # Box for age group
            ax.add_patch(plt.Rectangle(
                (0, y - 0.4), 2, 0.8,
                facecolor='lightblue', edgecolor='black', linewidth=2
            ))
            ax.text(1, y, row['Age_Group'], ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Top hubs
            hubs_text = f"Top 3 Hubs:\n1. {row['Hub_1_Name']}\n2. {row['Hub_2_Name']}\n3. {row['Hub_3_Name']}"
            
            ax.add_patch(plt.Rectangle(
                (2.5, y - 0.4), 5, 0.8,
                facecolor='lightyellow', edgecolor='black', linewidth=1.5
            ))
            ax.text(5, y, hubs_text, ha='center', va='center', fontsize=8)
            
            # Network metrics (including Alpha)
            metrics_text = f"E={int(row['N_Edges'])}\nD={row['Density']:.3f}\nα={row['Alpha']:.3f}"
            ax.add_patch(plt.Rectangle(
                (8, y - 0.4), 2, 0.8,
                facecolor='lightgreen', edgecolor='black', linewidth=1.5
            ))
            ax.text(9, y, metrics_text, ha='center', va='center', fontsize=8)
            
            # Arrow to next age group
            if i < len(group_data) - 1:
                ax.arrow(1, y - 0.5, 0, -0.8, head_width=0.2, head_length=0.1,
                        fc='gray', ec='gray', linewidth=2)
        
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(0, max(y_positions) + 1)
        ax.set_title(f"{sex} - {mets}", fontsize=12, fontweight='bold')
        ax.axis('off')
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'Figure_S2_Hub_Transitions_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    print(f"✅ Saved: {output_file}")
    plt.close()

# ============================================================================
# FIGURE S3: Partial Correlation Heatmaps (GGM-specific)
# ============================================================================

def generate_figure_s3():
    """Generate Figure S3: Partial Correlation heatmaps for representative groups"""
    print("\n📊 Generating Figure S3: Partial Correlation Heatmaps (GGM)...")
    
    # Select 4 representative groups
    representative_groups = [
        ('남성', '청년층(19-39세)', 'MetS(+)', 'Male Young MetS(+)'),
        ('남성', '장년층(60-74세)', 'MetS(-)', 'Male Older MetS(-)'),
        ('여성', '중년층(40-59세)', 'MetS(+)', 'Female Middle MetS(+)'),
        ('여성', '중년층(40-59세)', 'MetS(-)', 'Female Middle MetS(-)'),
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 18))
    axes = axes.flatten()
    
    for idx, (sex, age_group, mets_status, label) in enumerate(representative_groups):
        ax = axes[idx]
        
        # Load partial correlation matrix
        partial_corr_df = load_partial_corr_matrix(sex, age_group, mets_status)
        
        if partial_corr_df is None:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center')
            ax.set_title(label, fontsize=12, fontweight='bold')
            ax.axis('off')
            continue
        
        # Plot heatmap
        sns.heatmap(
            partial_corr_df,
            cmap='RdBu_r',  # Red-Blue diverging colormap
            center=0,  # Center colormap at 0
            annot=True,
            fmt='.2f',
            linewidths=0.5,
            cbar_kws={'label': 'Partial Correlation'},
            ax=ax,
            vmin=-1,
            vmax=1,
            square=True
        )
        
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        # Rotate labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)
    
    plt.suptitle('Partial Correlation Matrices (GGM)', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    output_file = FIGURES_DIR / 'Figure_S3_Partial_Correlation_Heatmaps_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    print(f"✅ Saved: {output_file}")
    plt.close()

# ============================================================================
# TABLE S1: Sample Characteristics
# ============================================================================

def generate_table_s1():
    """Generate Table S1: Sample characteristics for 11 groups"""
    print("\n📋 Generating Table S1: Sample Characteristics (GGM)...")
    
    stats_df = load_stratified_statistics()
    if stats_df is None:
        print("⚠️  Cannot load statistics file")
        return
    
    # Prepare table
    table_data = []
    
    for _, row in stats_df.iterrows():
        table_data.append({
            'Group': f"{row['Sex']} - {row['Age_Group']} - {row['MetS_Status']}",
            'Sex': row['Sex'],
            'Age Group': row['Age_Group'],
            'MetS Status': row['MetS_Status'],
            'Sample Size (N)': int(row['N_Samples']),
            'Proportion (%)': f"{row['N_Samples'] / stats_df['N_Samples'].sum() * 100:.2f}",
        })
    
    # Add total row
    total_n = stats_df['N_Samples'].sum()
    table_data.append({
        'Group': 'TOTAL',
        'Sex': '-',
        'Age Group': '-',
        'MetS Status': '-',
        'Sample Size (N)': int(total_n),
        'Proportion (%)': '100.00'
    })
    
    df_table = pd.DataFrame(table_data)
    
    # Save as CSV
    output_file = TABLES_DIR / 'Table_S1_Sample_Characteristics_GGM.csv'
    df_table.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")
    
    # Also save as formatted text
    output_txt = TABLES_DIR / 'Table_S1_Sample_Characteristics_GGM.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("TABLE S1. Sample Characteristics of 11 Stratified Groups (GGM Analysis)\n")
        f.write("=" * 100 + "\n\n")
        f.write(df_table.to_string(index=False))
        f.write("\n\n" + "=" * 100 + "\n")
        f.write(f"\nTotal Sample Size: {int(total_n):,}\n")
        f.write(f"Number of Groups: 11 (excluding 여성_청년층_MetS(+) due to insufficient sample)\n")
        f.write(f"Network Method: Gaussian Graphical Models (GGM)\n")
    
    print(f"✅ Saved: {output_txt}")
    
    return df_table

# ============================================================================
# TABLE S2: Network Metrics
# ============================================================================

def generate_table_s2():
    """Generate Table S2: GGM network metrics for all groups"""
    print("\n📋 Generating Table S2: Network Metrics (GGM)...")
    
    metrics_data = []
    
    for sex, age_group, mets_status in GROUPS:
        G = load_network_file(sex, age_group, mets_status)
        
        if G is None or G.number_of_nodes() == 0:
            continue
        
        group_label = f"{sex}_{age_group}_{mets_status}"
        
        # Calculate metrics
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()
        density = nx.density(G)
        
        # Average clustering
        try:
            avg_clustering = nx.average_clustering(G)
        except:
            avg_clustering = 0.0
        
        # Average degree
        avg_degree = sum(dict(G.degree()).values()) / n_nodes if n_nodes > 0 else 0
        
        # Diameter (for connected graphs)
        try:
            if nx.is_connected(G):
                diameter = nx.diameter(G)
            else:
                diameter = np.nan
        except:
            diameter = np.nan
        
        # Average path length
        try:
            if nx.is_connected(G):
                avg_path_length = nx.average_shortest_path_length(G)
            else:
                avg_path_length = np.nan
        except:
            avg_path_length = np.nan
        
        # Get alpha from summary
        stats_df = load_stratified_statistics()
        alpha_value = stats_df[
            (stats_df['Sex'] == sex) & 
            (stats_df['Age_Group'] == age_group) & 
            (stats_df['MetS_Status'] == mets_status)
        ]['Alpha'].values[0] if stats_df is not None else np.nan
        
        metrics_data.append({
            'Group': group_label,
            'Nodes': n_nodes,
            'Edges': n_edges,
            'Density': f"{density:.4f}",
            'Avg Clustering': f"{avg_clustering:.4f}",
            'Avg Degree': f"{avg_degree:.2f}",
            'Diameter': int(diameter) if not np.isnan(diameter) else 'N/A',
            'Avg Path Length': f"{avg_path_length:.4f}" if not np.isnan(avg_path_length) else 'N/A',
            'Alpha': f"{alpha_value:.4f}"
        })
    
    df_metrics = pd.DataFrame(metrics_data)
    
    # Save as CSV
    output_file = TABLES_DIR / 'Table_S2_Network_Metrics_GGM.csv'
    df_metrics.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")
    
    # Also save as formatted text
    output_txt = TABLES_DIR / 'Table_S2_Network_Metrics_GGM.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("TABLE S2. GGM Network Metrics for All Stratified Groups\n")
        f.write("=" * 150 + "\n\n")
        f.write(df_metrics.to_string(index=False))
        f.write("\n\n" + "=" * 150 + "\n")
        f.write("\nNote: Networks constructed using Gaussian Graphical Models (GGM)\n")
        f.write("Alpha: Regularization parameter from cross-validated Graphical Lasso\n")
    
    print(f"✅ Saved: {output_txt}")
    
    return df_metrics

# ============================================================================
# TABLE S3: Edge Lists with Partial Correlations
# ============================================================================

def generate_table_s3():
    """Generate Table S3: Complete edge lists with partial correlations for all groups"""
    print("\n📋 Generating Table S3: Edge Lists (GGM)...")
    
    all_edges = []
    
    for sex, age_group, mets_status in GROUPS:
        G = load_network_file(sex, age_group, mets_status)
        
        if G is None or G.number_of_edges() == 0:
            continue
        
        group_label = f"{sex}_{age_group}_{mets_status}"
        
        for u, v, data in G.edges(data=True):
            # Get edge attributes
            weight = data.get('weight', 0)
            partial_corr = data.get('partial_corr', weight)
            
            all_edges.append({
                'Group': group_label,
                'Node 1': u,
                'Node 2': v,
                'Partial Correlation': f"{partial_corr:.4f}",
                'Absolute Weight': f"{weight:.4f}"
            })
    
    df_edges = pd.DataFrame(all_edges)
    
    # Save as CSV
    output_file = TABLES_DIR / 'Table_S3_Edge_Lists_GGM.csv'
    df_edges.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")
    
    # Summary statistics
    output_summary = TABLES_DIR / 'Table_S3_Edge_Lists_Summary_GGM.txt'
    with open(output_summary, 'w', encoding='utf-8') as f:
        f.write("TABLE S3. Complete Edge Lists with Partial Correlations (GGM) - Summary\n")
        f.write("=" * 80 + "\n\n")
        
        for group in df_edges['Group'].unique():
            group_edges = df_edges[df_edges['Group'] == group]
            f.write(f"\n{group}: {len(group_edges)} edges\n")
        
        f.write(f"\n\nTotal edges across all groups: {len(df_edges)}\n")
        f.write("=" * 80 + "\n")
        f.write("\nNote: Partial correlations estimated using Graphical Lasso\n")
        f.write("Complete edge list saved in Table_S3_Edge_Lists_GGM.csv\n")
    
    print(f"✅ Saved: {output_summary}")
    
    return df_edges

# ============================================================================
# TABLE S4: Centrality Rankings
# ============================================================================

def generate_table_s4():
    """Generate Table S4: Top 5 centrality rankings for all groups"""
    print("\n📋 Generating Table S4: Centrality Rankings (GGM)...")
    
    centrality_rankings = []
    
    for sex, age_group, mets_status in GROUPS:
        G = load_network_file(sex, age_group, mets_status)
        
        if G is None or G.number_of_nodes() == 0:
            continue
        
        group_label = f"{sex}_{age_group}_{mets_status}"
        
        # Calculate centralities
        degree_cent = nx.degree_centrality(G)
        
        try:
            betweenness_cent = nx.betweenness_centrality(G)
        except:
            betweenness_cent = {node: 0 for node in G.nodes()}
        
        try:
            closeness_cent = nx.closeness_centrality(G)
        except:
            closeness_cent = {node: 0 for node in G.nodes()}
        
        # Get top 5 for each centrality
        top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
        top_betweenness = sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:5]
        top_closeness = sorted(closeness_cent.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for rank in range(5):
            centrality_rankings.append({
                'Group': group_label,
                'Rank': rank + 1,
                'Top Degree': f"{top_degree[rank][0]} ({top_degree[rank][1]:.4f})" if rank < len(top_degree) else '',
                'Top Betweenness': f"{top_betweenness[rank][0]} ({top_betweenness[rank][1]:.4f})" if rank < len(top_betweenness) else '',
                'Top Closeness': f"{top_closeness[rank][0]} ({top_closeness[rank][1]:.4f})" if rank < len(top_closeness) else ''
            })
    
    df_rankings = pd.DataFrame(centrality_rankings)
    
    # Save as CSV
    output_file = TABLES_DIR / 'Table_S4_Centrality_Rankings_GGM.csv'
    df_rankings.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")
    
    # Also save as formatted text
    output_txt = TABLES_DIR / 'Table_S4_Centrality_Rankings_GGM.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("TABLE S4. Top 5 Centrality Rankings for All Stratified Groups (GGM)\n")
        f.write("=" * 150 + "\n\n")
        
        for group in df_rankings['Group'].unique():
            f.write(f"\n{group}:\n")
            f.write("-" * 150 + "\n")
            group_data = df_rankings[df_rankings['Group'] == group]
            f.write(group_data.to_string(index=False, columns=['Rank', 'Top Degree', 'Top Betweenness', 'Top Closeness']))
            f.write("\n")
        
        f.write("\n" + "=" * 150 + "\n")
    
    print(f"✅ Saved: {output_txt}")
    
    return df_rankings

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function"""
    print("=" * 80)
    print("GENERATING SUPPLEMENTARY MATERIALS - VER4.0 GGM")
    print("Stratified Network Analysis using Gaussian Graphical Models")
    print("=" * 80)
    
    # Generate all figures
    print("\n" + "=" * 80)
    print("PART 1: GENERATING FIGURES")
    print("=" * 80)
    
    generate_figure_s1()  # Network visualizations
    
    # Generate Figure S2 (modern hub transitions) by calling external script
    print("\n📊 Generating Figure S2: Modern Hub Transitions...")
    import subprocess
    s2_script = BASE_DIR / 'src' / 'generate_figure_s2_modern.py'
    if s2_script.exists():
        result = subprocess.run(['python', str(s2_script)], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Figure S2 generated via external script")
        else:
            print(f"⚠️  Figure S2 generation failed, using fallback")
            generate_figure_s2()  # Fallback to original
    else:
        generate_figure_s2()  # Hub transitions (original)
    
    generate_figure_s3()  # Partial correlation heatmaps (GGM-specific)
    
    # Generate Figure S4 (decision tree) by calling external script
    print("\n📊 Generating Figure S4: Clinical Decision Tree...")
    import subprocess
    s4_script = BASE_DIR / 'src' / 'generate_figure_s4_decision_tree.py'
    if s4_script.exists():
        result = subprocess.run(['python', str(s4_script)], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Figure S4 generated via external script")
        else:
            print(f"⚠️  Figure S4 generation failed: {result.stderr}")
    
    # Generate all tables
    print("\n" + "=" * 80)
    print("PART 2: GENERATING TABLES")
    print("=" * 80)
    
    generate_table_s1()  # Sample characteristics
    generate_table_s2()  # Network metrics
    generate_table_s3()  # Edge lists with partial correlations
    generate_table_s4()  # Centrality rankings
    
    # Generate Table S5 (coaching strategies) by calling external script
    print("\n📋 Generating Table S5: Coaching Strategies...")
    s5_script = BASE_DIR / 'src' / 'generate_table_s5_coaching.py'
    if s5_script.exists():
        result = subprocess.run(['python', str(s5_script)], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Table S5 generated via external script")
        else:
            print(f"⚠️  Table S5 generation failed: {result.stderr}")
    
    print("\n" + "=" * 80)
    print("✅ ALL SUPPLEMENTARY MATERIALS GENERATED SUCCESSFULLY!")
    print("=" * 80)
    
    # Summary
    print("\n📊 Generated Files:")
    print("\nFigures:")
    print("  - Figure_S1_Network_Visualizations_GGM.png")
    print("  - Figure_S2_Hub_Transitions_GGM.png")
    print("  - Figure_S3_Partial_Correlation_Heatmaps_GGM.png")
    print("  - Figure_S4_Clinical_Decision_Tree_GGM.png (NEW)")
    
    print("\nTables:")
    print("  - Table_S1_Sample_Characteristics_GGM.csv/.txt")
    print("  - Table_S2_Network_Metrics_GGM.csv/.txt")
    print("  - Table_S3_Edge_Lists_GGM.csv/.txt")
    print("  - Table_S4_Centrality_Rankings_GGM.csv/.txt")
    print("  - Table_S5_Personalized_Coaching_Strategies_GGM.csv/.txt (NEW)")
    
    print(f"\n📁 Output Directory: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
