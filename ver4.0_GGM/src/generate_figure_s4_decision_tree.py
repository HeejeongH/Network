#!/usr/bin/env python3
"""
Generate Figure S4: Clinical Decision Tree for Personalized Dietary Coaching
Based on Age, Sex, and MetS Status
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

# Set up paths
BASE_DIR = Path('/home/user/webapp/ver4.0_GGM')
FIGURES_DIR = BASE_DIR / 'result' / 'supplementary_figures'
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def draw_box(ax, x, y, width, height, text, color, text_color='black', fontsize=9, fontweight='normal'):
    """Draw a fancy box with text"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.1",
        edgecolor='black',
        facecolor=color,
        linewidth=2,
        zorder=2
    )
    ax.add_patch(box)
    
    # Add text
    ax.text(x, y, text, ha='center', va='center', 
            fontsize=fontsize, fontweight=fontweight, color=text_color,
            zorder=3, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='black', linewidth=2):
    """Draw arrow between boxes"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='->,head_width=0.4,head_length=0.4',
        color=color,
        linewidth=linewidth,
        zorder=1
    )
    ax.add_patch(arrow)
    
    # Add label if provided
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(mid_x, mid_y, label, ha='center', va='center',
                fontsize=7, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                zorder=3)

def generate_figure_s4():
    """Generate Figure S4: Decision tree for personalized coaching"""
    print("\n📊 Generating Figure S4: Clinical Decision Tree...")
    
    fig, ax = plt.subplots(figsize=(20, 28))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 50)
    ax.axis('off')
    
    # Title
    ax.text(10, 48, 'Clinical Decision Tree for Personalized Dietary Coaching',
            ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(10, 46.5, 'Based on GGM Hub Analysis of Dietary Networks',
            ha='center', va='center', fontsize=12, style='italic')
    
    # ========== LEVEL 0: Entry Point ==========
    draw_box(ax, 10, 44, 4, 1.2, 'Patient\nEnrollment', '#E8F4F8', fontsize=10, fontweight='bold')
    draw_arrow(ax, 10, 43.4, 10, 42)
    
    # ========== LEVEL 1: Age Stratification ==========
    draw_box(ax, 10, 41, 5, 1.2, 'Age Group?', '#B3E5FC', fontsize=11, fontweight='bold')
    
    # Age branches
    draw_arrow(ax, 7.5, 40.4, 3, 38.5, '19-39세', 'blue')
    draw_arrow(ax, 10, 40.4, 10, 38.5, '40-59세', 'blue')
    draw_arrow(ax, 12.5, 40.4, 17, 38.5, '60-74세', 'blue')
    
    # ========== AGE: 청년층 (19-39세) ==========
    y_base = 38
    draw_box(ax, 3, y_base, 4, 1, '청년층\n(19-39세)', '#81D4FA', fontsize=10, fontweight='bold')
    draw_arrow(ax, 3, y_base - 0.6, 3, y_base - 1.5)
    
    # Sex branch
    y_sex = y_base - 2.2
    draw_box(ax, 3, y_sex, 3, 0.8, 'Sex?', '#FFE082', fontsize=9, fontweight='bold')
    draw_arrow(ax, 1.8, y_sex - 0.5, 1, y_sex - 1.5, 'Male')
    draw_arrow(ax, 4.2, y_sex - 0.5, 5, y_sex - 1.5, 'Female')
    
    # Male Youth
    y_mets = y_sex - 2.5
    draw_box(ax, 1, y_mets, 1.5, 0.7, 'MetS?', '#FFCCBC', fontsize=8, fontweight='bold')
    draw_arrow(ax, 0.4, y_mets - 0.45, 0.4, y_mets - 1.2, 'Yes')
    draw_arrow(ax, 1.6, y_mets - 0.45, 1.6, y_mets - 1.2, 'No')
    
    # Male Youth MetS(+)
    y_strat = y_mets - 2
    draw_box(ax, 0.4, y_strat, 1.4, 1.8,
             '남성 청년 MetS(+)\n\n목표:\n· 튀김류 감소\n· 가공식품 감소\n· 채소 증가\n\n우선순위: HIGH',
             '#FFCDD2', fontsize=7)
    
    # Male Youth MetS(-)
    draw_box(ax, 1.6, y_strat, 1.4, 1.8,
             '남성 청년 MetS(-)\n\n목표:\n· 가공식품 예방\n· 단백질 유지\n\n우선순위: MODERATE',
             '#C8E6C9', fontsize=7)
    
    # Female Youth (only MetS-)
    draw_box(ax, 5, y_mets, 1.5, 0.7, 'MetS(-) only', '#C8E6C9', fontsize=8)
    draw_arrow(ax, 5, y_mets - 0.45, 5, y_mets - 1.2)
    
    draw_box(ax, 5, y_strat, 1.4, 1.8,
             '여성 청년 MetS(-)\n\n목표:\n· 고지방육 대체\n· 가공식품 감소\n\n우선순위: MODERATE',
             '#C8E6C9', fontsize=7)
    
    # ========== AGE: 중년층 (40-59세) ==========
    draw_box(ax, 10, y_base, 4, 1, '중년층\n(40-59세)', '#81D4FA', fontsize=10, fontweight='bold')
    draw_arrow(ax, 10, y_base - 0.6, 10, y_base - 1.5)
    
    # Sex branch
    draw_box(ax, 10, y_sex, 3, 0.8, 'Sex?', '#FFE082', fontsize=9, fontweight='bold')
    draw_arrow(ax, 8.8, y_sex - 0.5, 8, y_sex - 1.5, 'Male')
    draw_arrow(ax, 11.2, y_sex - 0.5, 12, y_sex - 1.5, 'Female')
    
    # Male Middle
    draw_box(ax, 8, y_mets, 1.5, 0.7, 'MetS?', '#FFCCBC', fontsize=8, fontweight='bold')
    draw_arrow(ax, 7.4, y_mets - 0.45, 7.4, y_mets - 1.2, 'Yes')
    draw_arrow(ax, 8.6, y_mets - 0.45, 8.6, y_mets - 1.2, 'No')
    
    draw_box(ax, 7.4, y_strat, 1.4, 1.8,
             '남성 중년 MetS(+)\n\n목표:\n· 조리법 변경\n  (튀김→구이)\n· 가공식품 대체\n\n우선순위: HIGH',
             '#FFCDD2', fontsize=7)
    
    draw_box(ax, 8.6, y_strat, 1.4, 1.8,
             '남성 중년 MetS(-)\n\n목표:\n· 양질 단백질 유지\n· 튀김 모니터링\n\n우선순위: LOW',
             '#C8E6C9', fontsize=7)
    
    # Female Middle
    draw_box(ax, 12, y_mets, 1.5, 0.7, 'MetS?', '#FFCCBC', fontsize=8, fontweight='bold')
    draw_arrow(ax, 11.4, y_mets - 0.45, 11.4, y_mets - 1.2, 'Yes')
    draw_arrow(ax, 12.6, y_mets - 0.45, 12.6, y_mets - 1.2, 'No')
    
    draw_box(ax, 11.4, y_strat, 1.4, 1.8,
             '여성 중년 MetS(+)\n\n목표:\n· 단식품 감소★\n· 튀김/가공식품\n  감소\n\n우선순위: VERY HIGH',
             '#F44336', 'white', fontsize=7, fontweight='bold')
    
    draw_box(ax, 12.6, y_strat, 1.4, 1.8,
             '여성 중년 MetS(-)\n\n목표:\n· 가공식품 대체\n· 단백질 유지\n\n우선순위: MODERATE',
             '#FFF9C4', fontsize=7)
    
    # ========== AGE: 장년층 (60-74세) ==========
    draw_box(ax, 17, y_base, 4, 1, '장년층\n(60-74세)', '#81D4FA', fontsize=10, fontweight='bold')
    draw_arrow(ax, 17, y_base - 0.6, 17, y_base - 1.5)
    
    # Sex branch
    draw_box(ax, 17, y_sex, 3, 0.8, 'Sex?', '#FFE082', fontsize=9, fontweight='bold')
    draw_arrow(ax, 15.8, y_sex - 0.5, 15, y_sex - 1.5, 'Male')
    draw_arrow(ax, 18.2, y_sex - 0.5, 19, y_sex - 1.5, 'Female')
    
    # Male Elderly
    draw_box(ax, 15, y_mets, 1.5, 0.7, 'MetS?', '#FFCCBC', fontsize=8, fontweight='bold')
    draw_arrow(ax, 14.4, y_mets - 0.45, 14.4, y_mets - 1.2, 'Yes')
    draw_arrow(ax, 15.6, y_mets - 0.45, 15.6, y_mets - 1.2, 'No')
    
    draw_box(ax, 14.4, y_strat, 1.4, 1.8,
             '남성 장년 MetS(+)\n\n목표:\n· 당음료 제한★\n· 튀김/가공식품\n  감소\n\n우선순위: VERY HIGH',
             '#F44336', 'white', fontsize=7, fontweight='bold')
    
    draw_box(ax, 15.6, y_strat, 1.4, 1.8,
             '남성 장년 MetS(-)\n\n목표:\n· 단백질 유지\n  (근감소 예방)\n\n우선순위: LOW',
             '#C8E6C9', fontsize=7)
    
    # Female Elderly
    draw_box(ax, 19, y_mets, 1.5, 0.7, 'MetS?', '#FFCCBC', fontsize=8, fontweight='bold')
    draw_arrow(ax, 18.4, y_mets - 0.45, 18.4, y_mets - 1.2, 'Yes')
    draw_arrow(ax, 19.6, y_mets - 0.45, 19.6, y_mets - 1.2, 'No')
    
    draw_box(ax, 18.4, y_strat, 1.4, 1.8,
             '여성 장년 MetS(+)\n\n목표:\n· 고지방육 감소\n· 튀김 감소\n· 단백질 유지\n\n우선순위: HIGH',
             '#FFCDD2', fontsize=7)
    
    draw_box(ax, 19.6, y_strat, 1.4, 1.8,
             '여성 장년 MetS(-)\n\n모범 사례!\n· 단백질+채소\n· 현상 유지\n\n우선순위: MAINTAIN',
             '#4CAF50', 'white', fontsize=7, fontweight='bold')
    
    # ========== KEY INSIGHTS PANEL ==========
    y_key = 28
    
    # Background box for key insights
    key_box = FancyBboxPatch(
        (0.5, y_key - 9), 19, 9,
        boxstyle="round,pad=0.3",
        edgecolor='black',
        facecolor='#F5F5F5',
        linewidth=3,
        zorder=0
    )
    ax.add_patch(key_box)
    
    ax.text(10, y_key - 0.5, 'KEY INSIGHTS FROM GGM HUB ANALYSIS',
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Insight boxes
    # 1. MetS-Specific Pattern
    draw_box(ax, 3.5, y_key - 2.5, 6, 2,
             'MetS-SPECIFIC INTERVENTION TARGETS\n\n'
             '🔴 Fried Foods:\n'
             '   · MetS(+): 100% hub frequency\n'
             '   · MetS(-): 66.7% hub frequency\n'
             '   → PRIMARY reduction target for MetS patients\n\n'
             '🔵 Protein Foods:\n'
             '   · MetS(-): 100% hub frequency\n'
             '   · MetS(+): 40% hub frequency\n'
             '   → KEY for health maintenance',
             '#E3F2FD', fontsize=8)
    
    # 2. Group-Specific Hubs
    draw_box(ax, 10, y_key - 2.5, 5, 2,
             'UNIQUE GROUP-SPECIFIC HUBS\n\n'
             '⭐ Sweet Foods:\n'
             '   ONLY in middle-aged MetS(+) women\n'
             '   → Gender-specific intervention\n\n'
             '⭐ Sugar-Sweetened Beverages:\n'
             '   ONLY in elderly MetS(+) men\n'
             '   → Critical diabetes risk\n\n'
             '⭐ Vegetables:\n'
             '   Youth MetS(+) men\n'
             '   Elderly MetS(-) women\n'
             '   → Positive patterns to reinforce',
             '#FFF3E0', fontsize=8)
    
    # 3. Model Pattern
    draw_box(ax, 16.5, y_key - 2.5, 6, 2,
             'TARGET DIETARY PATTERN\n\n'
             '🏆 EXEMPLARY GROUP:\n'
             '   Elderly MetS(-) Women\n\n'
             '✓ Hub Foods:\n'
             '   · Protein Foods\n'
             '   · Vegetables\n\n'
             '✓ Network Structure:\n'
             '   · Sparsest network (density=0.045)\n'
             '   · Only 3 edges\n'
             '   · Most independent food consumption\n\n'
             'This is the ASPIRATIONAL pattern\n'
             'for all other groups',
             '#E8F5E9', fontsize=8)
    
    # Intervention Priority Legend
    draw_box(ax, 3, y_key - 5.5, 4, 2,
             'INTERVENTION PRIORITY LEVELS\n\n'
             'VERY HIGH: Immediate action\n'
             '  · Middle F_MetS+ (sweet foods)\n'
             '  · Elderly M_MetS+ (SSB)\n\n'
             'HIGH: Active intervention\n'
             '  · Youth M_MetS+ (fried foods)\n'
             '  · Middle M_MetS+ (cooking method)\n'
             '  · Elderly F_MetS+ (high-fat meat)\n\n'
             'MODERATE: Preventive counseling\n\n'
             'LOW: Monitoring\n\n'
             'MAINTAIN: Positive reinforcement',
             '#FCE4EC', fontsize=7.5)
    
    # Universal vs Personalized
    draw_box(ax, 8, y_key - 5.5, 5, 2,
             'TWO-TIERED INTERVENTION APPROACH\n\n'
             '🌍 UNIVERSAL TARGETS (All groups):\n'
             '   · Reduce processed food consumption\n'
             '     (appears in 10/11 groups = 90.9%)\n'
             '   · Reduce fried food consumption\n'
             '     (appears in 9/11 groups = 81.8%)\n\n'
             '👤 PERSONALIZED TARGETS:\n'
             '   · Age-specific hubs\n'
             '   · Sex-specific hubs\n'
             '   · MetS-specific hubs\n'
             '   · Group-specific intervention priorities',
             '#E1F5FE', fontsize=7.5)
    
    # GGM Advantage
    draw_box(ax, 14, y_key - 5.5, 5, 2,
             'GGM METHODOLOGICAL ADVANTAGE\n\n'
             '❌ Co-occurrence Networks:\n'
             '   · Vegetables, grains as hubs\n'
             '   · Uniform topology (20 edges)\n'
             '   · Spurious associations\n\n'
             '✅ GGM Networks:\n'
             '   · Processed/fried foods as hubs\n'
             '   · Variable topology (3-9 edges)\n'
             '   · Genuine conditional dependencies\n\n'
             '→ GGM reveals ACTUAL consumption\n'
             '   patterns, not guideline ideals',
             '#FFF9C4', fontsize=7.5)
    
    # Bottom note
    ax.text(10, y_key - 8.5,
            'Note: Coaching strategies derived from Gaussian Graphical Model analysis of 22,964 Korean adults (KNHANES)',
            ha='center', va='center', fontsize=9, style='italic')
    ax.text(10, y_key - 9,
            'Hub foods identified using degree centrality with partial correlation threshold ≥0.10',
            ha='center', va='center', fontsize=8, style='italic', color='gray')
    
    # Star legend for unique hubs
    ax.text(0.7, y_key - 9.5, '★ = Unique hub appearing only in this specific group',
            ha='left', va='center', fontsize=8, style='italic')
    
    plt.tight_layout()
    output_file = FIGURES_DIR / 'Figure_S4_Clinical_Decision_Tree_GGM.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='none', transparent=True)
    print(f"✅ Saved: {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")
    plt.close()

def main():
    """Main execution"""
    print("=" * 80)
    print("GENERATING FIGURE S4: CLINICAL DECISION TREE")
    print("Personalized Dietary Coaching Based on GGM Hub Analysis")
    print("=" * 80)
    
    generate_figure_s4()
    
    print("\n✅ Figure S4 generated successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
