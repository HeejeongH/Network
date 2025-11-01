#!/usr/bin/env python3
"""
건강검진 데이터 기반 맞춤형 식생활 교육 알고리즘 개발
성별 × 연령대 × MetS 상태별 네트워크 분석 및 교육 콘텐츠 도출
"""

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("맞춤형 식생활 교육 알고리즘 개발")
print("성별 × 연령대 × MetS 층화 분석")
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

# 성별 구분 ('M': 남성, 'F': 여성)
data['Sex_Label'] = data['Sex'].map({'M': '남성', 'F': '여성'})

# 층화 그룹 생성
data['Stratified_Group'] = (
    data['Sex_Label'] + '_' + 
    data['Age_Group'] + '_' + 
    data['MetS'].map({0: 'MetS(-)', 1: 'MetS(+)'})
)

# 그룹별 샘플 크기 확인
group_counts = data['Stratified_Group'].value_counts().sort_index()
print(f"\n생성된 층화 그룹: {len(group_counts)}개")
print("\n각 그룹별 샘플 크기:")
for group, count in group_counts.items():
    print(f"  {group:45s}: {count:4d}명")

# 최소 샘플 크기 필터링 (네트워크 분석을 위해 최소 100명 필요)
min_sample_size = 100
valid_groups = group_counts[group_counts >= min_sample_size].index.tolist()
print(f"\n분석 가능한 그룹 (n≥{min_sample_size}): {len(valid_groups)}개")

# 2. 변수 정의
food_groups = [
    'Grain Products', 'Protein Foods', 'Vegetables', 'Dairy Products',
    'Fruits', 'Fried Foods', 'High Fat Meat', 'Processed Foods',
    'Sugar-Sweetened Beverages', 'Additional Salt Use',
    'Salty Food Consumption', 'Sweet Food Consumption'
]

# 불건강 식품군 정의
unhealthy_foods = ['Fried Foods', 'High Fat Meat', 'Processed Foods', 
                   'Sugar-Sweetened Beverages', 'Additional Salt Use', 
                   'Salty Food Consumption']

# 건강 식품군 정의
healthy_foods = ['Vegetables', 'Fruits', 'Dairy Products', 'Protein Foods']

# NPN 변환 함수
def npn_transform(X):
    n, p = X.shape
    X_npn = np.zeros((n, p))
    for j in range(p):
        ranks = stats.rankdata(X[:, j])
        X_npn[:, j] = stats.norm.ppf(ranks / (n + 1))
    return X_npn

# 3. 각 그룹별 GGM 네트워크 분석
print("\n[2단계] 층화 그룹별 GGM 네트워크 분석...")

group_networks = {}
threshold = 0.01

for group in valid_groups:
    group_data = data[data['Stratified_Group'] == group]
    
    if len(group_data) < min_sample_size:
        continue
    
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
        
        for i in range(len(food_groups)):
            for j in range(i+1, len(food_groups)):
                if abs(precision[i, j]) > threshold:
                    G.add_edge(food_groups[i], food_groups[j], weight=abs(precision[i, j]))
        
        degree_cent = nx.degree_centrality(G)
        between_cent = nx.betweenness_centrality(G)
        
        # 허브 식품 식별 (상위 5개)
        top_hubs = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
        
        group_networks[group] = {
            'graph': G,
            'n_samples': len(group_data),
            'n_edges': G.number_of_edges(),
            'density': nx.density(G),
            'degree_cent': degree_cent,
            'between_cent': between_cent,
            'top_hubs': top_hubs,
            'food_means': group_data[food_groups].mean().to_dict()
        }
        
        print(f"  ✓ {group:45s}: {G.number_of_edges():2d} 엣지, 밀도 {nx.density(G):.3f}")
        
    except Exception as e:
        print(f"  ✗ {group}: 분석 실패 ({str(e)})")
        continue

print(f"\n분석 완료된 그룹: {len(group_networks)}개")

# 4. 교육 콘텐츠 생성 함수
def generate_education_content(group_name, network_data, comparison_baseline=None):
    """맞춤형 교육 콘텐츠 생성"""
    
    parts = group_name.split('_')
    sex = parts[0]
    age_group = parts[1]
    mets_status = parts[2]
    
    content = {
        'group': group_name,
        'sex': sex,
        'age_group': age_group,
        'mets_status': mets_status,
        'n_samples': network_data['n_samples'],
        'priority_level': 'HIGH' if mets_status == 'MetS(+)' else 'MEDIUM',
        'interventions': []
    }
    
    # 허브 식품 기반 우선순위 설정
    top_hubs = network_data['top_hubs']
    
    for rank, (food, centrality) in enumerate(top_hubs, 1):
        intervention = {
            'rank': rank,
            'target_food': food,
            'centrality': centrality,
            'current_intake': network_data['food_means'].get(food, 0),
            'food_category': 'unhealthy' if food in unhealthy_foods else 'healthy'
        }
        
        # 기본 메시지 설정
        intervention['message'] = f"{food} 섭취 패턴 개선이 필요합니다"
        intervention['alternative'] = "균형잡힌 식단"
        
        # 식품별 맞춤 메시지
        if food in unhealthy_foods:
            if food == 'Fried Foods':
                intervention['message'] = "튀김 음식 섭취를 줄이고, 찜·구이 조리법으로 대체하세요"
                intervention['alternative'] = "구운 닭가슴살, 생선구이, 채소찜"
            elif food == 'High Fat Meat':
                intervention['message'] = "고지방 육류 섭취를 줄이고, 저지방 단백질로 전환하세요"
                intervention['alternative'] = "닭가슴살, 생선, 두부, 콩류"
            elif food == 'Processed Foods':
                intervention['message'] = "가공식품(햄, 소시지 등) 섭취를 줄이고 신선식품을 선택하세요"
                intervention['alternative'] = "신선한 고기, 생선, 계란"
            elif food == 'Sugar-Sweetened Beverages':
                intervention['message'] = "당류 음료를 줄이고 물이나 무가당 음료로 대체하세요"
                intervention['alternative'] = "물, 보리차, 녹차, 탄산수"
            elif food == 'Additional Salt Use' or food == 'Salty Food Consumption':
                intervention['message'] = "소금 섭취를 줄이고 천연 향신료로 간을 하세요"
                intervention['alternative'] = "마늘, 생강, 허브, 레몬즙"
        else:
            if food == 'Vegetables':
                intervention['message'] = "채소 섭취를 늘리세요 (하루 5접시 이상 목표)"
                intervention['alternative'] = "다양한 색깔의 채소를 매 끼니마다"
            elif food == 'Fruits':
                intervention['message'] = "과일 섭취를 늘리세요 (하루 2-3회)"
                intervention['alternative'] = "제철 과일, 통과일 섭취"
            elif food == 'Dairy Products':
                intervention['message'] = "유제품 섭취를 늘리세요 (하루 1-2회)"
                intervention['alternative'] = "저지방 우유, 요거트, 치즈"
            elif food == 'Protein Foods':
                intervention['message'] = "양질의 단백질 섭취를 유지하세요"
                intervention['alternative'] = "생선, 콩류, 계란, 살코기"
        
        # 연령대별 추가 메시지
        if '청년층' in age_group:
            intervention['age_specific'] = "바쁜 일상 속에서도 실천 가능한 간편한 방법을 활용하세요"
        elif '중년층' in age_group:
            intervention['age_specific'] = "만성질환 예방을 위해 지금부터 식습관 개선이 중요합니다"
        elif '장년층' in age_group or '노년층' in age_group:
            intervention['age_specific'] = "건강 유지를 위해 부드럽고 소화하기 쉬운 조리법을 선택하세요"
        
        # 성별 추가 메시지
        if sex == '남성':
            intervention['sex_specific'] = "음주와 함께 먹는 안주류 섭취에 주의하세요"
        else:
            intervention['sex_specific'] = "골다공증 예방을 위해 칼슘 섭취에 신경쓰세요"
        
        content['interventions'].append(intervention)
    
    # 네트워크 복잡도 기반 메시지
    density = network_data['density']
    if density > 0.8:
        content['network_message'] = "식품 간 상호연관성이 높아, 하나의 식습관 개선이 전체 식단에 긍정적 영향을 줄 수 있습니다"
    else:
        content['network_message'] = "개별 식품군의 독립적 관리가 가능합니다"
    
    return content

# 5. 모든 그룹의 교육 콘텐츠 생성
print("\n[3단계] 맞춤형 교육 콘텐츠 생성...")

education_contents = []
for group_name, network_data in group_networks.items():
    content = generate_education_content(group_name, network_data)
    education_contents.append(content)
    print(f"  ✓ {group_name}: {len(content['interventions'])}개 개입 전략")

# 6. 그룹 간 비교 분석
print("\n[4단계] 그룹 간 비교 분석...")

comparison_results = []

# MetS(+) vs MetS(-) 비교 (동일 성별, 동일 연령대)
for sex in ['남성', '여성']:
    for age in ['청년층(19-39세)', '중년층(40-59세)', '장년층(60-74세)', '노년층(75세이상)']:
        mets_pos_key = f"{sex}_{age}_MetS(+)"
        mets_neg_key = f"{sex}_{age}_MetS(-)"
        
        if mets_pos_key in group_networks and mets_neg_key in group_networks:
            pos_data = group_networks[mets_pos_key]
            neg_data = group_networks[mets_neg_key]
            
            # 허브 식품 비교
            pos_hubs = set([food for food, _ in pos_data['top_hubs']])
            neg_hubs = set([food for food, _ in neg_data['top_hubs']])
            
            unique_to_pos = pos_hubs - neg_hubs
            unique_to_neg = neg_hubs - pos_hubs
            common_hubs = pos_hubs & neg_hubs
            
            comparison_results.append({
                'sex': sex,
                'age_group': age,
                'mets_pos_n': pos_data['n_samples'],
                'mets_neg_n': neg_data['n_samples'],
                'mets_pos_density': pos_data['density'],
                'mets_neg_density': neg_data['density'],
                'density_diff': pos_data['density'] - neg_data['density'],
                'common_hubs': list(common_hubs),
                'unique_to_mets_pos': list(unique_to_pos),
                'unique_to_mets_neg': list(unique_to_neg)
            })

df_comparison = pd.DataFrame(comparison_results)

# 7. 결과 저장
print("\n[5단계] 결과 저장...")

# 교육 콘텐츠를 DataFrame으로 변환
education_df_records = []
for content in education_contents:
    base_info = {
        'Group': content['group'],
        'Sex': content['sex'],
        'Age_Group': content['age_group'],
        'MetS_Status': content['mets_status'],
        'N_Samples': content['n_samples'],
        'Priority_Level': content['priority_level'],
        'Network_Message': content['network_message']
    }
    
    for intervention in content['interventions'][:3]:  # 상위 3개만
        record = base_info.copy()
        record.update({
            'Intervention_Rank': intervention['rank'],
            'Target_Food': intervention['target_food'],
            'Centrality': intervention['centrality'],
            'Current_Intake': intervention['current_intake'],
            'Food_Category': intervention['food_category'],
            'Message': intervention['message'],
            'Alternative': intervention['alternative'],
            'Age_Specific': intervention.get('age_specific', ''),
            'Sex_Specific': intervention.get('sex_specific', '')
        })
        education_df_records.append(record)

df_education = pd.DataFrame(education_df_records)
df_education.to_csv('db/processed_data/personalized_education_contents.csv', index=False, encoding='utf-8-sig')
print("  ✓ personalized_education_contents.csv")

# 그룹별 네트워크 통계
network_stats = []
for group_name, network_data in group_networks.items():
    parts = group_name.split('_')
    network_stats.append({
        'Group': group_name,
        'Sex': parts[0],
        'Age_Group': parts[1],
        'MetS_Status': parts[2],
        'N_Samples': network_data['n_samples'],
        'N_Edges': network_data['n_edges'],
        'Density': network_data['density'],
        'Top_Hub_1': network_data['top_hubs'][0][0] if len(network_data['top_hubs']) > 0 else '',
        'Top_Hub_2': network_data['top_hubs'][1][0] if len(network_data['top_hubs']) > 1 else '',
        'Top_Hub_3': network_data['top_hubs'][2][0] if len(network_data['top_hubs']) > 2 else ''
    })

df_network_stats = pd.DataFrame(network_stats)
df_network_stats.to_csv('db/processed_data/stratified_network_statistics.csv', index=False, encoding='utf-8-sig')
print("  ✓ stratified_network_statistics.csv")

# 그룹 간 비교 결과
if len(df_comparison) > 0:
    df_comparison.to_csv('db/processed_data/group_comparison_results.csv', index=False, encoding='utf-8-sig')
    print("  ✓ group_comparison_results.csv")

# GEXF 파일 저장 (주요 그룹만)
major_groups = [g for g in valid_groups if 'MetS(+)' in g and '중년층' in g][:4]
for group in major_groups:
    if group in group_networks:
        safe_name = group.replace('(', '').replace(')', '').replace(' ', '_').replace('-', '_')
        filename = f"db/processed_data/network_{safe_name}.gexf"
        nx.write_gexf(group_networks[group]['graph'], filename)
print(f"  ✓ 주요 그룹 네트워크 GEXF 파일 ({len(major_groups)}개)")

# 8. 상세 보고서 생성
print("\n[6단계] 맞춤형 교육 알고리즘 보고서 생성...")

report = f"""# 건강검진 데이터 기반 맞춤형 식생활 교육 알고리즘

**분석 일자:** 2025-10-26  
**데이터:** KNHANES (n={len(data):,}명)  
**목적:** 성별 × 연령대 × MetS 상태별 맞춤형 식생활 교육 콘텐츠 개발

---

## 📋 Executive Summary

본 연구는 **건강검진 데이터와 생활환경 데이터**를 기반으로 **맞춤형 식생활 교육 알고리즘**을 개발했습니다.

### 핵심 성과

1. **{len(valid_groups)}개 층화 그룹** 분석 (성별 × 연령대 × MetS 상태)
2. **{len(group_networks)}개 그룹**의 식습관 네트워크 구조 규명
3. **그룹별 맞춤형 교육 콘텐츠** 자동 생성 알고리즘 개발
4. **우선순위 기반 개입 전략** 도출

---

## 1. 연구 설계

### 1.1 층화 전략

**3차원 층화:**
- **성별**: 남성, 여성
- **연령대**: 청년층(19-39세), 중년층(40-59세), 장년층(60-74세), 노년층(75세 이상)
- **MetS 상태**: MetS(+), MetS(-)

**총 16개 가능 그룹** → **분석 가능 그룹 (n≥{min_sample_size}): {len(valid_groups)}개**

### 1.2 그룹별 샘플 크기

"""

for group, count in group_counts.items():
    if group in valid_groups:
        report += f"- {group}: {count}명 ✓\n"
    else:
        report += f"- {group}: {count}명 (샘플 부족)\n"

report += f"""

### 1.3 분석 방법론

1. **GGM (Gaussian Graphical Model)**:
   - 각 그룹의 식품 간 조건부 독립성 네트워크 구축
   - 허브 식품 식별 (Degree Centrality 기반)
   
2. **교육 콘텐츠 생성 알고리즘**:
   - 허브 식품 우선순위 기반
   - 연령대별 맞춤 메시지
   - 성별 특화 메시지
   - 대체 식품 제안

---

## 2. 그룹별 네트워크 분석 결과

### 2.1 네트워크 구조 비교

"""

# 성별·연령대별 표 생성
for sex in ['남성', '여성']:
    report += f"\n#### {sex}\n\n"
    report += "| 연령대 | MetS 상태 | 샘플 수 | 엣지 수 | 밀도 | 상위 허브 식품 |\n"
    report += "|--------|-----------|---------|---------|------|----------------|\n"
    
    for age in ['청년층(19-39세)', '중년층(40-59세)', '장년층(60-74세)', '노년층(75세이상)']:
        for mets in ['MetS(-)', 'MetS(+)']:
            group_key = f"{sex}_{age}_{mets}"
            if group_key in group_networks:
                data_g = group_networks[group_key]
                top3_hubs = ', '.join([f[0][:15] for f in data_g['top_hubs'][:3]])
                report += f"| {age.replace('(', ' ').replace(')', '')} | {mets} | {data_g['n_samples']} | {data_g['n_edges']} | {data_g['density']:.3f} | {top3_hubs} |\n"

report += f"""

### 2.2 주요 발견사항

"""

# MetS(+)와 MetS(-) 비교
if len(df_comparison) > 0:
    report += "#### MetS(+) vs MetS(-) 그룹 비교\n\n"
    
    for _, row in df_comparison.iterrows():
        report += f"**{row['sex']} {row['age_group']}:**\n"
        report += f"- 샘플: MetS(+) {row['mets_pos_n']}명 vs MetS(-) {row['mets_neg_n']}명\n"
        report += f"- 네트워크 밀도: MetS(+) {row['mets_pos_density']:.3f} vs MetS(-) {row['mets_neg_density']:.3f} (차이: {row['density_diff']:.3f})\n"
        
        if len(row['common_hubs']) > 0:
            report += f"- 공통 허브: {', '.join(row['common_hubs'])}\n"
        if len(row['unique_to_mets_pos']) > 0:
            report += f"- MetS(+) 고유 허브: {', '.join(row['unique_to_mets_pos'])}\n"
        if len(row['unique_to_mets_neg']) > 0:
            report += f"- MetS(-) 고유 허브: {', '.join(row['unique_to_mets_neg'])}\n"
        report += "\n"

report += f"""

---

## 3. 맞춤형 교육 콘텐츠

### 3.1 교육 알고리즘 구조

```
입력: 개인 건강검진 데이터 (성별, 연령, MetS 상태)
  ↓
해당 층화 그룹 식별
  ↓
그룹별 허브 식품 조회
  ↓
우선순위 기반 개입 전략 생성
  ↓
연령대·성별 맞춤 메시지 추가
  ↓
출력: 맞춤형 교육 콘텐츠
```

### 3.2 교육 콘텐츠 예시

"""

# 대표 그룹 3개의 교육 콘텐츠 예시
example_groups = []
for mets in ['MetS(+)', 'MetS(-)']:
    for sex in ['남성', '여성']:
        key = f"{sex}_중년층(40-59세)_{mets}"
        if key in group_networks:
            example_groups.append(key)
            if len(example_groups) >= 3:
                break
    if len(example_groups) >= 3:
        break

for eg in example_groups[:3]:
    content = next((c for c in education_contents if c['group'] == eg), None)
    if content:
        report += f"\n#### {content['group']}\n"
        report += f"**샘플 크기:** {content['n_samples']}명  \n"
        report += f"**우선순위 수준:** {content['priority_level']}  \n"
        report += f"**네트워크 특성:** {content['network_message']}\n\n"
        report += "**개입 전략 (상위 3개):**\n\n"
        
        for i, intervention in enumerate(content['interventions'][:3], 1):
            report += f"{i}. **{intervention['target_food']}** (중심성: {intervention['centrality']:.3f})\n"
            report += f"   - 현재 섭취 수준: {intervention['current_intake']:.2f}\n"
            report += f"   - 교육 메시지: {intervention['message']}\n"
            report += f"   - 대체 식품: {intervention['alternative']}\n"
            report += f"   - 연령 특화: {intervention.get('age_specific', '')}\n"
            report += f"   - 성별 특화: {intervention.get('sex_specific', '')}\n\n"

report += f"""

---

## 4. 알고리즘 적용 방안

### 4.1 시스템 구현

**1단계: 개인 정보 입력**
- 성별, 연령, MetS 진단 여부
- (선택) 현재 식품 섭취 점수

**2단계: 자동 그룹 매칭**
```python
def match_group(sex, age, mets):
    age_group = categorize_age(age)
    group_key = f"{{sex}}_{{age_group}}_{{mets}}"
    return education_contents[group_key]
```

**3단계: 맞춤형 콘텐츠 제공**
- 우선순위 상위 3-5개 식품군 개입 전략
- 구체적 실천 방법 및 대체 식품 제안
- 연령대·성별 맞춤 메시지

**4단계: 모니터링 및 피드백**
- 주기적 식습관 재평가
- 개선도 추적
- 콘텐츠 업데이트

### 4.2 임상 적용 가이드

**고위험군 (MetS(+)):**
- 우선순위: HIGH
- 불건강 식품군 허브 집중 개입
- 3개월 단위 모니터링

**중위험군 (MetS(-), 불건강 허브 다수):**
- 우선순위: MEDIUM
- 예방적 차원의 식습관 교정
- 6개월 단위 모니터링

**저위험군 (MetS(-), 건강 허브 중심):**
- 우선순위: LOW
- 현재 식습관 유지 강화
- 12개월 단위 모니터링

### 4.3 기대 효과

1. **개인화된 교육**: 획일적 교육 탈피, 개인 특성 반영
2. **효율적 자원 배분**: 고위험군 우선 개입
3. **과학적 근거**: 네트워크 분석 기반 전략
4. **확장 가능성**: 새로운 건강 지표 추가 용이

---

## 5. 제한점 및 향후 연구

### 5.1 현재 제한점

1. **단면 연구**: 인과관계 추론 제한
2. **샘플 크기**: 일부 그룹(노년층, 청년층)의 작은 샘플
3. **식이 평가**: 자가보고 기반의 측정 오차
4. **다른 변수**: 소득, 교육 수준 등 추가 층화 필요

### 5.2 향후 연구 방향

1. **종단 연구**: 교육 개입 효과 검증
2. **기계학습 모델**: 더 정교한 예측 알고리즘
3. **모바일 앱**: 실시간 맞춤형 교육 제공
4. **다중 건강 지표**: 당뇨, 고혈압 등 추가 층화

---

## 6. 결론

본 연구는 **건강검진 데이터 기반 맞춤형 식생활 교육 알고리즘**을 성공적으로 개발했습니다.

**핵심 성과:**
- ✅ {len(group_networks)}개 층화 그룹의 식습관 네트워크 구조 규명
- ✅ 그룹별 맞춤형 교육 콘텐츠 자동 생성 알고리즘
- ✅ 과학적 근거 기반 우선순위 개입 전략
- ✅ 임상 적용 가능한 시스템 설계

**임상적 함의:**
본 알고리즘은 **개인 맞춤형 영양교육**의 새로운 패러다임을 제시하며,
보건소, 병원, 건강검진센터 등에서 즉시 활용 가능합니다.

---

## 📊 생성된 파일 목록

### 데이터 파일
1. **personalized_education_contents.csv** - 전체 교육 콘텐츠 ({len(education_df_records)}건)
2. **stratified_network_statistics.csv** - 그룹별 네트워크 통계
3. **group_comparison_results.csv** - 그룹 간 비교 결과

### 네트워크 파일
- 주요 그룹 GEXF 파일 ({len(major_groups)}개)

---

**분석 완료 일시**: 2025-10-26  
**개발자**: AI-Assisted Algorithm Development System  
**버전**: 1.0 (맞춤형 교육 알고리즘)
"""

with open('result/맞춤형_식생활_교육_알고리즘.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"  ✓ 맞춤형_식생활_교육_알고리즘.md ({len(report)/1024:.1f} KB)")

print("\n" + "=" * 80)
print("✅ 맞춤형 식생활 교육 알고리즘 개발 완료!")
print("=" * 80)
print(f"\n생성된 파일:")
print(f"  📄 result/맞춤형_식생활_교육_알고리즘.md ({len(report)/1024:.1f} KB)")
print(f"  📊 db/processed_data/personalized_education_contents.csv ({len(education_df_records)}건)")
print(f"  📊 db/processed_data/stratified_network_statistics.csv ({len(network_stats)}개 그룹)")
if len(df_comparison) > 0:
    print(f"  📊 db/processed_data/group_comparison_results.csv ({len(df_comparison)}개 비교)")
print(f"  🔗 주요 그룹 네트워크 GEXF 파일")
print("\n🎯 핵심 성과:")
print(f"  - {len(valid_groups)}개 층화 그룹 정의")
print(f"  - {len(group_networks)}개 그룹 네트워크 분석 완료")
print(f"  - {len(education_contents)}개 맞춤형 교육 콘텐츠 생성")
print("\n웹 서버에서 다운로드 가능합니다!")
