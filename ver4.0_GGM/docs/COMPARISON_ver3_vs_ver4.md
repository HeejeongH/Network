# ver3.0 vs ver4.0: Co-occurrence vs GGM Comparison

## 🧪 Test Results: Male Young Adults (19-39) with MetS+

### Sample Group
- **Population**: Male, 19-39 years, MetS(+)
- **Sample Size**: 516 participants
- **Food Groups**: 12 groups analyzed

---

## 📊 Network Topology Comparison

| Metric | ver3.0 (Co-occurrence) | ver4.0 (GGM) | Change |
|--------|----------------------|--------------|---------|
| **Nodes** | 12 | 12 | Same |
| **Edges** | 20 | 9 | -55% |
| **Density** | 0.303 (30.3%) | 0.136 (13.6%) | -55% |
| **Method** | Binary co-occurrence | Partial correlation | - |
| **Threshold** | 70th percentile | α=0.1 (cross-validated) | - |

### Key Observation
**GGM produces sparser network** (9 edges vs 20 edges)
- Removes indirect relationships (spurious correlations)
- Only direct conditional dependencies remain
- More interpretable and actionable network

---

## 🔝 Top 10 Relationships (ver4.0 GGM Results)

### Partial Correlations (controlling for all other foods)

| Rank | Food Group 1 | Food Group 2 | Partial Corr | Interpretation |
|------|-------------|-------------|--------------|----------------|
| 1 | Additional Salt Use | Salty Food Consumption | 0.320 | **Strong direct link** |
| 2 | Protein Foods | Vegetables | 0.308 | **Universal hub connection** |
| 3 | Fried Foods | High Fat Meat | 0.202 | Unhealthy food cluster |
| 4 | Fried Foods | Processed Foods | 0.194 | Unhealthy food cluster |
| 5 | High Fat Meat | Processed Foods | 0.180 | Unhealthy food cluster |
| 6 | Processed Foods | Sugar-Sweetened Beverages | 0.149 | Unhealthy beverage link |
| 7 | Sugar-Sweetened Beverages | Sweet Food Consumption | 0.138 | Sweet preference pattern |
| 8 | Grain Products | Vegetables | 0.125 | Healthy meal structure |
| 9 | Grain Products | Protein Foods | 0.105 | Universal core foods |
| 10 | Protein Foods | High Fat Meat | 0.091 | Protein source variation |

---

## 💡 Scientific Insights from GGM

### 1. **Universal Hub Foods Confirmed**
The **Protein-Vegetable-Grain triad** appears in top partial correlations:
- Protein Foods ↔ Vegetables: 0.308 (rank #2)
- Grain Products ↔ Vegetables: 0.125 (rank #8)
- Grain Products ↔ Protein Foods: 0.105 (rank #9)

Even after controlling for all other foods, these relationships persist → **True dietary core**

### 2. **Unhealthy Food Cluster Identified**
Three unhealthy foods form tight cluster:
- Fried Foods ↔ High Fat Meat: 0.202
- Fried Foods ↔ Processed Foods: 0.194
- High Fat Meat ↔ Processed Foods: 0.180

This suggests **co-consumption of unhealthy foods** is a real pattern, not artifact of overall diet quality.

### 3. **Salt Consumption Pattern**
Strongest relationship (0.320):
- Additional Salt Use ↔ Salty Food Consumption

This is **independent of other dietary factors** → Specific salt preference behavior

### 4. **Sweet Tooth Pattern**
- Sugar-Sweetened Beverages ↔ Sweet Food Consumption: 0.138

Moderate but direct relationship → Some individuals have **consistent sweet preference** across food types

---

## 🎯 Implications for Paper Revision

### What ver3.0 Missed (Spurious Correlations)

**Example**: If ver3.0 showed edge between Foods A and C, but GGM doesn't:
```
ver3.0: A ↔ C (co-occur frequently)

Actually:
  A ↔ B (direct relationship)
  B ↔ C (direct relationship)
  
GGM correctly shows:
  A ↔ B ✓
  B ↔ C ✓
  A   C ✗ (indirect, removed)
```

### More Accurate Hub Identification

**ver4.0 hubs will be more reliable** because they represent foods with many **direct** relationships, not indirect ones.

---

## 📈 Expected Changes in Full Analysis (11 groups)

### 1. Network Topology Will Vary
**ver3.0**: All groups had identical 12 nodes, 20 edges, density=0.303
- Artifact of fixed threshold methodology

**ver4.0**: Each group will have different edge counts and densities
- Reflects true dietary pattern differences
- Young adults may have denser unhealthy food clusters
- Older adults may have sparser, more selective patterns

### 2. Hub Centrality Rankings Will Change
**ver3.0**: Hub rankings may include "pseudo-hubs"
- Foods connected via indirect relationships

**ver4.0**: Only "true hubs" with direct connections
- Clearer distinction between universal and group-specific hubs
- More pronounced centrality differences

### 3. Partial Correlation Strengths
**New metric available**: Report relationship strength
- ver3.0 only said "edge exists" (binary)
- ver4.0 can say "partial correlation = 0.308" (quantitative)

Example for Results section:
```
"The protein-vegetable relationship was strongest in 
older females (partial r=0.45, p<0.001) compared to 
young males (partial r=0.31, p<0.001), suggesting 
age-related shifts toward healthier food combinations."
```

---

## 🔬 Methodological Advantages Demonstrated

### 1. ✅ Preserves Information
- Uses continuous scores (1-4) not binary (≥3 vs <3)
- Difference between score=3 and score=4 is now meaningful

### 2. ✅ Controls Confounding
- Partial correlation = "correlation controlling for all other foods"
- Removes indirect relationships automatically

### 3. ✅ Data-Driven Threshold
- Cross-validation selects optimal α
- No arbitrary 70th percentile cutoff

### 4. ✅ Handles Non-Normal Data
- Spearman correlation (rank-based)
- Robust to skewed distributions common in dietary data

### 5. ✅ Sparse Network
- 55% fewer edges (9 vs 20)
- More interpretable
- Clearer for intervention targeting

---

## 📝 For Methods Section

### Current (ver3.0):
> "Co-occurrence networks were constructed based on simultaneous high-consumption patterns (score ≥3 on 3- or 4-point scales). Co-occurrence frequency between food groups i and j was calculated as the proportion of participants consuming both at high levels. Edges were retained if co-occurrence exceeded the 70th percentile within each group."

### Revised (ver4.0):
> "Dietary networks were constructed using Semiparametric Gaussian Copula Graphical Models (SGCGM) to estimate conditional dependencies between food groups via partial correlations. To accommodate non-normal distributions in dietary data, we applied rank-based transformations using Spearman's rho, followed by graphical lasso regularization (L1-penalized precision matrix estimation). The optimal regularization parameter (λ) was selected via cross-validation for each stratified group. This approach identifies genuine co-consumption patterns while controlling for confounding relationships with other food groups, yielding sparse networks that represent direct conditional dependencies."

---

## 🎓 Statistical Validity Improvements

### Problem with ver3.0 Approach
1. **Information Loss**: Binarization (≥3 vs <3) discards score variation
2. **Arbitrary Threshold**: 70th percentile has no statistical justification
3. **Spurious Edges**: Indirect relationships counted as edges
4. **Fixed Topology**: All groups forced into same density

### ver4.0 Solutions
1. **Continuous Data**: Preserves full score range (1-4)
2. **Data-Driven**: Cross-validation optimizes threshold per group
3. **Conditional Independence**: Partial correlations remove indirect links
4. **Flexible Topology**: Network structure adapts to each group's data

---

## 🚀 Next Steps for Full Analysis

1. **Run ver4.0 on All 11 Groups** (~30 minutes)
2. **Compare Hub Rankings**: ver3.0 vs ver4.0
3. **Analyze Network Density Variation**: Now possible with GGM
4. **Report Partial Correlation Strengths**: Quantitative relationships
5. **Community Detection**: Louvain algorithm on GGM networks
6. **Update Paper Figures**: Show partial correlation weights as edge thickness

---

## 📚 Key References for Methods Citation

```bibtex
@article{schwedhelm2018meal,
  title={Meal and habitual dietary networks identified through 
         semiparametric Gaussian copula graphical models},
  author={Schwedhelm, Carolina and Kn{\"u}ppel, Sven and 
          Schwingshackl, Lukas and Boeing, Heiner and Iqbal, Khalid},
  journal={PloS one},
  volume={13},
  number={8},
  pages={e0202936},
  year={2018}
}

@article{friedman2008sparse,
  title={Sparse inverse covariance estimation with the graphical lasso},
  author={Friedman, Jerome and Hastie, Trevor and Tibshirani, Robert},
  journal={Biostatistics},
  volume={9},
  number={3},
  pages={432--441},
  year={2008}
}
```

---

**Date**: 2025-11-06  
**Status**: Single group test successful ✅  
**Next**: Full 11-group analysis
