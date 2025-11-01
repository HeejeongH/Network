# Paper 2 파일 구조 설명 및 정리 가이드

## 📁 전체 파일 개요 (총 30개 파일)

---

## 🎯 **핵심 논문 파일 (반드시 보관)** - 7개

### 1. 메인 원고
- **`Paper2_Main_Manuscript.md`** (50 KB)
  - ✅ **보관 필수**: 투고용 메인 논문
  - 내용: 전체 논문 (~6,500 단어)
  - 포함: Abstract, Introduction, Methods, Results, Discussion, Conclusions, References (50개)
  - 상태: 투고 준비 완료 (저자 정보만 추가하면 됨)

### 2. 보충 자료
- **`Supplementary_Materials_Complete.md`** (19 KB)
  - ✅ **보관 필수**: 저널 투고 시 함께 제출
  - 내용: 통합 보충 자료 문서
  - 포함: 모든 보충 그림/표 설명, 보충 결과, 보충 논의

- **`Supplementary_Methods.md`** (13 KB)
  - ✅ **보관 필수**: 상세 방법론
  - 내용: 네트워크 구축, 중심성 계산, 통계 분석 세부 사항
  - 일부 저널은 이를 별도 파일로 요구

### 3. 참고문헌
- **`References.md`** (9.9 KB)
  - ✅ **보관 필수**: 50개 완전한 참고문헌 목록
  - 형식: Vancouver style
  - 용도: 논문 작성 참조, 인용 관리

---

## 📊 **메인 그림/표 (저널 투고용)** - 6개

### 메인 그림 (Main Figures)
- **`main_figures/Figure_1_Representative_Networks.png`** (1.3 MB, 300 DPI)
  - ✅ **보관 필수**: 논문 Figure 1
  - 내용: 4개 대표 네트워크 비교 (2×2 grid)
  
- **`main_figures/Figure_2_Hub_Centrality_Comparison.png`** (396 KB, 300 DPI)
  - ✅ **보관 필수**: 논문 Figure 2
  - 내용: 허브 식품 중심성 비교 (Panel A: 보편적, Panel B: 변동성)

### 메인 표 (Main Tables)
- **`main_tables/Table_1_Sample_Characteristics.csv`** (511 bytes)
- **`main_tables/Table_1_Sample_Characteristics.txt`** (1.1 KB)
  - ✅ **보관 필수**: 논문 Table 1
  - 내용: 11개 그룹별 표본 특성 요약

- **`main_tables/Table_2_Network_Metrics.csv`** (1.1 KB)
- **`main_tables/Table_2_Network_Metrics.txt`** (2.1 KB)
  - ✅ **보관 필수**: 논문 Table 2
  - 내용: 네트워크 구조 지표 + 상위 3개 허브

---

## 📈 **보충 그림/표 (Supplementary Materials)** - 11개

### 보충 그림
- **`figures/Figure_S1_Network_Visualizations.png`** (2.2 MB, 300 DPI)
  - ✅ **보관 필수**: 11개 네트워크 전체 시각화
  
- **`figures/Figure_S2_Hub_Transitions.png`** (444 KB, 300 DPI)
  - ✅ **보관 필수**: 연령대별 허브 전환 흐름도
  
- **`figures/Figure_S3_Centrality_Heatmaps.png`** (862 KB, 300 DPI)
  - ✅ **보관 필수**: 중심성 히트맵 (Degree/Betweenness/Closeness)

### 보충 표
- **`tables/Table_S1_Sample_Characteristics.csv/.txt`** (1 KB + 1.8 KB)
  - ✅ **보관 필수**: 상세 표본 특성

- **`tables/Table_S2_Network_Metrics.csv/.txt`** (826 bytes + 1.6 KB)
  - ✅ **보관 필수**: 상세 네트워크 지표

- **`tables/Table_S3_Edge_Lists.csv`** (16 KB)
- **`tables/Table_S3_Edge_Lists_Summary.txt`** (799 bytes)
  - ✅ **보관 필수**: 220개 엣지 목록 (11 그룹 × 20 엣지)

- **`tables/Table_S4_Centrality_Rankings.csv/.txt`** (5.7 KB + 7.9 KB)
  - ✅ **보관 필수**: 중심성 순위 (상위 5개 식품/그룹)

---

## 💻 **분석 스크립트 (재현성용)** - 3개

- **`scripts/create_stratified_networks.py`** (7.9 KB)
  - ✅ **보관 필수**: 11개 GEXF 네트워크 파일 생성
  - 용도: 데이터 재현성, 방법론 투명성

- **`scripts/generate_supplementary_materials.py`** (23 KB)
  - ✅ **보관 필수**: 보충 그림/표 생성
  - 용도: 그림/표 재생성, 수정 시 필요

- **`scripts/generate_main_figures_tables.py`** (18 KB)
  - ✅ **보관 필수**: 메인 그림/표 생성
  - 용도: 메인 그림/표 재생성, 저널 요구사항 변경 시

---

## 📝 **문서 및 요약 파일** - 3개 + 3개 중복

### 🔴 **중복/불필요 파일 (삭제 가능)** - 3개

다음 파일들은 **작업 과정 중 생성된 요약 문서**로, 현재는 불필요합니다:

1. **`COMPLETION_SUMMARY.md`** (12 KB)
   - ❌ **삭제 가능**: 중간 완료 요약 (과거 버전)
   - 이유: PROJECT_COMPLETE_SUMMARY.md에 포함됨

2. **`FINAL_REPORT.md`** (16 KB)
   - ❌ **삭제 가능**: 중간 최종 보고서 (과거 버전)
   - 이유: PROJECT_COMPLETE_SUMMARY.md에 포함됨

3. **`PROJECT_COMPLETE_SUMMARY.md`** (17 KB)
   - ⚠️ **선택 가능**: 프로젝트 완료 요약 (최신)
   - 보관 이유: 전체 프로젝트 요약 참조
   - 삭제 이유: README.md에 핵심 내용 있음

### ✅ **유용한 참조 문서** - 3개

4. **`README.md`** (9.9 KB)
   - ✅ **보관 권장**: 프로젝트 개요, 파일 구조, 사용법
   - 용도: GitHub/저장소 설명, 타인과 공유 시 필요

5. **`Title_Options.md`** (6.2 KB)
   - ⚠️ **선택 가능**: 제목 옵션 6개 분석
   - 보관 이유: 제목 선택 근거 기록
   - 삭제 이유: 최종 제목 이미 결정됨

6. **`TITLE_UPDATE_SUMMARY.md`** (6.6 KB)
   - ✅ **보관 권장**: 최종 제목 선택 이유, 효과 분석
   - 용도: 저널 에디터/리뷰어 질문 시 제목 변경 근거 제시

---

## 🗂️ **권장 파일 정리 방안**

### Option 1: 최소 보관 (저널 투고용만)
```
paper2_stratified_networks/
├── Paper2_Main_Manuscript.md              ← 메인 논문
├── Supplementary_Materials_Complete.md    ← 보충 자료
├── Supplementary_Methods.md               ← 상세 방법론
├── References.md                          ← 참고문헌
├── main_figures/                          ← 메인 그림 2개
├── main_tables/                           ← 메인 표 4개
├── figures/                               ← 보충 그림 3개
├── tables/                                ← 보충 표 8개
└── scripts/                               ← 재현성 스크립트 3개

삭제 파일: COMPLETION_SUMMARY.md, FINAL_REPORT.md, PROJECT_COMPLETE_SUMMARY.md, Title_Options.md
```

### Option 2: 문서 보관 (참조용 포함)
```
위 Option 1 + 다음 파일 보관:
├── README.md                              ← 프로젝트 설명
└── TITLE_UPDATE_SUMMARY.md                ← 제목 선택 근거

삭제 파일: COMPLETION_SUMMARY.md, FINAL_REPORT.md, PROJECT_COMPLETE_SUMMARY.md, Title_Options.md
```

### Option 3: 완전 보관 (모든 기록 유지)
```
현재 상태 그대로 유지 (30개 파일)
- 장점: 모든 작업 기록 보존
- 단점: 불필요한 중복 파일 포함
```

---

## 🔍 **파일별 상세 설명**

| 파일명 | 크기 | 용도 | 보관 | 비고 |
|--------|------|------|------|------|
| **논문 원고** |
| Paper2_Main_Manuscript.md | 50 KB | 투고용 메인 논문 | ✅ 필수 | 저자 정보만 추가하면 완료 |
| Supplementary_Materials_Complete.md | 19 KB | 통합 보충 자료 | ✅ 필수 | 저널 투고 시 함께 제출 |
| Supplementary_Methods.md | 13 KB | 상세 방법론 | ✅ 필수 | 일부 저널 별도 요구 |
| References.md | 9.9 KB | 참고문헌 50개 | ✅ 필수 | Vancouver 형식 |
| **메인 그림/표** |
| Figure_1_Representative_Networks.png | 1.3 MB | 논문 Figure 1 | ✅ 필수 | 300 DPI, 출판 품질 |
| Figure_2_Hub_Centrality_Comparison.png | 396 KB | 논문 Figure 2 | ✅ 필수 | 300 DPI, 출판 품질 |
| Table_1_Sample_Characteristics (csv/txt) | 1.6 KB | 논문 Table 1 | ✅ 필수 | 양식 선택 가능 |
| Table_2_Network_Metrics (csv/txt) | 3.2 KB | 논문 Table 2 | ✅ 필수 | 양식 선택 가능 |
| **보충 그림/표** |
| Figure_S1_Network_Visualizations.png | 2.2 MB | 전체 11개 네트워크 | ✅ 필수 | 300 DPI |
| Figure_S2_Hub_Transitions.png | 444 KB | 허브 전환 흐름도 | ✅ 필수 | 300 DPI |
| Figure_S3_Centrality_Heatmaps.png | 862 KB | 중심성 히트맵 | ✅ 필수 | 300 DPI |
| Table_S1 (csv/txt) | 2.8 KB | 상세 표본 특성 | ✅ 필수 | |
| Table_S2 (csv/txt) | 2.4 KB | 상세 네트워크 지표 | ✅ 필수 | |
| Table_S3 (csv/txt) | 16.8 KB | 엣지 목록 | ✅ 필수 | 220개 엣지 |
| Table_S4 (csv/txt) | 13.6 KB | 중심성 순위 | ✅ 필수 | Top 5 per group |
| **스크립트** |
| create_stratified_networks.py | 7.9 KB | 네트워크 생성 | ✅ 필수 | 재현성 |
| generate_supplementary_materials.py | 23 KB | 보충 자료 생성 | ✅ 필수 | 재현성 |
| generate_main_figures_tables.py | 18 KB | 메인 자료 생성 | ✅ 필수 | 재현성 |
| **문서 (보관 권장)** |
| README.md | 9.9 KB | 프로젝트 설명 | ✅ 권장 | GitHub/공유용 |
| TITLE_UPDATE_SUMMARY.md | 6.6 KB | 제목 선택 근거 | ✅ 권장 | 리뷰어 질문 대응 |
| **문서 (선택)** |
| Title_Options.md | 6.2 KB | 제목 옵션 분석 | ⚠️ 선택 | 최종 결정 완료됨 |
| PROJECT_COMPLETE_SUMMARY.md | 17 KB | 프로젝트 요약 | ⚠️ 선택 | README에 포함됨 |
| **문서 (삭제 가능)** |
| COMPLETION_SUMMARY.md | 12 KB | 중간 요약 (과거) | ❌ 삭제 | 중복 |
| FINAL_REPORT.md | 16 KB | 중간 보고서 (과거) | ❌ 삭제 | 중복 |

---

## 💾 **저장 공간 분석**

### 현재 전체 크기
- **총 파일**: 30개
- **총 크기**: 약 5.5 MB

### 삭제 후 크기 (Option 1 권장 시)
- **총 파일**: 26개
- **총 크기**: 약 5.4 MB
- **절약**: 약 100 KB (중복 문서 4개 삭제)

**결론**: 저장 공간은 크게 문제되지 않으므로, **문서 보관 가치**를 기준으로 판단하세요.

---

## ✅ **권장 사항**

### 즉시 삭제 가능 (4개)
```bash
# 중복된 요약 문서 삭제
rm COMPLETION_SUMMARY.md
rm FINAL_REPORT.md
rm PROJECT_COMPLETE_SUMMARY.md
rm Title_Options.md
```

### 보관 권장 (26개)
- 논문 원고 4개
- 메인 그림/표 6개
- 보충 그림/표 11개
- 스크립트 3개
- 문서 2개 (README.md, TITLE_UPDATE_SUMMARY.md)

---

## 🎯 **최종 정리 후 구조**

```
paper2_stratified_networks/
│
├── 📄 논문 원고
│   ├── Paper2_Main_Manuscript.md
│   ├── Supplementary_Materials_Complete.md
│   ├── Supplementary_Methods.md
│   └── References.md
│
├── 🖼️ 메인 그림/표
│   ├── main_figures/
│   │   ├── Figure_1_Representative_Networks.png
│   │   └── Figure_2_Hub_Centrality_Comparison.png
│   └── main_tables/
│       ├── Table_1_Sample_Characteristics.csv + .txt
│       └── Table_2_Network_Metrics.csv + .txt
│
├── 📊 보충 그림/표
│   ├── figures/
│   │   ├── Figure_S1_Network_Visualizations.png
│   │   ├── Figure_S2_Hub_Transitions.png
│   │   └── Figure_S3_Centrality_Heatmaps.png
│   └── tables/
│       ├── Table_S1_Sample_Characteristics.csv + .txt
│       ├── Table_S2_Network_Metrics.csv + .txt
│       ├── Table_S3_Edge_Lists.csv + summary.txt
│       └── Table_S4_Centrality_Rankings.csv + .txt
│
├── 💻 재현성 스크립트
│   └── scripts/
│       ├── create_stratified_networks.py
│       ├── generate_supplementary_materials.py
│       └── generate_main_figures_tables.py
│
└── 📝 참조 문서
    ├── README.md
    └── TITLE_UPDATE_SUMMARY.md
```

**총 26개 파일, 모두 실용적 용도 있음**

---

## ❓ **사용자 결정 필요**

어떤 정리 방안을 선택하시겠습니까?

1. **Option 1 (권장)**: 중복 문서 4개 삭제 → 26개 파일 유지
2. **Option 2**: 추가로 Title_Options.md 삭제 → 25개 파일 유지
3. **Option 3**: 현재 상태 유지 → 30개 파일 모두 보관
4. **Custom**: 직접 선택하여 삭제

---

**작성일**: 2025-11-01
