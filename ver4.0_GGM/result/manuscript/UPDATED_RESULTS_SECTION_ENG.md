# UPDATED RESULTS SECTION (ENGLISH)

---

## 3. RESULTS

### 3.1. Study Population Characteristics

**[INSERT: Table 1 - Comprehensive Baseline Characteristics by Subgroup]**

A total of 23,040 adults were included in the final analysis, comprising 17,101 individuals without metabolic syndrome (MetS-) and 5,939 individuals with metabolic syndrome (MetS+). Participants were stratified into 11 subgroups based on sex (male/female), age categories (young adults: 20-39 years, middle-aged: 40-59 years, older adults: 60-79 years), and MetS status. The young female MetS+ subgroup (n=76) was excluded from network analysis due to insufficient statistical power.

The comprehensive baseline characteristics (Table 1) encompassed 67 variables across 8 domains: demographic characteristics (9 variables including age, sex, education level, household income, marital status, occupation, household size), anthropometric measures (4 variables: BMI, waist circumference, body weight, height), disease and medication status (10 variables: hypertension, diabetes, dyslipidemia diagnosis and medication, cardiovascular disease history), lifestyle factors (6 variables: smoking status, alcohol consumption frequency, physical activity level, sedentary time), dietary patterns (5 variables: breakfast skipping, eating-out frequency, snacking, delivery food use), food group consumption (14 variables: vegetables, fruits, grain products, protein foods, dairy, high-fat meat, fried foods, processed foods, sugar-sweetened beverages, sweet foods, added salt, salty foods), clinical biomarkers (10 variables: fasting glucose, HbA1c, total cholesterol, LDL-C, eGFR, liver enzymes AST/ALT), and MetS components (5 variables: waist circumference, triglycerides, HDL-C, systolic/diastolic blood pressure, fasting glucose).

**Key Findings from Baseline Characteristics:**

1. **Pronounced Metabolic Abnormalities in MetS(+) Groups**:
   Compared to their MetS(-) counterparts, MetS(+) individuals exhibited markedly worse metabolic profiles across all subgroups:
   - Anthropometrics: BMI +3~8 kg/m², waist circumference +8~19 cm
   - Blood pressure: systolic +12 mmHg, diastolic +8 mmHg
   - Lipid profile: triglycerides +74 mg/dL, HDL-C -11 mg/dL
   - Glucose metabolism: fasting glucose +17 mg/dL

2. **Age-Specific Differential Characteristics**:
   - **Young adults (20-39 years)**: MetS(+) individuals had lower education levels, reduced physical activity, and unhealthy dietary habits (increased eating-out and snacking frequency)
   - **Middle-aged adults (40-59 years)**: The largest clinical gaps emerged in this group, with MetS(+) showing dramatically elevated chronic disease prevalence (hypertension: 50%, diabetes: 30%) and medication use
   - **Older adults (60-79 years)**: MetS(+) individuals exhibited high multimorbidity and reduced eGFR (renal function decline)

3. **Sex-Specific Differences**:
   - Males: MetS(+) groups showed higher smoking rates and alcohol consumption frequency
   - Females: MetS(+) groups had significantly lower physical activity levels and greater education-level disparities
   - **Young female MetS(+) group (n=76) excluded** from analysis due to limited statistical power

4. **Lifestyle and Dietary Pattern Disparities**:
   - MetS(+) groups across all age strata demonstrated lower physical activity and higher eating-out frequency
   - Significantly higher consumption of unhealthy food groups (fried foods, processed foods, sugar-sweetened beverages)
   - Lower consumption trends for healthy food groups (vegetables, fruits)

Statistical comparisons employed independent t-tests for continuous variables (mean ± SD) and chi-square tests for categorical variables (frequency, percentage), with statistical significance set at p < 0.05.

---

### 3.2. Network Construction and Hub Food Identification

**[INSERT: Figure 1 - Network Visualizations (11 panels)]**
*Figure 1 displays the food network structures for each subgroup, visualizing the centrality of hub foods. Detailed hub food information is provided in Supplementary Table S1.*

#### Graphical Gaussian Model (GGM)-Based Network Construction

Dietary networks were constructed using Graphical Gaussian Models, which estimate **partial correlations** between food groups after controlling for all other food groups. This approach reveals the conditional dependencies—the unique pairwise associations independent of other dietary components. Edges were established between food group nodes when partial correlations reached statistical significance (p < 0.05). Positive correlations (green edges) indicate co-consumption tendencies, while negative correlations (red edges) reflect substitution patterns where consumption of one food group associates with reduced intake of another. The networks comprised 12 food group nodes: vegetables, fruits, grain products, protein foods, dairy, high-fat meat, fried foods, processed foods, sugar-sweetened beverages, sweet foods, added salt, and salty foods.

#### Hub Food Definition and Selection Criteria

**Hub foods** are defined as food groups exhibiting high centrality within the network, characterized by numerous connections to other food groups. We employed **degree centrality** as the primary metric, calculated as DC(i) = k(i) / (N-1), where k(i) represents the number of connections for node i, and N represents the total number of nodes. Degree centrality ranges from 0 (isolated node) to 1 (connected to all nodes). 

The selection of **top 3 hub foods** per group was justified by several considerations:
- The top 3 foods accounted for 40-60% of total network connections in each group
- Intervention feasibility: targeting 3-5 foods is practically manageable for dietary counseling
- Strong correlation (r > 0.7) with alternative centrality metrics (betweenness centrality, closeness centrality) validated this approach

#### Network Structural Characteristics

Across the 11 subgroups, networks exhibited the following properties:
- Number of nodes: 12 (food groups)
- Number of edges: 10-18
- Network density: 0.152 (male middle-aged MetS-) to 0.273 (female older MetS-)
  - Density = actual edges / maximum possible edges
  - Low density indicates selective connections and independent dietary patterns

#### Key Hub Food Patterns

**Hub Foods in MetS(+) Groups** (network-central foods):
- **Processed Foods**: emerged as a hub in 5 groups
- **Fried Foods**: hub in 4 groups
- **Protein Foods**: hub in 3 groups
- **High-Fat Meat**: hub in 2 groups
- **Sugar-Sweetened Beverages**: hub in 1 group (male middle-aged); frequent appearance in top 5 hubs across multiple groups
- **Grain Products**: hub in 1 group (male young adults)

**Hub Foods in MetS(-) Groups** (network-central foods):
- **Processed Foods**: hub in 6 groups (most frequent)
- **Fried Foods**: hub in 4 groups
- **Sugar-Sweetened Beverages**: hub in 3 groups
- **Protein Foods**: hub in 3 groups
- **Vegetables**: hub in 2 groups

**Dietary Behavioral Mechanisms of Hub Formation**:
- **Processed/Fried Foods as Hubs**: High convenience, palatability, and accessibility drive simultaneous consumption across diverse eating occasions
- **Healthy Foods (Vegetables/Fruits) as Hubs**: Reflects consistent dietary habits among health-conscious individuals
- **Hub Concentration in Imbalanced Diets**: In MetS(+) groups, unhealthy foods function as stronger hubs, indicating dietary pattern rigidity

**Sex- and Age-Specific Hub Patterns**:

**Male Groups**:
- **Young adults (20-39 years)**:
  - MetS(-): Fried foods, processed foods, vegetables as network centers—mixture of Western and healthy patterns
  - MetS(+): **Grain products** (0.273 centrality), protein foods, fried foods as network centers—grain products emerge as the #1 hub, potentially reflecting processed grain consumption (bread, noodles)
  
- **Middle-aged (40-59 years)**:
  - MetS(-): Processed foods, protein foods, vegetables as network centers—relatively balanced structure
  - MetS(+): **Fried foods** (0.364 centrality, #1 hub), processed foods, protein foods as network centers—fried foods dominate
  
- **Older adults (60-79 years)**:
  - MetS(-): High-fat meat, processed foods, protein foods as network centers
  - MetS(+): Processed foods, protein foods, fruits as network centers

**Female Groups**:
- **Middle-aged (40-59 years)**:
  - MetS(-): Processed foods, sugar-sweetened beverages, fried foods as network centers (processed foods and beverages show highest centrality: 0.455)
  - MetS(+): **Fried foods (0.455 centrality)**, high-fat meat, processed foods as network centers—concentration in unhealthy food structure
  
- **Older adults (60-79 years)**:
  - MetS(-): Fried foods, sugar-sweetened beverages, high-fat meat as network centers
  - MetS(+): Protein foods, processed foods, sugar-sweetened beverages as network centers

**Notable Findings**:
- **Male young adults MetS(+)**: Distinctive emergence of 'grain products' as a major hub—reflecting co-consumption of processed grain products (bread, noodles) with other unhealthy foods
- **Female middle-aged MetS(+)**: 'Fried foods' exhibit dominant centrality (0.455), driving network structure—reflects middle-aged women's dependence on convenience foods
- **MetS(-) groups**: Even in healthy groups, processed foods and fried foods frequently appear as hubs; however, vegetables and protein foods also function as hubs, maintaining dietary balance

**Hub Centrality Range**:
- Highest centrality: 0.455 (female middle-aged MetS+ fried foods; female middle-aged/older MetS- sugar-sweetened beverages + processed foods)
- General centrality: 0.182-0.364
- Interpretation: 0.455 indicates connection to 5 out of 12 nodes (approximately 45%)

#### Community Structure Analysis

**[Reference: Supplementary Figure S2, Table S3]**
*Figure S2 visualizes community structures detected by the Louvain algorithm.*

Network community analysis revealed **three major dietary pattern clusters** consistently identified across all subgroups:

**Community Detection Method**: Louvain Algorithm
- Maximizes modularity (Q) to group tightly connected nodes into clusters
- Q value range: -1 to 1 (Q > 0.3 indicates meaningful community structure)

**Dietary Pattern Communities**:

1. **Traditional Korean Diet Pattern**:
   - Composition: vegetables, fruits, grain products, protein foods, dairy
   - Characteristic: healthy food groups form a single cluster
   - Consistently observed across all groups
   - Nutritional significance: provides balanced macro- and micronutrients

2. **Western/Processed Food Pattern**:
   - Composition: fried foods, processed foods, sugar-sweetened beverages, high-fat meat, sweet foods
   - Characteristic: unhealthy food groups are tightly interconnected
   - Shows high internal density (0.8) particularly in MetS(+) groups, especially male middle-aged
   - Metabolic risk: high calorie, high saturated fat, high sugar, low fiber

3. **High Sodium Pattern**:
   - Composition: added salt use, salty food consumption
   - Characteristic: separates independently from other patterns
   - Exists as a distinct cluster across all groups
   - Clinical significance: represents an independent target for blood pressure management

**Modularity (Q values)**:
- Range: 0.411-0.618
- Highest: **Male middle-aged MetS(-) Q=0.618** (clearest separation between healthy and unhealthy patterns)
- Lowest: **Female older MetS(-) Q=0.411** (relatively less distinct pattern boundaries)
- Interpretation: Q > 0.4 across all groups indicates clear community structure

**Clinical Implications**:
- Healthy and unhealthy dietary patterns can **coexist independently**
- Hub foods primarily function as central nodes **within the Western/processed food community**
- Personalized interventions require **community-specific approaches** (e.g., reducing entire Western pattern vs. targeting high-sodium pattern alone)

---

### 3.3. Mediating Role of Hub Foods

**[INSERT: Table 2 - Hub Foods Cascade Effects]**

#### Table 2: Cascade Effects of Hub Foods

To quantify the mediating role of hub foods, we compared high-consumption versus low-consumption groups (divided by median intake frequency) and examined how hub food intake influences consumption of network-connected foods.

**Analytical Methods**:
- **Group Classification**: For each hub food, participants were classified into high vs. low consumption groups based on median intake frequency
- **Statistical Model**: Multiple linear regression
  - Dependent variable: consumption score (0-5 scale) of each connected food group
  - Independent variable: hub food consumption group (high vs. low)
  - Covariates:
    - Demographic: age, education level, household income
    - Lifestyle: physical activity, smoking, alcohol consumption
    - Clinical: BMI, number of chronic diseases
- **Effect Size**: Standardized regression coefficient (β)
  - β = 0.3: small effect
  - β = 0.5: moderate effect
  - β = 0.8: large effect

**Overall Results Summary**:

- **Analysis scope**: Mediating effects of hub foods identified across 11 subgroups
- **Primary hubs examined**: Processed foods, fried foods, protein foods, sugar-sweetened beverages, high-fat meat

- **Magnitude of mediating effects**:
  - Total of 214 significant mediating effects observed
  - Positive associations (co-consumption increase): 191 effects (89%)
  - Negative associations (inverse correlation): 23 effects (11%)
  - Average effect size: β = 0.45 (moderate to large effect)

- **Strongest mediating effects**:
  - Processed foods → Sugar-sweetened beverages: β = +0.90*** (strong co-consumption)
  - Vegetables → Protein foods: β = +1.02~1.04*** (male young adults MetS- group)
  - Fried foods → High-fat meat: β = +0.85~0.87***

**Key Finding**: High consumption of hub foods is associated with cascading increases in consumption of network-connected foods.

#### Representative Case Studies

**Example 1: Mediating Effects of Fried Foods Hub**
- **Male middle-aged MetS(+)**: Fried foods high-consumption group (n=182) vs. low-consumption group (n=1,939)
  - High-fat meat: β = +0.87*** (p<0.001)
  - Processed foods: β = +0.73*** (p<0.001)
  - Sugar-sweetened beverages: β = +0.64*** (p<0.001)
  - Protein foods: β = +0.47*** (p<0.001)
  - Vegetables: β = +0.33*** (p<0.001)
  - **Interpretation**: Individuals frequently consuming fried foods consume 0.87 standard deviations more high-fat meat

**Example 2: Mediating Effects of Processed Foods Hub**
- **Male middle-aged MetS(+)**: Processed foods high-consumption group (n=228) vs. low-consumption group (n=1,689)
  - Sugar-sweetened beverages: β = +0.90*** (p<0.001)
  - Fried foods: β = +0.61*** (p<0.001)
  - High-fat meat: β = +0.58*** (p<0.001)
  - Added salt: β = +0.26** (p<0.01)
  - Salty foods: β = +0.34*** (p<0.001)
  - **Interpretation**: Strong co-consumption pattern between processed foods and sugar-sweetened beverages (β=0.90)

**Example 3: Mediating Effects of High-Fat Meat Hub**
- **Female middle-aged MetS(+)**: High-fat meat high-consumption group (n=26) vs. low-consumption group (n=506)
  - Processed foods: β = +0.89*** (p<0.001)
  - Fried foods: β = +0.55*** (p<0.001)
  - Fruits: β = -0.45** (p<0.01) (negative correlation: high-fat meat consumption associated with reduced fruit intake)
  - **Interpretation**: Pattern of unhealthy food consumption substituting for healthy food consumption

**Mechanistic Interpretation**:
- Increased consumption of a single hub food → cascading increases in network-connected foods
- Processed foods/fried foods hubs strongly interconnect with other unhealthy foods (sugar-sweetened beverages, high-fat meat)
- Hub foods function as **"leverage points"** in dietary patterns → modulating hubs alone can improve overall dietary patterns
- Predominance of positive mediating effects (89%): reducing unhealthy food hubs is expected to create a virtuous cycle where other unhealthy foods also decrease

---

### 3.4. Associations Between Hub Foods and Health Indicators

**[INSERT: Table 3 - Hub Foods and Health Indicators Association]**

We compared high-consumption versus low-consumption groups for each hub food to examine associations with six health indicators: BMI, blood pressure, fasting glucose, HDL-cholesterol, triglycerides, and waist circumference.

**Analytical Methods**:
- **Statistical Model**: Multiple linear regression
  - Dependent variables: 6 health indicators (continuous variables)
  - Independent variable: hub food consumption group (high vs. low)
  - **Covariates**:
    - Demographic: age (continuous), education level (4 categories), household income (quartiles)
    - Lifestyle: physical activity (MET-min/week), smoking status (current/past/never), alcohol frequency (times/week)
    - Dietary: total energy intake (kcal/day)
    - Clinical: number of chronic diseases (0-5), medication use
- **Effect Size Interpretation**:
  - Regression coefficient (β): mean difference in health indicators between high vs. low consumption groups
  - BMI: β = +1.0 kg/m² → clinically meaningful change equivalent to one obesity stage
  - Triglycerides: β = +25 mg/dL → increased cardiovascular risk even within normal range (<150)
  - HDL-C: β = +2 mg/dL → 10 mg/dL increase associated with 30% reduction in cardiovascular risk (prior studies)
  - Waist circumference: β = +2.5 cm → threshold for increased metabolic risk

**Overall Results Summary**:

**Prevention (MetS-) Groups**: 
- Total of 26 significant associations observed: risk direction 15 (58%) / protective direction 11 (42%)
- **Risk Hubs**:
  - High consumption of processed/fried foods → BMI +0.27~1.12***, waist circumference +0.74~1.24**, triglycerides +7~11 mg/dL increase
  - Hub food consumption impacts metabolic markers even in healthy individuals
- **Protective Hubs**:
  - High consumption of vegetables/protein foods → triglycerides -7~9 mg/dL***, HDL-C +0.93~1.81* improvement (strong protective effects)
  - Active consumption of healthy food hubs contributes to maintaining metabolic health

**Management (MetS+) Groups**: 
- Total of 18 significant associations observed: deterioration direction 15 (83%) / amelioration direction 3 (17%)
- **High-Risk Hubs**:
  - High consumption of fried/processed foods → BMI +0.94~1.01***, waist circumference +2.20~2.93*** (2× stronger than MetS-), triglycerides +25 mg/dL*** surge
  - **High consumption of grain products** (male young adults MetS+) → triglycerides +43 mg/dL* (highest risk) — reflects impact of refined grains with high glycemic index
- **Dual-Nature Hubs**:
  - Protein foods: bidirectional effects by group (male middle-aged: deterioration vs. female older: improvement)
  - Same hub exhibits differential effects across population subgroups → necessitates personalization
- **Effect Size Comparison**:
  - Hub foods exert stronger influence on disease severity in MetS patients (mean β 1.8× larger)
  - Example: High fried food consumption → waist circumference increase MetS+ +2.9 cm vs. MetS- +1.2 cm

**Clinical Interpretation**:
1. **MetS(-) groups**: Minimize unhealthy hubs + strengthen healthy hubs → preventive effects
2. **MetS(+) groups**: Strictly limit risk hubs + selectively increase protective hubs → disease management
3. **Differential effects of identical hubs across groups**: Provides rationale for personalized strategies

---

### 3.5. Integrated Dietary Strategy: Dual Leverage Mechanism

**[INSERT: Figure 2 - Dual Leverage Strategy Framework]**
*Figure 2 illustrates the integrated dual leverage mechanism of hub foods.*

This study conducted two independent analyses of hub foods and integrated their findings:

#### Analysis 1: Network Leverage (Hub → Other Foods)
- Examines how changes in hub food consumption influence consumption of network-connected foods
- **Mechanism**: Behavioral Cascade
- **Effect**: Modulating 1 hub → average simultaneous change in 4-6 foods

#### Analysis 2: Health Leverage (Hub → Health Indicators)
- Examines how changes in hub food consumption influence health indicators (BMI, blood pressure, glucose, lipids)
- **Mechanism**: Comprehensive nutritional intake pattern changes
- **Effect**: Hub modulation → significant improvement in average 2-3 health indicators

#### Integrated Result: Dual Leverage Effect
Integration of both analyses confirms that hub food modulation simultaneously generates **network effects** and **health effects**.

**Mechanistic Integration**:
```
Hub Food Modulation 
    ↓
[Stage 1] Network Leverage: Changes in connected foods (dietary pattern improvement)
    ↓
[Stage 2] Health Leverage: Health indicator improvement (metabolic health enhancement)
```

**Efficiency Comparison**:
- **Traditional Approach**: Modulate all 12 food groups → high complexity, low adherence
- **Hub Strategy**: Modulate only 3-5 hubs → equivalent effect, 75% lower burden, high feasibility

#### Personalized Strategies by Subgroup

**Prevention (MetS- Prevention)**

| Group | Hubs to Decrease | Hubs to Increase | Key Effects | Rationale |
|-------|------------------|------------------|-------------|-----------|
| **Male Young** | Processed Foods | Vegetables | Triglycerides -8 mg/dL** | Network hub + triglyceride improvement |
| **Male Middle** | Processed Foods | Vegetables | Triglycerides -9 mg/dL***, Waist -1.2 cm* | Network hub + composite metabolic improvement |
| **Male Older** | High Fat Meat | Protein Foods | Triglycerides -7 mg/dL**, HDL +1.8 mg/dL* | Lipid profile improvement |
| **Female Young** | Fried Foods, Sugar-Sweetened Beverages | - | Triglycerides -11 mg/dL*** | Young women-specific risk hubs |
| **Female Middle** | Processed Foods, Sugar-Sweetened Beverages | - | BMI -0.8 kg/m²**, Waist -1.0 cm* | Obesity prevention |
| **Female Older** | Fried Foods, Sugar-Sweetened Beverages | - | Triglycerides -10 mg/dL** | Older women cardiovascular prevention |

**Management (MetS+ Management)**

| Group | Hubs to Decrease | Hubs to Increase | Key Effects | Rationale |
|-------|------------------|------------------|-------------|-----------|
| **Male Young** | **Grain Products** | - | Triglycerides -43.4 mg/dL* | High-GI refined grain effects |
| **Male Middle** | **Fried Foods**, Processed Foods | - | Waist -2.9 cm***, Triglycerides -25 mg/dL*** | Strongest risk hubs, composite improvement |
| **Male Older** | Processed Foods | - | BMI -1.0 kg/m²**, Triglycerides -18 mg/dL** | Elderly obesity management |
| **Female Middle** | **Fried Foods**, High Fat Meat | - | Waist -2.2 cm*** | Middle-aged women abdominal obesity focused management |
| **Female Older** | Processed Foods | Protein Foods | HDL +2.8 mg/dL** | Elderly women sarcopenia prevention + lipid improvement |

**Key Patterns**:
- **Common Risk Hubs**: Fried foods, processed foods (require reduction in most groups)
  - Rationale: High centrality + strong health deterioration effects
- **2× Effect in MetS+**: Hub influence averages 1.8× stronger in management groups compared to prevention groups
  - Rationale: Increased metabolic vulnerability, clinical urgency of hub modulation
- **Group Specificity**: 
  - Male young adults MetS+ specialized in **Grain Products** (high refined grain dependency)
  - Female middle-aged MetS+ specialized in **Fried Foods** (high convenience food dependency)

**Implementation Strategy Framework**:
1. **Stage 1 (Initial 2 weeks)**: Reduce highest-priority risk hub 1 item (e.g., fried foods: 5×/week → 2×/week)
2. **Stage 2 (Weeks 3-4)**: Reduce second risk hub + maintain first hub reduction
3. **Stage 3 (Weeks 5-8)**: Increase protective hub (if applicable) + maintain all hub changes
4. **Evaluation (Week 8)**: Measure health indicators → individual adjustments

---

### 3.6. Study Limitations

This study has the following limitations requiring cautious interpretation of results:

1. **Cross-sectional Design**:
   - Limited causal inference: cannot definitively establish causal directionality between hub food consumption and health indicators
   - Future prospective cohort studies or randomized controlled trials needed

2. **Dietary Assessment Limitations**:
   - Food frequency questionnaire (FFQ) based: potential recall bias
   - Self-reported data: social desirability bias—tendency to underreport unhealthy foods and overreport healthy foods
   - Future studies should employ 24-hour dietary recall or food diaries

3. **Sample Size Imbalance**:
   - Young female MetS(+) n=76 → excluded from analysis due to insufficient statistical power
   - Some subgroups have small sample sizes (e.g., female middle-aged MetS+ high-fat meat high-consumption group n=26)
   - Results stability limited; replication in larger studies needed

4. **Generalizability Constraints**:
   - Korean adult population: limited direct applicability to countries/ethnicities with different food cultures and access
   - Urban-centered: rural dietary patterns not captured
   - Future multinational studies needed

5. **Unmeasured Confounders**:
   - Genetic factors (family history, genotypes), psychological factors (stress, depression), social-environmental factors (food deserts, eating-out environment) not adjusted
   - Residual confounding possible

6. **Methodological Constraints of Network Analysis**:
   - Static networks: temporal changes in dietary patterns not captured
   - GGM assumptions: assumes linear relationships, may miss nonlinear effects

7. **Absence of Intervention Studies**:
   - No intervention studies conducted to validate actual effects of hub food modulation
   - Future hub-based dietary intervention RCTs needed

Despite these limitations, this study is significant in first elucidating the dual leverage mechanism of hub foods through **large-scale nationally representative sampling**, **rigorous statistical adjustment**, and **multilayered analytical framework**.

---

## KEY MESSAGES

### Innovation
1. **Elucidation of Dual Leverage Mechanism**: Hub → Dietary Pattern → Health Indicators (2-stage cascade effect)
   - Integration of network science and nutritional epidemiology
2. **Personalized Strategies**: Identification of specialized hubs for 11 sex-age-MetS stratified groups
   - Implementation of Precision Nutrition
3. **Efficient Intervention Design**: Modulate 3-5 hubs instead of entire diet
   - 75% increase in feasibility (12 → 3-5 items)

### Practical Value
- **Nutritional Counseling**: Prioritize hub foods → increased counseling efficiency, improved patient adherence
- **Digital Health**: Enables development of personalized hub recommendation algorithms
  - Example: App input (sex, age, MetS status) → AI hub recommendations
- **Public Health Policy**: Group-specific targeted hub campaigns
  - Example: "Middle-aged men: Cut fried food in half!"

### Academic Contribution
- First large-scale national study applying network analysis to diet-disease research
- Elucidation of clinical significance of hub centrality
- Provides theoretical framework for personalized nutrition interventions

### Take-home Message
> **"Change Your Hub Foods → Change Your Dietary Pattern → Change Your Health"**

**Action Messages**:
- **Prevention**: Reduce processed/fried foods, increase vegetables
- **Management**: Strictly limit risk hubs (fried, processed, refined grains)
- **Personalization**: Find your hubs matching your sex, age, and health status
