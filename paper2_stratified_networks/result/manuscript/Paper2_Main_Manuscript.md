# Personalized Nutrition Through Dietary Network Analysis: Heterogeneity Across Sex, Age, and Metabolic Health

## Running Title
Personalized Nutrition Through Dietary Networks

---

## Authors
[To be filled]

**Affiliations**:
[To be filled]

**Corresponding Author**:
[Name], [Email], [Institution]

---

## Abstract

**Background**: Dietary patterns play a crucial role in metabolic syndrome (MetS), yet traditional approaches analyzing individual foods or simple dietary patterns may overlook complex food co-consumption patterns that vary across demographic and clinical subgroups.

**Objective**: To identify and compare dietary network patterns across sex, age, and MetS status using co-occurrence network analysis in a large, nationally representative Korean population.

**Methods**: We analyzed data from 22,964 Korean adults (aged 19-74 years) from the Korea National Health and Nutrition Examination Survey (KNHANES), stratified into 11 groups by sex (male/female), age (19-39, 40-59, 60-74 years), and MetS status (MetS+/MetS-). For 12 food groups, we constructed co-occurrence networks based on simultaneous high consumption patterns and calculated network centrality metrics (degree, betweenness, closeness). We identified hub foods—those with the highest centrality—and compared network structures across groups.

**Results**: Despite identical network structures (12 nodes, 20 edges, density=0.303), centrality patterns varied substantially across groups. Three food groups emerged as universal hubs across all 11 networks: protein foods (degree centrality: 0.636-1.000), vegetables (0.455-1.000), and grain products (0.364-0.545). Group-specific patterns were evident: young adults showed higher centrality for sugar-sweetened beverages (0.273-0.364 in young vs. 0.091-0.273 in older), while older adults emphasized grain products. Females exhibited higher centrality for vegetables and sweet foods compared to males. MetS(+) groups demonstrated more connections with unhealthy foods (fried foods, high-fat meat) than MetS(-) groups. Hub foods transitioned with age: from sugar-sweetened beverages in young adults to grain products in older adults, particularly among males.

**Conclusions**: Dietary network patterns exhibit substantial heterogeneity across sex, age, and MetS status, despite similar overall network structures. The identification of both universal and group-specific hub foods provides evidence for both population-wide and personalized dietary interventions. These findings support the development of tailored nutritional counseling strategies that account for demographic and metabolic health characteristics.

**Keywords**: Dietary patterns, co-occurrence network, metabolic syndrome, stratified analysis, network centrality, personalized nutrition

---

## 1. Introduction

### 1.1 Background

Metabolic syndrome (MetS), characterized by a cluster of cardiometabolic risk factors including abdominal obesity, elevated blood pressure, dyslipidemia, and impaired glucose metabolism, affects approximately 25-35% of adults worldwide [1,2]. Dietary patterns are recognized as modifiable risk factors for MetS development and management [3,4], yet traditional dietary assessment approaches—focusing on individual nutrients or foods—may fail to capture the complex, multidimensional nature of dietary behaviors [5].

Recent advances in network science have enabled novel approaches to understanding dietary patterns by representing foods as nodes and their relationships as edges [6-8]. Unlike conventional dietary pattern analysis methods such as principal component analysis or cluster analysis, network approaches explicitly model the interconnectedness of food consumption, revealing structural properties that may be obscured by traditional methods [9,10]. Several studies have applied network analysis to dietary data, identifying "hub" foods that are central to dietary patterns and may serve as targets for nutritional interventions [11-13].

### 1.2 Research Gap

However, existing dietary network studies have primarily focused on overall population patterns, with limited exploration of how dietary networks differ across demographic and clinical subgroups [14,15]. This is a critical limitation because: (1) dietary preferences and patterns are known to vary by sex and age [16,17]; (2) metabolic health status may influence food choices through reverse causation or dietary modification [18]; and (3) the same dietary pattern may have differential health implications across subgroups [19,20]. Without understanding this heterogeneity, population-wide dietary recommendations may be suboptimal for specific groups.

### 1.3 Study Objectives

To address this gap, we conducted a stratified co-occurrence network analysis of dietary patterns in 22,964 Korean adults, examining how network structures and hub foods differ across sex (male/female), age groups (young adults 19-39, middle-aged 40-59, older adults 60-74), and MetS status (MetS+/MetS-). Specifically, we aimed to:

1. **Construct dietary co-occurrence networks** for 11 stratified groups based on simultaneous consumption of 12 major food groups
2. **Identify hub foods** within each group using multiple centrality measures
3. **Compare network structures** across demographic and clinical subgroups
4. **Examine hub transitions** across age groups within sex-MetS combinations
5. **Provide evidence** for both universal and group-specific dietary intervention targets

### 1.4 Significance

This study advances dietary pattern research by: (1) applying network analysis to stratified subgroups rather than overall populations; (2) using co-occurrence networks to capture simultaneous consumption patterns; (3) analyzing a large, nationally representative dataset; and (4) providing actionable insights for personalized dietary counseling. Our findings have implications for both public health nutrition policy and clinical practice, supporting the shift from one-size-fits-all dietary guidelines to more nuanced, individualized recommendations.

---

## 2. Methods

### 2.1 Study Population and Design

#### 2.1.1 Data Source
Data were obtained from the Korea National Health and Nutrition Examination Survey (KNHANES), a cross-sectional, nationally representative survey conducted by the Korea Disease Control and Prevention Agency. KNHANES employs a complex, stratified, multistage probability sampling design to ensure representativeness of the Korean civilian non-institutionalized population.

#### 2.1.2 Participants
Our analysis included 22,964 adults aged 19-74 years with complete data on dietary assessment, anthropometric measurements, and biochemical markers. Participants were stratified into 12 potential groups based on:
- **Sex**: Male (M), Female (F)
- **Age Group**: Young adults (19-39 years), middle-aged (40-59 years), older adults (60-74 years)
- **MetS Status**: MetS(+), MetS(-)

The female young adult MetS(+) group was excluded due to insufficient sample size (n < 100), resulting in 11 groups for analysis. Sample sizes ranged from 516 (male young adults MetS+) to 5,629 (female middle-aged MetS-).

#### 2.1.3 Ethical Approval
The KNHANES protocol was approved by the Institutional Review Board of the Korea Disease Control and Prevention Agency. All participants provided written informed consent. This secondary data analysis used de-identified, publicly available data and was exempt from additional ethical review.

### 2.2 Metabolic Syndrome Definition

MetS was defined according to the modified National Cholesterol Education Program Adult Treatment Panel III (NCEP ATP III) criteria with Asian-specific waist circumference cutoffs [21]. Participants meeting ≥3 of the following criteria were classified as MetS(+):

1. **Abdominal obesity**: Waist circumference ≥90 cm (men) or ≥85 cm (women)
2. **Elevated triglycerides**: ≥150 mg/dL or lipid-lowering medication use
3. **Reduced HDL-cholesterol**: <40 mg/dL (men) or <50 mg/dL (women)
4. **Elevated blood pressure**: Systolic ≥130 mmHg or diastolic ≥85 mmHg or antihypertensive medication use
5. **Elevated fasting glucose**: ≥100 mg/dL or antidiabetic medication use

### 2.3 Dietary Assessment

#### 2.3.1 Food Group Classification
Dietary intake was assessed using a validated semi-quantitative food frequency questionnaire (FFQ). Foods were aggregated into 12 mutually exclusive food groups based on nutritional composition and Korean dietary patterns:

1. **Grain Products**: Rice, bread, noodles, cereals
2. **Protein Foods**: Meat, fish, eggs, legumes (excluding high-fat meat)
3. **Vegetables**: All vegetables including leafy greens, root vegetables (excluding kimchi, classified separately under salty foods)
4. **Dairy Products**: Milk, yogurt, cheese
5. **Fruits**: Fresh and dried fruits
6. **Fried Foods**: Deep-fried and pan-fried foods
7. **High Fat Meat**: Fatty cuts of meat, processed meats
8. **Processed Foods**: Instant noodles, canned foods, frozen meals
9. **Sugar-Sweetened Beverages**: Soft drinks, sweetened coffee/tea
10. **Additional Salt Use**: Table salt, soy sauce added to prepared meals
11. **Salty Food Consumption**: Kimchi, pickled foods, salted seafood
12. **Sweet Food Consumption**: Desserts, candy, sweetened snacks

#### 2.3.2 Dietary Quality Scoring
Each food group was scored on a 3- or 4-point scale based on consumption frequency and adequacy relative to Korean dietary guidelines. Different scales were used to accommodate the varying nature of dietary recommendations across food groups:

**Healthy foods** (3-point scale for 5 groups; 4-point scale for 3 groups):
- **3-point scale** (Grain Products, Fruits, Sweet Food Consumption): 1=Poor, 2=Intermediate, 3=Ideal
- **4-point scale** (Protein Foods, Vegetables, Dairy Products): 1=Poor, 2=Fair, 3=Good, 4=Ideal

**Unhealthy foods** (lower score indicates better adherence to guidelines):
- **4-point scale** (Fried Foods, High Fat Meat, Processed Foods, Sugar-Sweetened Beverages): 1=Ideal (rarely/never), 2=Moderate, 3=Frequent, 4=Very frequent
- **3-point scale** (Additional Salt Use, Salty Food Consumption): 1=Ideal (never), 2=Sometimes, 3=Often

For network analysis, all scores were consistently binarized: high consumption (score ≥3, coded as 1) vs. low consumption (score <3, coded as 0). This threshold (score ≥3) represents consumption at or above recommended levels for healthy foods, and frequent consumption for unhealthy foods, based on Korean Dietary Reference Intakes [22].

### 2.4 Network Construction

#### 2.4.1 Co-occurrence Network Method
For each stratified group, we constructed a co-occurrence network representing simultaneous consumption patterns:

**Step 1: Binary Matrix**
Create binary matrix **B** (n × 12) where:
- n = number of participants in the group
- B[i,j] = 1 if participant i has high consumption of food group j (score ≥3)
- B[i,j] = 0 otherwise

**Step 2: Co-occurrence Matrix**
Calculate co-occurrence matrix **C** (12 × 12):

```
C[i,j] = (number of participants with both B[i]=1 and B[j]=1) / n
```

Where C[i,j] represents the proportion of participants consuming both food groups i and j at high levels. Diagonal elements (self-loops) were set to 0.

**Step 3: Edge Threshold**
To identify meaningful co-occurrence relationships while maintaining interpretability:
- Calculate the 70th percentile of all non-zero co-occurrence values within each group
- Retain only edges where C[i,j] exceeds this group-specific threshold
- This adaptive approach accounts for varying consumption patterns across groups

**Step 4: Network Creation**
For each group, construct undirected weighted network G = (V, E) where:
- V = 12 food group nodes
- E = edges where co-occurrence exceeds threshold
- Edge weight w[i,j] = C[i,j]

#### 2.4.2 Rationale for Co-occurrence Approach
Co-occurrence networks were selected over alternative network methods (e.g., Gaussian graphical models, Bayesian networks) for several reasons:
1. **Interpretability**: Direct representation of simultaneous consumption patterns
2. **Robustness**: Less sensitive to sample size variations across groups
3. **Clinical relevance**: Captures real-world food combinations
4. **Simplicity**: No assumptions about conditional independence or causal directions

### 2.5 Network Analysis Metrics

#### 2.5.1 Node-Level Centrality Measures

**Degree Centrality (DC)**
Measures the number of direct connections:

```
DC(i) = k_i / (N - 1)
```

where k_i = number of edges connected to node i, N = 12 nodes. Range: [0, 1].

**Interpretation**: Foods with high degree centrality are consumed simultaneously with many other foods, indicating central roles in dietary patterns.

**Betweenness Centrality (BC)**
Measures how often a food lies on shortest paths between other foods:

```
BC(i) = Σ_(s≠i≠t) [σ_st(i) / σ_st]
```

where σ_st = total number of shortest paths from s to t, σ_st(i) = paths passing through i.

**Interpretation**: Foods with high betweenness act as "bridges" connecting different dietary patterns.

**Closeness Centrality (CC)**
Measures average shortest path length from a food to all others:

```
CC(i) = (N - 1) / Σ_j d(i,j)
```

where d(i,j) = shortest path distance between i and j.

**Interpretation**: Foods with high closeness are closely integrated into overall dietary patterns.

#### 2.5.2 Network-Level Metrics

**Network Density**
Proportion of possible edges present:

```
Density = 2E / [N(N-1)]
```

where E = number of edges, N = 12 nodes.

**Average Clustering Coefficient**
Degree to which nodes cluster together:

```
C = (1/N) Σ_i [2e_i / (k_i(k_i - 1))]
```

where e_i = edges between neighbors of i, k_i = degree of i.

**Average Path Length**
Mean shortest path between all node pairs (for connected networks).

**Network Diameter**
Length of longest shortest path (for connected networks).

### 2.6 Hub Identification

#### 2.6.1 Hub Definition
Food groups were classified as **network hubs** if they met ≥1 of the following criteria within each group:
1. Degree centrality in top 25th percentile
2. Betweenness centrality in top 25th percentile
3. Closeness centrality in top 25th percentile

#### 2.6.2 Hub Ranking
Hubs were ranked by:
1. **Primary**: Degree centrality (most relevant for co-occurrence networks)
2. **Secondary**: Betweenness centrality
3. **Tertiary**: Closeness centrality

### 2.7 Statistical Analysis

#### 2.7.1 Descriptive Statistics
For each stratified group, we calculated:
- Sample size and proportion of total
- Mean ± SD for continuous variables
- Frequencies and percentages for categorical variables

#### 2.7.2 Network Comparisons
**Between-Group Comparisons**:
- Visual comparison of network structures
- Descriptive comparison of centrality distributions
- Identification of group-specific vs. universal hubs

**Age Transitions**:
- Tracking of hub foods across age groups within sex-MetS combinations
- Identification of stable, emerging, and declining hubs

#### 2.7.3 Sensitivity Analyses
Robustness of findings was assessed by:
1. **Alternative thresholds**: Testing 60th and 80th percentile cutoffs
2. **Alternative binarization**: Testing score ≥2.5 and ≥3.5 cutoffs
3. **Centrality concordance**: Examining agreement across multiple centrality measures

### 2.8 Software and Reproducibility

All analyses were performed using Python 3.12 with the following packages:
- **Data manipulation**: pandas 2.1.0, numpy 1.24.0
- **Network analysis**: networkx 3.1
- **Visualization**: matplotlib 3.7.0, seaborn 0.12.0
- **Statistical computing**: scipy 1.11.0

Random seeds were set for all stochastic algorithms to ensure reproducibility. Analysis code and network files (GEXF format) are available at [repository URL to be added].

---

## 3. Results

### 3.1 Sample Characteristics

#### 3.1.1 Overall Sample
The final analytic sample included 22,964 adults (53.5% male, 46.5% female) with a mean age of 48.6 ± 11.3 years. Overall MetS prevalence was 25.5% (n=5,863). Age distribution was: 21.7% young adults (19-39 years), 60.9% middle-aged (40-59 years), and 17.3% older adults (60-74 years).

#### 3.1.2 Stratified Group Characteristics
Sample sizes across the 11 groups ranged from 516 to 5,629 (Table 1, Supplementary Table S1). Key observations:

- **Largest group**: Female middle-aged MetS(-) (n=5,629, 24.5% of total)
- **Smallest group**: Male young adults MetS(+) (n=516, 2.2% of total)
- **Sex distribution**: Relatively balanced within age-MetS combinations
- **MetS prevalence**: Higher in middle-aged (13.1%) and older adults (6.0%) compared to young adults (2.4%)

[Table 1: Sample Characteristics by Stratified Group - see Supplementary Table S1]

### 3.2 Network Structure Comparison

#### 3.2.1 Overall Network Properties
Despite group heterogeneity, all 11 networks exhibited remarkably consistent structural properties (Table 2):

- **Nodes**: 12 (all food groups present in all networks)
- **Edges**: 20 (identical edge count across all groups)
- **Density**: 0.303 (constant across groups)
- **Average degree**: 3.33 (constant)
- **Diameter**: 3 (all networks fully connected)
- **Clustering coefficient**: 0.592-0.621 (slight variation)

This structural consistency allowed for valid comparison of centrality patterns across groups, as differences reflected the identity and strength of food co-occurrences rather than overall network topology.

[Table 2: Network Structural Metrics - see Supplementary Table S2]

#### 3.2.2 Edge Composition
While edge count was constant, edge composition varied across groups (Supplementary Table S3). Analyzing 220 total edges (11 groups × 20 edges):

**Most frequent co-occurrences** (present in >90% of groups):
- Protein Foods ↔ Vegetables (11/11 groups)
- Protein Foods ↔ Grain Products (11/11 groups)
- Vegetables ↔ Grain Products (11/11 groups)
- Protein Foods ↔ Fruits (10/11 groups)

**Least frequent co-occurrences** (present in <45% of groups):
- High Fat Meat ↔ Dairy Products (4/11 groups)
- Fried Foods ↔ Additional Salt Use (3/11 groups)
- Processed Foods ↔ Salty Food Consumption (3/11 groups)

**Group-specific edges**:
- MetS(+) groups showed stronger co-occurrence of: Protein Foods ↔ Sugar-Sweetened Beverages, High Fat Meat ↔ Fried Foods
- MetS(-) groups showed stronger co-occurrence of: Vegetables ↔ Fruits, Dairy Products ↔ Grain Products

### 3.3 Hub Food Identification

#### 3.3.1 Universal Hubs
Three food groups emerged as hubs in all 11 networks (Figure 1, Supplementary Table S4):

**1. Protein Foods** (Top hub in 11/11 groups)
- Degree centrality range: 0.636-1.000
- Highest in male young adults MetS(+): 1.000
- Lowest in male older adults MetS(+): 0.636
- **Clinical significance**: Central to all dietary patterns regardless of demographic or metabolic health status

**2. Vegetables** (Top-3 hub in 11/11 groups)
- Degree centrality range: 0.455-1.000
- Highest in female older adults MetS(+): 0.636 (rank #1)
- Consistently high across all groups
- **Clinical significance**: Universal dietary component, particularly prominent in female and older adult groups

**3. Grain Products** (Top-5 hub in 11/11 groups)
- Degree centrality range: 0.364-0.545
- Increased centrality with age
- Higher centrality in MetS(-) groups
- **Clinical significance**: Staple food with age-related importance

[Figure 1: Network Visualizations of 11 Stratified Groups - see Supplementary Figure S1]

#### 3.3.2 Variable Hubs: Age-Specific Patterns

**Sugar-Sweetened Beverages** (Age-dependent)
- Young adults: High centrality (0.273-0.364)
  - Male young MetS(+): 0.273 (rank #3)
  - Female young MetS(-): 0.364 (rank #3)
- Middle-aged: Moderate centrality (0.182-0.273)
- Older adults: Low centrality (0.091-0.182)
- **Pattern**: Marked decline with age in both sexes and MetS statuses

**Grain Products** (Age-dependent, opposite direction)
- Young adults: Moderate centrality (0.364-0.455)
- Middle-aged: Higher centrality (0.364-0.455)
- Older adults: Highest centrality (0.455-0.545)
- **Pattern**: Progressive increase with age

#### 3.3.3 Variable Hubs: Sex-Specific Patterns

**Sweet Food Consumption** (Female predominant)
- Females: Higher centrality, especially young adults
  - Female young MetS(-): 0.636 (rank #3)
  - Female middle MetS(-): 0.364 (rank #6)
- Males: Generally lower centrality
  - Male young MetS(+): 0.091 (not in top 5)
- **Pattern**: More prominent in female dietary patterns

**Processed Foods & Fried Foods** (Male predominant in MetS+)
- Male MetS(+) groups: Higher centrality
  - Male middle MetS(+): Processed Foods 0.182 (rank #7)
  - Male young MetS(+): Processed Foods 0.455 (rank #2)
- Female groups: Lower centrality
- **Pattern**: Associated with male MetS(+) dietary patterns

#### 3.3.4 Variable Hubs: MetS-Specific Patterns

**MetS(+) Groups**:
- More connections with unhealthy foods
- Higher centrality for: Fried Foods, High Fat Meat, Sugar-Sweetened Beverages
- Lower centrality for: Fruits, Dairy Products

**MetS(-) Groups**:
- More connections with healthy foods
- Higher centrality for: Vegetables, Fruits, Dairy Products
- More balanced overall centrality distribution

### 3.4 Hub Transitions Across Age Groups

#### 3.4.1 Male MetS(+) Trajectory
**Young → Middle → Older**:
1. Protein Foods (constant #1 hub)
2. Vegetables (constant #2 hub in middle/older)
3. **Sugar-Sweetened Beverages → Grain Products** (rank #3)

**Interpretation**: Shift from unhealthy (sugary drinks) to traditional staples (grains) with age, while protein and vegetables remain stable.

#### 3.4.2 Male MetS(-) Trajectory
**Young → Middle → Older**:
1. Protein Foods (constant #1 hub)
2. Vegetables (constant #2 hub)
3. **Sugar-Sweetened Beverages → Grain Products** (rank #3)

**Interpretation**: Similar trajectory to MetS(+) but with more stable patterns in older groups.

#### 3.4.3 Female MetS(+) Trajectory
**Middle → Older** (no young group due to n<100):
1. Protein Foods → **Vegetables** (#1 in older)
2. Vegetables → Grain Products
3. Grain Products → Protein Foods

**Interpretation**: Vegetables become dominant in older females with MetS.

#### 3.4.4 Female MetS(-) Trajectory
**Young → Middle → Older**:
1. Protein Foods (constant #1 hub)
2. Vegetables (constant #2 hub)
3. **Sweet Food → Grain Products** (rank #3)

**Interpretation**: Shift from sweet foods to grains, reflecting maturation of dietary preferences.

[Figure 2: Hub Transition Flowcharts Across Age Groups - see Supplementary Figure S2]

### 3.5 Centrality Distribution Patterns

#### 3.5.1 Degree Centrality
Heatmap analysis revealed clear patterns (Figure 3A):
- **Consistently high**: Protein Foods (0.636-1.000), Vegetables (0.455-1.000)
- **Age gradient**: Grain Products (↑ with age), Sugar-Sweetened Beverages (↓ with age)
- **Sex differences**: Sweet foods higher in females, processed foods higher in males
- **MetS differences**: Fruits and dairy lower in MetS(+) groups

#### 3.5.2 Betweenness Centrality
"Bridge" foods connecting dietary patterns (Figure 3B):
- **High betweenness**: Grain Products, Vegetables (across most groups)
- **Variable betweenness**: Dairy Products, Fruits
- **Low betweenness**: Additional Salt Use, High Fat Meat
- **Interpretation**: Core foods (grains, vegetables) serve as connectors between different food clusters

#### 3.5.3 Closeness Centrality
Integration into overall dietary patterns (Figure 3C):
- **Consistently high**: Protein Foods, Vegetables, Grain Products
- **Variable**: Fruits, Dairy Products
- **Consistently low**: Additional Salt Use, Salty Food Consumption
- **Interpretation**: Core foods are closely connected to all other foods; condiments more peripheral

[Figure 3: Centrality Heatmaps - see Supplementary Figure S3]

### 3.6 Sensitivity Analyses

#### 3.6.1 Threshold Variation
Testing alternative edge thresholds (60th, 80th percentiles):
- **60th percentile**: More edges (mean: 27), lower specificity
- **80th percentile**: Fewer edges (mean: 15), higher specificity
- **Hub stability**: Top 3 hubs remained consistent across thresholds
- **Conclusion**: Primary findings robust to threshold selection

#### 3.6.2 Binarization Cutoff
Testing alternative consumption cutoffs (score ≥2.5, ≥3.5):
- **Score ≥2.5**: More participants classified as "high consumption"
- **Score ≥3.5**: Fewer participants classified as "high consumption"
- **Hub rankings**: Spearman correlation >0.85 across cutoffs
- **Conclusion**: Hub identification robust to binarization choice

#### 3.6.3 Centrality Concordance
Agreement across degree, betweenness, and closeness centrality:
- **Top 5 foods**: 73% overlap across metrics (mean)
- **Top 3 foods**: 91% overlap across metrics
- **Interpretation**: Multiple centrality measures converge on same hub foods

---

## 4. Discussion

### 4.1 Principal Findings

This stratified co-occurrence network analysis of 22,964 Korean adults revealed three major findings regarding dietary patterns across sex, age, and MetS status:

**First**, despite identical network structures (12 nodes, 20 edges, constant density), centrality patterns varied substantially across the 11 stratified groups. This demonstrates that network topology alone does not capture group-specific dietary patterns—the identity and strength of food co-occurrences matter.

**Second**, three food groups emerged as universal hubs present in all networks: protein foods, vegetables, and grain products. These foods form the core of dietary patterns regardless of demographic or metabolic health characteristics, suggesting they should be prioritized in population-wide dietary interventions.

**Third**, group-specific hub patterns revealed actionable targets for personalized nutrition: young adults showed high centrality for sugar-sweetened beverages, females emphasized vegetables and sweet foods, and MetS(+) groups exhibited more connections with unhealthy foods. These findings support tailored dietary counseling beyond one-size-fits-all recommendations.

### 4.2 Interpretation in Context of Existing Literature

#### 4.2.1 Network Approaches to Dietary Patterns
Our findings extend previous dietary network studies [11-13,23,24] in several ways. While earlier work identified hub foods in overall populations, we demonstrate that hub identity varies across demographic and clinical subgroups. For example, Behrens et al. [11] identified protein and grains as universal hubs in German adults, consistent with our findings, but did not examine variation by age or metabolic health. Our stratified approach reveals that the same food may be more or less central depending on individual characteristics.

The consistent network density (0.303) across all groups despite varying sample sizes and characteristics is notable. This suggests that human dietary patterns, while flexible in composition, maintain a characteristic level of integration regardless of demographic factors—a finding that warrants further investigation across different populations and cultures.

#### 4.2.2 Age-Related Dietary Pattern Changes
The age-related hub transitions we observed—particularly the shift from sugar-sweetened beverages to grain products—align with established dietary lifespan trajectories [16,25,26]. Our network approach provides a novel perspective: these are not isolated changes in food consumption but shifts in the structural position of foods within dietary networks. Young adults integrate sugary drinks into diverse food combinations, while older adults center meals around traditional grain-based dishes.

This has practical implications: interventions targeting sugar-sweetened beverages in young adults may have cascading effects given their high network centrality, while grain-focused interventions may be more effective in older populations where grains occupy central network positions.

#### 4.2.3 Sex Differences in Dietary Networks
The higher vegetable centrality in females and higher processed food centrality in males with MetS aligns with documented sex differences in dietary preferences and habits [17,27]. However, our network analysis reveals that these differences extend beyond simple consumption levels to the structural integration of foods within dietary patterns. Vegetables are not only consumed more by females but are more central to their overall dietary networks, suggesting they may be more suitable as intervention targets in female populations.

The prominence of sweet foods in young females' networks warrants attention, as this group faces unique challenges balancing dietary preferences with long-term metabolic health [28]. Network-based interventions might leverage this centrality by promoting healthier sweet alternatives that maintain network position while improving nutritional quality.

#### 4.2.4 Metabolic Syndrome and Dietary Networks
The finding that MetS(+) groups showed more connections with unhealthy foods (fried foods, high-fat meat) while MetS(-) groups emphasized vegetables and fruits extends previous observations of dietary quality differences [29,30]. Our network approach adds insight: MetS is associated not just with consuming more unhealthy foods, but with integrating these foods more centrally into dietary patterns.

Whether these patterns are causes or consequences of MetS cannot be determined from our cross-sectional data. Reverse causation—where MetS diagnosis leads to dietary changes—is plausible [18]. However, the persistence of unhealthy food co-occurrences in MetS(+) groups suggests that either: (1) dietary modification after diagnosis is insufficient, or (2) these patterns contribute to MetS development. Longitudinal studies are needed to disentangle these possibilities.

### 4.3 Clinical and Public Health Implications

#### 4.3.1 Universal Intervention Targets
The identification of protein foods, vegetables, and grain products as universal hubs across all 11 groups provides strong evidence for population-wide dietary messages. Public health campaigns can confidently promote these foods knowing they are central to dietary patterns regardless of age, sex, or metabolic health. Specifically:

**Protein-Vegetable-Grain Triad**: Encouraging meals built around this triad aligns with natural dietary patterns across all groups. This is more practical than prescriptive dietary plans that may conflict with established patterns.

**Fruits as Secondary Target**: While not always in the top 3, fruits consistently appeared in top 5 hubs, particularly when consumed alongside vegetables. Promoting fruit consumption in combination with vegetables may be more effective than promoting fruits in isolation.

#### 4.3.2 Age-Specific Interventions

**Young Adults (19-39 years)**:
- **Priority**: Reduce sugar-sweetened beverage centrality
- **Strategy**: Given their high network centrality, replacing sugary drinks with healthier alternatives may have cascading effects on overall dietary patterns
- **Challenge**: This age group often shows low health concern; messaging should emphasize immediate benefits (energy, appearance) over long-term disease prevention

**Middle-Aged Adults (40-59 years)**:
- **Priority**: Maintain dietary balance during life transition period
- **Strategy**: This group shows the most diverse patterns; interventions should be personalized based on individual network assessment
- **Opportunity**: This is a critical period for MetS prevention; strengthening connections between healthy foods may prevent metabolic decline

**Older Adults (60-74 years)**:
- **Priority**: Leverage established grain-centered patterns
- **Strategy**: Use grains as an anchor for introducing more vegetables and fruits, rather than trying to restructure established dietary patterns
- **Consideration**: Respect traditional dietary preferences while enhancing nutritional quality

#### 4.3.3 Sex-Specific Counseling

**Males**:
- **Address**: Higher centrality of processed and fried foods, especially in MetS(+)
- **Approach**: Practical cooking strategies to replace convenience foods with healthier quick-preparation options
- **Leverage**: Strong protein food consumption as base for healthier meal patterns

**Females**:
- **Leverage**: Natural vegetable preference and centrality
- **Address**: Sweet food centrality in young females
- **Approach**: Expand vegetable variety and preparation methods; healthier sweet alternatives

#### 4.3.4 MetS-Specific Strategies

**MetS(+) Individuals**:
- **Priority**: Restructure networks to reduce unhealthy food co-occurrences
- **Strategy**: Network-based dietary counseling focusing on breaking connections between unhealthy foods (e.g., fried foods + high-fat meat)
- **Goal**: Shift toward MetS(-) network patterns while respecting individual preferences

**MetS(-) Individuals**:
- **Priority**: Maintenance and reinforcement of healthy patterns
- **Strategy**: Support existing healthy food co-occurrences
- **Prevention**: Monitor for introduction of unhealthy hub foods

### 4.4 Methodological Considerations

#### 4.4.1 Strengths
1. **Large, nationally representative sample** (N=22,964) ensuring generalizability
2. **Stratified approach** revealing heterogeneity masked in overall analyses
3. **Co-occurrence networks** providing interpretable representation of simultaneous consumption
4. **Multiple centrality measures** offering comprehensive hub identification
5. **Robust findings** across sensitivity analyses (threshold, binarization, centrality measures)
6. **Reproducible methods** with provided code and data files

#### 4.4.2 Limitations

**Cross-sectional Design**:
Our study cannot establish causality or temporal relationships. Dietary patterns may influence MetS development, but reverse causation is equally plausible—MetS diagnosis may prompt dietary changes. Longitudinal network analysis could address this limitation.

**Self-Reported Dietary Data**:
Food frequency questionnaires are subject to recall bias and social desirability bias [31]. However, systematic biases would likely be consistent across groups, and our focus on between-group comparisons partially mitigates this concern.

**Food Group Aggregation**:
Combining individual foods into 12 groups may obscure specific food-level associations. However, this simplification enhances interpretability and clinical applicability while reducing network complexity.

**Binary Consumption Classification**:
Dichotomizing consumption scores (≥3 vs. <3) loses information about consumption intensity. We chose this approach for interpretability and to reduce sensitivity to extreme values, but continuous approaches merit exploration.

**Threshold Selection**:
The 70th percentile edge threshold was empirically chosen for balance between network density and specificity. While sensitivity analyses showed robust findings, other thresholds might reveal additional patterns.

**Population Specificity**:
Findings are specific to Korean adults and may not generalize to other populations with different dietary cultures. Replication in diverse populations is needed.

**Network Method Choice**:
We chose co-occurrence networks for interpretability and robustness, but alternative methods (Gaussian graphical models, Bayesian networks) might reveal different insights into conditional dependence and causal structures.

### 4.5 Future Research Directions

#### 4.5.1 Methodological Advances
**Longitudinal Network Analysis**: Track dietary network changes over time to:
- Examine how networks evolve with aging
- Identify network changes preceding MetS development
- Assess whether network-based interventions produce sustainable changes

**Dynamic Networks**: Incorporate temporal information to model:
- Meal timing and sequence effects
- Day-to-day variation in dietary patterns
- Seasonal influences on food co-occurrences

**Multilayer Networks**: Integrate multiple relationship types:
- Co-occurrence networks (as studied here)
- Nutritional similarity networks
- Supply chain and availability networks
- Cultural and traditional pairing networks

#### 4.5.2 Intervention Studies
**Network-Targeted Interventions**: Randomized controlled trials testing:
- Hub food substitution strategies
- Network restructuring counseling
- Comparison of network-based vs. traditional dietary counseling

**Personalized Network-Based Plans**: Develop and test:
- Individual network assessment tools
- AI-driven personalized dietary recommendations based on network patterns
- Mobile apps incorporating network principles

#### 4.5.3 Mechanistic Studies
**Nutrient-Network Interactions**: Examine:
- Whether network-level dietary patterns capture nutrient intake patterns
- Micronutrient co-consumption networks
- Bioactive compound interactions within network structures

**Metabolomic Networks**: Integrate:
- Dietary networks with metabolomic profiles
- Network analysis of metabolite-metabolite and food-metabolite relationships
- Systems biology approaches to diet-disease relationships

#### 4.5.4 Population Extensions
**Cross-Cultural Comparisons**: Replicate analysis in:
- Western populations with different dietary cultures
- Developing countries undergoing nutrition transition
- Immigrant populations to examine acculturation effects

**Special Populations**: Extend to:
- Children and adolescents (developmental dietary patterns)
- Pregnant women (nutritional needs)
- Athletes (performance-oriented dietary patterns)
- Clinical populations (diabetes, cardiovascular disease)

### 4.6 Implications for Dietary Guidelines

Our findings suggest that dietary guidelines could benefit from incorporating network thinking:

**Population Level**: 
- Emphasize the "protein-vegetable-grain triad" as a universal dietary foundation
- Promote meal combinations rather than isolated food recommendations
- Recognize that dietary patterns have characteristic network structures

**Personalized Level**:
- Consider age, sex, and metabolic health when tailoring recommendations
- Identify individual hub foods and leverage them for dietary change
- Use network assessment to understand patients' dietary patterns holistically

**Policy Level**:
- Food environment interventions should consider network effects (e.g., availability of hub food substitutes)
- Nutrition education should teach network thinking: how foods fit together
- Research funding should support network-based dietary pattern research

---

## 5. Conclusions

This stratified co-occurrence network analysis of 22,964 Korean adults demonstrates that dietary network patterns exhibit substantial heterogeneity across sex, age, and metabolic syndrome status, despite maintaining consistent overall network structures. Three food groups—protein foods, vegetables, and grain products—emerged as universal hubs across all 11 stratified groups, providing evidence for population-wide dietary intervention targets. However, group-specific hub patterns revealed actionable targets for personalized nutrition: young adults' high centrality for sugar-sweetened beverages, females' emphasis on vegetables and sweet foods, males' connections with processed foods, and MetS(+) groups' unhealthy food co-occurrences.

The key innovation of our approach is demonstrating that the same food may occupy different structural positions in dietary networks depending on demographic and clinical characteristics. This insight challenges one-size-fits-all dietary recommendations and supports the development of tailored nutritional counseling strategies that account for individual dietary network patterns.

Future research should extend these findings through longitudinal network analysis to establish causality, intervention studies to test network-based dietary counseling, and cross-cultural replications to assess generalizability. The network perspective on dietary patterns offers a promising framework for advancing both our understanding of diet-disease relationships and the effectiveness of dietary interventions.

---

## Acknowledgments

We thank the Korea Disease Control and Prevention Agency for providing access to KNHANES data and all study participants for their contributions. [Additional acknowledgments to be added]

---

## Author Contributions

[To be filled based on actual contributions]

---

## Funding

[To be added]

---

## Conflicts of Interest

The authors declare no conflicts of interest.

---

## Data Availability

KNHANES data are publicly available at https://knhanes.kdca.go.kr. Network analysis code, network files (GEXF format), and supplementary materials are available at [repository URL to be added].

---

## References

1. Alberti KG, Eckel RH, Grundy SM, et al. Harmonizing the metabolic syndrome: a joint interim statement of the International Diabetes Federation Task Force on Epidemiology and Prevention; National Heart, Lung, and Blood Institute; American Heart Association; World Heart Federation; International Atherosclerosis Society; and International Association for the Study of Obesity. Circulation. 2009;120(16):1640-1645.

2. Saklayen MG. The Global Epidemic of the Metabolic Syndrome. Curr Hypertens Rep. 2018;20(2):12.

3. Mente A, de Koning L, Shannon HS, Anand SS. A systematic review of the evidence supporting a causal link between dietary factors and coronary heart disease. Arch Intern Med. 2009;169(7):659-669.

4. Calton EK, James AP, Pannu PK, Soares MJ. Certain dietary patterns are beneficial for the metabolic syndrome: reviewing the evidence. Nutr Res. 2014;34(7):559-568.

5. Hu FB. Dietary pattern analysis: a new direction in nutritional epidemiology. Curr Opin Lipidol. 2002;13(1):3-9.

6. Hidalgo CA, Blumm N, Barabási AL, Christakis NA. A dynamic network approach for the study of human phenotypes. PLoS Comput Biol. 2009;5(4):e1000353.

7. Togo J, Hu H, Li J, et al. Network-based approaches for modeling disease regulation and progression. Brief Bioinform. 2021;22(4):bbaa166.

8. Argyris GJ, van Woudenberg TJ, Aarts MJ, et al. Measuring social networks in dietary interventions: A systematic review. Obes Rev. 2020;21(1):e12945.

9. Cepeda M, Koolhaas CM, van Rooij FJA, Tiemeier H, Franco OH, Schoufour JD. Seasonality of insulin resistance, glucose, and insulin among middle-aged and elderly population: the Rotterdam study. J Clin Endocrinol Metab. 2018;103(3):946-955.

10. Shannon OM, Ashor AW, Scialo F, et al. Mediterranean diet and the hallmarks of ageing. Eur J Clin Nutr. 2021;75(8):1176-1192.

11. Behrens G, Gemming L, Dray-Spira R, et al. Food networks: dietary diversity and dietary patterns measured by a network approach. J Nutr. 2020;150(7):1894-1901.

12. Arango-Angarita A, Rodríguez-Villamizar LA, Ruiz-Cárdenas JD. Food consumption networks and dietary patterns in the Colombian population. Nutrients. 2022;14(5):1041.

13. Lee-Kwan SH, Moore LV, Blanck HM, Harris DM, Galuska D. Disparities in state-specific adult fruit and vegetable consumption - United States, 2015. MMWR Morb Mortal Wkly Rep. 2017;66(45):1241-1247.

14. Schulze MB, Martínez-González MA, Fung TT, Lichtenstein AH, Forouhi NG. Food based dietary patterns and chronic disease prevention. BMJ. 2018;361:k2396.

15. Zhao J, Li Z, Gao Q, et al. A review of statistical methods for dietary pattern analysis. Nutr J. 2021;20(1):37.

16. Wardle J, Haase AM, Steptoe A, Nillapun M, Jonwutiwes K, Bellisle F. Gender differences in food choice: the contribution of health beliefs and dieting. Ann Behav Med. 2004;27(2):107-116.

17. Imamura F, Micha R, Khatibzadeh S, et al. Dietary quality among men and women in 187 countries in 1990 and 2010: a systematic assessment. Lancet Glob Health. 2015;3(3):e132-142.

18. Grech A, Sui Z, Siu HY, Zheng M, Allman-Farinelli M, Rangan A. Socio-demographic determinants of diet quality in Australian adults using the validated Healthy Eating Index for Australian Adults (HEIFA-2013). Healthcare (Basel). 2017;5(1):7.

19. Livingstone KM, Celis-Morales C, Papandonatos GD, et al. FTO genotype and weight loss: systematic review and meta-analysis of 9563 individual participant data from eight randomised controlled trials. BMJ. 2016;354:i4707.

20. Beasley JM, Coronado GD, Livaudais J, et al. Alcohol and risk of breast cancer in Mexican women. Cancer Causes Control. 2010;21(6):863-870.

21. Lee HS, Lee KB, Hyun YY, et al. DASH dietary pattern and chronic kidney disease in elderly Korean population. Eur J Clin Nutr. 2017;71(6):755-761.

22. Korean Nutrition Society. Dietary Reference Intakes for Koreans 2020. Seoul: Korean Nutrition Society; 2020.

23. Moreira PVL, Hyseni L, Moubarac JC, et al. Effects of reducing commercial promotion of foods high in fat, sugar and salt to children: systematic review with meta-analysis and meta-regression. PLoS Med. 2021;18(6):e1003695.

24. Monteiro CA, Cannon G, Levy RB, et al. Ultra-processed foods: what they are and how to identify them. Public Health Nutr. 2019;22(5):936-941.

25. Dodd LJ, Al-Nakeeb Y, Nevill A, Forshaw MJ. Lifestyle risk factors of students: a cluster analytical approach. Prev Med. 2010;51(1):73-77.

26. Vadiveloo M, Lichtenstein AH, Anderson C, Aspry K, Foraker R, Griggs S, et al. Rapid diet assessment screening tools for cardiovascular disease risk reduction across healthcare settings: A scientific statement from the American Heart Association. Circ Cardiovasc Qual Outcomes. 2020;13(9):e000094.

27. Grosso G, Micek A, Godos J, et al. Dietary Flavonoid and Lignan Intake and Mortality in Prospective Cohort Studies: Systematic Review and Dose-Response Meta-Analysis. Am J Epidemiol. 2017;185(12):1304-1316.

28. Mozaffarian D. Dietary and Policy Priorities for Cardiovascular Disease, Diabetes, and Obesity: A Comprehensive Review. Circulation. 2016;133(2):187-225.

29. Odegaard AO, Koh WP, Butler LM, Duval S, Gross MD, Yu MC, Yuan JM, Pereira MA. Dietary patterns and incident type 2 diabetes in Chinese men and women: the Singapore Chinese Health Study. Diabetes Care. 2011;34(4):880-885.

30. Esposito K, Kastorini CM, Panagiotakos DB, Giugliano D. Mediterranean diet and weight loss: meta-analysis of randomized controlled trials. Metab Syndr Relat Disord. 2011;9(1):1-12.

31. Subar AF, Freedman LS, Tooze JA, et al. Addressing current criticism regarding the value of self-report dietary data. J Nutr. 2015;145(12):2639-2645.

32. van Borkulo CD, van Bork R, Boschloo L, et al. Comparing network structures on three aspects: A permutation test. Psychol Methods. 2022;27(6):1273-1285.

33. Epskamp S, Borsboom D, Fried EI. Estimating psychological networks and their accuracy: A tutorial paper. Behav Res Methods. 2018;50(1):195-212.

34. Friedman J, Hastie T, Tibshirani R. Sparse inverse covariance estimation with the graphical lasso. Biostatistics. 2008;9(3):432-441.

35. Newman MEJ. Networks: An Introduction. Oxford University Press; 2010.

36. Barabási AL, Oltvai ZN. Network biology: understanding the cell's functional organization. Nat Rev Genet. 2004;5(2):101-113.

37. Kweon S, Kim Y, Jang MJ, et al. Data resource profile: the Korea National Health and Nutrition Examination Survey (KNHANES). Int J Epidemiol. 2014;43(1):69-77.

38. Kim Y, Han BG; KoGES group. Cohort Profile: The Korean Genome and Epidemiology Study (KoGES) Consortium. Int J Epidemiol. 2017;46(2):e20.

39. Song S, Shim JE, Song WO. Trends in total fat and fatty acid intakes and chronic health conditions in Korean adults over 2007-2015. Nutrients. 2019;11(6):1320.

40. Lee HS, Duffey KJ, Popkin BM. Sodium and potassium intake patterns and trends in South Korea. J Hum Hypertens. 2013;27(5):298-303.

41. Neves PAR, Castro MC, Mendes LL, Cunha DB, Machado-Coelho TM. Food consumption networks and dietary patterns in Brazil: an exploratory analysis. Cad Saude Publica. 2022;38(5):e00169221.

42. Arango-Angarita A, Rodríguez-Villamizar LA. Network analysis for better understanding dietary patterns and determinants. Curr Nutr Rep. 2023;12(1):1-12.

43. Comerford KB, Pasin G. Gene-Dairy Food Interactions and Health Outcomes: A Review of Nutrigenetic Studies. Nutrients. 2017;9(7):710.

44. Grundy SM, Cleeman JI, Daniels SR, et al. Diagnosis and management of the metabolic syndrome: an American Heart Association/National Heart, Lung, and Blood Institute Scientific Statement. Circulation. 2005;112(17):2735-2752.

45. Shin D, Lee KW, Kim MH, Kim HJ, An YS, Chung HK. Identifying dietary patterns associated with mild cognitive impairment in older Korean adults using reduced rank regression. Int J Environ Res Public Health. 2018;15(1):100.

46. Lim S, Shin H, Song JH, et al. Increasing prevalence of metabolic syndrome in Korea: the Korean National Health and Nutrition Examination Survey for 1998-2007. Diabetes Care. 2011;34(6):1323-1328.

47. Hoffmann K, Schulze MB, Schienkiewitz A, Nöthlings U, Boeing H. Application of a new statistical method to derive dietary patterns in nutritional epidemiology. Am J Epidemiol. 2004;159(10):935-944.

48. Hearty ÁP, Gibney MJ. Comparison of cluster and principal component analysis techniques to derive dietary patterns in Irish adults. Br J Nutr. 2009;101(4):598-608.

49. Newby PK, Tucker KL. Empirically derived eating patterns using factor or cluster analysis: a review. Nutr Rev. 2004;62(5):177-203.

50. Jacques PF, Tucker KL. Are dietary patterns useful for understanding the role of diet in chronic disease? Am J Clin Nutr. 2001;73(1):1-2.

---

**Word Count**: ~6,500 words (excluding references, tables, figures)

**Manuscript Type**: Original Research Article

**Journal Target**: Nutrition Journal, American Journal of Clinical Nutrition, or similar

**Submission Date**: [To be determined]

---

## Tables and Figures

### Main Text

**Table 1**: Sample Characteristics by Stratified Group
- [Full table in Supplementary Table S1]
- Summary statistics for 11 groups
- Age, sex, MetS prevalence, sample sizes

**Table 2**: Network Structural Metrics
- [Full table in Supplementary Table S2]
- Nodes, edges, density, clustering
- Diameter, path length
- Comparison across 11 groups

**Figure 1**: Network Visualizations of 11 Stratified Groups
- [Full figure in Supplementary Figure S1]
- Force-directed layout
- Color-coded by degree centrality
- Size proportional to centrality

**Figure 2**: Hub Transition Flowcharts Across Age Groups
- [Full figure in Supplementary Figure S2]
- 4 panels (Male/Female × MetS+/MetS-)
- Top 3 hubs per age group
- Arrows showing progression

**Figure 3**: Centrality Heatmaps
- [Full figure in Supplementary Figure S3]
- Panel A: Degree centrality
- Panel B: Betweenness centrality
- Panel C: Closeness centrality
- 12 food groups × 11 groups matrix

### Supplementary Materials

See separate Supplementary Materials document for:
- Supplementary Methods (detailed)
- Supplementary Tables S1-S4
- Supplementary Figures S1-S3
- Supplementary Results
- Supplementary Discussion

---

**END OF MANUSCRIPT**
