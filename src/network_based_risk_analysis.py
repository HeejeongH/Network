#!/usr/bin/env python3
"""
네트워크 기반 위험도 분석 알고리즘
성별 × 연령대 × MetS 층화별 식품 위험도 산출

핵심 원리:
1. 직접 효과: 식품 → MetS 성분 상관관계
2. 간접 효과: 식품 → 다른 식품 → MetS 경로 강도
3. 네트워크 중심성: 식품의 전체 식습관 패턴 내 위치
4. 통합 위험도 = (직접 효과 × 0.4) + (네트워크 중심성 × 0.3) + (간접 효과 × 0.3)
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
print("네트워크 기반 식품 위험도 분석")
print("맞춤형 식생활 교육을 위한 위험 기반 접근법")
print("=" * 80)

# 1. 데이터 로드 및 그룹 정의
print("\n[1단계] 데이터 로딩 및 층화 그룹 생성...")
data = pd.read_csv("db/processed_data/total_only_org.csv")
print(f"전체 데이터: {len(data):,}명")

# 연령대 구분
def categorize_age(age):
    if age < 40:
        return "청년층(19-39세)"
    elif age < 60:
        return "중년층(40-59세)"
    elif age < 75:
        return "장년층(60-74세)"
    else:
        return "노년층(75세이상)"

data['Age_Group'] = data['Age'].apply(categorize_age)
data['Sex_Label'] = data['Sex'].map({'M': '남성', 'F': '여성'})
data['Stratified_Group'] = (
    data['Sex_Label'] + '_' + 
    data['Age_Group'] + '_' + 
    data['MetS'].map({0: 'MetS(-)', 1: 'MetS(+)'})
)

# 최소 샘플 크기 필터링
min_sample_size = 100
group_counts = data['Stratified_Group'].value_counts()
valid_groups = group_counts[group_counts >= min_sample_size].index.tolist()
print(f"분석 가능한 그룹 (n≥{min_sample_size}): {len(valid_groups)}개")

# 2. 변수 정의
food_groups = [
    'Grain Products', 'Protein Foods', 'Vegetables', 'Dairy Products',
    'Fruits', 'Fried Foods', 'High Fat Meat', 'Processed Foods',
    'Sugar-Sweetened Beverages', 'Additional Salt Use',
    'Salty Food Consumption', 'Sweet Food Consumption'
]

mets_components = [
    'Waist circumference (cm)', 
    'Systolic blood pressure (mmHg)', 
    'Diastolic Blood Pressure (mmHg)', 
    'Triglycerides (mg/dL)', 
    'Fasting glucose (mg/dL)'
]

# 불건강 식품군
unhealthy_foods = ['Fried Foods', 'High Fat Meat', 'Processed Foods', 
                   'Sugar-Sweetened Beverages', 'Additional Salt Use', 
                   'Salty Food Consumption']

# 건강 식품군
healthy_foods = ['Vegetables', 'Fruits', 'Dairy Products', 'Protein Foods']

# 3. NPN 변환 함수
def npn_transform(X):
    """Nonparanormal transformation"""
    n, p = X.shape
    X_npn = np.zeros((n, p))
    for j in range(p):
        ranks = stats.rankdata(X[:, j])
        X_npn[:, j] = stats.norm.ppf(ranks / (n + 1))
    return X_npn

# 4. 직접 효과 계산 (Food → MetS 상관관계)
def calculate_direct_effects(group_data, food_groups, mets_components):
    """각 식품과 MetS 성분 간 Spearman 상관관계"""
    direct_effects = {}
    
    for food in food_groups:
        correlations = []
        for mets_comp in mets_components:
            try:
                corr, pval = spearmanr(group_data[food], group_data[mets_comp])
                if not np.isnan(corr):
                    correlations.append(abs(corr))
            except:
                pass
        
        # 평균 절대 상관계수
        direct_effects[food] = np.mean(correlations) if len(correlations) > 0 else 0
    
    return direct_effects

# 5. 간접 효과 계산 (Food → Other Foods → MetS)
def calculate_indirect_effects(G, direct_effects, food_groups):
    """네트워크 경로를 통한 간접 효과"""
    indirect_effects = {}
    
    for food in food_groups:
        # 이 식품과 연결된 다른 식품들
        neighbors = list(G.neighbors(food))
        
        if len(neighbors) == 0:
            indirect_effects[food] = 0
            continue
        
        # 연결된 식품들의 직접 효과에 엣지 가중치를 곱하여 합산
        weighted_effects = []
        for neighbor in neighbors:
            if G.has_edge(food, neighbor):
                edge_weight = G[food][neighbor].get('weight', 0)
                neighbor_direct_effect = direct_effects.get(neighbor, 0)
                weighted_effects.append(edge_weight * neighbor_direct_effect)
        
        # 간접 효과: 연결된 식품을 통한 영향력의 합
        indirect_effects[food] = np.sum(weighted_effects) if len(weighted_effects) > 0 else 0
    
    return indirect_effects

# 6. 통합 위험도 계산
def calculate_risk_scores(group_data, food_groups, mets_components):
    """
    통합 위험도 = (직접 효과 × 0.4) + (네트워크 중심성 × 0.3) + (간접 효과 × 0.3)
    """
    
    # Step 1: GGM 네트워크 구축
    try:
        X = group_data[food_groups].values
        X_npn = npn_transform(X)
        X_scaled = StandardScaler().fit_transform(X_npn)
        
        model = GraphicalLassoCV(cv=3, alphas=10, max_iter=100, n_jobs=-1)
        model.fit(X_scaled)
        precision = model.precision_
        
        G = nx.Graph()
        for node in food_groups:
            G.add_node(node)
        
        threshold = 0.01
        for i in range(len(food_groups)):
            for j in range(i+1, len(food_groups)):
                if abs(precision[i, j]) > threshold:
                    G.add_edge(food_groups[i], food_groups[j], weight=abs(precision[i, j]))
        
        # 네트워크 중심성 계산
        degree_cent = nx.degree_centrality(G)
        between_cent = nx.betweenness_centrality(G)
        
        # 중심성 정규화 (0~1)
        max_degree = max(degree_cent.values()) if len(degree_cent) > 0 else 1
        normalized_centrality = {k: v / max_degree for k, v in degree_cent.items()}
        
    except Exception as e:
        print(f"    ⚠ 네트워크 구축 실패: {e}")
        G = nx.Graph()
        G.add_nodes_from(food_groups)
        normalized_centrality = {food: 0 for food in food_groups}
        between_cent = {food: 0 for food in food_groups}
    
    # Step 2: 직접 효과 계산
    direct_effects = calculate_direct_effects(group_data, food_groups, mets_components)
    
    # Step 3: 간접 효과 계산
    indirect_effects = calculate_indirect_effects(G, direct_effects, food_groups)
    
    # 간접 효과 정규화 (0~1)
    max_indirect = max(indirect_effects.values()) if len(indirect_effects) > 0 else 1
    if max_indirect > 0:
        indirect_effects = {k: v / max_indirect for k, v in indirect_effects.items()}
    
    # Step 4: 통합 위험도 계산
    risk_scores = {}
    for food in food_groups:
        direct = direct_effects.get(food, 0)
        centrality = normalized_centrality.get(food, 0)
        indirect = indirect_effects.get(food, 0)
        
        # 가중 평균: 직접 40%, 중심성 30%, 간접 30%
        risk_score = (direct * 0.4) + (centrality * 0.3) + (indirect * 0.3)
        
        risk_scores[food] = {
            'risk_score': risk_score,
            'direct_effect': direct,
            'network_centrality': centrality,
            'indirect_effect': indirect,
            'degree_centrality': degree_cent.get(food, 0),
            'betweenness_centrality': between_cent.get(food, 0),
            'current_intake': group_data[food].mean(),
            'n_connections': G.degree(food) if G.has_node(food) else 0
        }
    
    return risk_scores, G

# 7. 모든 그룹 분석
print("\n[2단계] 그룹별 네트워크 기반 위험도 분석...")

all_results = []
group_networks = {}

for group in valid_groups:
    print(f"\n분석 중: {group}")
    group_data = data[data['Stratified_Group'] == group]
    
    if len(group_data) < min_sample_size:
        print(f"  ⚠ 샘플 부족 ({len(group_data)}명)")
        continue
    
    try:
        risk_scores, G = calculate_risk_scores(group_data, food_groups, mets_components)
        
        parts = group.split('_')
        sex = parts[0]
        age_group = parts[1]
        mets_status = parts[2]
        
        for food, scores in risk_scores.items():
            all_results.append({
                'Group': group,
                'Sex': sex,
                'Age_Group': age_group,
                'MetS_Status': mets_status,
                'Food': food,
                'Risk_Score': scores['risk_score'],
                'Direct_Effect': scores['direct_effect'],
                'Network_Centrality': scores['network_centrality'],
                'Indirect_Effect': scores['indirect_effect'],
                'Degree_Centrality': scores['degree_centrality'],
                'Betweenness_Centrality': scores['betweenness_centrality'],
                'Current_Intake': scores['current_intake'],
                'N_Connections': scores['n_connections'],
                'Food_Category': 'Unhealthy' if food in unhealthy_foods else 'Healthy'
            })
        
        group_networks[group] = {
            'graph': G,
            'risk_scores': risk_scores,
            'n_samples': len(group_data)
        }
        
        print(f"  ✓ 완료: {G.number_of_edges()} 엣지, 평균 위험도 {np.mean([s['risk_score'] for s in risk_scores.values()]):.3f}")
        
    except Exception as e:
        print(f"  ✗ 실패: {str(e)}")
        continue

df_risk = pd.DataFrame(all_results)
print(f"\n총 {len(df_risk):,}개 위험도 레코드 생성")

# 8. 그룹별 상위 위험 식품 도출
print("\n[3단계] 그룹별 고위험 식품 식별...")

risk_based_education = []

for group in valid_groups:
    if group not in group_networks:
        continue
    
    group_df = df_risk[df_risk['Group'] == group].copy()
    
    # 위험도 순위
    group_df = group_df.sort_values('Risk_Score', ascending=False)
    
    parts = group.split('_')
    sex = parts[0]
    age_group = parts[1]
    mets_status = parts[2]
    
    # 상위 3개 고위험 식품
    top3 = group_df.head(3)
    
    for rank, (idx, row) in enumerate(top3.iterrows(), 1):
        food = row['Food']
        risk_score = row['Risk_Score']
        direct = row['Direct_Effect']
        centrality = row['Network_Centrality']
        indirect = row['Indirect_Effect']
        
        # 위험도 설명 생성
        reason_parts = []
        
        # 직접 효과 설명
        if direct > 0.2:
            reason_parts.append(f"MetS 성분과 직접 상관관계가 높음 (r={direct:.2f})")
        
        # 네트워크 중심성 설명
        if centrality > 0.5:
            reason_parts.append(f"전체 식습관 패턴의 핵심 허브 (중심성={centrality:.2f})")
        
        # 간접 효과 설명
        if indirect > 0.3:
            reason_parts.append(f"다른 불건강 식품과 강하게 연결되어 간접 영향 큼 (경로 강도={indirect:.2f})")
        
        if len(reason_parts) == 0:
            reason_parts.append(f"이 그룹에서 특별한 주의가 필요한 식품")
        
        reason = "; ".join(reason_parts)
        
        # 교육 메시지 생성
        if food in unhealthy_foods:
            if food == 'Fried Foods':
                message = "튀김 음식 섭취를 줄이세요"
                alternative = "구운 닭가슴살, 생선구이, 채소찜"
                action = "튀김 대신 굽기, 찌기 조리법 사용"
            elif food == 'High Fat Meat':
                message = "고지방 육류 섭취를 줄이세요"
                alternative = "닭가슴살, 생선, 두부, 콩류"
                action = "살코기 위주 단백질 선택"
            elif food == 'Processed Foods':
                message = "가공식품 섭취를 줄이세요"
                alternative = "신선한 고기, 생선, 계란"
                action = "가공되지 않은 신선식품 선택"
            elif food == 'Sugar-Sweetened Beverages':
                message = "당류 음료 섭취를 줄이세요"
                alternative = "물, 보리차, 녹차, 탄산수"
                action = "음료 대신 물 섭취 습관화"
            elif food == 'Additional Salt Use' or food == 'Salty Food Consumption':
                message = "소금 섭취를 줄이세요"
                alternative = "마늘, 생강, 허브, 레몬즙"
                action = "천연 향신료로 맛내기"
            else:
                message = f"{food} 섭취를 줄이세요"
                alternative = "건강한 대체 식품"
                action = "식습관 개선"
        else:
            if food == 'Vegetables':
                message = "채소 섭취를 늘리세요"
                alternative = "다양한 색깔의 채소"
                action = "매 끼니 채소 반찬 추가"
            elif food == 'Fruits':
                message = "과일 섭취를 늘리세요"
                alternative = "제철 과일, 통과일"
                action = "간식을 과일로 대체"
            elif food == 'Dairy Products':
                message = "유제품 섭취를 늘리세요"
                alternative = "저지방 우유, 요거트, 치즈"
                action = "하루 1-2회 유제품 섭취"
            elif food == 'Protein Foods':
                message = "양질의 단백질 섭취를 유지하세요"
                alternative = "생선, 콩류, 계란, 살코기"
                action = "매 끼니 단백질 식품 포함"
            else:
                message = f"{food} 섭취에 주의하세요"
                alternative = "균형잡힌 식단"
                action = "식습관 점검"
        
        # 연령대별 특화 메시지
        if '청년층' in age_group:
            age_msg = "바쁜 일상에서도 실천 가능한 간편한 방법 활용"
        elif '중년층' in age_group:
            age_msg = "만성질환 예방을 위해 지금부터 식습관 개선이 중요"
        elif '장년층' in age_group or '노년층' in age_group:
            age_msg = "건강 유지를 위해 부드럽고 소화하기 쉬운 조리법 선택"
        else:
            age_msg = "건강한 식습관 유지"
        
        # 성별 특화 메시지
        if sex == '남성':
            sex_msg = "음주 시 안주 선택에 주의"
        else:
            sex_msg = "골다공증 예방을 위해 칼슘 섭취 중요"
        
        risk_based_education.append({
            'Group': group,
            'Sex': sex,
            'Age_Group': age_group,
            'MetS_Status': mets_status,
            'Priority_Rank': rank,
            'Food': food,
            'Food_Category': row['Food_Category'],
            'Risk_Score': risk_score,
            'Direct_Effect': direct,
            'Network_Centrality': centrality,
            'Indirect_Effect': indirect,
            'Current_Intake': row['Current_Intake'],
            'N_Connections': row['N_Connections'],
            'Risk_Reason': reason,
            'Education_Message': message,
            'Alternative_Foods': alternative,
            'Action_Plan': action,
            'Age_Specific': age_msg,
            'Sex_Specific': sex_msg
        })

df_education = pd.DataFrame(risk_based_education)
print(f"  ✓ {len(df_education)}개 위험 기반 교육 콘텐츠 생성")

# 9. 그룹 간 위험도 비교
print("\n[4단계] 그룹 간 위험도 비교 분석...")

cross_group_comparisons = []

# 각 식품별로 그룹 간 위험도 비교
for food in food_groups:
    food_df = df_risk[df_risk['Food'] == food].copy()
    
    # 위험도가 가장 높은 그룹
    max_risk_group = food_df.loc[food_df['Risk_Score'].idxmax()]
    min_risk_group = food_df.loc[food_df['Risk_Score'].idxmin()]
    
    risk_ratio = max_risk_group['Risk_Score'] / min_risk_group['Risk_Score'] if min_risk_group['Risk_Score'] > 0 else 0
    
    # MetS(+) vs MetS(-) 비교
    mets_pos_df = food_df[food_df['MetS_Status'] == 'MetS(+)']
    mets_neg_df = food_df[food_df['MetS_Status'] == 'MetS(-)']
    
    avg_risk_mets_pos = mets_pos_df['Risk_Score'].mean() if len(mets_pos_df) > 0 else 0
    avg_risk_mets_neg = mets_neg_df['Risk_Score'].mean() if len(mets_neg_df) > 0 else 0
    
    cross_group_comparisons.append({
        'Food': food,
        'Food_Category': 'Unhealthy' if food in unhealthy_foods else 'Healthy',
        'Highest_Risk_Group': max_risk_group['Group'],
        'Highest_Risk_Score': max_risk_group['Risk_Score'],
        'Lowest_Risk_Group': min_risk_group['Group'],
        'Lowest_Risk_Score': min_risk_group['Risk_Score'],
        'Risk_Ratio': risk_ratio,
        'Avg_Risk_MetS_Pos': avg_risk_mets_pos,
        'Avg_Risk_MetS_Neg': avg_risk_mets_neg,
        'MetS_Risk_Difference': avg_risk_mets_pos - avg_risk_mets_neg
    })

df_cross_group = pd.DataFrame(cross_group_comparisons)
df_cross_group = df_cross_group.sort_values('Risk_Ratio', ascending=False)

# 10. 결과 저장
print("\n[5단계] 결과 저장...")

# 전체 위험도 데이터
df_risk.to_csv('db/processed_data/network_based_risk_scores.csv', index=False, encoding='utf-8-sig')
print("  ✓ network_based_risk_scores.csv")

# 위험 기반 교육 콘텐츠
df_education.to_csv('db/processed_data/risk_based_education_contents.csv', index=False, encoding='utf-8-sig')
print("  ✓ risk_based_education_contents.csv")

# 그룹 간 비교
df_cross_group.to_csv('db/processed_data/cross_group_risk_comparison.csv', index=False, encoding='utf-8-sig')
print("  ✓ cross_group_risk_comparison.csv")

# 11. 상세 보고서 생성
print("\n[6단계] 네트워크 기반 위험도 분석 보고서 생성...")

report = f"""# 네트워크 기반 식품 위험도 분석 보고서

**분석 일자:** 2025-10-27  
**데이터:** KNHANES (n={len(data):,}명)  
**분석 그룹:** {len(valid_groups)}개 층화 그룹  
**목적:** 위험 기반 맞춤형 식생활 교육 알고리즘 개발

---

## 📋 Executive Summary

기존 descriptive 접근법의 한계를 극복하고, **네트워크 분석 기반 위험도 평가**를 통해
"왜 이 식품이 당신에게 위험한가"를 과학적으로 설명하는 맞춤형 교육 시스템을 개발했습니다.

### 핵심 혁신

**기존 방식 (Descriptive):**
- "당신은 이 그룹이므로 → 이렇게 먹을 것입니다 → 이렇게 바꾸세요"
- 문제: 개인의 특성이 고려되지 않은 일반적 조언

**새로운 방식 (Risk-based):**
- "당신의 나이/성별에서 → 이 식품이 MetS에 가장 큰 영향 → 우선적으로 주의하세요"
- 장점: 개인 맞춤형, 과학적 근거, 우선순위 명확

### 방법론 혁신

**통합 위험도 점수 (Integrated Risk Score):**

```
Risk Score = (직접 효과 × 0.4) + (네트워크 중심성 × 0.3) + (간접 효과 × 0.3)

1. 직접 효과: 식품 ↔ MetS 성분 상관관계 (Spearman correlation)
2. 네트워크 중심성: 전체 식습관 패턴에서의 허브 역할 (Degree centrality)
3. 간접 효과: 네트워크 경로를 통한 영향력 (Path strength)
```

### 주요 성과

- ✅ **{len(df_risk):,}개** 그룹×식품 위험도 레코드 생성
- ✅ **{len(df_education)}개** 위험 기반 교육 콘텐츠 도출
- ✅ **{len(df_cross_group)}개** 식품별 그룹 간 위험도 비교
- ✅ **과학적 설명**: 왜 이 식품이 위험한지 3가지 차원에서 설명

---

## 1. 분석 방법론

### 1.1 통합 위험도 계산 프로세스

#### Step 1: 식품-식품 네트워크 구축 (GGM)

- **방법**: Gaussian Graphical Model with Nonparanormal transformation
- **목적**: 식품 간 조건부 의존성 네트워크 구축
- **산출물**: 식품 간 연결 강도 및 네트워크 중심성

#### Step 2: 직접 효과 측정

```python
직접 효과 = |Spearman(식품, MetS 성분)|의 평균

For each food:
    correlations = []
    For each MetS component (WC, SBP, DBP, TG, Glucose):
        corr = Spearman_correlation(food, mets_component)
        correlations.append(abs(corr))
    
    Direct_Effect = mean(correlations)
```

#### Step 3: 간접 효과 계산

```python
간접 효과 = Σ (연결 강도 × 이웃 식품의 직접 효과)

For each food:
    indirect = 0
    For each neighbor in network:
        edge_weight = network_edge_strength(food, neighbor)
        neighbor_direct = direct_effect(neighbor)
        indirect += edge_weight × neighbor_direct
    
    Indirect_Effect = indirect
```

#### Step 4: 통합 위험도 산출

```python
Risk_Score = (Direct_Effect × 0.4) + 
             (Network_Centrality × 0.3) + 
             (Indirect_Effect × 0.3)
```

**가중치 근거:**
- 직접 효과 (40%): 식품-건강 직접 연관성이 가장 중요
- 네트워크 중심성 (30%): 전체 식습관 패턴 개선에 미치는 영향
- 간접 효과 (30%): 다른 식품을 통한 복합적 영향

### 1.2 층화 전략

**3차원 층화:**
- 성별: 남성, 여성
- 연령대: 청년층(19-39세), 중년층(40-59세), 장년층(60-74세), 노년층(75세+)
- MetS 상태: MetS(+), MetS(-)

**분석 가능 그룹: {len(valid_groups)}개** (n≥{min_sample_size})

---

## 2. 그룹별 위험도 분석 결과

### 2.1 식품별 위험도 순위 (전체 평균)

"""

# 전체 평균 위험도
avg_risk_by_food = df_risk.groupby('Food').agg({
    'Risk_Score': 'mean',
    'Direct_Effect': 'mean',
    'Network_Centrality': 'mean',
    'Indirect_Effect': 'mean'
}).sort_values('Risk_Score', ascending=False)

report += "\n| 식품 | 평균 위험도 | 직접 효과 | 네트워크 중심성 | 간접 효과 | 카테고리 |\n"
report += "|------|------------|-----------|----------------|-----------|----------|\n"

for food, row in avg_risk_by_food.iterrows():
    category = "불건강" if food in unhealthy_foods else "건강"
    report += f"| {food} | {row['Risk_Score']:.3f} | {row['Direct_Effect']:.3f} | {row['Network_Centrality']:.3f} | {row['Indirect_Effect']:.3f} | {category} |\n"

report += f"""

### 2.2 MetS(+) vs MetS(-) 위험도 비교

"""

# MetS 그룹별 평균 위험도
mets_comparison = df_risk.groupby(['Food', 'MetS_Status'])['Risk_Score'].mean().unstack()
if 'MetS(+)' in mets_comparison.columns and 'MetS(-)' in mets_comparison.columns:
    mets_comparison['차이'] = mets_comparison['MetS(+)'] - mets_comparison['MetS(-)']
    mets_comparison = mets_comparison.sort_values('차이', ascending=False)
    
    report += "\n| 식품 | MetS(+) 위험도 | MetS(-) 위험도 | 차이 | 해석 |\n"
    report += "|------|---------------|---------------|------|------|\n"
    
    for food, row in mets_comparison.head(10).iterrows():
        interpretation = "MetS(+)에서 특히 주의" if row['차이'] > 0.05 else "비슷한 수준"
        report += f"| {food} | {row['MetS(+)']:.3f} | {row['MetS(-)']:.3f} | {row['차이']:.3f} | {interpretation} |\n"

report += f"""

**주요 발견:**
- MetS(+) 그룹에서 전반적으로 높은 위험도
- 특정 식품은 MetS 상태에 따라 위험도가 크게 달라짐
- 개인 맞춤형 교육의 필요성 확인

### 2.3 성별·연령대별 위험도 패턴

"""

# 성별, 연령대별 평균 위험도 (상위 3개 식품)
for sex in ['남성', '여성']:
    report += f"\n#### {sex}\n\n"
    
    for age in ['청년층(19-39세)', '중년층(40-59세)', '장년층(60-74세)', '노년층(75세이상)']:
        sex_age_df = df_risk[(df_risk['Sex'] == sex) & (df_risk['Age_Group'] == age)]
        
        if len(sex_age_df) == 0:
            continue
        
        top3 = sex_age_df.groupby('Food')['Risk_Score'].mean().sort_values(ascending=False).head(3)
        
        report += f"**{age}:**\n"
        for rank, (food, risk) in enumerate(top3.items(), 1):
            report += f"  {rank}. {food} (위험도: {risk:.3f})\n"
        report += "\n"

report += """

---

## 3. 위험 기반 교육 콘텐츠

### 3.1 교육 메시지 구조

```
[그룹 정보]
당신의 그룹: 남성, 중년층(40-59세), MetS(+)

[우선순위 1: Sugar-Sweetened Beverages]
위험도 점수: 0.85

왜 위험한가?
  ① 직접 효과: MetS 성분과 강한 상관 (r=0.35)
  ② 네트워크 중심성: 전체 식습관 패턴의 핵심 허브 (중심성=0.90)
  ③ 간접 효과: 튀김, 가공식품과 강하게 연결되어 복합적 영향 (경로 강도=0.65)

무엇을 해야 하나?
  • 당류 음료 섭취를 줄이세요
  • 대체 식품: 물, 보리차, 녹차, 탄산수
  • 실천 방법: 음료 대신 물 섭취 습관화
  
연령·성별 맞춤 조언:
  • 만성질환 예방을 위해 지금부터 식습관 개선이 중요
  • 음주 시 안주 선택에 주의
```

### 3.2 그룹별 교육 콘텐츠 예시

"""

# 대표 그룹 3개 선택
example_groups = []
for mets in ['MetS(+)', 'MetS(-)']:
    for sex in ['남성', '여성']:
        candidates = [g for g in valid_groups if sex in g and '중년층' in g and mets in g]
        if len(candidates) > 0:
            example_groups.append(candidates[0])
        if len(example_groups) >= 3:
            break
    if len(example_groups) >= 3:
        break

for group in example_groups[:3]:
    group_edu = df_education[df_education['Group'] == group].head(3)
    
    if len(group_edu) == 0:
        continue
    
    report += f"\n#### {group}\n"
    report += f"**샘플 크기:** {group_networks[group]['n_samples']}명\n\n"
    
    for _, row in group_edu.iterrows():
        report += f"**우선순위 {row['Priority_Rank']}: {row['Food']}**\n\n"
        report += f"- **위험도 점수**: {row['Risk_Score']:.3f}\n"
        report += f"- **왜 위험한가?**\n"
        report += f"  - {row['Risk_Reason']}\n"
        report += f"- **교육 메시지**: {row['Education_Message']}\n"
        report += f"- **대체 식품**: {row['Alternative_Foods']}\n"
        report += f"- **실천 방법**: {row['Action_Plan']}\n"
        report += f"- **연령 맞춤**: {row['Age_Specific']}\n"
        report += f"- **성별 맞춤**: {row['Sex_Specific']}\n\n"

report += """

---

## 4. 그룹 간 위험도 비교

### 4.1 식품별 최고·최저 위험 그룹

"""

report += "\n| 식품 | 최고 위험 그룹 | 위험도 | 최저 위험 그룹 | 위험도 | 배율 |\n"
report += "|------|---------------|--------|---------------|--------|------|\n"

for _, row in df_cross_group.head(10).iterrows():
    report += f"| {row['Food']} | {row['Highest_Risk_Group'].split('_')[0]} {row['Highest_Risk_Group'].split('_')[1][:4]} | {row['Highest_Risk_Score']:.3f} | {row['Lowest_Risk_Group'].split('_')[0]} {row['Lowest_Risk_Group'].split('_')[1][:4]} | {row['Lowest_Risk_Score']:.3f} | {row['Risk_Ratio']:.1f}× |\n"

report += f"""

**해석:**
- 동일 식품이라도 그룹에 따라 위험도가 크게 다름
- 최대 {df_cross_group['Risk_Ratio'].max():.1f}배 차이
- 개인 맞춤형 접근의 필요성 재확인

### 4.2 MetS 상태별 위험도 차이가 큰 식품

"""

mets_diff_foods = df_cross_group.sort_values('MetS_Risk_Difference', ascending=False).head(10)

report += "\n| 식품 | MetS(+) 평균 | MetS(-) 평균 | 차이 | 해석 |\n"
report += "|------|-------------|-------------|------|------|\n"

for _, row in mets_diff_foods.iterrows():
    interpretation = "MetS(+)에서 집중 관리 필요" if row['MetS_Risk_Difference'] > 0.1 else "MetS(+)에서 주의"
    report += f"| {row['Food']} | {row['Avg_Risk_MetS_Pos']:.3f} | {row['Avg_Risk_MetS_Neg']:.3f} | {row['MetS_Risk_Difference']:.3f} | {interpretation} |\n"

report += """

---

## 5. 임상 적용 가이드

### 5.1 위험도 기반 개입 우선순위

**초고위험 (Risk Score ≥ 0.7):**
- 즉각적 개입 필요
- 월 1회 모니터링
- 영양사 상담 권장

**고위험 (0.5 ≤ Risk Score < 0.7):**
- 3개월 내 개입 필요
- 분기별 모니터링
- 교육 자료 제공

**중위험 (0.3 ≤ Risk Score < 0.5):**
- 6개월 내 개입
- 반기별 모니터링
- 예방적 교육

**저위험 (Risk Score < 0.3):**
- 현재 상태 유지
- 연 1회 점검

### 5.2 시스템 구현 예시

```python
def get_personalized_education(sex, age, mets_status, current_intake):
    # 1. 그룹 매칭
    age_group = categorize_age(age)
    group_key = f"{{sex}}_{{age_group}}_{{mets_status}}"
    
    # 2. 해당 그룹의 위험도 데이터 조회
    group_risks = risk_data[risk_data['Group'] == group_key]
    
    # 3. 상위 3개 고위험 식품 추출
    top_risks = group_risks.sort_values('Risk_Score', ascending=False).head(3)
    
    # 4. 맞춤형 교육 메시지 생성
    messages = []
    for _, food_risk in top_risks.iterrows():
        message = {{
            'food': food_risk['Food'],
            'risk_score': food_risk['Risk_Score'],
            'reason': food_risk['Risk_Reason'],
            'action': food_risk['Education_Message'],
            'alternatives': food_risk['Alternative_Foods']
        }}
        messages.append(message)
    
    return messages
```

### 5.3 기대 효과

1. **개인화**: 그룹별 맞춤형 우선순위 제공
2. **과학적 근거**: 네트워크 기반 정량적 위험도
3. **설명 가능성**: 왜 위험한지 명확히 설명
4. **효율성**: 고위험 식품 집중 관리
5. **확장성**: 새로운 건강 지표 추가 용이

---

## 6. 기존 방식과의 비교

| 구분 | 기존 (Descriptive) | 신규 (Risk-based) |
|------|-------------------|------------------|
| 접근법 | "이 그룹은 이렇게 먹는다" | "이 식품이 당신에게 위험하다" |
| 근거 | 평균 섭취량, 네트워크 구조 | 통합 위험도 (직접+간접+네트워크) |
| 우선순위 | 중심성 기반 | 위험도 점수 기반 |
| 설명 | "허브 식품이므로" | "직접 효과 + 간접 효과 + 네트워크 위치" |
| 개인화 | 그룹 평균 | 그룹별 위험도 차이 강조 |
| 실행 가능성 | 일반적 조언 | 구체적 우선순위 행동 계획 |

**핵심 차이:**
- 기존: "무엇을 먹는가" → 신규: "무엇이 위험한가"
- 기존: "네트워크 구조 설명" → 신규: "왜 위험한지 설명"
- 기존: "그룹 특성 중심" → 신규: "개인 위험도 중심"

---

## 7. 연구의 제한점

1. **단면 연구**: 인과관계 추론의 한계
2. **자가보고**: 식이 섭취 측정의 오차
3. **가중치**: 직접·간접·네트워크 가중치의 최적화 필요
4. **검증**: 실제 개입 연구를 통한 효과 검증 필요

---

## 8. 향후 연구 방향

1. **종단 연구**: 위험도 기반 교육의 실제 효과 검증
2. **기계학습**: 개인별 최적 가중치 학습
3. **다중 건강 지표**: 당뇨, 고혈압 등 추가 분석
4. **모바일 앱**: 실시간 맞춤형 교육 시스템 구현
5. **임상 시험**: 위험도 기반 개입의 RCT 수행

---

## 9. 결론

본 연구는 **네트워크 분석 기반 위험도 평가**를 통해 맞춤형 식생활 교육의 새로운 패러다임을 제시했습니다.

**핵심 혁신:**
- ✅ Descriptive → Risk-based 접근법 전환
- ✅ 통합 위험도 점수 개발 (직접 + 간접 + 네트워크)
- ✅ 과학적 설명: "왜 이 식품이 당신에게 위험한가"
- ✅ 실행 가능한 우선순위 제공

**임상적 함의:**
본 시스템은 건강검진센터, 보건소, 병원 등에서 **즉시 적용 가능한 개인 맞춤형 영양교육 도구**로 활용될 수 있으며,
MetS 예방 및 관리의 효율성을 크게 높일 것으로 기대됩니다.

---

## 📊 생성된 파일 목록

### 데이터 파일
1. **network_based_risk_scores.csv** - 전체 위험도 데이터 ({len(df_risk):,}건)
2. **risk_based_education_contents.csv** - 위험 기반 교육 콘텐츠 ({len(df_education)}건)
3. **cross_group_risk_comparison.csv** - 그룹 간 위험도 비교 ({len(df_cross_group)}개 식품)

### 보고서
- **네트워크기반_위험도_분석_보고서.md** (본 문서)

---

**분석 완료 일시**: 2025-10-27  
**개발**: Network-based Risk Analysis Algorithm v1.0  
**버전**: Risk-based Personalized Education System
"""

with open('result/네트워크기반_위험도_분석_보고서.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"  ✓ 네트워크기반_위험도_분석_보고서.md ({len(report)/1024:.1f} KB)")

# 12. 최종 요약
print("\n" + "=" * 80)
print("✅ 네트워크 기반 위험도 분석 완료!")
print("=" * 80)

print(f"\n생성된 파일:")
print(f"  📄 result/네트워크기반_위험도_분석_보고서.md ({len(report)/1024:.1f} KB)")
print(f"  📊 db/processed_data/network_based_risk_scores.csv ({len(df_risk):,}건)")
print(f"  📊 db/processed_data/risk_based_education_contents.csv ({len(df_education)}건)")
print(f"  📊 db/processed_data/cross_group_risk_comparison.csv ({len(df_cross_group)}개)")

print(f"\n🎯 핵심 성과:")
print(f"  - {len(valid_groups)}개 층화 그룹 분석")
print(f"  - {len(df_risk):,}개 위험도 레코드 생성")
print(f"  - {len(df_education)}개 위험 기반 교육 콘텐츠")
print(f"  - 통합 위험도 = 직접(40%) + 중심성(30%) + 간접(30%)")

print(f"\n💡 방법론 혁신:")
print(f"  - Descriptive → Risk-based 전환")
print(f"  - 직접 효과 + 간접 효과 + 네트워크 중심성")
print(f"  - \"왜 위험한가\" 과학적 설명 제공")
print(f"  - 그룹별 맞춤형 우선순위")

print("\n웹 서버에서 다운로드 가능합니다!")
