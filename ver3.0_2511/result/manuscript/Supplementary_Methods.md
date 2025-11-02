# Supplementary Methods

## Study Design and Population

### Data Source
Data were obtained from the Korea National Health and Nutrition Examination Survey (KNHANES), a nationally representative cross-sectional survey conducted by the Korea Centers for Disease Control and Prevention. The analysis included 23,040 participants aged 19-74 years with complete dietary and metabolic data.

### Stratification Criteria
Participants were stratified into 12 groups based on three demographic and clinical factors:

1. **Sex**: Male (M), Female (F)
2. **Age Group**: 
   - Young adults (19-39 years)
   - Middle-aged (40-59 years)
   - Older adults (60-74 years)
3. **Metabolic Syndrome Status**: MetS(+), MetS(-)

**Note**: The female young adult MetS(+) group (n < 100) was excluded from analysis due to insufficient sample size, resulting in 11 groups for network analysis.

### Metabolic Syndrome Definition
Metabolic syndrome (MetS) was defined according to the modified National Cholesterol Education Program Adult Treatment Panel III (NCEP ATP III) criteria with Asian-specific waist circumference cutoffs:

- **Abdominal obesity**: Waist circumference ≥90 cm (men) or ≥85 cm (women)
- **Elevated triglycerides**: ≥150 mg/dL or medication use
- **Reduced HDL-cholesterol**: <40 mg/dL (men) or <50 mg/dL (women)
- **Elevated blood pressure**: ≥130/85 mmHg or antihypertensive medication use
- **Elevated fasting glucose**: ≥100 mg/dL or antidiabetic medication use

Participants meeting ≥3 criteria were classified as MetS(+).

---

## Dietary Assessment

### Food Group Classification
Dietary intake was assessed using a semi-quantitative food frequency questionnaire (FFQ). Foods were aggregated into 12 mutually exclusive food groups:

1. **Grain Products**: Rice, bread, noodles, cereals
2. **Protein Foods**: Meat, fish, eggs, legumes
3. **Vegetables**: All vegetables except kimchi
4. **Dairy Products**: Milk, yogurt, cheese
5. **Fruits**: Fresh and dried fruits
6. **Fried Foods**: Deep-fried and pan-fried foods
7. **High Fat Meat**: Fatty cuts of meat, processed meats
8. **Processed Foods**: Instant noodles, canned foods, frozen meals
9. **Sugar-Sweetened Beverages**: Soft drinks, sweetened coffee/tea
10. **Additional Salt Use**: Table salt, soy sauce added to meals
11. **Salty Food Consumption**: Kimchi, pickled foods, salted seafood
12. **Sweet Food Consumption**: Desserts, candy, sweetened snacks

### Dietary Quality Scoring

Each food group was scored on a 3- or 4-point scale based on food group-specific dietary recommendations:

**Rationale for Variable Scales**: Different food groups have different recommendation structures in Korean dietary guidelines. Some foods (e.g., grains, fruits) have clear categorical recommendations (daily, sometimes, rarely), while others (e.g., proteins, vegetables) require more granular assessment due to wider acceptable intake ranges.

**Scoring Systems**:

*Healthy foods (higher score = better)*:
- **3-point scale** (5 groups: Grain Products, Fruits, Sweet Food Consumption):
  - 1 = Poor (inadequate/rarely consumed)
  - 2 = Intermediate (moderate consumption)
  - 3 = Ideal (recommended level)

- **4-point scale** (3 groups: Protein Foods, Vegetables, Dairy Products):
  - 1 = Poor (rarely consumed)
  - 2 = Fair (occasionally consumed)
  - 3 = Good (regularly consumed)
  - 4 = Ideal (frequently consumed)

*Unhealthy foods (lower score = better)*:
- **4-point scale** (4 groups: Fried Foods, High Fat Meat, Processed Foods, Sugar-Sweetened Beverages):
  - 1 = Ideal (rarely/never consumed)
  - 2 = Moderate (occasional consumption)
  - 3 = Frequent (regular consumption)
  - 4 = Very frequent (daily consumption)

- **3-point scale** (2 groups: Additional Salt Use, Salty Food Consumption):
  - 1 = Ideal (never)
  - 2 = Sometimes
  - 3 = Often

**Validation**: Scoring criteria were based on Korean Dietary Reference Intakes (KDRIs) 2020 and validated by a nutritionist expert panel.

For network construction, all scores were consistently binarized:
- **High consumption**: Score ≥ 3 (coded as 1)
- **Low consumption**: Score < 3 (coded as 0)

---

## Network Construction

### Co-occurrence Network Method
Co-occurrence networks were constructed to represent simultaneous consumption patterns of food groups within each stratified group.

#### Step 1: Binary Matrix Creation
For each group, a binary matrix **B** (n × 12) was created, where:
- n = number of participants in the group
- Rows represent participants
- Columns represent 12 food groups
- B[i,j] = 1 if participant i has high consumption of food group j
- B[i,j] = 0 otherwise

#### Step 2: Co-occurrence Matrix Calculation
The co-occurrence matrix **C** (12 × 12) was calculated as:

```
C = (B^T × B) / n
```

Where:
- C[i,j] represents the proportion of participants consuming both food groups i and j at high levels
- Diagonal elements were set to 0 (self-loops excluded)

#### Step 3: Edge Threshold Selection
To identify meaningful co-occurrence relationships while maintaining network interpretability:
- Threshold was set at the 70th percentile of all non-zero co-occurrence values
- Only co-occurrence values above this threshold were retained as network edges
- This approach balances network density and biological significance

#### Step 4: Network Construction
For each stratified group:
1. Create graph G = (V, E) where V = 12 food group nodes
2. Add edge (i, j) if C[i,j] ≥ threshold
3. Assign edge weight w[i,j] = C[i,j]

### Rationale for Co-occurrence Method
Co-occurrence networks were chosen over other network methods for several reasons:
1. **Interpretability**: Direct representation of simultaneous consumption patterns
2. **Simplicity**: No assumptions about conditional independence
3. **Robustness**: Less sensitive to sample size variations across groups
4. **Clinical Relevance**: Captures real-world dietary patterns and food combinations

---

## Network Analysis Metrics

### Node-Level Metrics

#### 1. Degree Centrality
Measures the number of direct connections a food group has:

```
DC(i) = k_i / (N - 1)
```

Where:
- k_i = number of edges connected to node i
- N = total number of nodes (12)
- Range: [0, 1]

**Interpretation**: Foods with high degree centrality are consumed simultaneously with many other foods, suggesting they are central to dietary patterns.

#### 2. Betweenness Centrality
Measures how often a food group lies on the shortest path between other food groups:

```
BC(i) = Σ_(s≠i≠t) (σ_st(i) / σ_st)
```

Where:
- σ_st = total number of shortest paths from node s to node t
- σ_st(i) = number of those paths passing through node i

**Interpretation**: Foods with high betweenness centrality act as "bridges" connecting different dietary patterns.

#### 3. Closeness Centrality
Measures the average shortest path length from a food group to all other food groups:

```
CC(i) = (N - 1) / Σ_j d(i,j)
```

Where:
- d(i,j) = shortest path distance between nodes i and j
- N = total number of nodes

**Interpretation**: Foods with high closeness centrality are closely connected to all other foods in the diet.

### Network-Level Metrics

#### 1. Network Density
Proportion of possible edges that are present:

```
Density = 2E / (N(N-1))
```

Where:
- E = number of edges
- N = number of nodes (12)

**Interpretation**: Higher density indicates more interconnected dietary patterns.

#### 2. Average Clustering Coefficient
Measures the degree to which nodes cluster together:

```
C = (1/N) Σ_i C_i
```

Where C_i is the local clustering coefficient of node i:

```
C_i = 2e_i / (k_i(k_i - 1))
```

- e_i = number of edges between neighbors of node i
- k_i = degree of node i

**Interpretation**: Higher clustering suggests tightly connected food consumption patterns.

#### 3. Average Degree
Mean number of connections per node:

```
<k> = 2E / N
```

**Interpretation**: Indicates overall connectivity of the dietary network.

#### 4. Network Diameter (when connected)
Length of the longest shortest path:

```
diam(G) = max_(i,j) d(i,j)
```

**Interpretation**: Maximum "distance" between any two foods in the network.

#### 5. Average Path Length (when connected)
Mean shortest path length between all node pairs:

```
L = (1/(N(N-1))) Σ_(i≠j) d(i,j)
```

**Interpretation**: Average "steps" needed to connect any two foods through the network.

---

## Hub Identification

### Hub Definition
Food groups were classified as **network hubs** if they met one or more of the following criteria:

1. **High Degree Centrality**: Top 25th percentile within each network
2. **High Betweenness Centrality**: Top 25th percentile within each network
3. **High Closeness Centrality**: Top 25th percentile within each network

### Hub Ranking
Within each stratified group, hubs were ranked by:
1. Primary criterion: Degree centrality (most important for co-occurrence networks)
2. Secondary criterion: Betweenness centrality
3. Tertiary criterion: Closeness centrality

### Hub Transitions Across Age Groups
To identify changes in dietary patterns with aging, we analyzed how hub foods change across age groups within each sex-MetS combination:
- **Stable hubs**: Foods maintaining hub status across all three age groups
- **Emerging hubs**: Foods becoming hubs in older age groups
- **Declining hubs**: Foods losing hub status in older age groups

---

## Visualization Methods

### Network Layout Algorithm
Force-directed layout (Fruchterman-Reingold algorithm) was used for all network visualizations with the following parameters:
- **k (optimal distance)**: 0.5
- **Iterations**: 50
- **Seed**: 42 (for reproducibility)
- **Node size**: Proportional to degree centrality
- **Node color**: Mapped to degree centrality (yellow-orange-red scale)
- **Edge width**: Proportional to co-occurrence strength
- **Edge color**: Gray with transparency (α = 0.3)

### Heatmap Construction
Centrality heatmaps were created with:
- **Rows**: 12 food groups
- **Columns**: 11 stratified groups
- **Color scale**: Yellow-orange-red (YlOrRd) from matplotlib
- **Value range**: [0, 1] for degree and closeness; [0, max] for betweenness
- **Annotations**: Cell values displayed to 3 decimal places

### Flowchart Design
Hub transition flowcharts were constructed to show:
- **Boxes**: Age groups (vertical arrangement, oldest to youngest)
- **Content per box**:
  - Top 3 hub foods (ranked by degree centrality)
  - Network metrics (edge count, density)
- **Arrows**: Indicate progression through age groups
- **Color coding**:
  - Light blue: Age group labels
  - Light yellow: Hub food information
  - Light green: Network metrics

---

## Statistical Analysis

### Group Comparisons

#### Network Structure Comparison
Differences in network metrics across groups were assessed using:
- **Descriptive statistics**: Mean, SD, range for each metric
- **Visual inspection**: Side-by-side comparison of network properties
- **Effect size**: Absolute differences in density, clustering, etc.

#### Hub Stability Analysis
Consistency of hub foods across groups was evaluated by:
1. Counting frequency of each food appearing as a hub
2. Identifying foods that are hubs in multiple groups
3. Assessing sex-, age-, and MetS-specific hub patterns

### Software and Packages

All analyses were performed using Python 3.12 with the following packages:

- **Data manipulation**: pandas (v2.1.0), numpy (v1.24.0)
- **Network analysis**: networkx (v3.1)
- **Visualization**: matplotlib (v3.7.0), seaborn (v0.12.0)
- **Statistical computing**: scipy (v1.11.0)

Network files were saved in GEXF (Graph Exchange XML Format) for interoperability with other network analysis tools (e.g., Gephi, Cytoscape).

---

## Quality Control and Validation

### Data Quality Checks
1. **Missing data**: Participants with >20% missing dietary data were excluded
2. **Outlier detection**: Extreme values (>3 SD from mean) were reviewed
3. **Consistency checks**: Logical inconsistencies were flagged and resolved

### Network Validation
1. **Minimum sample size**: Groups with n < 100 were excluded
2. **Network connectivity**: All networks were checked for disconnected components
3. **Edge threshold sensitivity**: Alternative thresholds (60th, 80th percentiles) were tested
4. **Reproducibility**: Random seed was set for all stochastic algorithms

### Robustness Checks
1. **Threshold variation**: Results were stable across 60-80th percentile thresholds
2. **Binarization cutoff**: Alternative cutoffs (≥2.5, ≥3.5) yielded similar hub rankings
3. **Centrality metrics**: Multiple centrality measures showed consistent hub identification

---

## Limitations and Considerations

### Methodological Limitations
1. **Cross-sectional design**: Cannot establish causality or temporal relationships
2. **Self-reported dietary data**: Subject to recall and social desirability bias
3. **Food group aggregation**: May obscure specific food-level associations
4. **Binary threshold**: Loss of information from continuous consumption scores

### Network-Specific Limitations
1. **Co-occurrence vs. causality**: Edges represent correlation, not causation
2. **Threshold selection**: Somewhat arbitrary, though biologically motivated
3. **Small-world properties**: Not assessed due to network size (n=12 nodes)
4. **Temporal dynamics**: Cannot capture changes in dietary patterns over time

### Generalizability
Results are specific to:
- Korean adult population
- KNHANES sampling and assessment methods
- 12 predefined food groups
- Binary consumption classification

---

## Ethical Considerations

This study was approved by the Institutional Review Board of [Institution Name]. All participants provided written informed consent. The KNHANES data are publicly available and de-identified, ensuring participant confidentiality.

---

## Data and Code Availability

- **Network files**: Available in GEXF format (Graph Exchange XML Format)
- **Network statistics**: Available in CSV format
- **Analysis scripts**: Python scripts for network construction and visualization
- **Supplementary data**: Complete edge lists and centrality rankings for all 11 groups

All materials are available at: [Repository URL to be added]

---

**Correspondence**: [Contact information for data/code requests]

**Last Updated**: November 1, 2025
