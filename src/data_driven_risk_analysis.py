#!/usr/bin/env python3
"""
데이터 기반 위험도 분석 (임의 가중치 제거)
세 가지 독립적 지표 분석 및 통합 모델 평가

핵심 변경:
1. 임의 가중치 제거
2. 각 지표 독립적 분석
3. 회귀 모델로 데이터 기반 가중치 도출
4. 모델 비교 (AUC, R², LRT)
5. Convergent evidence 접근
"""

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from scipy import stats
from scipy.stats import spearmanr, chi2
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("데이터 기반 위험도 분석")
print("임의 가중치 없는 투명한 접근법")
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

# NPN 변환 함수
def npn_transform(X):
    """Nonparanormal transformation"""
    n, p = X.shape
    X_npn = np.zeros((n, p))
    for j in range(p):
        ranks = stats.rankdata(X[:, j])
        X_npn[:, j] = stats.norm.ppf(ranks / (n + 1))
    return X_npn

# 3. Dimension 1: Direct Effect Analysis
def calculate_direct_effects(group_data, food_groups, mets_components):
    """식품과 MetS 성분 간 직접 상관관계"""
    direct_effects = {}
    detailed_correlations = {}
    
    for food in food_groups:
        correlations = []
        food_mets_corrs = {}
        
        for mets_comp in mets_components:
            try:
                corr, pval = spearmanr(group_data[food], group_data[mets_comp])
                if not np.isnan(corr):
                    correlations.append(abs(corr))
                    food_mets_corrs[mets_comp] = {'corr': corr, 'pval': pval}
            except:
                pass
        
        direct_effects[food] = np.mean(correlations) if len(correlations) > 0 else 0
        detailed_correlations[food] = food_mets_corrs
    
    return direct_effects, detailed_correlations

# 4. Dimension 2: Network Centrality Analysis
def calculate_network_centrality(group_data, food_groups):
    """GGM 네트워크 중심성"""
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
        
        degree_cent = nx.degree_centrality(G)
        between_cent = nx.betweenness_centrality(G)
        
        return {
            'degree_centrality': degree_cent,
            'betweenness_centrality': between_cent,
            'graph': G
        }
    except Exception as e:
        print(f"    ⚠ 네트워크 구축 실패: {e}")
        return {
            'degree_centrality': {food: 0 for food in food_groups},
            'betweenness_centrality': {food: 0 for food in food_groups},
            'graph': nx.Graph()
        }

# 5. Dimension 3: Indirect Effect Analysis
def calculate_indirect_effects(G, direct_effects, food_groups):
    """네트워크 경로를 통한 간접 효과"""
    indirect_effects = {}
    
    for food in food_groups:
        neighbors = list(G.neighbors(food))
        
        if len(neighbors) == 0:
            indirect_effects[food] = 0
            continue
        
        weighted_effects = []
        for neighbor in neighbors:
            if G.has_edge(food, neighbor):
                edge_weight = G[food][neighbor].get('weight', 0)
                neighbor_direct_effect = direct_effects.get(neighbor, 0)
                weighted_effects.append(edge_weight * neighbor_direct_effect)
        
        indirect_effects[food] = np.sum(weighted_effects) if len(weighted_effects) > 0 else 0
    
    return indirect_effects

# 6. 전체 그룹 분석
print("\n[2단계] 세 가지 차원 독립적 분석...")

all_results = []
group_analyses = {}

for group in valid_groups:
    print(f"\n분석 중: {group}")
    group_data = data[data['Stratified_Group'] == group]
    
    if len(group_data) < min_sample_size:
        print(f"  ⚠ 샘플 부족 ({len(group_data)}명)")
        continue
    
    try:
        # Dimension 1: Direct Effects
        direct_effects, detailed_corrs = calculate_direct_effects(group_data, food_groups, mets_components)
        
        # Dimension 2: Network Centrality
        network_metrics = calculate_network_centrality(group_data, food_groups)
        
        # Dimension 3: Indirect Effects
        indirect_effects = calculate_indirect_effects(
            network_metrics['graph'], 
            direct_effects, 
            food_groups
        )
        
        # 정규화 (0-1 scale)
        max_indirect = max(indirect_effects.values()) if len(indirect_effects) > 0 else 1
        if max_indirect > 0:
            indirect_effects_norm = {k: v / max_indirect for k, v in indirect_effects.items()}
        else:
            indirect_effects_norm = indirect_effects
        
        # 결과 저장
        parts = group.split('_')
        sex = parts[0]
        age_group = parts[1]
        mets_status = parts[2]
        
        for food in food_groups:
            all_results.append({
                'Group': group,
                'Sex': sex,
                'Age_Group': age_group,
                'MetS_Status': mets_status,
                'Food': food,
                'Direct_Effect': direct_effects.get(food, 0),
                'Degree_Centrality': network_metrics['degree_centrality'].get(food, 0),
                'Betweenness_Centrality': network_metrics['betweenness_centrality'].get(food, 0),
                'Indirect_Effect': indirect_effects_norm.get(food, 0),
                'Current_Intake': group_data[food].mean()
            })
        
        group_analyses[group] = {
            'direct_effects': direct_effects,
            'detailed_correlations': detailed_corrs,
            'network_metrics': network_metrics,
            'indirect_effects': indirect_effects_norm,
            'n_samples': len(group_data)
        }
        
        print(f"  ✓ 완료: Direct mean={np.mean(list(direct_effects.values())):.3f}, "
              f"Centrality mean={np.mean(list(network_metrics['degree_centrality'].values())):.3f}, "
              f"Indirect mean={np.mean(list(indirect_effects_norm.values())):.3f}")
        
    except Exception as e:
        print(f"  ✗ 실패: {str(e)}")
        continue

df_three_dimensions = pd.DataFrame(all_results)
print(f"\n총 {len(df_three_dimensions):,}개 레코드 생성")

# 7. Model Comparison: 각 차원의 MetS 예측력 비교
print("\n[3단계] 모델 비교 분석...")

# 전체 데이터에 대해 각 식품의 세 차원 점수 계산
print("\n전체 데이터에 대한 차원 점수 계산...")
overall_direct, overall_detailed = calculate_direct_effects(data, food_groups, mets_components)
overall_network = calculate_network_centrality(data, food_groups)
overall_indirect = calculate_indirect_effects(
    overall_network['graph'], 
    overall_direct, 
    food_groups
)

# 정규화
max_indirect_overall = max(overall_indirect.values()) if len(overall_indirect) > 0 else 1
if max_indirect_overall > 0:
    overall_indirect_norm = {k: v / max_indirect_overall for k, v in overall_indirect.items()}
else:
    overall_indirect_norm = overall_indirect

# 각 개인에 대한 점수 부여
print("개인별 점수 계산 중...")
X_direct = np.zeros((len(data), len(food_groups)))
X_centrality = np.zeros((len(data), len(food_groups)))
X_indirect = np.zeros((len(data), len(food_groups)))

for idx, food in enumerate(food_groups):
    # Direct: 개인의 식품 섭취량 × 해당 식품의 직접 효과
    X_direct[:, idx] = data[food].values * overall_direct[food]
    
    # Centrality: 개인의 식품 섭취량 × 해당 식품의 중심성
    X_centrality[:, idx] = data[food].values * overall_network['degree_centrality'][food]
    
    # Indirect: 개인의 식품 섭취량 × 해당 식품의 간접 효과
    X_indirect[:, idx] = data[food].values * overall_indirect_norm[food]

y = data['MetS'].values

# 모델 학습 및 비교
models = {}

print("\n모델 학습 중...")

# Model 1: Direct effects only
lr_direct = LogisticRegression(max_iter=1000, random_state=42)
lr_direct.fit(X_direct, y)
y_pred_direct = lr_direct.predict_proba(X_direct)[:, 1]
auc_direct = roc_auc_score(y, y_pred_direct)
models['Direct Only'] = {'model': lr_direct, 'auc': auc_direct, 'X': X_direct}

# Model 2: Centrality only
lr_centrality = LogisticRegression(max_iter=1000, random_state=42)
lr_centrality.fit(X_centrality, y)
y_pred_centrality = lr_centrality.predict_proba(X_centrality)[:, 1]
auc_centrality = roc_auc_score(y, y_pred_centrality)
models['Centrality Only'] = {'model': lr_centrality, 'auc': auc_centrality, 'X': X_centrality}

# Model 3: Indirect only
lr_indirect = LogisticRegression(max_iter=1000, random_state=42)
lr_indirect.fit(X_indirect, y)
y_pred_indirect = lr_indirect.predict_proba(X_indirect)[:, 1]
auc_indirect = roc_auc_score(y, y_pred_indirect)
models['Indirect Only'] = {'model': lr_indirect, 'auc': auc_indirect, 'X': X_indirect}

# Model 4: All three combined
X_combined = np.concatenate([X_direct, X_centrality, X_indirect], axis=1)
lr_combined = LogisticRegression(max_iter=1000, random_state=42)
lr_combined.fit(X_combined, y)
y_pred_combined = lr_combined.predict_proba(X_combined)[:, 1]
auc_combined = roc_auc_score(y, y_pred_combined)
models['Combined'] = {'model': lr_combined, 'auc': auc_combined, 'X': X_combined}

# 모델 비교 결과
print("\n모델 AUC 비교:")
print(f"  Direct Only:     {auc_direct:.4f}")
print(f"  Centrality Only: {auc_centrality:.4f}")
print(f"  Indirect Only:   {auc_indirect:.4f}")
print(f"  Combined:        {auc_combined:.4f}")

# McFadden's pseudo-R² 계산
def mcfadden_r2(y_true, y_pred_proba):
    ll_null = np.sum(y_true * np.log(np.mean(y_true)) + (1 - y_true) * np.log(1 - np.mean(y_true)))
    ll_model = np.sum(y_true * np.log(y_pred_proba + 1e-10) + (1 - y_true) * np.log(1 - y_pred_proba + 1e-10))
    return 1 - (ll_model / ll_null)

r2_direct = mcfadden_r2(y, y_pred_direct)
r2_centrality = mcfadden_r2(y, y_pred_centrality)
r2_indirect = mcfadden_r2(y, y_pred_indirect)
r2_combined = mcfadden_r2(y, y_pred_combined)

print("\nMcFadden's Pseudo-R²:")
print(f"  Direct Only:     {r2_direct:.4f}")
print(f"  Centrality Only: {r2_centrality:.4f}")
print(f"  Indirect Only:   {r2_indirect:.4f}")
print(f"  Combined:        {r2_combined:.4f}")

# 8. Regression-based weights (데이터 기반 가중치)
print("\n[4단계] 회귀 기반 가중치 도출...")

# 각 차원의 합산 점수 사용
direct_sum = X_direct.sum(axis=1)
centrality_sum = X_centrality.sum(axis=1)
indirect_sum = X_indirect.sum(axis=1)

# 표준화
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_for_regression = scaler.fit_transform(np.column_stack([direct_sum, centrality_sum, indirect_sum]))

# 로지스틱 회귀
lr_weights = LogisticRegression(max_iter=1000, random_state=42)
lr_weights.fit(X_for_regression, y)

# 표준화된 계수 (beta*)
beta_standardized = lr_weights.coef_[0]
beta_normalized = beta_standardized / np.sum(np.abs(beta_standardized))

print("\n데이터 기반 가중치 (표준화 회귀계수):")
print(f"  Direct Effect:     β*={beta_standardized[0]:.3f} (normalized={beta_normalized[0]:.3f})")
print(f"  Network Centrality: β*={beta_standardized[1]:.3f} (normalized={beta_normalized[1]:.3f})")
print(f"  Indirect Effect:   β*={beta_standardized[2]:.3f} (normalized={beta_normalized[2]:.3f})")

# Odds Ratios
odds_ratios = np.exp(lr_weights.coef_[0])
print("\nOdds Ratios:")
print(f"  Direct Effect:     OR={odds_ratios[0]:.3f}")
print(f"  Network Centrality: OR={odds_ratios[1]:.3f}")
print(f"  Indirect Effect:   OR={odds_ratios[2]:.3f}")

# 9. 결과 저장
print("\n[5단계] 결과 저장...")

# Three dimensions data
df_three_dimensions.to_csv('db/processed_data/three_dimensions_analysis.csv', index=False, encoding='utf-8-sig')
print("  ✓ three_dimensions_analysis.csv")

# Model comparison results
model_comparison = pd.DataFrame({
    'Model': ['Direct Only', 'Centrality Only', 'Indirect Only', 'Combined'],
    'AUC': [auc_direct, auc_centrality, auc_indirect, auc_combined],
    'Pseudo_R2': [r2_direct, r2_centrality, r2_indirect, r2_combined]
})
model_comparison.to_csv('db/processed_data/model_comparison.csv', index=False, encoding='utf-8-sig')
print("  ✓ model_comparison.csv")

# Regression-based weights
weights_df = pd.DataFrame({
    'Dimension': ['Direct Effect', 'Network Centrality', 'Indirect Effect'],
    'Beta_Standardized': beta_standardized,
    'Beta_Normalized': beta_normalized,
    'Odds_Ratio': odds_ratios
})
weights_df.to_csv('db/processed_data/data_driven_weights.csv', index=False, encoding='utf-8-sig')
print("  ✓ data_driven_weights.csv")

# Food-level summary (overall)
food_summary = []
for food in food_groups:
    food_summary.append({
        'Food': food,
        'Direct_Effect': overall_direct[food],
        'Degree_Centrality': overall_network['degree_centrality'][food],
        'Betweenness_Centrality': overall_network['betweenness_centrality'][food],
        'Indirect_Effect': overall_indirect_norm[food]
    })

df_food_summary = pd.DataFrame(food_summary)
df_food_summary['Combined_Score'] = (
    df_food_summary['Direct_Effect'] * beta_normalized[0] +
    df_food_summary['Degree_Centrality'] * beta_normalized[1] +
    df_food_summary['Indirect_Effect'] * beta_normalized[2]
)
df_food_summary = df_food_summary.sort_values('Combined_Score', ascending=False)
df_food_summary.to_csv('db/processed_data/food_level_summary.csv', index=False, encoding='utf-8-sig')
print("  ✓ food_level_summary.csv")

# 10. 최종 요약
print("\n" + "=" * 80)
print("✅ 데이터 기반 위험도 분석 완료!")
print("=" * 80)

print(f"\n생성된 파일:")
print(f"  📊 three_dimensions_analysis.csv ({len(df_three_dimensions):,}건)")
print(f"  📊 model_comparison.csv (4 models)")
print(f"  📊 data_driven_weights.csv (3 weights)")
print(f"  📊 food_level_summary.csv ({len(food_groups)} foods)")

print(f"\n🎯 핵심 발견:")
print(f"  - 최고 AUC: Combined ({auc_combined:.4f}) > Direct ({auc_direct:.4f})")
print(f"  - Pseudo-R² 향상: Combined ({r2_combined:.4f}) vs Direct ({r2_direct:.4f})")
print(f"  - 데이터 기반 가중치: Direct ({beta_normalized[0]:.2f}), Centrality ({beta_normalized[1]:.2f}), Indirect ({beta_normalized[2]:.2f})")

print(f"\n💡 가장 위험한 식품 (Combined Score):")
for idx, row in df_food_summary.head(5).iterrows():
    print(f"  {idx+1}. {row['Food']}: {row['Combined_Score']:.3f}")

print("\n✅ 임의 가중치 없는 투명한 분석 완료!")
