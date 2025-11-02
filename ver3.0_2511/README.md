# Paper 2: Dietary Co-occurrence Network Analysis (ver 3.0 - November 2025)

## 📌 Project Overview

This is the **latest version (ver3.0_2511)** of the dietary co-occurrence network analysis project examining food consumption patterns across demographic groups in Korean adults.

**Key Finding**: Protein Foods, Vegetables, and Grain Products emerge as **universal hub foods** across all 11 stratified demographic groups.

---

## 📂 Project Structure

```
ver3.0_2511/
├── db/                          # Data files
│   ├── processed_data/
│   │   ├── total_only_org.csv   # Main dataset (original scoring) ⭐
│   │   ├── stratified_network_statistics.csv
│   │   └── old_analysis/        # Previous analysis files (archived)
│   └── raw/                     # Raw data files
│
├── result/                      # Analysis outputs
│   ├── manuscript/
│   │   ├── Paper2_Main_Manuscript.md          # Main manuscript ⭐
│   │   ├── References.md
│   │   ├── Supplementary_Materials_Complete.md
│   │   └── Supplementary_Methods.md
│   ├── network_files/           # 11 GEXF network files
│   ├── figures/                 # Main and supplementary figures
│   └── tables/                  # Statistical tables
│
└── src/                         # Analysis scripts
    ├── create_stratified_networks.py          # Main analysis ⭐
    ├── generate_main_figures_tables.py
    └── generate_supplementary_materials.py
```

---

## 🎯 Key Analysis Details

### Dataset
- **File**: `total_only_org.csv` (5.4 MB, 23,040 subjects)
- **Scoring**: Original 3-point or 4-point scales
- **Interpretation**: Higher score = more/frequent consumption

### Methodology
- **Network Type**: Co-occurrence network (binary)
- **Threshold**: Score ≥3 (frequent/adequate consumption)
- **Stratification**: 11 groups (Sex × Age × MetS status)
- **Food Groups**: 12 total (6 healthy + 6 unhealthy)

### Key Results
**Universal Hub Foods** (appear as hubs in all 11 groups):
1. 🍖 **Protein Foods**
2. 🥦 **Vegetables**
3. 🍚 **Grain Products**

**Clinical Implication**: Build dietary interventions around the protein-vegetable-grain triad for maximum population impact.

---

## 🔬 Analysis Scripts

### 1. `create_stratified_networks.py`
**Purpose**: Generate 11 stratified co-occurrence networks

**Usage**:
```bash
cd /home/user/webapp/ver3.0_2511
python3 src/create_stratified_networks.py
```

**Output**:
- 11 GEXF files in `result/network_files/`
- `stratified_network_statistics.csv` summary

**Key Parameters**:
- Binary threshold: `score >= 3`
- Network type: Undirected, weighted
- Centrality metrics: Degree, Betweenness, Closeness

---

### 2. `generate_main_figures_tables.py`
**Purpose**: Create main manuscript figures and tables

**Generates**:
- Figure 1: Representative networks
- Figure 2: Hub centrality comparison
- Table 1: Sample characteristics
- Table 2: Network metrics

---

### 3. `generate_supplementary_materials.py`
**Purpose**: Generate supplementary figures and tables

**Generates**:
- Figure S1: All network visualizations
- Figure S2: Hub transition analysis
- Figure S3: Centrality heatmaps
- Tables S1-S4: Detailed statistics

---

## 📊 Data Files

### Main Dataset: `total_only_org.csv`
- **Size**: 5.4 MB
- **Rows**: 23,040 subjects
- **Columns**: Demographics + 12 food group scores

**Food Groups**:

**Healthy Foods** (6):
1. Grain Products (3-point)
2. Protein Foods (4-point)
3. Vegetables (4-point)
4. Fruits (3-point)
5. Dairy Products (4-point)
6. Sweet Food Consumption (3-point)

**Unhealthy Foods** (6):
1. Fried Foods (4-point)
2. High Fat Meat (4-point)
3. Processed Foods (4-point)
4. Sugar-Sweetened Beverages (4-point)
5. Additional Salt Use (3-point)
6. Salty Food Consumption (3-point)

---

## 🎓 Manuscript Status

### Main Manuscript
- **File**: `result/manuscript/Paper2_Main_Manuscript.md`
- **Length**: ~50 KB
- **Sections**: Abstract, Introduction, Methods, Results, Discussion, Conclusions
- **Status**: Complete ✅

### Key Sections:
1. **Abstract**: Concise summary of findings
2. **Methods**: 
   - Study design and population
   - Dietary assessment (3- and 4-point scales)
   - Network construction (binary threshold ≥3)
   - Statistical analysis
3. **Results**:
   - Universal hub identification
   - Demographic variations
   - Network topology metrics
4. **Discussion**: Clinical implications and limitations

---

## 🔄 Version History

### ver3.0_2511 (November 2025) - **CURRENT** ✅
- Finalized manuscript with corrected scoring system
- Complete supplementary materials
- All figures and tables generated
- Network files organized
- Main finding: Protein-Vegetables-Grains universal hub triad

### ver2.0_2510 (October 2025)
- Alternative analysis using transformed scores
- Explored avoidance pattern clustering
- **Status**: Archived for reference

### ver1.0_2509 (September 2025)
- Initial integrated diet-health analysis
- MetS stratification exploration
- **Status**: Archived for reference

---

## 💡 Important Notes

### Why Binary Classification?

**Binary threshold (≥3) is used instead of continuous scores because:**

1. **Co-occurrence definition**: Networks require clear "yes/no" relationships
2. **Scale harmonization**: Unifies 3-point and 4-point scales
3. **Clinical interpretation**: Score ≥3 has meaningful threshold (adequate intake)
4. **Statistical robustness**: Less sensitive to measurement error

For detailed justification, see previous documentation in ver2.0_2510 alternative analysis.

---

### Why total_only_org.csv?

**This dataset uses original scoring where higher = more/frequent consumption:**

- ✅ Captures what foods are **actually consumed together**
- ✅ Identifies positive dietary patterns (actionable for interventions)
- ✅ Aligns with co-occurrence network methodology
- ✅ Provides clear clinical guidance

**Alternative**: `total_only.csv` (transformed 1-3-5 scale) captures avoidance patterns instead - archived in ver2.0_2510 for future research.

---

## 📝 Next Steps

Potential future work:
1. Submit manuscript to target journal
2. Create presentation slides for conferences
3. Explore ver2.0_2510 alternative analysis as separate paper
4. Validate findings in other populations
5. Develop intervention materials based on hub foods

---

## 👥 Contact

For questions about this analysis, refer to:
- Main manuscript: `result/manuscript/Paper2_Main_Manuscript.md`
- Analysis code: `src/create_stratified_networks.py`
- Data dictionary: Check supplementary methods

---

**Last Updated**: November 2, 2025  
**Status**: Analysis complete, manuscript ready for submission ✅
