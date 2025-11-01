# Paper 2: Stratified Dietary Network Analysis

## Sex-, Age-, and Metabolic Syndrome-Stratified Analysis of Dietary Patterns

**Status**: ✅ Supplementary Materials Complete  
**Date**: November 1, 2025  
**Sample Size**: N = 22,964 (11 stratified groups)

---

## 📋 Project Overview

This project contains all supplementary materials for Paper 2, which analyzes dietary network patterns across different demographic and clinical subgroups using co-occurrence network analysis.

### Research Question
How do dietary network patterns differ across sex, age groups, and metabolic syndrome status?

### Stratification
- **Sex**: Male (M), Female (F)
- **Age Groups**: Young adults (19-39), Middle-aged (40-59), Older adults (60-74)
- **MetS Status**: MetS(+), MetS(-)
- **Total Groups**: 11 (excluding Female young adults with MetS(+) due to n < 100)

---

## 📁 Directory Structure

```
paper2_stratified_networks/
│
├── README.md                                    # This file
├── Supplementary_Methods.md                     # Detailed methodology
├── Supplementary_Materials_Complete.md          # Complete supplementary materials
│
├── figures/                                     # All supplementary figures
│   ├── Figure_S1_Network_Visualizations.png    # 11 network visualizations
│   ├── Figure_S2_Hub_Transitions.png           # Hub transitions across ages
│   └── Figure_S3_Centrality_Heatmaps.png       # Centrality heatmaps
│
├── tables/                                      # All supplementary tables
│   ├── Table_S1_Sample_Characteristics.*       # Sample sizes and proportions
│   ├── Table_S2_Network_Metrics.*              # Network structural metrics
│   ├── Table_S3_Edge_Lists.*                   # Complete edge lists
│   └── Table_S4_Centrality_Rankings.*          # Top 5 centrality rankings
│
├── scripts/                                     # Analysis scripts
│   ├── create_stratified_networks.py           # Generate 11 networks
│   └── generate_supplementary_materials.py     # Generate figures & tables
│
└── data/                                        # Network data files
    └── [See ../db/processed_data/network_*.gexf]
```

---

## 📊 Generated Materials

### ✅ Figures (3)
1. **Figure S1**: Network Visualizations
   - 11 force-directed layout networks
   - Color-coded by degree centrality
   - Node size proportional to degree

2. **Figure S2**: Hub Transition Flowcharts
   - Age progression for each sex-MetS combination
   - Top 3 hub foods per age group
   - Network metrics displayed

3. **Figure S3**: Centrality Heatmaps
   - Degree, Betweenness, Closeness centrality
   - All 12 food groups × 11 groups
   - Color intensity indicates centrality values

### ✅ Tables (4 + summaries)
1. **Table S1**: Sample Characteristics
   - 11 groups + total
   - Sample sizes and proportions
   - Demographic breakdown

2. **Table S2**: Network Metrics
   - Nodes, edges, density
   - Clustering coefficient
   - Diameter and path length

3. **Table S3**: Edge Lists
   - Complete listing: 220 edges (20 per network)
   - Node pairs and co-occurrence weights
   - Summary statistics

4. **Table S4**: Centrality Rankings
   - Top 5 foods per centrality type
   - All 11 groups
   - Degree, betweenness, closeness

### ✅ Documentation (2)
1. **Supplementary Methods**: Detailed methodology
2. **Supplementary Materials Complete**: Integrated document with all materials

---

## 🔑 Key Findings

### Network Structure
- **Consistent topology**: All 11 networks have 12 nodes, 20 edges, density = 0.303
- **Different configurations**: Despite identical structure, centrality patterns vary
- **Fully connected**: All networks have diameter = 3

### Universal Hubs (Present in all/most groups)
1. **Protein Foods**: Most stable hub (100% of groups)
2. **Vegetables**: Second most stable (100% of groups)
3. **Grain Products**: Consistently central (100% of groups)

### Variable Hubs (Group-specific)
1. **Sugar-Sweetened Beverages**: High in young, low in older adults
2. **Sweet Food Consumption**: Higher in females, especially young
3. **Fried Foods**: Variable, higher in some male MetS(+) groups

### Age-Related Patterns
- **Young Adults**: More sugar-sweetened beverages and sweet foods
- **Middle-Aged**: Balanced, diverse dietary patterns
- **Older Adults**: More grain products, traditional dietary patterns

### Sex Differences
- **Males**: Higher centrality for processed/fried foods in MetS(+)
- **Females**: Higher centrality for vegetables and sweet foods

### MetS Patterns
- **MetS(+)**: Lower overall centrality, more unhealthy food co-occurrences
- **MetS(-)**: Higher centrality for vegetables/fruits, balanced patterns

---

## 🔬 Methodology Summary

### Network Type
**Co-occurrence Network Analysis**

### Network Construction
1. **Binarization**: Food scores ≥3 = high consumption (1), <3 = low (0)
2. **Co-occurrence matrix**: Proportion of simultaneous high consumption
3. **Threshold**: 70th percentile of non-zero co-occurrence values
4. **Edge creation**: Connect food pairs above threshold

### Network Metrics
- **Degree centrality**: Number of direct connections
- **Betweenness centrality**: Bridge role in network
- **Closeness centrality**: Average distance to all other nodes
- **Network density**: Proportion of possible edges present
- **Clustering coefficient**: Tendency to form triangles

### Visualization
- **Layout**: Force-directed (Fruchterman-Reingold)
- **Node size**: Proportional to degree centrality
- **Node color**: Yellow-orange-red scale (centrality)
- **Edge width**: Proportional to co-occurrence strength

---

## 🚀 How to Reproduce

### Prerequisites
```bash
pip install pandas numpy networkx matplotlib seaborn scipy
```

### Step 1: Create Networks
```bash
cd /home/user/webapp
python3 paper2_stratified_networks/scripts/create_stratified_networks.py
```

**Output**: 11 GEXF network files in `db/processed_data/`

### Step 2: Generate Supplementary Materials
```bash
python3 paper2_stratified_networks/scripts/generate_supplementary_materials.py
```

**Output**: 
- 3 figures in `figures/`
- 4 tables in `tables/` (CSV and TXT formats)

### Step 3: Review Documents
- Read `Supplementary_Methods.md` for detailed methodology
- Read `Supplementary_Materials_Complete.md` for integrated materials

---

## 📈 Sample Sizes by Group

| Group | N | % | Notes |
|-------|---|---|-------|
| 남성_청년층_MetS(+) | 516 | 2.25% | Smallest group |
| 남성_청년층_MetS(-) | 1,963 | 8.55% | |
| 남성_중년층_MetS(+) | 2,938 | 12.79% | |
| 남성_중년층_MetS(-) | 4,737 | 20.63% | |
| 남성_장년층_MetS(+) | 971 | 4.23% | |
| 남성_장년층_MetS(-) | 1,169 | 5.09% | |
| 여성_청년층_MetS(-) | 2,519 | 10.97% | No MetS(+) (n<100) |
| 여성_중년층_MetS(+) | 758 | 3.30% | |
| 여성_중년층_MetS(-) | 5,629 | 24.51% | **Largest group** |
| 여성_장년층_MetS(+) | 680 | 2.96% | |
| 여성_장년층_MetS(-) | 1,084 | 4.72% | |
| **TOTAL** | **22,964** | **100%** | |

---

## 🎯 Clinical Implications

### Universal Recommendations
1. **Promote core triads**: Protein-Vegetables-Grains (stable hubs)
2. **Increase fruits**: Co-consumption with vegetables
3. **Reduce sugary beverages**: Especially in young adults

### Targeted Interventions

**Young Adults**:
- ⚠️ High sugar-sweetened beverages and sweet foods
- ✅ Leverage protein foods consumption
- 🎯 Replace sugary drinks with healthier alternatives

**MetS(+) Groups**:
- ⚠️ Unhealthy food co-occurrences
- ✅ Address fried and high-fat meat consumption
- 🎯 Increase vegetables and fruits

**Females**:
- ✅ Natural vegetable preference
- 🎯 Maintain and enhance vegetable consumption
- ⚠️ Monitor sweet food intake in young adults

**Males**:
- ⚠️ Higher processed and fried foods
- 🎯 Reduce unhealthy food combinations
- ✅ Leverage grain products as intervention point

**Older Adults**:
- ✅ Stable traditional dietary patterns
- 🎯 Reinforce healthy patterns
- ⚠️ Ensure adequate fruit intake

---

## 📚 References

### Data Source
Korea National Health and Nutrition Examination Survey (KNHANES)
- Website: https://knhanes.kdca.go.kr
- Public dataset, de-identified

### Network Analysis Methods
- Newman, M.E.J. (2018). Networks: An Introduction. Oxford University Press.
- Barabási, A.L. (2016). Network Science. Cambridge University Press.

### Software
- Python 3.12: https://www.python.org
- NetworkX: https://networkx.org
- Matplotlib: https://matplotlib.org
- Seaborn: https://seaborn.pydata.org

---

## 📝 Citation

[To be added after publication]

```bibtex
@article{paper2_stratified_networks_2025,
  title={Dietary Network Patterns Differ Across Sex, Age, and Metabolic Syndrome Status: A Stratified Co-occurrence Network Analysis},
  author={[Authors]},
  journal={[Journal]},
  year={2025},
  volume={[Volume]},
  pages={[Pages]},
  doi={[DOI]}
}
```

---

## 👥 Authors

[To be filled]

---

## 📧 Contact

For questions about data, methods, or code:
- **Email**: [To be added]
- **GitHub**: [To be added]

---

## 📄 License

[To be determined]

---

## 🔄 Version History

- **v1.0** (2025-11-01): Initial complete version
  - 11 networks created
  - 3 figures generated
  - 4 tables created
  - Supplementary methods documented
  - Complete supplementary materials compiled

---

## ✅ Checklist

- [x] Create 11 stratified networks
- [x] Generate Figure S1 (Network visualizations)
- [x] Generate Figure S2 (Hub transitions)
- [x] Generate Figure S3 (Centrality heatmaps)
- [x] Create Table S1 (Sample characteristics)
- [x] Create Table S2 (Network metrics)
- [x] Create Table S3 (Edge lists)
- [x] Create Table S4 (Centrality rankings)
- [x] Write Supplementary Methods
- [x] Compile Complete Supplementary Materials
- [x] Create README documentation
- [ ] Final review and proofreading
- [ ] Submit for peer review

---

**Last Updated**: November 1, 2025  
**Document Version**: 1.0  
**Status**: ✅ Ready for Review
