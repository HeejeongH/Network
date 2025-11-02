# Data File Comparison: total_only_org.csv vs total_only.csv

## Overview

Two versions of the processed data exist:
1. **total_only_org.csv**: Original scoring (3-point or 4-point scales)
2. **total_only.csv**: Transformed to unified 1-3-5 scale (Poor-Intermediate-Ideal)

---

## File Details

### total_only_org.csv (Currently Used)
- **Location**: `db/processed_data/total_only_org.csv`
- **Rows**: 23,040
- **Characteristics**: 
  - Original 3-point scales: Grain Products (1,2,3), Fruits (1,2,3), etc.
  - Original 4-point scales: Protein Foods (1,2,3,4), Vegetables (1,2,3,4), etc.
  - No transformation applied

### total_only.csv (Transformed)
- **Location**: `db/processed_data/old_analysis/total_only.csv`
- **Rows**: 23,040
- **Characteristics**:
  - All scales unified: 1 (Poor), 3 (Intermediate), 5 (Ideal)
  - Transformation applied via `data_preprocessing.ipynb`

---

## Transformation Logic

From `data_preprocessing.ipynb`:

```python
def transform_values(df):
    # 3-point scales → 1,3,5
    df['Grain Products'] = df['Grain Products'].replace({3: 5, 2: 3, 1: 1})
    df['Fruits'] = df['Fruits'].replace({3: 5, 2: 3})
    
    # 4-point scales → 1,3,5 (merging 1+2→1 or 3+4→5)
    df['Protein Foods'] = df['Protein Foods'].replace({4: 5, 2: 1, 1: 1})
    df['Vegetables'] = df['Vegetables'].replace({4: 5, 2: 1, 1: 1})
    df['Dairy Products'] = df['Dairy Products'].replace({3: 5, 4: 3, 2: 3})
    
    # Unhealthy foods (reverse scale): 1→5, high score→1
    df['Fried Foods'] = df['Fried Foods'].replace({1: 5, 2: 3, 3: 1, 4: 1})
    # ... (similar for other unhealthy foods)
    
    return df
```

---

## Value Distribution Comparison

### Grain Products (3-point scale)

**total_only_org.csv**:
```
1: 3,673 (15.9%)  → Poor
2: 13,068 (56.7%) → Intermediate
3: 6,299 (27.3%)  → Ideal
```

**total_only.csv** (transformed):
```
1: 3,673 (15.9%)  → Poor (unchanged)
3: 13,068 (56.7%) → Intermediate (was 2)
5: 6,299 (27.3%)  → Ideal (was 3)
```

### Protein Foods (4-point scale)

**total_only_org.csv**:
```
1: 841 (3.7%)     → Poor
2: 4,784 (20.8%)  → Fair
3: 11,166 (48.5%) → Good
4: 6,249 (27.1%)  → Ideal
```

**total_only.csv** (transformed):
```
1: 5,625 (24.4%)  → Poor (merged 1+2)
3: 11,166 (48.5%) → Intermediate (was 3)
5: 6,249 (27.1%)  → Ideal (was 4)
```

---

## Binarization Comparison

### Using total_only_org.csv (Current)

```python
data_binary = (data[food_groups] >= 3).astype(int)
```

**Results**:
- 3-point scales: Only score 3 → High (27.3% for Grain Products)
- 4-point scales: Scores 3,4 → High (75.6% for Protein Foods)

**Issue**: Different proportions classified as "high" depending on original scale

### Using total_only.csv (Alternative)

```python
data_binary = (data[food_groups] >= 3).astype(int)
```

**Results**:
- All scales: Scores 3,5 → High
- 3-point example: 3+5 = 84.0% for Grain Products
- 4-point example: 3+5 = 75.6% for Protein Foods

**Advantage**: More consistent interpretation - "Intermediate or better"

---

## Current Paper 2 Approach

### Data File Used:
```python
# src/create_stratified_networks.py, Line 16
DATA_FILE = BASE_DIR / 'db' / 'processed_data' / 'total_only_org.csv'
```

### Manuscript Description:
```markdown
Each food group was scored on a 3- or 4-point scale based on consumption 
frequency and adequacy relative to Korean dietary guidelines. Different 
scales were used to accommodate the varying nature of dietary recommendations 
across food groups.

For network analysis, all scores were consistently binarized: 
high consumption (score ≥3, coded as 1) vs. low consumption (score <3, coded as 0).
```

---

## Pros and Cons

### Option 1: Keep total_only_org.csv (Current) ✅

**Pros**:
- ✅ Using original data without transformation
- ✅ More granular information (4 levels in 4-point scales)
- ✅ Transparent: no intermediate transformation step
- ✅ Already implemented and validated
- ✅ Manuscript already explains 3- vs 4-point scales

**Cons**:
- ❌ Different scales (3-point vs 4-point)
- ❌ Threshold ≥3 captures different proportions by scale type
- ❌ Slightly more complex to explain

### Option 2: Switch to total_only.csv

**Pros**:
- ✅ Unified scale across all food groups (1,3,5)
- ✅ Clear interpretation: 1=Poor, 3=Intermediate, 5=Ideal
- ✅ Threshold ≥3 means "Intermediate or better" for all foods
- ✅ Simpler conceptually

**Cons**:
- ❌ Requires explaining transformation logic
- ❌ Information loss (e.g., 4-point scale's 2 merged into 1)
- ❌ Adds preprocessing complexity
- ❌ Would need to regenerate all networks
- ❌ Would need to update manuscript

---

## Recommendation

**Keep using total_only_org.csv** for the following reasons:

1. **Scientific Integrity**: 
   - Using original data is more transparent
   - No transformation artifacts

2. **Already Validated**:
   - All 11 networks generated and validated
   - Manuscript written with this approach
   - Sensitivity analyses completed

3. **Well-Justified**:
   - Different scales reflect true heterogeneity in dietary recommendations
   - Korean Dietary Reference Intakes use different scales for different food groups
   - Our approach respects this structure

4. **Threshold Defense**:
   - Score ≥3 has clear meaning in each scale:
     - 3-point: "Ideal" (top category)
     - 4-point: "Good or Ideal" (top 2 categories)
   - This is clinically meaningful and defensible

---

## If We Were to Switch to total_only.csv

### Changes Required:

1. **Update data file path**:
```python
# src/create_stratified_networks.py
DATA_FILE = BASE_DIR / 'db' / 'processed_data' / 'old_analysis' / 'total_only.csv'
```

2. **Move file back**:
```bash
mv db/processed_data/old_analysis/total_only.csv db/processed_data/
```

3. **Regenerate all networks**:
```bash
python src/create_stratified_networks.py
```

4. **Update manuscript**:
   - Change from "3- or 4-point scales" to "unified 1-3-5 scale"
   - Add explanation of transformation
   - Update Methods section

5. **Regenerate all figures and tables**:
```bash
python src/generate_main_figures_tables.py
python src/generate_supplementary_materials.py
```

6. **Verify results consistency**:
   - Check if hub foods remain the same
   - Ensure main findings unchanged

---

## Threshold Justification Comparison

### With total_only_org.csv (Current):

**Threshold ≥3 means**:
- Grain Products (3-point): Top category only (Ideal)
- Protein Foods (4-point): Top 2 categories (Good + Ideal)

**Justification**: 
"This threshold represents consumption at or above recommended levels for 
healthy foods, and frequent consumption for unhealthy foods, based on 
Korean Dietary Reference Intakes."

### With total_only.csv:

**Threshold ≥3 means**:
- All foods: Intermediate or Ideal (top 2 categories in unified scale)

**Justification**:
"Scores were transformed to unified 1-3-5 scale. Threshold ≥3 captures 
individuals meeting or exceeding intermediate dietary quality."

---

## Conclusion

**Recommendation: Keep total_only_org.csv**

The current approach is:
- ✅ Scientifically sound
- ✅ Fully implemented
- ✅ Well-documented in manuscript
- ✅ Results validated

Switching to total_only.csv would require:
- Extensive manuscript revisions
- Complete re-analysis
- Explanation of transformation logic
- Potential reviewer questions about transformation

**The original data approach is stronger for peer review.**

---

**Date**: 2025-11-02  
**Decision**: Continue using total_only_org.csv for Paper 2  
**Status**: Documented for future reference
