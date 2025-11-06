# ver4.0: GGM-Based Dietary Network Analysis

## 🎯 Overview

**Version 4.0** upgrades the dietary network analysis from simple co-occurrence to **Gaussian Graphical Models (GGM)**, implementing the methodology from:
- Schwedhelm et al. (2021) - *Int J Behav Nutr Phys Act*
- Schwedhelm et al. (2018) - *PLOS ONE*

## 🚀 Key Improvements over ver3.0

| Feature | ver3.0 (Co-occurrence) | ver4.0 (GGM) |
|---------|----------------------|--------------|
| **Data Type** | Binarized (≥3 vs <3) | Continuous scores (1-4) |
| **Relationship** | Simple co-occurrence | Partial correlations |
| **Confounding** | Not controlled | Controlled for all other foods |
| **Threshold** | Arbitrary (70th percentile) | Data-driven (cross-validation) |
| **Spurious Edges** | Possible | Removed via Graphical Lasso |
| **Information Loss** | High (binarization) | Low (continuous) |

## 📚 Method: Semiparametric Gaussian Copula Graphical Model (SGCGM)

### Pipeline

```
Raw Data (12 food groups, continuous scores)
    ↓
[1] Rank-based Transformation (Spearman correlation)
    ↓
[2] Graphical Lasso (L1-penalized precision matrix)
    ↓
[3] Cross-validation (optimal regularization parameter α)
    ↓
[4] Partial Correlation Network
    ↓
[5] Hub Identification (degree, betweenness, closeness centrality)
```

### Key Concepts

**Partial Correlation**: Correlation between two foods controlling for all other foods
- Removes indirect relationships (e.g., A→B→C doesn't create A↔C edge)
- Reveals true conditional dependencies

**Graphical Lasso**: Sparse precision matrix estimation
- Penalty parameter α controls network sparsity
- Prevents overfitting and false edges

**Cross-Validation**: Data-driven threshold selection
- Tests multiple α values
- Selects α that balances fit and sparsity

## 📁 Directory Structure

```
ver4.0_GGM/
├── src/
│   └── ggm_stratified_networks.py    # Main GGM analysis script
├── db/
│   └── (uses ver3.0 data)
├── result/
│   └── networks/
│       ├── ggm_network_*.gexf        # Network files (11 groups)
│       ├── ggm_network_*_partial_corr.csv  # Partial correlation matrices
│       └── ggm_network_summary.csv   # Summary statistics
├── docs/
└── README.md
```

## 🔧 Installation

### Requirements

```bash
# Python 3.8+
pip install pandas numpy scipy scikit-learn networkx
```

### Package Versions
- pandas >= 1.3.0
- numpy >= 1.20.0
- scipy >= 1.7.0
- scikit-learn >= 1.0.0
- networkx >= 2.6

## 🏃 Usage

### Basic Run

```bash
cd /home/user/Network/ver4.0_GGM
python src/ggm_stratified_networks.py
```

### Expected Output

```
🚀 GGM-BASED STRATIFIED DIETARY NETWORK ANALYSIS (ver4.0)
Method: Semiparametric Gaussian Copula Graphical Models
Improvements over ver3.0:
  ✅ Continuous scores (not binarized)
  ✅ Partial correlations (controlling for all other foods)
  ✅ Graphical Lasso (removes spurious correlations)
  ✅ Cross-validation for optimal regularization

📂 Loading data...
✅ Loaded 22,964 samples

🔬 Processing: 남성 - 청년층(19-39세) - MetS(+)
📊 Sample size: 516
  📊 Creating GGM network for 516 samples...
  📈 Step 1: Computing Spearman correlation matrix...
  🔧 Step 2: Applying Graphical Lasso with CV...
  🔍 Testing 15 alpha values with 5-fold CV...
  ✅ Best alpha: 0.0589
  🕸️  Step 3: Building network graph...
  ✅ Network created: 12 nodes, 18 edges
  📊 Density: 0.2727, Alpha: 0.0589
  
  🎯 Top 3 hubs by degree centrality:
    1. Protein Foods: 0.8182
    2. Vegetables: 0.7273
    3. Grain Products: 0.4545
...
```

## 📊 Output Files

### 1. Network Files (`.gexf`)
- Gephi-compatible network format
- Node: Food groups
- Edge: Partial correlation (weight = absolute value)
- Attributes: partial_corr (signed value)

### 2. Partial Correlation Matrices (`.csv`)
- 12×12 matrix of partial correlations
- Values range from -1 to +1
- Diagonal = 1.0

### 3. Summary Statistics (`ggm_network_summary.csv`)

| Column | Description |
|--------|-------------|
| Group | Stratification group |
| N_Samples | Sample size |
| N_Edges | Number of edges in network |
| Density | Network density (0-1) |
| Alpha | Optimal regularization parameter |
| Hub_1/2/3_Name | Top 3 hub food names |
| Hub_1/2/3_Degree | Degree centrality values |

## 🔬 Scientific Background

### Why GGM over Simple Co-occurrence?

**Problem with Simple Co-occurrence**:
```
If A and B often consumed together (co-occur), AND
   B and C often consumed together,
Then A and C will also show co-occurrence

BUT: A and C might not have direct relationship!
```

**GGM Solution (Partial Correlations)**:
```
Partial correlation between A and C = correlation controlling for B

If A↔C relationship disappears when controlling for B,
then A and C don't have direct relationship (removed from network)
```

### Mathematical Foundation

**Gaussian Graphical Model**:
- Assumes X ~ N(μ, Σ) where Σ is covariance matrix
- Precision matrix Θ = Σ⁻¹
- Partial correlation: ρᵢⱼ = -θᵢⱼ / √(θᵢᵢ × θⱼⱼ)
- Zero in Θ → conditional independence

**Graphical Lasso**:
```
minimize: -log det(Θ) + tr(SΘ) + λ||Θ||₁

where:
  S = empirical covariance matrix
  λ = regularization parameter (alpha)
  ||·||₁ = L1 norm (encourages sparsity)
```

**Semiparametric Extension (SGCGM)**:
- Handles non-normal distributions (common in dietary data)
- Uses rank-based transformation (Spearman correlation)
- Then applies Graphical Lasso

## 📈 Comparison with ver3.0

### Network Topology Differences

**ver3.0**: All groups had identical topology (12 nodes, 20 edges)
- Fixed by 70th percentile threshold
- Network structure doesn't vary across groups

**ver4.0**: Topology varies by group
- Data-driven edge selection
- Reflects true differences in dietary patterns
- Expected: Different edge counts and densities

### Hub Identification

**ver3.0**: Hub rankings may include spurious hubs
- Indirect relationships counted

**ver4.0**: Only direct relationships counted
- More accurate hub identification
- Clearer distinction between universal and group-specific hubs

## 🎓 For Paper Revision

### Methods Section Update

Replace:
```
"Co-occurrence networks were constructed based on 
simultaneous high-consumption patterns (score ≥3). 
Edges were retained if co-occurrence exceeded the 
70th percentile."
```

With:
```
"Dietary networks were constructed using Semiparametric 
Gaussian Copula Graphical Models (SGCGM), estimating 
conditional dependencies via partial correlations. 
To accommodate non-normal distributions in dietary data, 
we applied rank-based transformations (Spearman correlation) 
followed by graphical lasso regularization with L1 penalty. 
The optimal regularization parameter (λ) was selected via 
cross-validation. This approach identifies genuine 
co-consumption patterns while controlling for confounding 
relationships."
```

### Expected Results Changes

1. **Network Density**: Will likely vary across groups (not fixed at 0.303)
2. **Hub Centrality**: More pronounced differences between hubs and non-hubs
3. **Partial Correlations**: Can report strength of relationships (ver3.0 couldn't)
4. **Community Structure**: Can be analyzed (add Louvain community detection)

## 📝 Citation

If using this code, cite the methodological papers:

```bibtex
@article{schwedhelm2021meal,
  title={Using food network analysis to understand meal patterns in pregnant women with high and low diet quality},
  author={Schwedhelm, Carolina and Lipsky, Leah M and Shearrer, Grace E and others},
  journal={International Journal of Behavioral Nutrition and Physical Activity},
  volume={18},
  pages={1--15},
  year={2021}
}

@article{schwedhelm2018meal,
  title={Meal and habitual dietary networks identified through semiparametric Gaussian copula graphical models in a German adult population},
  author={Schwedhelm, Carolina and Kn{\"u}ppel, Sven and others},
  journal={PloS one},
  volume={13},
  number={8},
  year={2018}
}
```

## 🐛 Troubleshooting

### Issue: "Graphical Lasso failed to converge"
**Solution**: Reduce max_iter or adjust alpha range

### Issue: "No edges in network"
**Solution**: Lower min_correlation threshold (currently 0.1)

### Issue: "Memory error with large groups"
**Solution**: Process groups individually or reduce n_features

## 👥 Contributors

- Heejeong H. - Original analysis (ver1.0-3.0)
- ver4.0 GGM upgrade - 2025

## 📧 Contact

For questions about GGM methodology:
- Check Schwedhelm papers
- GitHub Issues: https://github.com/HeejeongH/Network/issues

---

**Last Updated**: 2025-11-06
**Status**: Ready for testing ✅
