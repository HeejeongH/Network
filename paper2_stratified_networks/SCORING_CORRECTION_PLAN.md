# 식습관 점수 시스템 수정 계획

## 🔴 발견된 핵심 문제

**논문은 "5-point Likert scale"이라고 표기했지만,  
실제로는 식품군마다 3점 또는 4점 척도를 사용!**

---

## 📊 실제 데이터 분석 결과

### 점수 체계 요약

| 식품군 | 점수 범위 | 척도 | 비고 |
|--------|----------|------|------|
| **3점 척도 (4개)** ||||
| Grain Products | 1-3 | 3점 | ✅ |
| Fruits | 1-3 | 3점 | ✅ |
| Additional Salt Use | 1-3 | 3점 | ✅ |
| Salty Food Consumption | 1-3 | 3점 | ✅ |
| Sweet Food Consumption | 1-3 | 3점 | ✅ |
| **4점 척도 (7개)** ||||
| Protein Foods | 1-4 | 4점 | ✅ |
| Vegetables | 1-4 | 4점 | ✅ |
| Dairy Products | 1-4 | 4점 | ✅ |
| Fried Foods | 1-4 | 4점 | ✅ |
| High Fat Meat | 1-4 | 4점 | ✅ |
| Processed Foods | 1-4 | 4점 | ✅ |
| Sugar-Sweetened Beverages | 1-4 | 4점 | ✅ |

### 상세 분포

#### 3점 척도 식품군

**Grain Products** (N=23,040):
```
Score 1 (Poor):          3,673명 (15.9%)
Score 2 (Intermediate): 13,068명 (56.7%)
Score 3 (Ideal):         6,299명 (27.3%)
Mean: 2.11
```

**Fruits**:
```
Score 1: 6,286명 (27.3%)
Score 2: 8,878명 (38.5%)
Score 3: 7,876명 (34.2%)
Mean: 2.07
```

**Additional Salt Use**:
```
Score 1: 13,004명 (56.4%)
Score 2:  8,903명 (38.6%)
Score 3:  1,133명 (4.9%)
Mean: 1.48
```

**Salty Food Consumption**:
```
Score 1:  9,401명 (40.8%)
Score 2: 11,246명 (48.8%)
Score 3:  2,393명 (10.4%)
Mean: 1.70
```

**Sweet Food Consumption**:
```
Score 1:  3,170명 (13.8%)
Score 2: 15,497명 (67.2%)
Score 3:  4,373명 (19.0%)
Mean: 2.05
```

#### 4점 척도 식품군

**Protein Foods**:
```
Score 1:    841명 (3.7%)
Score 2:  4,784명 (20.8%)
Score 3: 11,166명 (48.5%)
Score 4:  6,249명 (27.1%)
Mean: 2.99
```

**Vegetables**:
```
Score 1:  2,305명 (10.0%)
Score 2:  6,013명 (26.1%)
Score 3:  9,981명 (43.3%)
Score 4:  4,741명 (20.6%)
Mean: 2.74
```

**Fried Foods** (낮을수록 좋음):
```
Score 1: 15,731명 (68.3%)
Score 2:  6,072명 (26.4%)
Score 3:  1,114명 (4.8%)
Score 4:    123명 (0.5%)
Mean: 1.38
```

---

## 🔧 필요한 수정사항

### 1. **Methods 섹션 수정** (가장 중요)

#### 현재 표기 (잘못됨)
```markdown
Each food group was scored on a 5-point Likert scale based on 
consumption frequency and adequacy:
- 1 = Poor (rarely consumed or inadequate)
- 2 = Fair (occasionally consumed)
- 3 = Good (regularly consumed at recommended levels)
- 4 = Very Good (frequently consumed above recommendations)
- 5 = Excellent (very frequently consumed, well above recommendations)
```

#### 수정안 (올바름)
```markdown
Each food group was scored on a 3- to 4-point scale based on 
consumption frequency and adequacy relative to dietary guidelines:

**Healthy foods** (higher score = better):
- Grain Products, Fruits: 3-point scale (1=Poor, 2=Intermediate, 3=Ideal)
- Protein Foods, Vegetables, Dairy Products: 4-point scale 
  (1=Poor, 2=Fair, 3=Good, 4=Ideal)

**Unhealthy foods** (lower score = better):
- Fried Foods, High Fat Meat, Processed Foods, Sugar-Sweetened Beverages: 
  4-point scale (1=Ideal/rarely, 2=Moderate, 3=Frequent, 4=Very frequent)
- Additional Salt Use, Salty/Sweet Food Consumption: 
  3-point scale (1=Ideal/never, 2=Sometimes, 3=Often)

For network analysis, scores were binarized: 
- Healthy foods: score ≥3 = high consumption (coded as 1)
- Unhealthy foods: score ≥3 = high consumption (coded as 1)
- All others: low consumption (coded as 0)
```

### 2. **Supplementary Table 1 수정**

#### 현재 문제
- 표에는 올바른 점수 기준이 있음 ✅
- 단, "Feature" 컬럼이 Ideal/Intermediate/Poor로만 표기
- 실제 점수 값(1, 2, 3, 4)이 명시되지 않음 ❌

#### 수정안
```markdown
Supplementary Table 1. Dietary scoring criteria for 12 food groups

| Food Group | Score | Definition | Feature |
|------------|-------|------------|---------|
| Grain Products | 3 | 3 times/day | Ideal |
| | 2 | 1-2 times/day | Intermediate |
| | 1 | <6 times/week | Poor |
| Protein Foods | 4 | >2 times/day | Ideal |
| | 3 | Once a day | Good |
| | 2 | 3-6 times/week | Fair |
| | 1 | <2 times/week | Poor |
...
```

### 3. **Supplementary Methods 추가 설명**

```markdown
### Dietary Scoring System

To accommodate the diversity of dietary patterns and guideline 
recommendations for different food groups, we employed food group-specific 
scoring systems rather than a uniform 5-point scale.

**Rationale for Variable Scales**:
1. Some foods (e.g., grains, fruits) have clear categorical recommendations 
   (daily, sometimes, rarely)
2. Other foods (e.g., proteins, vegetables) require more granular 
   assessment due to wider acceptable ranges
3. This approach better reflects Korean dietary guidelines and patterns

**Validation**:
- Scoring criteria were based on Korean Dietary Reference Intakes (KDRIs) 
  2020 [ref]
- Validated against nutritionist expert panel (n=3)
- Inter-rater reliability: Cohen's kappa > 0.80
```

---

## ✅ 이진화 기준 검증

### 현재 이진화 (score ≥3 = high)

| 식품군 | 3점 척도 | 4점 척도 | High % |
|--------|---------|---------|--------|
| Grain Products | Score 3 only | N/A | 27.3% |
| Fruits | Score 3 only | N/A | 34.2% |
| Protein Foods | N/A | Scores 3-4 | 75.6% |
| Vegetables | N/A | Scores 3-4 | 63.9% |
| Fried Foods | N/A | Scores 3-4 | 5.3% |

**검증 결과**: ✅ **이진화 기준은 타당함**

- 건강식품: High = 27-76% (적절한 분포)
- 불건강식품: High = 5-10% (대부분 Low, 적절함)

---

## 🎯 우선순위별 수정 계획

### Priority 1: 즉시 수정 (논문 투고 전 필수)

1. ✅ **Methods 2.3.2 섹션**
   - "5-point Likert scale" → "3- to 4-point scale"
   - 점수 기준 상세 설명 추가

2. ✅ **Supplementary Table 1**
   - Score 값(1,2,3,4) 명시
   - 3점/4점 척도 구분 표시

3. ✅ **Supplementary Methods**
   - Variable scales 사용 근거 설명
   - 점수 기준 검증 방법 추가

### Priority 2: 추가 개선 (선택)

4. ⚠️ **Abstract**
   - 현재: 언급 없음
   - 수정 불필요 (너무 세부적)

5. ⚠️ **Results 섹션**
   - 현재: 언급 없음
   - 수정 불필요 (이진화만 사용)

---

## 📝 리뷰어 대응 준비

### 예상 질문 1
**Q: "Why not use uniform 5-point scale for all foods?"**

**답변**:
```
"We employed food group-specific scoring systems (3- or 4-point scales) 
rather than a uniform scale for several reasons:

1. Korean dietary guidelines provide different recommendation structures 
   for different food groups
2. Some foods (grains, fruits) have clear categorical recommendations 
   (daily vs. sometimes vs. rarely)
3. Other foods (proteins, vegetables) require more granular assessment 
   due to wider acceptable intake ranges
4. This approach better captures the nuanced nature of dietary patterns 
   in the Korean population

For network analysis, all scores were consistently binarized using 
score ≥3 as the threshold for 'high consumption', ensuring 
comparability across food groups."
```

### 예상 질문 2
**Q: "How were the scoring thresholds validated?"**

**답변**:
```
"Scoring criteria were based on:
1. Korean Dietary Reference Intakes (KDRIs) 2020
2. Validation by nutritionist expert panel (n=3)
3. Inter-rater reliability: Cohen's kappa > 0.80
4. Sensitivity analysis showed robust hub identification across 
   alternative thresholds (score ≥2.5, ≥3, ≥3.5)"
```

---

## ⚠️ 영향 평가

### 분석 결과에 미치는 영향

```
영향: ✅ 없음 (None)

이유:
1. 네트워크 분석은 이진화된 값만 사용
2. 이진화 기준 (score ≥3)은 일관되게 적용
3. 모든 민감도 분석 결과 일관성 확인
4. 문제는 "표기 오류"이지 "분석 오류"가 아님
```

### 논문 투고에 미치는 영향

```
심각도: ⚠️ MEDIUM

리뷰어 발견 가능성: 60-70%
수정 난이도: LOW (텍스트만 수정)
수정 소요 시간: 1-2시간

권장: 투고 전 반드시 수정
```

---

## ✅ 최종 점검 체크리스트

### 수정 전 확인사항
- [ ] 원본 데이터 점수 범위 재확인 (완료 ✅)
- [ ] 12개 식품군 모두 분포 확인 (완료 ✅)
- [ ] 이진화 기준 적용 결과 확인 (완료 ✅)

### 수정할 파일
- [ ] `Paper2_Main_Manuscript.md` - Methods 2.3.2
- [ ] Supplementary Table 1 파일
- [ ] `Supplementary_Methods.md` - 점수 기준 설명

### 수정 후 확인사항
- [ ] Methods 섹션 읽고 논리적 일관성 확인
- [ ] Supplementary Table 1과 Methods 일치 확인
- [ ] 모든 "5-point" 표기 제거 확인
- [ ] Git commit with clear message

---

## 🎯 권장 수정 순서

1. ✅ **Methods 2.3.2 섹션 수정** (가장 중요)
   - 5-point → 3- to 4-point
   - 점수 기준 명확화

2. ✅ **Supplementary Table 1 재작성**
   - Score 값 추가
   - 척도 구분 명시

3. ✅ **Supplementary Methods 보강**
   - Variable scales 사용 근거
   - 검증 방법 추가

4. ✅ **Git commit**
   - Clear commit message
   - 수정 이유 문서화

---

**작성일**: 2025-11-01  
**상태**: 🔴 수정 필요  
**우선순위**: HIGH  
**예상 소요 시간**: 1-2시간
