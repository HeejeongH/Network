# Alternative Analysis - Archived for Reference

## Status: 📦 ARCHIVED (참고용으로만 보관)

이 폴더는 `total_only.csv` (변환된 1-3-5 scale)를 사용한 탐색적 분석을 포함합니다.

## ⚠️ Important Note

**Paper 2는 original analysis (total_only_org.csv)를 계속 사용합니다.**

이 alternative analysis는:
- 탐색 목적으로만 수행됨
- 다른 연구 질문에 답함 ("회피 패턴" vs "공동 섭취 패턴")
- 현재 논문에는 사용하지 않음
- 향후 참고 또는 별도 논문 가능성을 위해 보관

## Files in This Folder

- `VISUAL_SUMMARY.txt` - 시각적 비교 요약
- `COMPARISON_REPORT.md` - 상세 비교 분석
- `compare_results.py` - 비교 스크립트
- `create_networks_alternative.py` - Alternative 분석 스크립트
- `network_summary_alternative.csv` - 결과 요약
- `networks/` - 11개 GEXF 파일
- `total_only.csv` - 변환된 데이터

## Key Finding

같은 threshold (≥3)를 사용해도 데이터 변환에 따라:
- **Original (total_only_org.csv)**: Protein-Vegetables-Grains as hubs ✅
- **Alternative (total_only.csv)**: Fried Foods-High Fat Meat as hubs (avoidance patterns)

→ **Paper 2는 original analysis가 올바른 선택입니다!** ✅

---

**Created**: 2025-11-02  
**Purpose**: Exploratory analysis (archived)  
**Status**: Reference only
