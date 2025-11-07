#!/usr/bin/env python3
"""
Generate Modern Figure S2: Hub Rank Transitions Across Age Groups
Clean line chart style similar to provided reference
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up paths
BASE_DIR = Path('/home/user/webapp/ver4.0_GGM')
NETWORK_DIR = BASE_DIR / 'result' / 'networks'
FIGURES_DIR = BASE_DIR / 'result' / 'supplementary_figures'

# Modern style settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("notebook", font_scale=1.1)

# Define food categories with colors (matching reference image style)
FOOD_COLORS = {
    'Protein Foods': '#C62828',  # Deep red
    'Vegetables': '#7CB342',      # Green
    'Processed Foods': '#F57C00', # Orange
    'Fried Foods': '#FFA726',     # Light orange
    'High Fat Meat': '#FFE082',   # Pale yellow
    'Sugar-Sweetened Beverages': '#FFE082',
    'Sweet Food Consumption': '#FFE082',
}

def load_network_summary():
    """Load network summary data"""
    return pd.read_csv(NETWORK_DIR / 'ggm_network_summary.csv')

def prepare_hub_rank_data(df_summary):
    """Prepare data for hub rank visualization across age groups"""
    
    # Age group mapping for ordering
    age_order = {
        '청년층(19-39세)': 0,
        '중년층(40-59세)': 1,
        '장년층(60-74세)': 2
    }
    
    age_labels = ['Youth\n(19-39)', 'Middle\n(40-59)', 'Older\n(60-74)']
    
    # Process data for each sex-MetS combination
    groups_data = {}
    
    for sex in ['남성', '여성']:
        for mets in ['MetS(-)', 'MetS(+)']:
            mask = (df_summary['Sex'] == sex) & (df_summary['MetS_Status'] == mets)
            group_df = df_summary[mask].copy()
            
            if len(group_df) == 0:
                continue
            
            # Sort by age
            group_df['age_rank'] = group_df['Age_Group'].map(age_order)
            group_df = group_df.sort_values('age_rank')
            
            # Extract hub ranks across age groups
            hub_transitions = {}
            
            for idx, row in group_df.iterrows():
                age_idx = age_order[row['Age_Group']]
                
                # Get top 3 hubs
                for rank in [1, 2, 3]:
                    hub_name = row[f'Hub_{rank}_Name']
                    
                    if hub_name not in hub_transitions:
                        hub_transitions[hub_name] = {0: None, 1: None, 2: None}
                    
                    hub_transitions[hub_name][age_idx] = rank
            
            groups_data[f"{sex}_{mets}"] = {
                'transitions': hub_transitions,
                'ages': group_df['Age_Group'].tolist()
            }
    
    return groups_data, age_labels

def generate_modern_figure_s2():
    """Generate modern hub transition figure"""
    print("\n📊 Generating Modern Figure S2: Hub Rank Transitions...")
    
    df_summary = load_network_summary()
    groups_data, age_labels = prepare_hub_rank_data(df_summary)
    
    # Create 2x2 subplot
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    # Define panel order
    panels = [
        ('남성_MetS(-)', 'Male - MetS(-)'),
        ('남성_MetS(+)', 'Male - MetS(+)'),
        ('여성_MetS(-)', 'Female - MetS(-)'),
        ('여성_MetS(+)', 'Female - MetS(+)'),
    ]
    
    x_positions = [0, 1, 2]  # Youth, Middle, Older
    
    for panel_idx, (group_key, title) in enumerate(panels):
        ax = axes[panel_idx]
        
        if group_key not in groups_data:
            ax.text(0.5, 0.5, 'Insufficient\nData', 
                   ha='center', va='center', fontsize=16, color='gray')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
            ax.set_xlim(-0.2, 2.2)
            ax.set_ylim(0.5, 3.5)
            ax.set_yticks([1, 2, 3])
            ax.set_yticklabels(['1st', '2nd', '3rd'])
            ax.set_xticks(x_positions)
            ax.set_xticklabels(age_labels)
            ax.invert_yaxis()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            continue
        
        transitions = groups_data[group_key]['transitions']
        
        # Plot each food's transition
        for food, ranks in transitions.items():
            # Get color
            color = FOOD_COLORS.get(food, '#BDBDBD')
            
            # Extract rank values for each age
            y_vals = [ranks[i] if ranks[i] is not None else np.nan for i in x_positions]
            x_vals = [i for i in x_positions]
            
            # Remove None values for plotting
            valid_indices = [i for i, val in enumerate(y_vals) if not np.isnan(val)]
            if len(valid_indices) == 0:
                continue
            
            x_plot = [x_vals[i] for i in valid_indices]
            y_plot = [y_vals[i] for i in valid_indices]
            
            # Plot line
            ax.plot(x_plot, y_plot, 
                   marker='o', 
                   markersize=10, 
                   linewidth=2.5, 
                   color=color, 
                   alpha=0.8,
                   label=food,
                   zorder=3)
            
            # Add connecting lines even across gaps (optional)
            if len(x_plot) > 1:
                for i in range(len(x_plot) - 1):
                    if x_plot[i+1] - x_plot[i] > 1:
                        # Draw faint line across gap
                        ax.plot([x_plot[i], x_plot[i+1]], 
                               [y_plot[i], y_plot[i+1]], 
                               linestyle=':', 
                               linewidth=1.5, 
                               color=color, 
                               alpha=0.3,
                               zorder=1)
        
        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Age Group', fontsize=12, fontweight='bold')
        ax.set_ylabel('Hub Rank', fontsize=12, fontweight='bold')
        ax.set_xlim(-0.2, 2.2)
        ax.set_ylim(0.5, 3.5)
        ax.set_xticks(x_positions)
        ax.set_xticklabels(age_labels, fontsize=11)
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(['1st', '2nd', '3rd'], fontsize=11)
        ax.invert_yaxis()  # Rank 1 at top
        
        # Grid
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, axis='y')
        ax.set_axisbelow(True)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
    
    # Create unified legend
    handles, labels = axes[0].get_legend_handles_labels()
    
    # Deduplicate legend entries
    unique_labels = []
    unique_handles = []
    for handle, label in zip(handles, labels):
        if label not in unique_labels:
            unique_labels.append(label)
            unique_handles.append(handle)
    
    # Sort by color importance (Protein, Vegetables, Processed, Fried, Others)
    priority_order = ['Protein Foods', 'Vegetables', 'Processed Foods', 'Fried Foods']
    sorted_items = []
    
    for food in priority_order:
        if food in unique_labels:
            idx = unique_labels.index(food)
            sorted_items.append((unique_handles[idx], unique_labels[idx]))
    
    for handle, label in zip(unique_handles, unique_labels):
        if label not in priority_order:
            sorted_items.append((handle, label))
    
    if sorted_items:
        legend_handles, legend_labels = zip(*sorted_items)
        fig.legend(legend_handles, legend_labels, 
                  loc='upper center', 
                  bbox_to_anchor=(0.5, 0.98),
                  ncol=4, 
                  frameon=True,
                  fontsize=11,
                  title='Hub Foods',
                  title_fontsize=12)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    output_file = FIGURES_DIR / 'Figure_S2_Hub_Transitions_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")
    plt.close()

def main():
    """Main execution"""
    print("=" * 80)
    print("GENERATING MODERN FIGURE S2: HUB RANK TRANSITIONS")
    print("Clean line chart style")
    print("=" * 80)
    
    generate_modern_figure_s2()
    
    print("\n✅ Modern Figure S2 generated successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
