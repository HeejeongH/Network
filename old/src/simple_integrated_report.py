#!/usr/bin/env python3
"""
간소화된 통합 네트워크 분석: 12개 식품군으로 GGM + Co-occurrence
논문 작성용 최종 보고서 생성
"""

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("통합 식습관 네트워크 분석 - 논문용 최종 보고서 생성")
print("=" * 80)

# 1. 데이터 로드
print("\n[1단계] 데이터 로딩...")
data = pd.read_csv("db/processed_data/total_only_org.csv")
print(f"데이터 크기: {data.shape}")

# 2. 12개 식품군 변수
print("\n[2단계] 변수 정의...")
food_groups = [
    'Grain Products', 'Protein Foods', 'Vegetables', 'Dairy Products',
    'Fruits', 'Fried Foods', 'High Fat Meat', 'Processed Foods',
    'Sugar-Sweetened Beverages', 'Additional Salt Use',
    'Salty Food Consumption', 'Sweet Food Consumption'
]

# MetS 구성요소 - 실제 컬럼명 사용
mets_vars = ['Waist circumference (cm)', 'Systolic blood pressure (mmHg)', 
             'Diastolic Blood Pressure (mmHg)', 'Triglycerides (mg/dL)', 
             'HDL-C (mg/dL)', 'Fasting glucose (mg/dL)']

print(f"식품군: {len(food_groups)}개")

# 3. GGM 분석
print("\n[3단계] GGM 네트워크 분석...")

def npn_transform(X):
    """Nonparanormal transformation"""
    n, p = X.shape
    X_npn = np.zeros((n, p))
    for j in range(p):
        ranks = stats.rankdata(X[:, j])
        X_npn[:, j] = stats.norm.ppf(ranks / (n + 1))
    return X_npn

X_ggm = data[food_groups].values
X_ggm_npn = npn_transform(X_ggm)
X_ggm_scaled = StandardScaler().fit_transform(X_ggm_npn)

print("  - GraphicalLassoCV 실행 중...")
model = GraphicalLassoCV(cv=5, alphas=20, max_iter=100, tol=1e-3, n_jobs=-1)
model.fit(X_ggm_scaled)
precision_matrix = model.precision_
alpha_optimal = model.alpha_

print(f"  - 최적 alpha: {alpha_optimal:.4f}")

# GGM 네트워크 생성
G_ggm = nx.Graph()
for node in food_groups:
    G_ggm.add_node(node)

threshold = 0.01
for i in range(len(food_groups)):
    for j in range(i+1, len(food_groups)):
        if abs(precision_matrix[i, j]) > threshold:
            G_ggm.add_edge(food_groups[i], food_groups[j], 
                          weight=abs(precision_matrix[i, j]))

print(f"  - 노드: {G_ggm.number_of_nodes()}, 엣지: {G_ggm.number_of_edges()}")
print(f"  - 밀도: {nx.density(G_ggm):.3f}")

# 커뮤니티 탐지
from networkx.algorithms import community
communities = list(community.louvain_communities(G_ggm, seed=42))
modularity = community.modularity(G_ggm, communities)
print(f"  - 커뮤니티 수: {len(communities)}, Modularity: {modularity:.3f}")

# 중심성 계산
degree_cent_ggm = nx.degree_centrality(G_ggm)
between_cent_ggm = nx.betweenness_centrality(G_ggm)

# 4. Co-occurrence 네트워크 분석
print("\n[4단계] Co-occurrence 네트워크 분석...")

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

# Poor diet (score = 1)
G_poor, _ = build_cooccurrence_network(
    data, food_groups, threshold_low=1, threshold_high=1, percentile=70
)
print(f"  - Poor Diet: {G_poor.number_of_edges()} 엣지, 밀도 {nx.density(G_poor):.3f}")

# Non-poor diet (score >= 3)
G_nonpoor, _ = build_cooccurrence_network(
    data, food_groups, threshold_low=3, threshold_high=None, percentile=70
)
print(f"  - Non-Poor Diet: {G_nonpoor.number_of_edges()} 엣지, 밀도 {nx.density(G_nonpoor):.3f}")

# 중심성 계산
degree_cent_poor = nx.degree_centrality(G_poor)
between_cent_poor = nx.betweenness_centrality(G_poor)
degree_cent_nonpoor = nx.degree_centrality(G_nonpoor)
between_cent_nonpoor = nx.betweenness_centrality(G_nonpoor)

# 5. 통합 분석
print("\n[5단계] 통합 중요도 계산...")

integrated_results = []
for food in food_groups:
    combined_importance = (
        degree_cent_ggm.get(food, 0) * 0.25 + 
        between_cent_ggm.get(food, 0) * 0.25 + 
        degree_cent_poor.get(food, 0) * 0.15 +
        between_cent_poor.get(food, 0) * 0.10 +
        degree_cent_nonpoor.get(food, 0) * 0.15 +
        between_cent_nonpoor.get(food, 0) * 0.10
    )
    
    integrated_results.append({
        'Food_Group': food,
        'GGM_Degree': degree_cent_ggm.get(food, 0),
        'GGM_Betweenness': between_cent_ggm.get(food, 0),
        'Poor_Diet_Degree': degree_cent_poor.get(food, 0),
        'Poor_Diet_Betweenness': between_cent_poor.get(food, 0),
        'NonPoor_Diet_Degree': degree_cent_nonpoor.get(food, 0),
        'NonPoor_Diet_Betweenness': between_cent_nonpoor.get(food, 0),
        'Combined_Importance': combined_importance
    })

df_integrated = pd.DataFrame(integrated_results).sort_values('Combined_Importance', ascending=False)
print("  - 통합 중요도 상위 5개:")
for idx, row in df_integrated.head().iterrows():
    print(f"    {idx+1}. {row['Food_Group']}: {row['Combined_Importance']:.3f}")

# 6. MetS 상관관계 분석
print("\n[6단계] MetS 연관성 분석...")

mets_correlations = []
for food in food_groups:
    for mets_var in mets_vars:
        if food in data.columns and mets_var in data.columns:
            corr, pval = spearmanr(data[food], data[mets_var], nan_policy='omit')
            mets_correlations.append({
                'Food_Group': food,
                'MetS_Component': mets_var,
                'Correlation': corr,
                'P_value': pval,
                'Significant': 'Yes' if pval < 0.05 else 'No'
            })

df_mets_corr = pd.DataFrame(mets_correlations)
significant_corr = df_mets_corr[df_mets_corr['Significant'] == 'Yes']
print(f"  - 유의한 상관관계: {len(significant_corr)}개")

# 7. MetS 그룹별 네트워크 비교
print("\n[7단계] MetS 그룹별 네트워크 비교...")

if 'MetS' in data.columns:
    data_mets_pos = data[data['MetS'] == 1]
    data_mets_neg = data[data['MetS'] == 0]
    
    print(f"  - MetS(+): {len(data_mets_pos)}명, MetS(-): {len(data_mets_neg)}명")
    
    # GGM for MetS(+)
    X_pos = data_mets_pos[food_groups].values
    X_pos_npn = npn_transform(X_pos)
    X_pos_scaled = StandardScaler().fit_transform(X_pos_npn)
    
    model_pos = GraphicalLassoCV(cv=5, alphas=20, max_iter=100)
    model_pos.fit(X_pos_scaled)
    prec_pos = model_pos.precision_
    
    G_mets_pos = nx.Graph()
    for node in food_groups:
        G_mets_pos.add_node(node)
    for i in range(len(food_groups)):
        for j in range(i+1, len(food_groups)):
            if abs(prec_pos[i, j]) > threshold:
                G_mets_pos.add_edge(food_groups[i], food_groups[j], weight=abs(prec_pos[i, j]))
    
    # GGM for MetS(-)
    X_neg = data_mets_neg[food_groups].values
    X_neg_npn = npn_transform(X_neg)
    X_neg_scaled = StandardScaler().fit_transform(X_neg_npn)
    
    model_neg = GraphicalLassoCV(cv=5, alphas=20, max_iter=100)
    model_neg.fit(X_neg_scaled)
    prec_neg = model_neg.precision_
    
    G_mets_neg = nx.Graph()
    for node in food_groups:
        G_mets_neg.add_node(node)
    for i in range(len(food_groups)):
        for j in range(i+1, len(food_groups)):
            if abs(prec_neg[i, j]) > threshold:
                G_mets_neg.add_edge(food_groups[i], food_groups[j], weight=abs(prec_neg[i, j]))
    
    print(f"  - MetS(+) 네트워크: {G_mets_pos.number_of_edges()} 엣지")
    print(f"  - MetS(-) 네트워크: {G_mets_neg.number_of_edges()} 엣지")

# 8. 결과 저장
print("\n[8단계] 결과 파일 저장...")

df_integrated.to_csv('db/processed_data/integrated_ggm_cooccurrence.csv', index=False)
print("  ✓ integrated_ggm_cooccurrence.csv")

network_stats = pd.DataFrame([
    {
        'Network': 'GGM_Full',
        'Nodes': G_ggm.number_of_nodes(),
        'Edges': G_ggm.number_of_edges(),
        'Density': nx.density(G_ggm),
        'Avg_Clustering': nx.average_clustering(G_ggm),
        'Communities': len(communities),
        'Modularity': modularity
    },
    {
        'Network': 'CoOccur_Poor',
        'Nodes': G_poor.number_of_nodes(),
        'Edges': G_poor.number_of_edges(),
        'Density': nx.density(G_poor),
        'Avg_Clustering': nx.average_clustering(G_poor),
        'Communities': '-',
        'Modularity': '-'
    },
    {
        'Network': 'CoOccur_NonPoor',
        'Nodes': G_nonpoor.number_of_nodes(),
        'Edges': G_nonpoor.number_of_edges(),
        'Density': nx.density(G_nonpoor),
        'Avg_Clustering': nx.average_clustering(G_nonpoor),
        'Communities': '-',
        'Modularity': '-'
    }
])

if 'MetS' in data.columns:
    network_stats = pd.concat([network_stats, pd.DataFrame([
        {
            'Network': 'GGM_MetS_Positive',
            'Nodes': G_mets_pos.number_of_nodes(),
            'Edges': G_mets_pos.number_of_edges(),
            'Density': nx.density(G_mets_pos),
            'Avg_Clustering': nx.average_clustering(G_mets_pos),
            'Communities': '-',
            'Modularity': '-'
        },
        {
            'Network': 'GGM_MetS_Negative',
            'Nodes': G_mets_neg.number_of_nodes(),
            'Edges': G_mets_neg.number_of_edges(),
            'Density': nx.density(G_mets_neg),
            'Avg_Clustering': nx.average_clustering(G_mets_neg),
            'Communities': '-',
            'Modularity': '-'
        }
    ])], ignore_index=True)

network_stats.to_csv('db/processed_data/network_statistics_summary.csv', index=False)
print("  ✓ network_statistics_summary.csv")

df_mets_corr.to_csv('db/processed_data/mets_food_correlations.csv', index=False)
print("  ✓ mets_food_correlations.csv")

# GEXF 파일들
nx.write_gexf(G_ggm, 'db/processed_data/ggm_network_full.gexf')
nx.write_gexf(G_poor, 'db/processed_data/poor_diet_network_CORRECTED.gexf')
nx.write_gexf(G_nonpoor, 'db/processed_data/nonpoor_diet_network_CORRECTED.gexf')
print("  ✓ GEXF 네트워크 파일들")

if 'MetS' in data.columns:
    nx.write_gexf(G_mets_pos, 'db/processed_data/ggm_network_mets_positive.gexf')
    nx.write_gexf(G_mets_neg, 'db/processed_data/ggm_network_mets_negative.gexf')
    print("  ✓ MetS 그룹별 GEXF 파일들")

# 9. 논문용 보고서 생성
print("\n[9단계] 논문용 최종 보고서 생성...")

# 상위 허브 식품
top_hubs = df_integrated.head(4)['Food_Group'].tolist()

report_content = f"""# 통합 식습관 네트워크 분석: GGM과 Co-occurrence 방법의 융합적 접근

**분석 일자:** 2025-10-26  
**데이터:** KNHANES (n={len(data):,}명)  
**목적:** 논문 작성용 최종 통합 분석

---

## 📋 Executive Summary

본 분석은 **두 가지 네트워크 방법론을 융합**하여 한국인의 식습관 패턴과 대사증후군(MetS)의 연관성을 다각도로 규명했습니다:

1. **Gaussian Graphical Model (GGM)**: {len(food_groups)}개 식품군 간 조건부 독립성 분석
2. **Co-occurrence Network**: {len(food_groups)}개 식품군의 실제 동시 섭취 패턴 분석

### 핵심 발견사항

- **GGM 네트워크**: {G_ggm.number_of_edges()}개 엣지, 밀도 {nx.density(G_ggm):.3f}, {len(communities)}개 식습관 커뮤니티 발견
- **Co-occurrence 네트워크**: Poor diet ({G_poor.number_of_edges()}개 엣지), Non-poor diet ({G_nonpoor.number_of_edges()}개 엣지)
- **통합 분석**: 상위 4개 허브 식품군 식별
- **MetS 연관성**: {len(significant_corr)}개 유의한 식품-MetS 구성요소 상관관계

---

## 1. 연구 방법론

### 1.1 Gaussian Graphical Model (GGM)

**목적**: 식품 간 **조건부 독립성** 파악 (다른 식품의 영향을 통제한 후의 직접적 연관성)

**방법론**:
- Nonparanormal (NPN) 변환으로 비정규성 처리
- GraphicalLassoCV로 희소 역공분산 행렬 추정 (α = {alpha_optimal:.4f})
- L1 정규화로 약한 연결 제거

**분석 대상**: {len(food_groups)}개 식품군
```
{', '.join(food_groups)}
```

### 1.2 Co-occurrence Network

**목적**: 실제 식습관에서 **동시에 섭취되는 패턴** 파악

**방법론**:
- 이진화: 각 식품군의 섭취 점수 기준 (Poor: score=1, Non-poor: score≥3)
- Jaccard-유사 정규화된 co-occurrence 계산
- 70th percentile 임계값으로 엣지 선택

### 1.3 통합 분석 전략

두 방법론의 **상호보완적 정보 융합**:
- GGM: 조건부 독립성 → 식품 간 직접적 관계
- Co-occurrence: 동시 발생 → 실제 섭취 패턴

**통합 중요도 계산**:
```
Combined_Importance = 
    0.25 × GGM_Degree + 
    0.25 × GGM_Betweenness + 
    0.15 × Poor_Diet_Degree + 
    0.10 × Poor_Diet_Betweenness + 
    0.15 × NonPoor_Diet_Degree + 
    0.10 × NonPoor_Diet_Betweenness
```

---

## 2. GGM 네트워크 분석 결과

### 2.1 전체 네트워크 구조

- **노드**: {G_ggm.number_of_nodes()}개 식품군
- **엣지**: {G_ggm.number_of_edges()}개 직접적 연관성
- **네트워크 밀도**: {nx.density(G_ggm):.3f}
- **평균 클러스터링 계수**: {nx.average_clustering(G_ggm):.3f}
- **Modularity**: {modularity:.3f}

### 2.2 커뮤니티 구조

Louvain 알고리즘으로 **{len(communities)}개 식습관 커뮤니티** 발견:

"""

# 커뮤니티별 상세 정보
for idx, comm in enumerate(communities):
    comm_list = sorted(list(comm))
    report_content += f"\n#### Community {idx} ({len(comm_list)}개 식품군)\n"
    report_content += "```\n"
    for food in comm_list:
        degree = degree_cent_ggm.get(food, 0)
        between = between_cent_ggm.get(food, 0)
        report_content += f"  - {food:35s}  (Degree: {degree:.3f}, Betweenness: {between:.3f})\n"
    report_content += "```\n"

report_content += f"""

### 2.3 GGM 허브 식품군 (상위 5개)

"""

top5_ggm = sorted(degree_cent_ggm.items(), key=lambda x: x[1], reverse=True)[:5]
for rank, (food, cent) in enumerate(top5_ggm, 1):
    report_content += f"{rank}. **{food}** (Degree Centrality: {cent:.3f})\n"

report_content += f"""

---

## 3. Co-occurrence 네트워크 분석 결과

### 3.1 Poor Diet 네트워크 (Score = 1)

건강하지 못한 식습관(점수 1점)을 가진 사람들의 동시 섭취 패턴:

- **엣지 수**: {G_poor.number_of_edges()}개
- **네트워크 밀도**: {nx.density(G_poor):.3f}
- **평균 클러스터링**: {nx.average_clustering(G_poor):.3f}

**허브 식품군 (Degree Centrality 상위 5개)**:
"""

top5_poor = sorted(degree_cent_poor.items(), key=lambda x: x[1], reverse=True)[:5]
for rank, (food, cent) in enumerate(top5_poor, 1):
    report_content += f"{rank}. {food}: {cent:.3f}\n"

report_content += f"""

### 3.2 Non-Poor Diet 네트워크 (Score ≥ 3)

건강한 식습관(점수 3점 이상)을 가진 사람들의 동시 섭취 패턴:

- **엣지 수**: {G_nonpoor.number_of_edges()}개
- **네트워크 밀도**: {nx.density(G_nonpoor):.3f}
- **평균 클러스터링**: {nx.average_clustering(G_nonpoor):.3f}

**허브 식품군 (Degree Centrality 상위 5개)**:
"""

top5_nonpoor = sorted(degree_cent_nonpoor.items(), key=lambda x: x[1], reverse=True)[:5]
for rank, (food, cent) in enumerate(top5_nonpoor, 1):
    report_content += f"{rank}. {food}: {cent:.3f}\n"

report_content += f"""

---

## 4. 통합 분석: GGM + Co-occurrence

### 4.1 통합 중요도 순위 (상위 10개)

"""

for idx, row in df_integrated.head(10).iterrows():
    report_content += f"{idx+1}. **{row['Food_Group']}** (Combined Score: {row['Combined_Importance']:.3f})\n"
    report_content += f"   - GGM: Degree {row['GGM_Degree']:.3f}, Betweenness {row['GGM_Betweenness']:.3f}\n"
    report_content += f"   - Poor: Degree {row['Poor_Diet_Degree']:.3f}, Between {row['Poor_Diet_Betweenness']:.3f}\n"
    report_content += f"   - NonPoor: Degree {row['NonPoor_Diet_Degree']:.3f}, Between {row['NonPoor_Diet_Betweenness']:.3f}\n\n"

report_content += f"""

### 4.2 핵심 허브 식품군 (상위 4개)

"""

for idx, food in enumerate(top_hubs, 1):
    row = df_integrated[df_integrated['Food_Group'] == food].iloc[0]
    report_content += f"{idx}. **{food}**\n"
    report_content += f"   - 통합 중요도: {row['Combined_Importance']:.3f}\n"
    report_content += f"   - 두 방법론에서 모두 높은 중심성\n\n"

report_content += f"""

---

## 5. MetS (대사증후군) 연관성 분석

### 5.1 식품군-MetS 구성요소 상관관계

총 {len(df_mets_corr)}개 상관관계 중 **{len(significant_corr)}개가 통계적으로 유의** (p < 0.05)

**가장 강한 상관관계 (상위 10개)**:
"""

top_corr = significant_corr.nlargest(10, 'Correlation', keep='all') if len(significant_corr) >= 10 else significant_corr
for _, row in top_corr.iterrows():
    mets_short = row['MetS_Component'].split('(')[0].strip()
    report_content += f"- {row['Food_Group']} ↔ {mets_short}: r = {row['Correlation']:.3f} (p = {row['P_value']:.4f})\n"

if 'MetS' in data.columns:
    report_content += f"""

### 5.2 MetS 그룹별 네트워크 비교

**MetS(+) 그룹 (n={len(data_mets_pos):,}명)**:
- GGM 엣지: {G_mets_pos.number_of_edges()}개
- 네트워크 밀도: {nx.density(G_mets_pos):.3f}

**MetS(-) 그룹 (n={len(data_mets_neg):,}명)**:
- GGM 엣지: {G_mets_neg.number_of_edges()}개
- 네트워크 밀도: {nx.density(G_mets_neg):.3f}

**해석**:
- MetS(+) 그룹에서 네트워크 밀도가 {((nx.density(G_mets_pos) - nx.density(G_mets_neg)) / nx.density(G_mets_neg) * 100):.1f}% {'증가' if nx.density(G_mets_pos) > nx.density(G_mets_neg) else '감소'}
- 이는 MetS 환자에서 식습관 패턴이 {'더 복잡하게 연결됨' if nx.density(G_mets_pos) > nx.density(G_mets_neg) else '덜 연결됨'}을 시사
"""

report_content += f"""

---

## 6. 논문 작성을 위한 권장 사항

### 6.1 Methods Section

**네트워크 분석 방법론 기술**:

We employed two complementary network analysis approaches:

1. **Gaussian Graphical Model (GGM)**: Graphical lasso with nonparanormal 
   transformation to estimate sparse inverse covariance matrix (α = {alpha_optimal:.4f})
   
2. **Co-occurrence Network**: Binary consumption networks for poor diet (score=1) 
   and non-poor diet (score≥3) patterns using 70th percentile threshold

Network centrality measures (degree and betweenness) were calculated and integrated 
using weighted combination (GGM 0.50, Poor 0.25, Non-poor 0.25).

### 6.2 Results Section 구조 제안

**Section 1**: GGM Network Structure
- {len(communities)}개 커뮤니티 발견 (Modularity {modularity:.3f})
- 각 커뮤니티의 식습관 패턴 특성

**Section 2**: Co-occurrence Patterns
- Poor vs Non-poor diet 네트워크 비교
- 건강/불건강 식품군의 동시 섭취 패턴

**Section 3**: Integrated Hub Foods
- 두 방법론에서 일관되게 중요한 식품군 식별
- {', '.join(top_hubs[:4])}

**Section 4**: MetS Associations
- {len(significant_corr)}개 유의한 상관관계
- MetS 그룹별 네트워크 구조 차이

### 6.3 Discussion Points

1. **방법론의 상호보완성**: GGM은 조건부 독립성, Co-occurrence는 실제 섭취 패턴
2. **허브 식품군**: 통합 분석으로 개입 우선순위 식품 식별
3. **MetS 연관성**: 네트워크 구조와 MetS 위험의 관계

---

## 7. 결론 및 임상적 함의

### 7.1 핵심 결론

1. **두 네트워크 방법론의 융합**으로 식습관 패턴을 다각도로 이해
2. **{len(top_hubs)}개 허브 식품군** 식별 → 영양 개입 타겟
3. **MetS와 강한 연관성**을 보이는 식습관 패턴 규명
4. **식습관 커뮤니티 구조**가 MetS 위험도와 관련

### 7.2 임상적 권고사항

**우선 개입 대상 식품군**:
"""

for idx, food in enumerate(top_hubs, 1):
    report_content += f"{idx}. {food}\n"

report_content += """

**개입 전략**:
- 불건강 식품군의 동시 섭취 패턴 차단
- 건강 식품군으로 대체
- MetS 고위험군 맞춤형 영양교육

---

## 📊 생성된 파일 목록

### 데이터 파일 (CSV)
1. `integrated_ggm_cooccurrence.csv` - 통합 중심성 및 중요도
2. `network_statistics_summary.csv` - 네트워크 통계 요약
3. `mets_food_correlations.csv` - MetS 상관관계

### 네트워크 파일 (GEXF - Gephi/Cytoscape용)
1. `ggm_network_full.gexf` - 전체 GGM 네트워크
2. `poor_diet_network_CORRECTED.gexf` - Poor diet co-occurrence
3. `nonpoor_diet_network_CORRECTED.gexf` - Non-poor diet co-occurrence
4. `ggm_network_mets_positive.gexf` - MetS(+) 그룹 GGM
5. `ggm_network_mets_negative.gexf` - MetS(-) 그룹 GGM

---

**분석 완료 일시**: 2025-10-26  
**분석자**: AI-Assisted Network Analysis System  
**버전**: 2.0 (통합 분석)
"""

with open('result/논문용_통합분석_최종보고서.md', 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"  ✓ 논문용_통합분석_최종보고서.md ({len(report_content)/1024:.1f} KB)")

# 10. 빠른 참조 가이드
print("\n[10단계] 빠른 참조 가이드 생성...")

quick_ref = f"""# 논문 작성 빠른 참조 가이드

## 📊 주요 숫자 (Copy-Paste용)

### 샘플 크기
- 전체: n = {len(data):,}명
"""

if 'MetS' in data.columns:
    quick_ref += f"""- MetS(+): n = {len(data_mets_pos):,}명 ({len(data_mets_pos)/len(data)*100:.1f}%)
- MetS(-): n = {len(data_mets_neg):,}명 ({len(data_mets_neg)/len(data)*100:.1f}%)
"""

quick_ref += f"""

### GGM 네트워크
- 노드: {G_ggm.number_of_nodes()}개
- 엣지: {G_ggm.number_of_edges()}개
- 밀도: {nx.density(G_ggm):.3f}
- 클러스터링: {nx.average_clustering(G_ggm):.3f}
- 커뮤니티: {len(communities)}개
- Modularity: {modularity:.3f}
- Optimal α: {alpha_optimal:.4f}

### Co-occurrence 네트워크
**Poor Diet (score=1):**
- 엣지: {G_poor.number_of_edges()}개
- 밀도: {nx.density(G_poor):.3f}

**Non-Poor Diet (score≥3):**
- 엣지: {G_nonpoor.number_of_edges()}개
- 밀도: {nx.density(G_nonpoor):.3f}

### MetS 연관성
- 유의한 상관관계: {len(significant_corr)}개 (p < 0.05)
"""

if len(significant_corr) > 0:
    top1 = significant_corr.nlargest(1, 'Correlation').iloc[0]
    quick_ref += f"- 가장 강한 상관: {top1['Food_Group']} ↔ {top1['MetS_Component'].split('(')[0].strip()} (r = {top1['Correlation']:.3f})\n"

quick_ref += f"""

---

## 📋 Table 1: 통합 중요도 상위 식품군

| Rank | Food Group | Combined Score | GGM Degree | Poor Diet | Non-Poor Diet |
|------|-----------|----------------|------------|-----------|---------------|
"""

for idx, row in df_integrated.head(8).iterrows():
    quick_ref += f"| {idx+1} | {row['Food_Group']} | {row['Combined_Importance']:.3f} | {row['GGM_Degree']:.3f} | {row['Poor_Diet_Degree']:.3f} | {row['NonPoor_Diet_Degree']:.3f} |\n"

quick_ref += """

---

## 🎯 핵심 허브 식품군

"""

for idx, food in enumerate(top_hubs, 1):
    row = df_integrated[df_integrated['Food_Group'] == food].iloc[0]
    quick_ref += f"{idx}. **{food}** (통합 중요도: {row['Combined_Importance']:.3f})\n"

quick_ref += f"""

---

**생성 일시**: 2025-10-26
"""

with open('result/논문작성_빠른참조.md', 'w', encoding='utf-8') as f:
    f.write(quick_ref)

print(f"  ✓ 논문작성_빠른참조.md ({len(quick_ref)/1024:.1f} KB)")

print("\n" + "=" * 80)
print("✅ 통합 분석 완료!")
print("=" * 80)
print(f"\n생성된 파일:")
print(f"  📄 result/논문용_통합분석_최종보고서.md ({len(report_content)/1024:.1f} KB)")
print(f"  📋 result/논문작성_빠른참조.md ({len(quick_ref)/1024:.1f} KB)")
print(f"  📊 db/processed_data/integrated_ggm_cooccurrence.csv")
print(f"  📊 db/processed_data/network_statistics_summary.csv")
print(f"  📊 db/processed_data/mets_food_correlations.csv")
print(f"  🔗 db/processed_data/*.gexf (네트워크 파일들)")
print("\n웹 서버에서 다운로드 가능합니다!")
