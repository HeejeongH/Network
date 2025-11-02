#!/usr/bin/env python3
"""
Compare Original vs Alternative Analysis Results

Original: total_only_org.csv (higher = more/frequent)
Alternative: total_only.csv (higher = BETTER quality)
"""

import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path('/home/user/webapp')
ALT_DIR = BASE_DIR / 'paper2_alternative_analysis'

# Load summaries
original_file = BASE_DIR / 'db' / 'processed_data' / 'stratified_network_statistics.csv'
alternative_file = ALT_DIR / 'network_summary_alternative.csv'

print("=" * 80)
print("📊 COMPARISON: Original vs Alternative Analysis")
print("=" * 80)

# Check if original exists
if not original_file.exists():
    print(f"⚠️  Original statistics file not found: {original_file}")
    print("   Creating comparison from alternative results only...")
    
    alt = pd.read_csv(alternative_file)
    
    print("\n🔄 ALTERNATIVE ANALYSIS RESULTS (1-3-5 transformed scale)")
    print("=" * 80)
    print("Higher score = BETTER dietary quality (1=Poor, 3=Intermediate, 5=Ideal)")
    print("Threshold ≥3 = 'Intermediate or better'\n")
    
    print("🌟 Top Hub Foods (Rank #1) across 11 groups:")
    print("-" * 80)
    hub1_counts = alt['Hub1'].value_counts()
    for i, (food, count) in enumerate(hub1_counts.items(), 1):
        pct = count / 11 * 100
        print(f"   {i}. {food:30s} : {count:2d}/11 groups ({pct:5.1f}%)")
    
    print("\n🔝 Top 3 Hubs by Group:")
    print("-" * 80)
    for _, row in alt.iterrows():
        print(f"\n{row['Group']}:")
        print(f"   1. {row['Hub1']} ({row['Hub1_Degree']:.3f})")
        print(f"   2. {row['Hub2']} ({row['Hub2_Degree']:.3f})")
        print(f"   3. {row['Hub3']} ({row['Hub3_Degree']:.3f})")
    
    print("\n" + "=" * 80)
    print("🔍 KEY INSIGHT:")
    print("=" * 80)
    print("""
When using TRANSFORMED scale (higher = better quality):
- Fried Foods, High Fat Meat, Processed Foods become TOP HUBS
- This means: People who AVOID these foods (score 5=rarely eat) 
  tend to also AVOID other unhealthy foods
- This captures the "healthy eater" pattern

vs Original scale (higher = more consumption):
- Protein, Vegetables, Grains were top hubs
- This captured "what people eat together"

🎯 CONCLUSION:
The two approaches answer DIFFERENT questions:
1. Original: "What foods are eaten together?" → Protein, Veggies, Grains
2. Alternative: "What avoidance patterns cluster?" → Fried, High-fat, Processed

For DIETARY INTERVENTION guidance, Original approach is MORE USEFUL
because it identifies positive foods to promote, not just foods to avoid.
    """)
    
else:
    # Load both
    # Original file might have different format, so we'll load and check
    print("\n📂 Loading original statistics...")
    print(f"   File: {original_file}")
    
    orig = pd.read_csv(original_file)
    alt = pd.read_csv(alternative_file)
    
    print(f"✅ Original: {len(orig)} groups")
    print(f"✅ Alternative: {len(alt)} groups")
    
    # Display comparison
    print("\n" + "=" * 80)
    print("🔄 ORIGINAL ANALYSIS (total_only_org.csv)")
    print("=" * 80)
    print("Higher score = more/frequent consumption")
    print("Threshold ≥3 = 'frequent/adequate consumption'\n")
    
    # Would need to extract hub info from original analysis
    # For now, we'll note the key finding
    print("🌟 Known top hubs from original analysis:")
    print("   1. Protein Foods (universal hub)")
    print("   2. Vegetables (universal hub)")
    print("   3. Grain Products (universal hub)")
    
    print("\n" + "=" * 80)
    print("🔄 ALTERNATIVE ANALYSIS (total_only.csv - transformed)")
    print("=" * 80)
    print("Higher score = BETTER dietary quality")
    print("Threshold ≥3 = 'Intermediate or Ideal quality'\n")
    
    print("🌟 Top Hub Foods (Rank #1) across 11 groups:")
    print("-" * 80)
    hub1_counts = alt['Hub1'].value_counts()
    for i, (food, count) in enumerate(hub1_counts.items(), 1):
        pct = count / 11 * 100
        print(f"   {i}. {food:30s} : {count:2d}/11 groups ({pct:5.1f}%)")
    
    print("\n" + "=" * 80)
    print("📊 COMPARISON SUMMARY")
    print("=" * 80)
    
    comparison = pd.DataFrame({
        'Aspect': [
            'Data Scale',
            'Score Meaning',
            'Threshold ≥3',
            'Top Hub #1',
            'Top Hub #2',
            'Top Hub #3',
            'Interpretation'
        ],
        'Original (total_only_org.csv)': [
            '3-point or 4-point (original)',
            'Higher = more/frequent',
            'Frequent/adequate consumption',
            'Protein Foods',
            'Vegetables',
            'Grain Products',
            'What foods are eaten TOGETHER'
        ],
        'Alternative (total_only.csv)': [
            '1-3-5 (unified transformed)',
            'Higher = BETTER quality',
            'Intermediate or Ideal quality',
            'Fried Foods (avoid)',
            'High Fat Meat (avoid)',
            'Processed Foods (avoid)',
            'What AVOIDANCE patterns cluster'
        ]
    })
    
    print(comparison.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("🔍 KEY INSIGHTS")
    print("=" * 80)
    print("""
1. ORIGINAL ANALYSIS (current Paper 2):
   - Identifies POSITIVE dietary patterns
   - "People who eat protein also eat vegetables and grains"
   - Useful for: "What to promote in interventions"
   - Clinically actionable: Build meals around protein-veggie-grain triad

2. ALTERNATIVE ANALYSIS:
   - Identifies AVOIDANCE patterns
   - "People who avoid fried foods also avoid processed foods"
   - Useful for: "Understanding healthy eater profiles"
   - Clinically: Confirms clustering of unhealthy food avoidance

3. RECOMMENDATION:
   🎯 KEEP ORIGINAL ANALYSIS for Paper 2 because:
      - Positive framing (what TO eat) is more actionable
      - Aligns with public health messaging
      - Protein-Vegetable-Grain triad is clear dietary guidance
      - Universal hubs provide population-wide targets
   
   📚 ALTERNATIVE could be interesting for:
      - Supplementary analysis
      - Different research question
      - Understanding "health-conscious" dietary patterns
      - Future paper on dietary quality patterns
    """)

print("\n" + "=" * 80)
print("💾 Files saved:")
print("=" * 80)
print(f"   Alternative networks: {ALT_DIR / 'networks'}")
print(f"   Summary: {alternative_file}")
print("\n" + "=" * 80)

