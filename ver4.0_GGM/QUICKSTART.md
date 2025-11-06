# ver4.0 Quick Start Guide

## ✅ Status: Ready to Run

GitHub Repository: https://github.com/HeejeongH/Network/tree/main/ver4.0_GGM

## 🚀 5-Minute Quick Start

### 1. Clone Repository (if not already)

```bash
git clone https://github.com/HeejeongH/Network.git
cd Network/ver4.0_GGM
```

### 2. Install Dependencies

```bash
pip install pandas numpy scipy scikit-learn networkx
```

### 3. Run Full Analysis (11 Groups)

```bash
python src/ggm_stratified_networks.py
```

**Expected Runtime**: ~5-10 minutes for all 11 groups

### 4. Check Results

```bash
# View summary statistics
cat result/networks/ggm_network_summary.csv

# List all generated network files
ls -lh result/networks/
```

## 📊 What You'll Get

### Output Files (33 files total for 11 groups)

**Per Group** (×11):
1. `ggm_network_{sex}_{age}_{mets}.gexf` - Network file for Gephi visualization
2. `ggm_network_{sex}_{age}_{mets}_partial_corr.csv` - 12×12 partial correlation matrix
3. Summary row in `ggm_network_summary.csv`

**Summary File**:
- `ggm_network_summary.csv` - All groups comparison table

### Example Output

```
================================================================================
🚀 GGM-BASED STRATIFIED DIETARY NETWORK ANALYSIS (ver4.0)
================================================================================

🔬 Processing: 남성 - 청년층(19-39세) - MetS(+)
📊 Sample size: 516

  📊 Creating GGM network for 516 samples...
  📈 Step 1: Computing Spearman correlation matrix...
  🔧 Step 2: Applying Graphical Lasso with CV...
  ✅ Best alpha: 0.0589
  🕸️  Step 3: Building network graph...
  ✅ Network created: 12 nodes, 9 edges
  📊 Density: 0.1364

  🎯 Top 3 hubs by degree centrality:
    1. Protein Foods: 0.8182
    2. Vegetables: 0.7273
    3. Grain Products: 0.4545

✅ Saved network: ggm_network_남성_청년층(19-39세)_MetS(+).gexf
...
```

## 🎯 Next Steps After Running

### 1. Compare with ver3.0 Results

```bash
# Compare network statistics
python -c "
import pandas as pd

# Load ver4.0 results
v4 = pd.read_csv('result/networks/ggm_network_summary.csv')
print('ver4.0 GGM Results:')
print(v4[['Group', 'N_Edges', 'Density', 'Alpha']].head())
print(f'\nAverage density: {v4['Density'].mean():.4f}')
print(f'Density range: {v4['Density'].min():.4f} - {v4['Density'].max():.4f}')

# Compare with ver3.0 (all groups had 20 edges, density=0.303)
print('\nver3.0 had:')
print('  All groups: 20 edges, density=0.303')
print('\nGGM removes spurious edges!')
"
```

### 2. Visualize Networks in Gephi

1. Download Gephi: https://gephi.org/
2. Open `.gexf` files from `result/networks/`
3. Apply ForceAtlas2 layout
4. Size nodes by degree centrality
5. Color by food group categories

### 3. Analyze Hub Foods

```bash
python -c "
import pandas as pd

df = pd.read_csv('result/networks/ggm_network_summary.csv')

print('='*80)
print('HUB FOOD ANALYSIS ACROSS ALL GROUPS')
print('='*80)

# Count hub appearances
from collections import Counter
hub1_counts = Counter(df['Hub_1_Name'])
hub2_counts = Counter(df['Hub_2_Name'])  
hub3_counts = Counter(df['Hub_3_Name'])

all_hubs = hub1_counts + hub2_counts + hub3_counts

print('\nTop Hub Foods (frequency as top-3 hub):')
for food, count in all_hubs.most_common(5):
    print(f'  {food}: {count}/11 groups ({count/11*100:.1f}%)')

print('\nUniversal Hubs (appear in all 11 groups):')
for food, count in all_hubs.items():
    if count >= 11:
        print(f'  ✅ {food}')
"
```

### 4. Extract Key Statistics for Paper

```bash
python -c "
import pandas as pd
import numpy as np

df = pd.read_csv('result/networks/ggm_network_summary.csv')

print('='*80)
print('KEY STATISTICS FOR PAPER RESULTS SECTION')
print('='*80)

print('\n1. Network Density:')
print(f'   Range: {df['Density'].min():.4f} - {df['Density'].max():.4f}')
print(f'   Mean: {df['Density'].mean():.4f} ± {df['Density'].std():.4f}')

print('\n2. Number of Edges:')
print(f'   Range: {int(df['N_Edges'].min())} - {int(df['N_Edges'].max())}')
print(f'   Mean: {df['N_Edges'].mean():.1f} ± {df['N_Edges'].std():.1f}')

print('\n3. Regularization Parameter (Alpha):')
print(f'   Range: {df['Alpha'].min():.4f} - {df['Alpha'].max():.4f}')
print(f'   Mean: {df['Alpha'].mean():.4f} ± {df['Alpha'].std():.4f}')

print('\n4. Hub Degree Centrality:')
print(f'   Hub 1 range: {df['Hub_1_Degree'].min():.4f} - {df['Hub_1_Degree'].max():.4f}')
print(f'   Hub 2 range: {df['Hub_2_Degree'].min():.4f} - {df['Hub_2_Degree'].max():.4f}')
print(f'   Hub 3 range: {df['Hub_3_Degree'].min():.4f} - {df['Hub_3_Degree'].max():.4f}')
"
```

## 🔧 Customization Options

### Change Minimum Correlation Threshold

Edit `ggm_stratified_networks.py` line 386:

```python
# Current: min_correlation=0.1
G, alpha, partial_corr = create_ggm_network(
    group_data, 
    FOOD_GROUPS, 
    min_correlation=0.15,  # ← Change this (higher = fewer edges)
    verbose=True
)
```

### Adjust Alpha Range for Cross-Validation

Edit line 165:

```python
# Current: np.logspace(-2, -0.3, 15)
best_alpha, precision, partial_corr = graphical_lasso_cv(
    corr_matrix, 
    alphas=np.logspace(-2, 0, 20),  # ← Change range/count
    cv_folds=5,
    verbose=verbose
)
```

### Add Community Detection

Add after line 390:

```python
# Add Louvain community detection
import community as community_louvain

if G.number_of_edges() > 0:
    communities = community_louvain.best_partition(G)
    print(f"  🏘️  Communities detected: {len(set(communities.values()))}")
    
    # Add to node attributes
    nx.set_node_attributes(G, communities, 'community')
```

## 📝 For Paper Writing

### Methods Section Template

```markdown
## Network Construction

Dietary networks were constructed using Semiparametric Gaussian Copula 
Graphical Models (SGCGM) to estimate conditional dependencies between 
food groups via partial correlations [1,2]. Food group scores (range: 1-4) 
were analyzed as continuous variables to preserve information. 

To accommodate non-normal distributions typical in dietary data, we applied 
rank-based transformations using Spearman's rho. The correlation matrix was 
then regularized via graphical lasso (L1-penalized precision matrix estimation) 
to yield sparse networks representing only direct conditional dependencies. 
The optimal regularization parameter (λ) was selected via 5-fold cross-validation 
for each stratified group independently. 

Precision matrix elements were converted to partial correlations, and edges 
were retained if the absolute partial correlation exceeded 0.10. This threshold 
ensures that only meaningful direct relationships are included while maintaining 
computational stability.

## Network Analysis

For each network, we calculated three centrality metrics: degree centrality 
(number of direct connections), betweenness centrality (frequency on shortest 
paths), and closeness centrality (inverse average path length). Hub foods were 
defined as those ranking in the top three for degree centrality within their 
stratified group.

References:
[1] Schwedhelm et al. (2018) PLoS ONE 13(8):e0202936
[2] Friedman et al. (2008) Biostatistics 9(3):432-441
```

### Results Section Template

```markdown
## Network Structure

All 11 stratified networks were successfully constructed using SGCGM. Network 
density ranged from [MIN] to [MAX] (mean: [MEAN] ± [SD]), representing 
[%] of possible connections. The number of edges varied from [MIN] to [MAX] 
(mean: [MEAN] ± [SD]), reflecting group-specific dietary patterns. The 
cross-validated regularization parameter α ranged from [MIN] to [MAX].

## Universal and Group-Specific Hubs

Three food groups emerged as universal hubs, appearing among the top three 
centrality ranks in all 11 networks: [FOOD1] (degree centrality range: 
[MIN]-[MAX]), [FOOD2] ([MIN]-[MAX]), and [FOOD3] ([MIN]-[MAX]). 
These foods represent a core dietary structure common across demographic 
and metabolic subgroups.

[Continue with group-specific patterns...]
```

## ❓ Troubleshooting

### Issue: "FloatingPointError in graphical_lasso"

**Solution**: Lower alpha values or reduce min_correlation threshold

```python
alphas=np.logspace(-3, -0.3, 20)  # Start from 0.001 instead of 0.01
```

### Issue: "Too few edges in some groups"

**Solution**: Lower min_correlation threshold

```python
min_correlation=0.05  # Down from 0.10
```

### Issue: "Analysis takes too long"

**Solution**: Reduce alpha search space

```python
alphas=np.logspace(-2, -0.3, 10)  # Test only 10 values instead of 15
```

## 📧 Support

- GitHub Issues: https://github.com/HeejeongH/Network/issues
- Documentation: See README.md and COMPARISON_ver3_vs_ver4.md

---

**Last Updated**: 2025-11-06  
**Version**: 4.0.0  
**Status**: Production Ready ✅
