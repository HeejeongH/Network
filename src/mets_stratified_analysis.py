#!/usr/bin/env python3
"""
MetS 층화 분석: MetS(+)와 MetS(-) 그룹의 식습관 패턴 비교
GGM + Co-occurrence (Poor/Non-Poor) 통합 분석
"""

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.stats import spearmanr, mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("MetS 층화 분석 - 식습관 패턴 비교")
print("=" * 80)

# 1. 데이터 로드
print("\n[1단계] 데이터 로딩 및 MetS 그룹 분리...")
data = pd.read_csv("db/processed_data/total_only_org.csv")
print(f"전체 데이터: {len(data):,}명")

# MetS 그룹 분리
data_mets_pos = data[data['MetS'] == 1].copy()
data_mets_neg = data[data['MetS'] == 0].copy()

print(f"  - MetS(+): {len(data_mets_pos):,}명 ({len(data_mets_pos)/len(data)*100:.1f}%)")
print(f"  - MetS(-): {len(data_mets_neg):,}명 ({len(data_mets_neg)/len(data)*100:.1f}%)")

# 2. 변수 정의
food_groups = [
    'Grain Products', 'Protein Foods', 'Vegetables', 'Dairy Products',
    'Fruits', 'Fried Foods', 'High Fat Meat', 'Processed Foods',
    'Sugar-Sweetened Beverages', 'Additional Salt Use',
    'Salty Food Consumption', 'Sweet Food Consumption'
]

# NPN 변환 함수
def npn_transform(X):
    """Nonparanormal transformation"""
    n, p = X.shape
    X_npn = np.zeros((n, p))
    for j in range(p):
        ranks = stats.rankdata(X[:, j])
        X_npn[:, j] = stats.norm.ppf(ranks / (n + 1))
    return X_npn

# Co-occurrence 네트워크 구축 함수
def build_cooccurrence_network(data, food_cols, threshold_low=1, 
                               threshold_high=None, percentile=70):
    """Co-occurrence 네트워크 구축"""
    if threshold_high is None:
        consumed = (data[food_cols] >= threshold_low).astype(int)
    else:
        consumed = (data[food_cols] == threshold_low).astype(int)
    
    cooccur_matrix = consumed.T.dot(consumed).values
    occurrence = consumed.sum(axis=0).values
    
    with np.errstate(divide='ignore', invalid='ignore'):
        cooccur_normalized = cooccur_matrix / np.sqrt(np.outer(occurrence, occurrence))
        cooccur_normalized = np.nan_to_num(cooccur_normalized, 0)
    
    G = nx.Graph()
    for food in food_cols:
        G.add_node(food)
    
    values = cooccur_normalized[np.triu_indices_from(cooccur_normalized, k=1)]
    values = values[values > 0]
    
    if len(values) > 0:
        threshold = np.percentile(values, percentile)
        for i in range(len(food_cols)):
            for j in range(i+1, len(food_cols)):
                if cooccur_normalized[i, j] > threshold:
                    G.add_edge(food_cols[i], food_cols[j], 
                             weight=cooccur_normalized[i, j])
    
    return G, cooccur_normalized

# 3. GGM 분석 - MetS(+) vs MetS(-)
print("\n[2단계] GGM 네트워크 분석 (MetS 그룹별)...")

threshold = 0.01
networks_ggm = {}

for group_name, group_data in [('MetS_Positive', data_mets_pos), ('MetS_Negative', data_mets_neg)]:
    print(f"\n  {group_name} GGM 분석 중...")
    
    X = group_data[food_groups].values
    X_npn = npn_transform(X)
    X_scaled = StandardScaler().fit_transform(X_npn)
    
    model = GraphicalLassoCV(cv=5, alphas=20, max_iter=100, n_jobs=-1)
    model.fit(X_scaled)
    precision = model.precision_
    
    G = nx.Graph()
    for node in food_groups:
        G.add_node(node)
    
    for i in range(len(food_groups)):
        for j in range(i+1, len(food_groups)):
            if abs(precision[i, j]) > threshold:
                G.add_edge(food_groups[i], food_groups[j], weight=abs(precision[i, j]))
    
    networks_ggm[group_name] = {
        'graph': G,
        'precision': precision,
        'alpha': model.alpha_,
        'degree_cent': nx.degree_centrality(G),
        'between_cent': nx.betweenness_centrality(G)
    }
    
    print(f"    - 엣지: {G.number_of_edges()}개")
    print(f"    - 밀도: {nx.density(G):.3f}")
    print(f"    - 최적 alpha: {model.alpha_:.4f}")

# 4. Co-occurrence 분석 - MetS 그룹별 Poor/Non-Poor
print("\n[3단계] Co-occurrence 네트워크 분석 (MetS x Diet Quality)...")

networks_cooccur = {}

for group_name, group_data in [('MetS_Positive', data_mets_pos), ('MetS_Negative', data_mets_neg)]:
    print(f"\n  {group_name} Co-occurrence 분석 중...")
    
    # Poor diet (score = 1)
    G_poor, _ = build_cooccurrence_network(
        group_data, food_groups, threshold_low=1, threshold_high=1, percentile=70
    )
    
    # Non-poor diet (score >= 3)
    G_nonpoor, _ = build_cooccurrence_network(
        group_data, food_groups, threshold_low=3, threshold_high=None, percentile=70
    )
    
    networks_cooccur[f'{group_name}_Poor'] = {
        'graph': G_poor,
        'degree_cent': nx.degree_centrality(G_poor),
        'between_cent': nx.betweenness_centrality(G_poor)
    }
    
    networks_cooccur[f'{group_name}_NonPoor'] = {
        'graph': G_nonpoor,
        'degree_cent': nx.degree_centrality(G_nonpoor),
        'between_cent': nx.betweenness_centrality(G_nonpoor)
    }
    
    print(f"    - Poor Diet: {G_poor.number_of_edges()}개 엣지, 밀도 {nx.density(G_poor):.3f}")
    print(f"    - Non-Poor Diet: {G_nonpoor.number_of_edges()}개 엣지, 밀도 {nx.density(G_nonpoor):.3f}")

# 5. 식품 섭취량 비교 (MetS+ vs MetS-)
print("\n[4단계] 식품군 섭취량 비교 (Mann-Whitney U test)...")

food_intake_comparison = []
for food in food_groups:
    pos_vals = data_mets_pos[food].dropna()
    neg_vals = data_mets_neg[food].dropna()
    
    stat, pval = mannwhitneyu(pos_vals, neg_vals, alternative='two-sided')
    
    food_intake_comparison.append({
        'Food_Group': food,
        'MetS_Pos_Mean': pos_vals.mean(),
        'MetS_Pos_Std': pos_vals.std(),
        'MetS_Neg_Mean': neg_vals.mean(),
        'MetS_Neg_Std': neg_vals.std(),
        'Mean_Difference': pos_vals.mean() - neg_vals.mean(),
        'U_Statistic': stat,
        'P_value': pval,
        'Significant': 'Yes' if pval < 0.05 else 'No'
    })

df_intake = pd.DataFrame(food_intake_comparison).sort_values('P_value')
significant_diff = df_intake[df_intake['Significant'] == 'Yes']
print(f"  - 유의한 차이가 있는 식품군: {len(significant_diff)}개")

# 6. 네트워크 통계 비교
print("\n[5단계] 네트워크 구조 비교...")

network_comparison = []

# GGM 비교
for group_name in ['MetS_Positive', 'MetS_Negative']:
    G = networks_ggm[group_name]['graph']
    network_comparison.append({
        'Network_Type': 'GGM',
        'MetS_Group': group_name.replace('_', ' '),
        'Diet_Quality': 'All',
        'Nodes': G.number_of_nodes(),
        'Edges': G.number_of_edges(),
        'Density': nx.density(G),
        'Avg_Clustering': nx.average_clustering(G),
        'Avg_Degree': sum(dict(G.degree()).values()) / G.number_of_nodes()
    })

# Co-occurrence 비교
for key, net_data in networks_cooccur.items():
    G = net_data['graph']
    parts = key.split('_')
    mets_group = f"{parts[0]} {parts[1]}"
    diet_quality = parts[2] if len(parts) > 2 else parts[1]
    
    network_comparison.append({
        'Network_Type': 'Co-occurrence',
        'MetS_Group': mets_group,
        'Diet_Quality': diet_quality,
        'Nodes': G.number_of_nodes(),
        'Edges': G.number_of_edges(),
        'Density': nx.density(G),
        'Avg_Clustering': nx.average_clustering(G),
        'Avg_Degree': sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0
    })

df_network_comp = pd.DataFrame(network_comparison)

# 7. 허브 식품 비교
print("\n[6단계] MetS 그룹별 허브 식품 분석...")

hub_comparison = {}

# GGM 허브
for group_name in ['MetS_Positive', 'MetS_Negative']:
    degree_cent = networks_ggm[group_name]['degree_cent']
    top_hubs = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
    hub_comparison[f'{group_name}_GGM'] = top_hubs

# Co-occurrence 허브
for key, net_data in networks_cooccur.items():
    degree_cent = net_data['degree_cent']
    top_hubs = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
    hub_comparison[key] = top_hubs

# 8. 결과 저장
print("\n[7단계] 결과 파일 저장...")

# CSV 파일들
df_intake.to_csv('db/processed_data/mets_food_intake_comparison.csv', index=False)
print("  ✓ mets_food_intake_comparison.csv")

df_network_comp.to_csv('db/processed_data/mets_network_comparison.csv', index=False)
print("  ✓ mets_network_comparison.csv")

# GEXF 파일들 - Co-occurrence 네트워크
for key, net_data in networks_cooccur.items():
    filename = f"db/processed_data/{key.lower()}_cooccurrence.gexf"
    nx.write_gexf(net_data['graph'], filename)
print("  ✓ MetS 층화 Co-occurrence GEXF 파일들 (4개)")

# 9. 상세 보고서 생성
print("\n[8단계] MetS 층화 분석 보고서 생성...")

report = f"""# MetS 층화 분석: 식습관 패턴의 그룹별 차이

**분석 일자:** 2025-10-26  
**데이터:** KNHANES (n={len(data):,}명)  
**목적:** MetS(+)와 MetS(-) 그룹 간 식습관 패턴의 차이 규명

---

## 📋 Executive Summary

MetS 유무에 따라 식습관 패턴이 **어떻게 다른지** 다각도로 분석했습니다:

1. **GGM 네트워크**: MetS(+)와 MetS(-) 그룹의 식품 간 조건부 독립성 비교
2. **Co-occurrence 네트워크**: 각 그룹에서 Poor/Non-Poor Diet 패턴 비교
3. **식품 섭취량**: 그룹 간 통계적 차이 검정
4. **허브 식품**: 각 그룹에서 중요한 식품군 식별

---

## 1. 샘플 특성

### 1.1 그룹 크기

| 그룹 | 인원수 | 비율 |
|------|--------|------|
| MetS(+) | {len(data_mets_pos):,}명 | {len(data_mets_pos)/len(data)*100:.1f}% |
| MetS(-) | {len(data_mets_neg):,}명 | {len(data_mets_neg)/len(data)*100:.1f}% |

### 1.2 식품 섭취량 차이

**유의한 차이가 있는 식품군 ({len(significant_diff)}개):**

"""

for idx, row in significant_diff.head(10).iterrows():
    direction = "↑" if row['Mean_Difference'] > 0 else "↓"
    report += f"- **{row['Food_Group']}** {direction}: "
    report += f"MetS(+) {row['MetS_Pos_Mean']:.2f}±{row['MetS_Pos_Std']:.2f} vs "
    report += f"MetS(-) {row['MetS_Neg_Mean']:.2f}±{row['MetS_Neg_Std']:.2f} "
    report += f"(p={row['P_value']:.4f})\n"

report += f"""

---

## 2. GGM 네트워크 비교

### 2.1 네트워크 구조 비교

| 지표 | MetS(+) | MetS(-) | 차이 |
|------|---------|---------|------|
| 엣지 수 | {networks_ggm['MetS_Positive']['graph'].number_of_edges()} | {networks_ggm['MetS_Negative']['graph'].number_of_edges()} | {networks_ggm['MetS_Positive']['graph'].number_of_edges() - networks_ggm['MetS_Negative']['graph'].number_of_edges()} |
| 밀도 | {nx.density(networks_ggm['MetS_Positive']['graph']):.3f} | {nx.density(networks_ggm['MetS_Negative']['graph']):.3f} | {nx.density(networks_ggm['MetS_Positive']['graph']) - nx.density(networks_ggm['MetS_Negative']['graph']):.3f} |
| 평균 클러스터링 | {nx.average_clustering(networks_ggm['MetS_Positive']['graph']):.3f} | {nx.average_clustering(networks_ggm['MetS_Negative']['graph']):.3f} | {nx.average_clustering(networks_ggm['MetS_Positive']['graph']) - nx.average_clustering(networks_ggm['MetS_Negative']['graph']):.3f} |

### 2.2 허브 식품군 비교

**MetS(+) 그룹 (GGM 상위 5개):**
"""

for rank, (food, cent) in enumerate(hub_comparison['MetS_Positive_GGM'], 1):
    report += f"{rank}. {food}: {cent:.3f}\n"

report += f"""

**MetS(-) 그룹 (GGM 상위 5개):**
"""

for rank, (food, cent) in enumerate(hub_comparison['MetS_Negative_GGM'], 1):
    report += f"{rank}. {food}: {cent:.3f}\n"

report += f"""

### 2.3 해석

"""

ggm_pos = networks_ggm['MetS_Positive']['graph']
ggm_neg = networks_ggm['MetS_Negative']['graph']
density_diff = nx.density(ggm_pos) - nx.density(ggm_neg)

if density_diff > 0:
    report += f"- MetS(+) 그룹의 네트워크가 **더 조밀함** (밀도 차이: +{density_diff:.3f})\n"
    report += "- 식품 간 상호작용이 더 복잡하게 얽혀있음\n"
    report += "- 특정 식품 개선 시 다른 식품에 미치는 영향이 더 클 수 있음\n"
else:
    report += f"- MetS(-) 그룹의 네트워크가 더 조밀함 (밀도 차이: {density_diff:.3f})\n"

report += f"""

---

## 3. Co-occurrence 네트워크 비교

### 3.1 Poor Diet 패턴 비교

| 지표 | MetS(+) Poor | MetS(-) Poor | 차이 |
|------|-------------|-------------|------|
| 엣지 수 | {networks_cooccur['MetS_Positive_Poor']['graph'].number_of_edges()} | {networks_cooccur['MetS_Negative_Poor']['graph'].number_of_edges()} | {networks_cooccur['MetS_Positive_Poor']['graph'].number_of_edges() - networks_cooccur['MetS_Negative_Poor']['graph'].number_of_edges()} |
| 밀도 | {nx.density(networks_cooccur['MetS_Positive_Poor']['graph']):.3f} | {nx.density(networks_cooccur['MetS_Negative_Poor']['graph']):.3f} | {nx.density(networks_cooccur['MetS_Positive_Poor']['graph']) - nx.density(networks_cooccur['MetS_Negative_Poor']['graph']):.3f} |

**MetS(+) 그룹의 Poor Diet 허브 (상위 5개):**
"""

if len(hub_comparison['MetS_Positive_Poor']) > 0:
    for rank, (food, cent) in enumerate(hub_comparison['MetS_Positive_Poor'], 1):
        report += f"{rank}. {food}: {cent:.3f}\n"
else:
    report += "(네트워크가 너무 희소하여 허브 식별 불가)\n"

report += f"""

**MetS(-) 그룹의 Poor Diet 허브 (상위 5개):**
"""

if len(hub_comparison['MetS_Negative_Poor']) > 0:
    for rank, (food, cent) in enumerate(hub_comparison['MetS_Negative_Poor'], 1):
        report += f"{rank}. {food}: {cent:.3f}\n"
else:
    report += "(네트워크가 너무 희소하여 허브 식별 불가)\n"

report += f"""

### 3.2 Non-Poor Diet 패턴 비교

| 지표 | MetS(+) NonPoor | MetS(-) NonPoor | 차이 |
|------|----------------|----------------|------|
| 엣지 수 | {networks_cooccur['MetS_Positive_NonPoor']['graph'].number_of_edges()} | {networks_cooccur['MetS_Negative_NonPoor']['graph'].number_of_edges()} | {networks_cooccur['MetS_Positive_NonPoor']['graph'].number_of_edges() - networks_cooccur['MetS_Negative_NonPoor']['graph'].number_of_edges()} |
| 밀도 | {nx.density(networks_cooccur['MetS_Positive_NonPoor']['graph']):.3f} | {nx.density(networks_cooccur['MetS_Negative_NonPoor']['graph']):.3f} | {nx.density(networks_cooccur['MetS_Positive_NonPoor']['graph']) - nx.density(networks_cooccur['MetS_Negative_NonPoor']['graph']):.3f} |

**MetS(+) 그룹의 Non-Poor Diet 허브 (상위 5개):**
"""

if len(hub_comparison['MetS_Positive_NonPoor']) > 0:
    for rank, (food, cent) in enumerate(hub_comparison['MetS_Positive_NonPoor'], 1):
        report += f"{rank}. {food}: {cent:.3f}\n"
else:
    report += "(네트워크가 너무 희소하여 허브 식별 불가)\n"

report += f"""

**MetS(-) 그룹의 Non-Poor Diet 허브 (상위 5개):**
"""

if len(hub_comparison['MetS_Negative_NonPoor']) > 0:
    for rank, (food, cent) in enumerate(hub_comparison['MetS_Negative_NonPoor'], 1):
        report += f"{rank}. {food}: {cent:.3f}\n"
else:
    report += "(네트워크가 너무 희소하여 허브 식별 불가)\n"

report += f"""

---

## 4. 종합 네트워크 비교표

| Network Type | MetS Group | Diet Quality | Nodes | Edges | Density | Avg Clustering | Avg Degree |
|-------------|-----------|--------------|-------|-------|---------|----------------|------------|
"""

for _, row in df_network_comp.iterrows():
    report += f"| {row['Network_Type']} | {row['MetS_Group']} | {row['Diet_Quality']} | {row['Nodes']} | {row['Edges']} | {row['Density']:.3f} | {row['Avg_Clustering']:.3f} | {row['Avg_Degree']:.2f} |\n"

report += f"""

---

## 5. 주요 발견사항

### 5.1 식품 섭취량 차이

"""

# 섭취량이 높은 식품과 낮은 식품
higher_in_mets = df_intake[df_intake['Mean_Difference'] > 0].sort_values('Mean_Difference', ascending=False)
lower_in_mets = df_intake[df_intake['Mean_Difference'] < 0].sort_values('Mean_Difference')

report += f"**MetS(+) 그룹에서 더 많이 섭취하는 식품:**\n"
for idx, row in higher_in_mets.head(5).iterrows():
    if row['Significant'] == 'Yes':
        report += f"- {row['Food_Group']} (+{row['Mean_Difference']:.2f}, p={row['P_value']:.4f}) *\n"
    else:
        report += f"- {row['Food_Group']} (+{row['Mean_Difference']:.2f}, p={row['P_value']:.4f})\n"

report += f"\n**MetS(+) 그룹에서 더 적게 섭취하는 식품:**\n"
for idx, row in lower_in_mets.head(5).iterrows():
    if row['Significant'] == 'Yes':
        report += f"- {row['Food_Group']} ({row['Mean_Difference']:.2f}, p={row['P_value']:.4f}) *\n"
    else:
        report += f"- {row['Food_Group']} ({row['Mean_Difference']:.2f}, p={row['P_value']:.4f})\n"

report += "\n(*: p < 0.05 유의함)\n"

report += f"""

### 5.2 네트워크 구조 차이

"""

# GGM 네트워크 밀도 비교
ggm_pos_density = nx.density(networks_ggm['MetS_Positive']['graph'])
ggm_neg_density = nx.density(networks_ggm['MetS_Negative']['graph'])

report += f"""
1. **GGM 네트워크**:
   - MetS(+): 밀도 {ggm_pos_density:.3f}, {networks_ggm['MetS_Positive']['graph'].number_of_edges()} 엣지
   - MetS(-): 밀도 {ggm_neg_density:.3f}, {networks_ggm['MetS_Negative']['graph'].number_of_edges()} 엣지
   - {'MetS(+) 그룹이 더 복잡한 식습관 네트워크를 보임' if ggm_pos_density > ggm_neg_density else 'MetS(-) 그룹이 더 복잡한 식습관 네트워크를 보임'}

2. **Co-occurrence 네트워크**:
"""

# Co-occurrence 비교
for diet_type in ['Poor', 'NonPoor']:
    pos_key = f'MetS_Positive_{diet_type}'
    neg_key = f'MetS_Negative_{diet_type}'
    
    pos_edges = networks_cooccur[pos_key]['graph'].number_of_edges()
    neg_edges = networks_cooccur[neg_key]['graph'].number_of_edges()
    
    report += f"   - {diet_type} Diet: MetS(+) {pos_edges}개 vs MetS(-) {neg_edges}개 엣지\n"

report += f"""

### 5.3 임상적 함의

1. **MetS 환자 맞춤형 영양교육**:
"""

# MetS(+)에서 더 많이 섭취하고 유의한 차이가 있는 불건강 식품
unhealthy_foods = ['Fried Foods', 'High Fat Meat', 'Processed Foods', 'Sugar-Sweetened Beverages']
target_foods = higher_in_mets[higher_in_mets['Significant'] == 'Yes']
target_foods = target_foods[target_foods['Food_Group'].isin(unhealthy_foods)]

if len(target_foods) > 0:
    report += "   - 다음 식품군 섭취 감소 집중:\n"
    for idx, row in target_foods.iterrows():
        report += f"     * {row['Food_Group']}\n"

report += f"""

2. **네트워크 기반 개입**:
   - MetS(+) 그룹의 {'복잡한' if ggm_pos_density > ggm_neg_density else '단순한'} 네트워크 구조 고려
   - 허브 식품군 우선 개입으로 연쇄 효과 기대

3. **식이 질 개선 전략**:
   - Poor diet 패턴의 그룹 간 차이를 고려한 맞춤형 접근
   - Non-poor diet 패턴 강화를 통한 예방 전략

---

## 6. 논문 작성을 위한 제안

### 6.1 Results Section 추가 내용

**"Differences in Dietary Patterns between MetS(+) and MetS(-) Groups"**

Paragraph 1: 식품 섭취량 차이
- {len(significant_diff)}개 식품군에서 유의한 차이 발견
- MetS(+) 그룹의 특징적 섭취 패턴 기술

Paragraph 2: GGM 네트워크 구조 차이
- 밀도, 클러스터링, 허브 식품 비교
- 네트워크 복잡도의 임상적 의미

Paragraph 3: Co-occurrence 패턴 차이
- Poor/Non-Poor diet 패턴의 그룹별 특성
- 동시 섭취 패턴의 차이

### 6.2 Discussion Points

1. **네트워크 구조와 MetS 위험**:
   - 식습관 네트워크의 복잡도가 대사 건강과 관련
   - 특정 식품군의 중심성이 MetS 위험에 미치는 영향

2. **그룹별 맞춤형 개입의 필요성**:
   - MetS(+) 환자는 다른 식습관 패턴을 보임
   - 일률적 영양교육보다 맞춤형 접근이 효과적

3. **예방적 관점**:
   - MetS(-) 그룹의 건강한 식습관 패턴 유지 전략
   - 고위험군의 조기 식습관 개선

---

## 📊 생성된 파일 목록

### 데이터 파일 (CSV)
1. `mets_food_intake_comparison.csv` - MetS 그룹별 식품 섭취량 비교
2. `mets_network_comparison.csv` - 네트워크 구조 비교

### 네트워크 파일 (GEXF)
1. `mets_positive_poor_cooccurrence.gexf` - MetS(+) Poor Diet
2. `mets_positive_nonpoor_cooccurrence.gexf` - MetS(+) Non-Poor Diet
3. `mets_negative_poor_cooccurrence.gexf` - MetS(-) Poor Diet
4. `mets_negative_nonpoor_cooccurrence.gexf` - MetS(-) Non-Poor Diet

---

**분석 완료 일시**: 2025-10-26  
**분석자**: AI-Assisted Network Analysis System  
**버전**: 3.0 (MetS 층화 분석)
"""

with open('result/MetS층화분석_최종보고서.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"  ✓ MetS층화분석_최종보고서.md ({len(report)/1024:.1f} KB)")

print("\n" + "=" * 80)
print("✅ MetS 층화 분석 완료!")
print("=" * 80)
print(f"\n생성된 파일:")
print(f"  📄 result/MetS층화분석_최종보고서.md ({len(report)/1024:.1f} KB)")
print(f"  📊 db/processed_data/mets_food_intake_comparison.csv")
print(f"  📊 db/processed_data/mets_network_comparison.csv")
print(f"  🔗 db/processed_data/*_cooccurrence.gexf (4개)")
print("\n웹 서버에서 다운로드 가능합니다!")
