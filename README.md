# Dietary Network Analysis Project

## 🎯 Project Versions

This repository contains multiple versions of dietary network analysis projects, organized chronologically.

---

## 📦 Version Overview

### ✅ **ver3.0_2511** (November 2025) - **CURRENT VERSION**

**Project**: Paper 2 - Dietary Co-occurrence Network Analysis  
**Status**: ✅ Complete, ready for submission  
**Key Finding**: Protein Foods, Vegetables, and Grain Products are **universal hubs** across all demographic groups

📁 **Path**: `ver3.0_2511/`

**Contains**:
- ✅ Complete manuscript
- ✅ 11 stratified network files
- ✅ Main figures and tables
- ✅ Supplementary materials
- ✅ Analysis scripts

👉 **[See ver3.0_2511/README.md for full documentation](ver3.0_2511/README.md)**

---

### 📚 **ver2.0_2510** (October 2025) - ARCHIVED

**Project**: Alternative Analysis (Dietary Quality Scores)  
**Status**: 📦 Archived for reference  
**Key Finding**: Unhealthy food avoidance patterns cluster together

**Contains**:
- Alternative analysis using transformed scores (1-3-5 scale)
- Avoidance pattern networks
- Comparison with original analysis

**Note**: Different research question than Paper 2. Could be separate future publication.

---

### 📚 **ver1.0_2509** (September 2025) - ARCHIVED

**Project**: Integrated Diet-Health Network Analysis  
**Status**: 📦 Archived for reference  
**Contents**: Initial exploration combining dietary patterns with health indicators

---

## 🚀 Quick Start

### For Paper 2 Work (Current):

```bash
cd ver3.0_2511/

# Run main analysis
python3 src/create_stratified_networks.py

# Generate figures and tables
python3 src/generate_main_figures_tables.py
python3 src/generate_supplementary_materials.py

# Read manuscript
cat result/manuscript/Paper2_Main_Manuscript.md
```

---

## 📊 Main Research Questions by Version

| Version | Research Question | Answer |
|---------|------------------|---------|
| **ver3.0_2511** ✅ | What foods co-occur in Korean diets? | Protein-Vegetables-Grains form universal triad |
| ver2.0_2510 📚 | What avoidance patterns cluster? | Unhealthy food avoidances correlate |
| ver1.0_2509 📚 | How do diet-health patterns interact? | Exploratory integrated analysis |

---

## 🎓 Current Paper Status

### Paper 2: Dietary Co-occurrence Networks (ver3.0_2511)

**Title**: "Dietary Co-occurrence Network Analysis Identifies Universal Hub Foods Across Demographic Groups in Korean Adults"

**Status**: 
- ✅ Manuscript complete
- ✅ Figures generated
- ✅ Tables prepared
- ✅ Supplementary materials ready
- ⏳ Ready for journal submission

**Target Journals**: 
- Nutrients
- Public Health Nutrition
- Journal of Nutrition

**Key Strengths**:
- Large sample (N=23,040)
- Novel network approach to dietary patterns
- Stratified analysis (11 demographic groups)
- Universal findings (protein-vegetable-grain triad)
- Clear clinical implications

---

## 📂 Repository Structure

```
Network/
├── README.md                    # This file
│
├── ver3.0_2511/                # ⭐ CURRENT VERSION
│   ├── README.md               # Detailed documentation
│   ├── db/                     # Data files
│   ├── result/                 # Manuscript, figures, tables
│   └── src/                    # Analysis scripts
│
├── ver2.0_2510/                # Alternative analysis (archived)
│   ├── db/
│   ├── networks/
│   └── src/
│
└── ver1.0_2509/                # Initial exploration (archived)
    ├── src/
    ├── result/
    └── paper/
```

---

## 🔬 Methodology Highlights

### Network Construction (ver3.0_2511)
- **Type**: Co-occurrence network (binary)
- **Threshold**: Score ≥3 (adequate/frequent consumption)
- **Food Groups**: 12 (6 healthy + 6 unhealthy)
- **Stratification**: Sex (2) × Age (3) × MetS (2) = 11 groups
  - Note: Young women with MetS(+) excluded due to small sample

### Why Binary Instead of Continuous?
1. Co-occurrence requires clear "yes/no" definition
2. Harmonizes different scales (3-point vs 4-point)
3. Clinical threshold (≥3) has meaningful interpretation
4. More robust to measurement error

---

## 📈 Key Findings (ver3.0_2511)

### Universal Hub Foods (All 11 Groups)
1. 🍖 **Protein Foods** - Central to dietary patterns
2. 🥦 **Vegetables** - Universal connector
3. 🍚 **Grain Products** - Foundational food

### Variable Hub Foods (Demographic-Specific)
- **Sweet foods**: More prominent in women
- **Dairy products**: Varies by age and MetS status
- **Processed foods**: Varies by demographic group

### Clinical Implications
✅ **Dietary interventions should focus on the protein-vegetable-grain triad**
- Universal applicability across all demographic groups
- Positive framing ("eat more of these")
- Clear, actionable guidance for healthcare providers
- Aligns with existing dietary guidelines

---

## 🛠️ Technical Requirements

### Python Environment
```bash
# Required packages
pandas>=1.5.0
numpy>=1.23.0
networkx>=2.8.0
matplotlib>=3.5.0
seaborn>=0.12.0
```

### Data Files
- Main dataset: `ver3.0_2511/db/processed_data/total_only_org.csv` (5.4 MB)
- Network outputs: `ver3.0_2511/result/network_files/*.gexf`

---

## 📝 Citation

If using this work, please cite:

**[Manuscript in preparation]**  
"Dietary Co-occurrence Network Analysis Identifies Universal Hub Foods Across Demographic Groups in Korean Adults"

---

## 📧 Contact & Contributions

For questions or collaborations:
- Check version-specific README files
- Review manuscript in `ver3.0_2511/result/manuscript/`
- Examine analysis code in `ver3.0_2511/src/`

---

## 🔄 Git Workflow

### Cloning the Repository
```bash
git clone https://github.com/HeejeongH/Network.git
cd Network
```

### Updating to Latest Version
```bash
git pull origin main
```

### Working with ver3.0_2511
```bash
cd ver3.0_2511/
# All current work happens here
```

---

## 📚 Documentation

- **Main README**: This file (repository overview)
- **Version README**: `ver3.0_2511/README.md` (detailed current project)
- **Manuscript**: `ver3.0_2511/result/manuscript/Paper2_Main_Manuscript.md`
- **Methods**: `ver3.0_2511/result/manuscript/Supplementary_Methods.md`

---

**Repository Created**: September 2025  
**Last Updated**: November 2, 2025  
**Current Status**: Paper 2 complete, ready for submission ✅
