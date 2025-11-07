#!/usr/bin/env python3
"""
Generate Table S5: Personalized Dietary Coaching Strategies by Age, Sex, and MetS Status
"""

import pandas as pd
from pathlib import Path

# Set up paths
BASE_DIR = Path('/home/user/webapp/ver4.0_GGM')
NETWORK_DIR = BASE_DIR / 'result' / 'networks'
TABLES_DIR = BASE_DIR / 'result' / 'supplementary_tables'

def generate_table_s5():
    """Generate Table S5: Personalized coaching strategies based on hub patterns"""
    print("\n📋 Generating Table S5: Personalized Coaching Strategies...")
    
    # Load network summary
    stats_df = pd.read_csv(NETWORK_DIR / 'ggm_network_summary.csv')
    
    # Define coaching strategies based on hub analysis
    coaching_data = []
    
    # 남성_청년층(19-39세)_MetS(+)
    coaching_data.append({
        'Group': '남성_청년층(19-39세)_MetS(+)',
        'Sex': '남성',
        'Age_Group': '청년층(19-39세)',
        'MetS_Status': 'MetS(+)',
        'Top_3_Hubs': 'Processed Foods, Vegetables, Fried Foods',
        'Hub_Frequency': 'Processed Foods (90.9%), Fried Foods (81.8%)',
        'Primary_Target': 'Fried Foods (MetS-specific, 100% vs 66.7%)',
        'Secondary_Target': 'Processed Foods (reduce central hub)',
        'Positive_Pattern': 'Vegetables appear (uncommon in young adults)',
        'Coaching_Strategy': 'Increase vegetable consumption while reducing fried/processed foods. Address sugar-sweetened beverage hub. Leverage existing vegetable consumption as foundation for healthier pattern.',
        'Intervention_Priority': 'High',
        'Rationale': 'Young MetS+ with unique vegetable hub offers intervention opportunity. Fried foods central in MetS+ (100%) vs MetS- (66.7%).'
    })
    
    # 남성_청년층(19-39세)_MetS(-)
    coaching_data.append({
        'Group': '남성_청년층(19-39세)_MetS(-)',
        'Sex': '남성',
        'Age_Group': '청년층(19-39세)',
        'MetS_Status': 'MetS(-)',
        'Top_3_Hubs': 'Processed Foods, Protein Foods, Fried Foods',
        'Hub_Frequency': 'Processed Foods (90.9%), Protein Foods (72.7%)',
        'Primary_Target': 'Processed Foods (preventive reduction)',
        'Secondary_Target': 'Maintain protein food quality',
        'Positive_Pattern': 'Protein Foods appear (health maintenance)',
        'Coaching_Strategy': 'Preventive intervention: reduce processed food centrality while maintaining protein intake. Monitor fried food consumption before it becomes entrenched.',
        'Intervention_Priority': 'Moderate',
        'Rationale': 'Healthy young adults with preventable risk pattern. Protein foods indicate potential for health maintenance (100% in MetS-).'
    })
    
    # 남성_중년층(40-59세)_MetS(+)
    coaching_data.append({
        'Group': '남성_중년층(40-59세)_MetS(+)',
        'Sex': '남성',
        'Age_Group': '중년층(40-59세)',
        'MetS_Status': 'MetS(+)',
        'Top_3_Hubs': 'Protein Foods, Fried Foods, Processed Foods',
        'Hub_Frequency': 'Fried Foods (81.8%), Processed Foods (90.9%)',
        'Primary_Target': 'Fried Foods (change cooking method to grilling)',
        'Secondary_Target': 'Processed Foods (gradual reduction)',
        'Positive_Pattern': 'Protein Foods hub (maintain quality)',
        'Coaching_Strategy': 'Modify cooking methods: transition from frying to grilling/steaming. Maintain protein intake but improve quality (lean cuts). Gradual processed food substitution.',
        'Intervention_Priority': 'High',
        'Rationale': 'Critical intervention window in middle age. Fried foods universal in MetS+ (100% vs 66.7% in MetS-).'
    })
    
    # 남성_중년층(40-59세)_MetS(-)
    coaching_data.append({
        'Group': '남성_중년층(40-59세)_MetS(-)',
        'Sex': '남성',
        'Age_Group': '중년층(40-59세)',
        'MetS_Status': 'MetS(-)',
        'Top_3_Hubs': 'Protein Foods, Fried Foods, Processed Foods',
        'Hub_Frequency': 'Protein Foods (72.7%), Fried Foods (81.8%)',
        'Primary_Target': 'Maintain high-quality protein consumption',
        'Secondary_Target': 'Monitor fried food intake',
        'Positive_Pattern': 'Protein Foods dominant (100% in MetS-)',
        'Coaching_Strategy': 'Health maintenance: emphasize lean protein sources (fish, chicken, legumes). Monitor but do not eliminate fried foods. Positive reinforcement for existing healthy protein pattern.',
        'Intervention_Priority': 'Low-Moderate',
        'Rationale': 'Healthy middle-aged men with strong protein hub (100% vs 40% in MetS+). Maintain protective pattern.'
    })
    
    # 남성_장년층(60-74세)_MetS(+)
    coaching_data.append({
        'Group': '남성_장년층(60-74세)_MetS(+)',
        'Sex': '남성',
        'Age_Group': '장년층(60-74세)',
        'MetS_Status': 'MetS(+)',
        'Top_3_Hubs': 'Fried Foods, Processed Foods, Sugar-Sweetened Beverages',
        'Hub_Frequency': 'Fried Foods (81.8%), Processed Foods (90.9%)',
        'Primary_Target': 'Sugar-Sweetened Beverages (unique to elderly MetS+)',
        'Secondary_Target': 'Fried Foods and Processed Foods',
        'Positive_Pattern': 'None identified',
        'Coaching_Strategy': 'CRITICAL: Restrict sugar-sweetened beverages (diabetes risk in elderly). Replace fried/processed foods with softer, easier-to-digest alternatives suitable for older adults. Consider dental/digestive constraints.',
        'Intervention_Priority': 'Very High',
        'Rationale': 'Elderly MetS+ with worst dietary pattern. Sugar-sweetened beverages appear only in this group (unique risk). Urgent intervention needed.'
    })
    
    # 남성_장년층(60-74세)_MetS(-)
    coaching_data.append({
        'Group': '남성_장년층(60-74세)_MetS(-)',
        'Sex': '남성',
        'Age_Group': '장년층(60-74세)',
        'MetS_Status': 'MetS(-)',
        'Top_3_Hubs': 'Protein Foods, Fried Foods, Processed Foods',
        'Hub_Frequency': 'Protein Foods (72.7%), Fried Foods (81.8%)',
        'Primary_Target': 'Maintain protein intake for sarcopenia prevention',
        'Secondary_Target': 'Gentle reduction of fried/processed foods',
        'Positive_Pattern': 'Protein Foods hub (100% vs 40% in MetS+)',
        'Coaching_Strategy': 'Geriatric health maintenance: ensure adequate protein for muscle mass. Gradually reduce fried foods with age-appropriate alternatives. Maintain current healthy pattern.',
        'Intervention_Priority': 'Low',
        'Rationale': 'Healthy elderly men with protective protein hub. Focus on maintaining functional nutrition in aging.'
    })
    
    # 여성_청년층(19-39세)_MetS(-)
    coaching_data.append({
        'Group': '여성_청년층(19-39세)_MetS(-)',
        'Sex': '여성',
        'Age_Group': '청년층(19-39세)',
        'MetS_Status': 'MetS(-)',
        'Top_3_Hubs': 'High Fat Meat, Processed Foods, Protein Foods',
        'Hub_Frequency': 'Processed Foods (90.9%), Protein Foods (72.7%)',
        'Primary_Target': 'High Fat Meat (female-specific hub)',
        'Secondary_Target': 'Processed Foods',
        'Positive_Pattern': 'Protein Foods indicate health awareness',
        'Coaching_Strategy': 'Redirect high-fat meat preference to lean proteins. Reduce processed food centrality. Leverage existing protein consumption for healthier substitutions (plant-based, fish).',
        'Intervention_Priority': 'Moderate',
        'Rationale': 'Young women with unique high-fat meat hub. Opportunity for early dietary pattern modification before MetS development.'
    })
    
    # 여성_중년층(40-59세)_MetS(+)
    coaching_data.append({
        'Group': '여성_중년층(40-59세)_MetS(+)',
        'Sex': '여성',
        'Age_Group': '중년층(40-59세)',
        'MetS_Status': 'MetS(+)',
        'Top_3_Hubs': 'Fried Foods, Processed Foods, Sweet Food Consumption',
        'Hub_Frequency': 'Fried Foods (81.8%), Processed Foods (90.9%)',
        'Primary_Target': 'Sweet Food Consumption (unique to middle-aged MetS+ women)',
        'Secondary_Target': 'Fried Foods and Processed Foods',
        'Positive_Pattern': 'None identified',
        'Coaching_Strategy': 'GENDER-SPECIFIC: Address sweet food consumption hub (appears only in this group). Reduce fried/processed foods. Consider hormonal/menopausal influences on dietary preferences. Substitute sweets with fruits.',
        'Intervention_Priority': 'Very High',
        'Rationale': 'Critical group: sweet foods appear uniquely in middle-aged MetS+ women. Combined with fried/processed hubs creates high-risk pattern.'
    })
    
    # 여성_중년층(40-59세)_MetS(-)
    coaching_data.append({
        'Group': '여성_중년층(40-59세)_MetS(-)',
        'Sex': '여성',
        'Age_Group': '중년층(40-59세)',
        'MetS_Status': 'MetS(-)',
        'Top_3_Hubs': 'Processed Foods, Protein Foods, Fried Foods',
        'Hub_Frequency': 'Processed Foods (90.9%), Protein Foods (72.7%)',
        'Primary_Target': 'Processed Foods (high centrality: 0.273)',
        'Secondary_Target': 'Maintain protein foods',
        'Positive_Pattern': 'Protein Foods hub (health maintenance)',
        'Coaching_Strategy': 'Focus on processed food substitution while maintaining protein intake. Preventive intervention for high-risk transition period (menopause). Reinforce healthy protein pattern.',
        'Intervention_Priority': 'Moderate-High',
        'Rationale': 'Healthy middle-aged women with highest processed food centrality (0.273). Preventive intervention during menopausal transition.'
    })
    
    # 여성_장년층(60-74세)_MetS(+)
    coaching_data.append({
        'Group': '여성_장년층(60-74세)_MetS(+)',
        'Sex': '여성',
        'Age_Group': '장년층(60-74세)',
        'MetS_Status': 'MetS(+)',
        'Top_3_Hubs': 'Protein Foods, Fried Foods, High Fat Meat',
        'Hub_Frequency': 'Fried Foods (81.8%), Protein Foods (72.7%)',
        'Primary_Target': 'High Fat Meat (reduce saturated fat intake)',
        'Secondary_Target': 'Fried Foods (cardiovascular risk)',
        'Positive_Pattern': 'Protein Foods hub (maintain for sarcopenia)',
        'Coaching_Strategy': 'Geriatric MetS management: reduce high-fat meat and fried foods (cardiovascular risk). Maintain adequate protein with lean sources. Age-appropriate portion sizes and textures.',
        'Intervention_Priority': 'High',
        'Rationale': 'Elderly MetS+ women with high-fat meat hub. Balance protein needs (sarcopenia) with cardiovascular risk reduction.'
    })
    
    # 여성_장년층(60-74세)_MetS(-)
    coaching_data.append({
        'Group': '여성_장년층(60-74세)_MetS(-)',
        'Sex': '여성',
        'Age_Group': '장년층(60-74세)',
        'MetS_Status': 'MetS(-)',
        'Top_3_Hubs': 'Protein Foods, Vegetables, Processed Foods',
        'Hub_Frequency': 'Protein Foods (72.7%), Vegetables (18.2%)',
        'Primary_Target': 'MAINTAIN current pattern (healthiest in study)',
        'Secondary_Target': 'Reduce minimal processed food intake',
        'Positive_Pattern': '**EXEMPLARY**: Protein + Vegetables, sparsest network (density=0.045)',
        'Coaching_Strategy': 'MODEL PATTERN: Use as benchmark for other groups. Maintain protein-vegetable core. Minimal intervention needed. Positive reinforcement for healthy aging dietary pattern.',
        'Intervention_Priority': 'Very Low (Maintenance Only)',
        'Rationale': 'HEALTHIEST GROUP: Elderly MetS- women with protein-vegetable hubs and sparsest network. This represents the target pattern for all groups.'
    })
    
    df_coaching = pd.DataFrame(coaching_data)
    
    # Save full version as CSV
    output_file = TABLES_DIR / 'Table_S5_Personalized_Coaching_Strategies_GGM.csv'
    df_coaching.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Saved: {output_file}")
    
    # Save formatted version as TXT
    output_txt = TABLES_DIR / 'Table_S5_Personalized_Coaching_Strategies_GGM.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 150 + "\n")
        f.write("TABLE S5. Personalized Dietary Coaching Strategies by Age, Sex, and MetS Status (GGM Analysis)\n")
        f.write("=" * 150 + "\n\n")
        
        f.write("Based on GGM hub analysis revealing:\n")
        f.write("  • Fried Foods: 100% hub frequency in MetS(+) vs 66.7% in MetS(-) → PRIMARY INTERVENTION TARGET\n")
        f.write("  • Protein Foods: 100% hub frequency in MetS(-) vs 40% in MetS(+) → HEALTH MAINTENANCE KEY\n")
        f.write("  • Group-specific hubs: Sweet foods (middle F_MetS+), SSB (elderly M_MetS+), Vegetables (youth M_MetS+, elderly F_MetS-)\n\n")
        
        f.write("-" * 150 + "\n\n")
        
        # Group by age
        for age in ['청년층(19-39세)', '중년층(40-59세)', '장년층(60-74세)']:
            f.write(f"\n{'='*150}\n")
            f.write(f"AGE GROUP: {age}\n")
            f.write(f"{'='*150}\n\n")
            
            age_data = df_coaching[df_coaching['Age_Group'] == age]
            
            for _, row in age_data.iterrows():
                f.write(f"\n{'─'*150}\n")
                f.write(f"Group: {row['Group']}\n")
                f.write(f"{'─'*150}\n")
                f.write(f"Top 3 Hubs:         {row['Top_3_Hubs']}\n")
                f.write(f"Hub Frequency:      {row['Hub_Frequency']}\n")
                f.write(f"Primary Target:     {row['Primary_Target']}\n")
                f.write(f"Secondary Target:   {row['Secondary_Target']}\n")
                f.write(f"Positive Pattern:   {row['Positive_Pattern']}\n")
                f.write(f"Intervention Priority: {row['Intervention_Priority']}\n\n")
                f.write(f"Coaching Strategy:\n")
                f.write(f"  {row['Coaching_Strategy']}\n\n")
                f.write(f"Rationale:\n")
                f.write(f"  {row['Rationale']}\n")
        
        f.write(f"\n\n{'='*150}\n")
        f.write("KEY INSIGHTS FOR PERSONALIZED COACHING:\n")
        f.write("=" * 150 + "\n\n")
        
        f.write("1. MetS-SPECIFIC PATTERNS:\n")
        f.write("   • Fried Foods: Universal in MetS(+) groups [5/5 = 100%] vs 2/3 = 66.7% in MetS(-)\n")
        f.write("     → PRIMARY intervention target for MetS patients\n\n")
        
        f.write("2. HEALTH MAINTENANCE PATTERNS:\n")
        f.write("   • Protein Foods: Universal in MetS(-) groups [6/6 = 100%] vs 2/5 = 40% in MetS(+)\n")
        f.write("     → KEY for maintaining metabolic health\n\n")
        
        f.write("3. UNIQUE GROUP-SPECIFIC HUBS:\n")
        f.write("   • Sweet Foods: Appear ONLY in middle-aged MetS(+) women → gender-specific intervention\n")
        f.write("   • Sugar-Sweetened Beverages: Appear ONLY in elderly MetS(+) men → critical diabetes risk\n")
        f.write("   • Vegetables: Appear in youth MetS(+) men and elderly MetS(-) women → positive patterns to reinforce\n\n")
        
        f.write("4. EXEMPLARY PATTERN:\n")
        f.write("   • Elderly MetS(-) women: Protein + Vegetables, sparsest network (density=0.045)\n")
        f.write("     → This is the TARGET pattern for all other groups to aspire to\n\n")
        
        f.write("5. INTERVENTION PRIORITY TIERS:\n")
        f.write("   • VERY HIGH: Elderly M_MetS+ (SSB risk), Middle F_MetS+ (sweet foods risk)\n")
        f.write("   • HIGH: Youth M_MetS+ (fried foods), Middle M_MetS+ (fried foods), Elderly F_MetS+ (high-fat meat)\n")
        f.write("   • MODERATE: Youth M_MetS-, Youth F_MetS-, Middle F_MetS-\n")
        f.write("   • LOW: Middle M_MetS-, Elderly M_MetS-\n")
        f.write("   • VERY LOW: Elderly F_MetS- (maintenance only - model pattern)\n\n")
        
        f.write("=" * 150 + "\n")
        f.write("Note: Coaching strategies derived from GGM conditional dependency analysis\n")
        f.write("      revealing actual dietary network structures, not dietary guideline ideals.\n")
        f.write("=" * 150 + "\n")
    
    print(f"✅ Saved: {output_txt}")
    
    return df_coaching

def main():
    """Main execution"""
    print("=" * 80)
    print("GENERATING TABLE S5: PERSONALIZED COACHING STRATEGIES")
    print("Based on MetS-specific hub pattern analysis")
    print("=" * 80)
    
    df_coaching = generate_table_s5()
    
    print("\n✅ Table S5 generated successfully!")
    print(f"\n📊 Summary:")
    print(f"   • Total groups: {len(df_coaching)}")
    print(f"   • Very High Priority: {len(df_coaching[df_coaching['Intervention_Priority'] == 'Very High'])}")
    print(f"   • High Priority: {len(df_coaching[df_coaching['Intervention_Priority'] == 'High'])}")
    print(f"   • Model Pattern: Elderly F_MetS- (Protein + Vegetables)")
    print("=" * 80)

if __name__ == "__main__":
    main()
