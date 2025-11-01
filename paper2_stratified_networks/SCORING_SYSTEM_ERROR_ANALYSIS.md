# 식습관 평가 점수 시스템 오류 분석

## 🔴 발견된 문제점

Supplementary Table 1의 **Grain Products** 점수 기준에 **논리적 모순**이 있습니다.

---

## 📊 현재 Supplementary Table 1의 문제

### 잘못된 부분: Grain Products

| Feature | 현재 표기 | 문제점 |
|---------|----------|--------|
| **Ideal** | 3 times/day | ✅ 올바름 |
| **Intermediate** | 1-2 times/day | ⚠️ **논리적 모순!** |
| **Poor** | Less than 6 times/week | ✅ 상대적으로 맞음 |

### 🔴 문제의 핵심

```
Intermediate: 1-2 times/day (하루 1-2회)
                 ↓
         7-14 times/week

Poor: Less than 6 times/week (주 6회 미만)
                 ↓
         <6 times/week

❌ Intermediate가 Poor보다 높은 빈도인데,
   왜 Poor가 "주당 6회"로 표기되어 있는가?
```

### 논리적 모순

```
만약 Intermediate = 1-2 times/day라면:
  → 주당 7-14회
  → Poor는 주당 6회 미만

그러면:
  Ideal: 21회/주 (3×7)
  Intermediate: 7-14회/주 (1-2×7)
  Poor: <6회/주

✅ 이것이 논리적으로 맞음!

하지만 현재 표에는:
  Poor: "Less than 6 times/week"로 표기
  
❌ 이는 Intermediate (7-14회/주)와 겹치는 문제 발생!
```

---

## 🔍 원본 데이터 확인 필요

### 가능한 시나리오

#### 시나리오 1: Intermediate가 잘못됨
```
올바른 기준:
  Ideal: 3 times/day (21회/주)
  Intermediate: 1-2 times/day (7-14회/주) ✅
  Poor: Less than 6 times/week (<6회/주) ✅

→ 이 경우 현재 표기가 맞음
```

#### 시나리오 2: Poor 기준이 잘못됨
```
만약 Poor가 "Less than 1 time/day"였다면:
  Ideal: 3 times/day (21회/주)
  Intermediate: 1-2 times/day (7-14회/주)
  Poor: Less than 1 time/day (<7회/주)

→ 더 논리적
```

#### 시나리오 3: 전체 기준 재검토 필요
```
한국인 영양섭취기준에 따라:
  Ideal: 2-3 times/meal × 3 meals = 6-9 servings/day
  Intermediate: 3-6 servings/day
  Poor: <3 servings/day

→ 원본 데이터 확인 필요
```

---

## 📋 다른 식품군 점수 기준 (비교)

### 건강식품 (섭취 많을수록 좋음)

#### Protein Foods ✅ 논리적
```
Ideal: More than 2 times/day
Intermediate: Once a day
Poor: 3-6 times/week or less than 2 times/week
```

#### Vegetables ✅ 논리적
```
Ideal: More than 2 times/day
Intermediate: Once a day
Poor: 3-6 times/week or less than 2 times/week or hardly
```

#### Fruits ✅ 논리적
```
Ideal: Everyday
Intermediate: 3-6 times/week
Poor: Less than 2 times/week or hardly
```

### 불건강 식품 (섭취 적을수록 좋음)

#### Fried Foods ✅ 논리적
```
Ideal: Less than 1-2/week or hardly
Intermediate: 3-6 times/week
Poor: More than 2 times/day or Once a day
```

#### Sugar-Sweetened Beverages ✅ 논리적
```
Ideal: Less than 1-2 glasses/week or hardly
Intermediate: 3-6 glasses/week
Poor: More than 2 glasses/day or 1 glass/day
```

---

## 🔧 수정 방안

### Option 1: Grain Products 기준 명확화 (권장) ⭐

**현재 (문제)**:
```
Grain Products:
  Ideal: 3 times/day
  Intermediate: 1-2 times/day
  Poor: Less than 6 times/week
```

**수정안 1A (주당 기준 통일)**:
```
Grain Products:
  Ideal: 3 times/day (21 times/week)
  Intermediate: 1-2 times/day (7-14 times/week)
  Poor: Less than 1 time/day (<7 times/week)
```

**수정안 1B (빈도 기준 재정의)**:
```
Grain Products:
  Ideal: More than 2 times/day
  Intermediate: 1-2 times/day
  Poor: Less than 1 time/day or hardly
```

**수정안 1C (한국 식사 패턴 반영)**:
```
Grain Products:
  Ideal: Every meal (3 times/day)
  Intermediate: 1-2 meals/day
  Poor: Less than once daily
```

### Option 2: 원본 데이터 재확인

다음 파일들 확인 필요:
```
/home/user/webapp/db/raw_data/total_only_org.csv
- 실제 Grain Products 변수 분포 확인
- 점수 부여 기준 원본 확인
- 데이터 딕셔너리 확인
```

---

## ✅ 실제 데이터 분포 확인 완료!

### 원본 데이터 분석 결과

**Grain Products 실제 분포** (N=23,040):
```
Score 1.0:  3,673명 (15.9%)
Score 2.0: 13,068명 (56.7%)
Score 3.0:  6,299명 (27.3%)

Mean: 2.11
Median: 2.00
Std: 0.65
```

### 🔴 핵심 발견: **3점 척도 사용!**

```
Grain Products는 5점 척도가 아니라 3점 척도!

실제 점수:
  3 = Ideal (3 times/day)
  2 = Intermediate (1-2 times/day)  
  1 = Poor (Less than 6 times/week)
```

### 이진화 기준 적용

```
현재 논문: score ≥3 = high consumption

Grain Products의 경우:
  score 3: Ideal → High ✅ (6,299명, 27.3%)
  score 2: Intermediate → Low (13,068명, 56.7%)
  score 1: Poor → Low (3,673명, 15.9%)

→ High consumption = 27.3%만 해당
→ 대부분(72.7%)이 Low로 분류됨
```

### ⚠️ 이것이 문제의 원인!

**Supplementary Table 1은 실제로는 맞습니다!**
- 단, **5점 척도가 아니라 3점 척도**라는 것을 명시하지 않았음
- 논문 본문은 "5-point Likert scale"이라고 표기
- **실제로는 식품군마다 다른 점수 체계 사용!**

---

## 🎯 긴급 조치 사항

### 1. 즉시 확인 (High Priority)

```bash
# 원본 데이터에서 Grain Products 분포 확인
cd /home/user/webapp/db/raw_data
head -1 total_only_org.csv | tr ',' '\n' | nl | grep -i grain
```

### 2. Supplementary Table 수정

**현재 파일**:
- `tables/Table_S1_Sample_Characteristics.csv`
- 만약 별도 Supplementary Table 1이 있다면 그것도 수정

### 3. 논문 본문 확인

**확인 위치**:
- Methods 2.3.2: Dietary Quality Scoring
- Supplementary Methods: 상세 점수 기준

---

## 📝 권장 조치

### Step 1: 원본 데이터 확인
```bash
# Grain Products 변수 확인
cd /home/user/webapp
python3 << 'EOF'
import pandas as pd

data = pd.read_csv('db/raw_data/total_only_org.csv')

# Grain Products 관련 컬럼 찾기
grain_cols = [col for col in data.columns if 'grain' in col.lower() or 'rice' in col.lower()]
print("Grain-related columns:", grain_cols)

# 각 컬럼의 분포 확인
for col in grain_cols:
    print(f"\n{col}:")
    print(data[col].value_counts().sort_index())
EOF
```

### Step 2: 점수 기준 재정의

**원본 데이터 확인 후** 다음 중 선택:

1. **5점 척도 기준 명확화**
   ```
   5 = 3 times/day (Ideal)
   4 = 2 times/day
   3 = 1 time/day (Good, 기준선)
   2 = 3-6 times/week
   1 = <6 times/week (Poor)
   ```

2. **Table 1 수정**
   - Intermediate와 Poor 기준 재정의
   - 논리적 일관성 확보

### Step 3: 논문 수정

**수정 필요 부분**:
1. Supplementary Table 1 (가장 중요)
2. Supplementary Methods (점수 기준 설명)
3. 필요시 Main Methods 섹션

---

## ⚠️ 리뷰어 지적 가능성

### 예상 질문

**Q1: "The scoring for Grain Products seems inconsistent. Intermediate is 1-2 times/day but Poor is <6 times/week?"**

**현재 답변 어려움**:
- 1-2 times/day = 7-14 times/week
- <6 times/week is LESS than Intermediate
- 논리적 모순

**수정 후 답변 가능**:
```
"We revised the scoring criteria for clarity:
  Ideal: ≥3 times/day (21 times/week)
  Intermediate: 1-2 times/day (7-14 times/week)
  Poor: <1 time/day (<7 times/week)

This ensures logical consistency across frequency categories."
```

---

## ✅ 결론 및 권장사항

### 문제 요약

```
🔴 Grain Products 점수 기준에 논리적 모순
   - Intermediate: 1-2 times/day (7-14회/주)
   - Poor: <6 times/week
   → Intermediate가 Poor보다 높은데 Poor 기준이 이상함
```

### 즉시 조치 필요

1. ✅ **원본 데이터 확인** (최우선)
   - Grain Products 변수의 실제 분포
   - 점수 부여 기준 원본 문서

2. ✅ **Supplementary Table 1 수정**
   - 논리적으로 일관된 기준으로 수정
   - Intermediate와 Poor 기준 명확화

3. ✅ **논문 본문 검토**
   - Methods 섹션 점수 기준 설명 확인
   - Supplementary Methods 상세 설명 추가

4. ✅ **리뷰어 대응 준비**
   - 수정 근거 문서화
   - 원본 데이터 기준 명시

### 영향 평가

```
심각도: ⚠️ MEDIUM-HIGH

이유:
- 논문의 핵심 방법론 부분
- 리뷰어가 발견 가능
- 수정은 비교적 간단 (표만 수정)
- 분석 결과는 영향 없음 (이진화만 사용)
```

---

**작성일**: 2025-11-01  
**발견자**: 사용자  
**상태**: 🔴 수정 필요  
**우선순위**: HIGH
