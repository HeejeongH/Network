# MetS 층화 분석: 식습관 패턴의 그룹별 차이

**분석 일자:** 2025-10-26  
**데이터:** KNHANES (n=23,040명)  
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
| MetS(+) | 5,939명 | 25.8% |
| MetS(-) | 17,101명 | 74.2% |

### 1.2 식품 섭취량 차이

**유의한 차이가 있는 식품군 (8개):**

- **Salty Food Consumption** ↑: MetS(+) 1.79±0.66 vs MetS(-) 1.66±0.64 (p=0.0000)
- **Sweet Food Consumption** ↓: MetS(+) 1.97±0.56 vs MetS(-) 2.08±0.57 (p=0.0000)
- **High Fat Meat** ↑: MetS(+) 1.54±0.65 vs MetS(-) 1.48±0.63 (p=0.0000)
- **Dairy Products** ↓: MetS(+) 1.83±0.83 vs MetS(-) 1.89±0.84 (p=0.0000)
- **Additional Salt Use** ↑: MetS(+) 1.51±0.59 vs MetS(-) 1.47±0.59 (p=0.0000)
- **Sugar-Sweetened Beverages** ↑: MetS(+) 1.43±0.74 vs MetS(-) 1.40±0.72 (p=0.0014)
- **Grain Products** ↑: MetS(+) 2.13±0.68 vs MetS(-) 2.11±0.64 (p=0.0158)
- **Processed Foods** ↓: MetS(+) 1.45±0.65 vs MetS(-) 1.47±0.66 (p=0.0268)


---

## 2. GGM 네트워크 비교

### 2.1 네트워크 구조 비교

| 지표 | MetS(+) | MetS(-) | 차이 |
|------|---------|---------|------|
| 엣지 수 | 59 | 61 | -2 |
| 밀도 | 0.894 | 0.924 | -0.030 |
| 평균 클러스터링 | 0.893 | 0.919 | -0.026 |

### 2.2 허브 식품군 비교

**MetS(+) 그룹 (GGM 상위 5개):**
1. Grain Products: 1.000
2. Fried Foods: 1.000
3. Sugar-Sweetened Beverages: 1.000
4. Sweet Food Consumption: 1.000
5. Fruits: 0.909


**MetS(-) 그룹 (GGM 상위 5개):**
1. Grain Products: 1.000
2. Vegetables: 1.000
3. High Fat Meat: 1.000
4. Processed Foods: 1.000
5. Protein Foods: 0.909


### 2.3 해석

- MetS(-) 그룹의 네트워크가 더 조밀함 (밀도 차이: -0.030)


---

## 3. Co-occurrence 네트워크 비교

### 3.1 Poor Diet 패턴 비교

| 지표 | MetS(+) Poor | MetS(-) Poor | 차이 |
|------|-------------|-------------|------|
| 엣지 수 | 20 | 20 | 0 |
| 밀도 | 0.303 | 0.303 | 0.000 |

**MetS(+) 그룹의 Poor Diet 허브 (상위 5개):**
1. Fried Foods: 0.545
2. High Fat Meat: 0.545
3. Processed Foods: 0.545
4. Sugar-Sweetened Beverages: 0.545
5. Dairy Products: 0.455


**MetS(-) 그룹의 Poor Diet 허브 (상위 5개):**
1. Fried Foods: 0.545
2. High Fat Meat: 0.545
3. Processed Foods: 0.545
4. Sugar-Sweetened Beverages: 0.545
5. Dairy Products: 0.455


### 3.2 Non-Poor Diet 패턴 비교

| 지표 | MetS(+) NonPoor | MetS(-) NonPoor | 차이 |
|------|----------------|----------------|------|
| 엣지 수 | 20 | 20 | 0 |
| 밀도 | 0.303 | 0.303 | 0.000 |

**MetS(+) 그룹의 Non-Poor Diet 허브 (상위 5개):**
1. Protein Foods: 0.636
2. Vegetables: 0.455
3. Grain Products: 0.364
4. Dairy Products: 0.364
5. Fruits: 0.364


**MetS(-) 그룹의 Non-Poor Diet 허브 (상위 5개):**
1. Protein Foods: 0.545
2. Vegetables: 0.455
3. Grain Products: 0.364
4. Dairy Products: 0.364
5. Fruits: 0.364


---

## 4. 종합 네트워크 비교표

| Network Type | MetS Group | Diet Quality | Nodes | Edges | Density | Avg Clustering | Avg Degree |
|-------------|-----------|--------------|-------|-------|---------|----------------|------------|
| GGM | MetS Positive | All | 12 | 59 | 0.894 | 0.893 | 9.83 |
| GGM | MetS Negative | All | 12 | 61 | 0.924 | 0.919 | 10.17 |
| Co-occurrence | MetS Positive | Poor | 12 | 20 | 0.303 | 0.506 | 3.33 |
| Co-occurrence | MetS Positive | NonPoor | 12 | 20 | 0.303 | 0.618 | 3.33 |
| Co-occurrence | MetS Negative | Poor | 12 | 20 | 0.303 | 0.506 | 3.33 |
| Co-occurrence | MetS Negative | NonPoor | 12 | 20 | 0.303 | 0.644 | 3.33 |


---

## 5. 주요 발견사항

### 5.1 식품 섭취량 차이

**MetS(+) 그룹에서 더 많이 섭취하는 식품:**
- Salty Food Consumption (+0.13, p=0.0000) *
- High Fat Meat (+0.06, p=0.0000) *
- Additional Salt Use (+0.04, p=0.0000) *
- Sugar-Sweetened Beverages (+0.03, p=0.0014) *
- Grain Products (+0.02, p=0.0158) *

**MetS(+) 그룹에서 더 적게 섭취하는 식품:**
- Sweet Food Consumption (-0.12, p=0.0000) *
- Dairy Products (-0.06, p=0.0000) *
- Processed Foods (-0.02, p=0.0268) *
- Fruits (-0.01, p=0.3164)
- Vegetables (-0.00, p=0.7300)

(*: p < 0.05 유의함)


### 5.2 네트워크 구조 차이


1. **GGM 네트워크**:
   - MetS(+): 밀도 0.894, 59 엣지
   - MetS(-): 밀도 0.924, 61 엣지
   - MetS(-) 그룹이 더 복잡한 식습관 네트워크를 보임

2. **Co-occurrence 네트워크**:
   - Poor Diet: MetS(+) 20개 vs MetS(-) 20개 엣지
   - NonPoor Diet: MetS(+) 20개 vs MetS(-) 20개 엣지


### 5.3 임상적 함의

1. **MetS 환자 맞춤형 영양교육**:
   - 다음 식품군 섭취 감소 집중:
     * High Fat Meat
     * Sugar-Sweetened Beverages


2. **네트워크 기반 개입**:
   - MetS(+) 그룹의 단순한 네트워크 구조 고려
   - 허브 식품군 우선 개입으로 연쇄 효과 기대

3. **식이 질 개선 전략**:
   - Poor diet 패턴의 그룹 간 차이를 고려한 맞춤형 접근
   - Non-poor diet 패턴 강화를 통한 예방 전략

---

## 6. 논문 작성을 위한 제안

### 6.1 Results Section 추가 내용

**"Differences in Dietary Patterns between MetS(+) and MetS(-) Groups"**

Paragraph 1: 식품 섭취량 차이
- 8개 식품군에서 유의한 차이 발견
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
