# Paper 2: 식품 동시섭취 네트워크 분석

## 프로젝트 개요

한국 성인의 인구집단별 식품 섭취 패턴을 네트워크 분석으로 살펴본 연구입니다.

주요 결과: 단백질, 채소, 곡류가 11개 모든 인구집단에서 중심 식품(hub)으로 나타남

## 폴더 구조

```
ver3.0_2511/
├── db/                          
│   ├── processed_data/
│   │   ├── total_only_org.csv   # 메인 데이터 (원본 점수)
│   │   ├── stratified_network_statistics.csv
│   │   └── old_analysis/        # 이전 분석 파일 (보관)
│   └── raw/                     
│
├── result/                      
│   ├── manuscript/
│   │   ├── Paper2_Main_Manuscript.md          # 논문 원고
│   │   ├── References.md
│   │   ├── Supplementary_Materials_Complete.md
│   │   └── Supplementary_Methods.md
│   ├── network_files/           # 11개 GEXF 네트워크 파일
│   ├── figures/                 
│   └── tables/                  
│
└── src/                         
    ├── create_stratified_networks.py          # 메인 분석
    ├── generate_main_figures_tables.py
    └── generate_supplementary_materials.py
```

## 분석 방법

### 데이터
- 파일: `total_only_org.csv` (5.4 MB, 23,040명)
- 점수 체계: 원본 3점 또는 4점 척도
- 해석: 높을수록 많이/자주 먹음

### 방법론
- 네트워크 유형: 동시섭취 네트워크 (이진)
- 임계값: 점수 ≥3 (충분한/빈번한 섭취)
- 층화: 11개 그룹 (성별 × 연령대 × 대사증후군 유무)
- 식품군: 총 12개 (건강 식품 6개 + 건강하지 않은 식품 6개)

### 주요 결과
11개 그룹 모두에서 중심 식품(Universal Hub):
1. 단백질 식품
2. 채소
3. 곡류

임상적 의미: 식이 중재 시 단백질-채소-곡류 조합에 집중하는 것이 모든 인구집단에 효과적

## 분석 스크립트

### 1. create_stratified_networks.py
11개 층화 동시섭취 네트워크 생성

실행:
```bash
cd /home/user/webapp/ver3.0_2511
python3 src/create_stratified_networks.py
```

출력:
- `result/network_files/`에 11개 GEXF 파일
- `stratified_network_statistics.csv` 요약

주요 설정:
- 이진 임계값: `score >= 3`
- 네트워크 타입: 무방향, 가중치
- 중심성 지표: Degree, Betweenness, Closeness

### 2. generate_main_figures_tables.py
논문 본문 그림과 표 생성

생성 파일:
- Figure 1: 대표 네트워크
- Figure 2: Hub 중심성 비교
- Table 1: 대상자 특성
- Table 2: 네트워크 지표

### 3. generate_supplementary_materials.py
보충 자료 생성

생성 파일:
- Figure S1: 모든 네트워크 시각화
- Figure S2: Hub 변화 분석
- Figure S3: 중심성 히트맵
- Tables S1-S4: 상세 통계

## 데이터 파일

### 메인 데이터: total_only_org.csv
- 크기: 5.4 MB
- 행: 23,040명
- 열: 인구통계학 정보 + 12개 식품군 점수

식품군:

건강 식품 (6개):
1. 곡류 (3점)
2. 단백질 식품 (4점)
3. 채소 (4점)
4. 과일 (3점)
5. 유제품 (4점)
6. 단 음식 섭취 (3점)

건강하지 않은 식품 (6개):
1. 튀긴 음식 (4점)
2. 고지방 육류 (4점)
3. 가공식품 (4점)
4. 당류 음료 (4점)
5. 소금 추가 사용 (3점)
6. 짠 음식 섭취 (3점)

## 논문 상태

### 메인 원고
- 파일: `result/manuscript/Paper2_Main_Manuscript.md`
- 크기: 약 50 KB
- 구성: 초록, 서론, 방법, 결과, 고찰, 결론
- 상태: 작성 완료

주요 섹션:
1. 초록: 연구 결과 요약
2. 방법: 
   - 연구 설계 및 대상
   - 식이 평가 (3점 및 4점 척도)
   - 네트워크 구축 (이진 임계값 ≥3)
   - 통계 분석
3. 결과:
   - Universal hub 확인
   - 인구집단별 차이
   - 네트워크 위상 지표
4. 고찰: 임상적 의미 및 제한점

## 버전 히스토리

### ver3.0_2511 (2025년 11월) - 현재
- 점수 체계 수정한 논문 완성
- 보충 자료 완성
- 모든 그림과 표 생성
- 네트워크 파일 정리
- 주요 결과: 단백질-채소-곡류 universal hub 삼각 구조

### ver2.0_2510 (2025년 10월)
- 변환 점수를 이용한 대안 분석
- 회피 패턴 군집화 탐색
- 상태: 참고용 보관

### ver1.0_2509 (2025년 9월)
- 식이-건강 통합 분석 초기 버전
- 대사증후군 층화 탐색
- 상태: 참고용 보관

## 중요 참고사항

### 이진 분류를 사용하는 이유

연속 점수 대신 이진 임계값(≥3)을 사용한 이유:

1. 동시섭취 정의: 네트워크는 명확한 yes/no 관계 필요
2. 척도 통일: 3점 척도와 4점 척도를 통일
3. 임상적 해석: 점수 ≥3이 의미 있는 기준 (충분한 섭취량)
4. 통계적 강건성: 측정 오차와 이상치에 덜 민감

자세한 설명은 ver2.0_2510 대안 분석 문서 참고.

### total_only_org.csv를 사용하는 이유

이 데이터는 원본 점수로 높을수록 많이/자주 먹음을 의미:

- 실제로 함께 섭취되는 식품이 무엇인지 파악
- 긍정적 식이 패턴 확인 (중재에 활용 가능)
- 동시섭취 네트워크 방법론과 일치
- 명확한 임상 지침 제공

대안: `total_only.csv` (변환된 1-3-5 척도)는 회피 패턴을 파악함 - ver2.0_2510에 보관, 향후 연구 가능

## 향후 작업

가능한 후속 작업:
1. 저널에 논문 투고
2. 학회 발표 자료 제작
3. ver2.0_2510 대안 분석을 별도 논문으로 발전
4. 다른 인구집단에서 검증
5. Hub 식품 기반 중재 자료 개발

---

마지막 업데이트: 2025년 11월 2일  
상태: 분석 완료, 논문 작성 중
