#!/usr/bin/env python3
"""
11개 층화 그룹별 맞춤형 영양 코칭 전략 (텍스트 분석)
"""

def print_personalized_coaching_strategies():
    """
    그룹별 맞춤형 코칭 전략 상세 분석
    """
    
    print("="*80)
    print("🎯 개인맞춤형 영양 코칭 전략 - 11개 층화 그룹별 상세 방안")
    print("="*80)
    print("🔬 네트워크 분석 기반 과학적 근거:")
    print("   • Protein-Vegetables: 0.318 (최강 상관관계)")
    print("   • Processed Foods: 90.9% 그룹에서 허브")
    print("   • Fried Foods: 81.8% 그룹에서 허브")
    print("   • 네트워크 복잡성: 3-9개 연결선 (4.5-13.6% 밀도)")
    print()
    
    # 그룹별 상세 전략
    strategies = [
        {
            'group': '1. 남성 청년층 MetS(+) [516명]',
            'network': '매우 복잡 (8개 연결선, 12.1% 밀도)',
            'hub_pattern': 'Processed→Fried→Protein (불건전한 허브 지배)',
            'primary_target': '🚨 Processed Foods 허브 완전 차단',
            'strategy': '공격적 네트워크 재구조화 (고위험군)',
            'actions': [
                '1순위: 가공식품 완전 제거 → 전체 네트워크 붕괴 유도',
                '2순위: 튀김류 → 그릴/찜/구이로 조리법 완전 변경',
                '3순위: Protein-Vegetables (0.318) 조합 새 허브로 육성',
                '4순위: 염분 관리 (Salt-Salty 0.222 관계 차단)',
                '5순위: 주 1회 식단 체크 및 즉시 피드백'
            ],
            'intensity': '🔴 고강도 (복잡성 + MetS 위험)',
            'timeline': '3개월 집중 → 6개월 정착',
            'expected': '허브 제거로 전체 식단 패턴 급격 개선, MetS 지표 호전'
        },
        {
            'group': '2. 남성 청년층 MetS(-) [1,963명] ⭐ 최대 그룹',
            'network': '극도 복잡 (9개 연결선, 13.6% 밀도) - 최고 복잡성',
            'hub_pattern': 'Processed→Fried→Protein (복잡하지만 건강)',
            'primary_target': '🎯 건강한 복잡성 → 최적화된 다양성',
            'strategy': '선택적 네트워크 최적화 (예방 중심)',
            'actions': [
                '1순위: Protein-Vegetables (0.318) 관계를 새로운 핵심 허브로',
                '2순위: 가공식품 점진적 감소 (급격한 변화 지양)',
                '3순위: 다양성 유지하면서 품질 향상 (9개 연결선 활용)',
                '4순위: MetS 예방 패턴 구축 (장기적 관점)',
                '5순위: 2주마다 모니터링으로 건강 패턴 유지'
            ],
            'intensity': '🟡 중강도 (복잡하지만 건강함)',
            'timeline': '6개월 점진적 변화',
            'expected': '건강한 복잡성 → 최적 다양성, 생애 전반 건강 식단 기반'
        },
        {
            'group': '3. 남성 중년층 MetS(+) [2,938명]',
            'network': '매우 복잡 (8개 연결선, 12.1% 밀도)',
            'hub_pattern': 'Processed→Fried→High Fat Meat (위험한 삼각 허브)',
            'primary_target': '🥩 High Fat Meat 허브 집중 타격',
            'strategy': '단계적 네트워크 단순화 (생활습관병 중재)',
            'actions': [
                '1순위: 고지방육류 → 저지방 단백질 완전 대체',
                '2순위: Processed-Fried 허브 연결고리 차단',
                '3순위: 염분 섭취 엄격 관리 (Salt-Salty 0.222)',
                '4순위: 혈압/혈당 고려한 식품 조합 재설계',
                '5순위: 주 2회 집중 상담 및 바이오마커 추적'
            ],
            'intensity': '🔴 고강도 (중년 + MetS + 복잡성)',
            'timeline': '4개월 집중 → 8개월 안정화',
            'expected': '생활습관병 진행 억제, 심혈관 위험 감소'
        },
        {
            'group': '4. 남성 중년층 MetS(-) [4,737명] ⭐ 최대 건강 그룹',
            'network': '복잡 (7개 연결선, 10.6% 밀도)',
            'hub_pattern': 'Processed→Protein→Fried (균형잡힌 허브)',
            'primary_target': '🏃‍♂️ 건강 패턴 유지 및 예방적 강화',
            'strategy': '품질 중심 최적화 (현상 유지 + 향상)',
            'actions': [
                '1순위: Protein-Vegetables (0.318) 관계 더욱 강화',
                '2순위: 현재 균형 유지하면서 전반적 질 향상',
                '3순위: 가공식품 의존도 서서히 감소',
                '4순위: 장년층 진입 대비 최적 패턴 준비',
                '5순위: 월 1회 모니터링으로 현상 유지'
            ],
            'intensity': '🟢 저강도 (현상 유지 + 미세 조정)',
            'timeline': '장기 지속형 (12개월+)',
            'expected': '건강 식단 패턴 장기 유지, 성공적 노화 준비'
        },
        {
            'group': '5. 남성 장년층 MetS(+) [971명]',
            'network': '중간 (6개 연결선, 9.1% 밀도)',
            'hub_pattern': 'Processed→Fried→High Fat Meat (여전히 위험)',
            'primary_target': '🎯 핵심 허브만 집중 타격 (현실적 목표)',
            'strategy': '최소 변화 최대 효과 (연령 고려)',
            'actions': [
                '1순위: 고지방육류 완전 제거 (단일 허브 타겟)',
                '2순위: 가공식품 최소 수준으로 감소',
                '3순위: 6개 연결선을 건강한 패턴으로 재배치',
                '4순위: 소화 부담 고려한 부드러운 조리법',
                '5순위: 2주마다 단순하고 명확한 목표 설정'
            ],
            'intensity': '🟡 중강도 (연령 고려한 현실적 목표)',
            'timeline': '6개월 점진적 변화',
            'expected': '단순하지만 효과적인 건강 패턴 확립'
        },
        {
            'group': '6. 남성 장년층 MetS(-) [1,169명]',
            'network': '중간 (6개 연결선, 9.1% 밀도)',
            'hub_pattern': 'Processed→Protein→Vegetables (건강 전환 시작)',
            'primary_target': '🥬 Vegetables 허브 극대화',
            'strategy': '채소 중심 건강 패턴 정착',
            'actions': [
                '1순위: 채소를 모든 식사의 핵심 허브로 육성',
                '2순위: Protein-Vegetables (0.318) 관계 활용',
                '3순위: 가공식품 허브 약화 지속',
                '4순위: 연령에 맞는 영양밀도 최적화',
                '5순위: 월 2회 건강 패턴 점검'
            ],
            'intensity': '🟢 저강도 (건강 유지형)',
            'timeline': '장기 지속형',
            'expected': '건강한 노화 패턴 확립'
        },
        {
            'group': '7. 여성 청년층 MetS(-) [2,519명]',
            'network': '단순 (5개 연결선, 7.6% 밀도)',
            'hub_pattern': 'Protein→Processed→Vegetables (효율적 패턴)',
            'primary_target': '💪 Protein-Vegetables 허브 강화',
            'strategy': '효율적 건강 패턴 구축 (이미 단순함)',
            'actions': [
                '1순위: 단백질-채소 조합을 식단의 절대 중심으로',
                '2순위: 5개 연결선 모두 고품질 식품으로 최적화',
                '3순위: 가공식품 의존도 더욱 낮추기',
                '4순위: 생애주기 변화(임신/수유) 대비 패턴',
                '5순위: 월 1회 간단한 체크로 패턴 유지'
            ],
            'intensity': '🟢 저강도 (이미 단순하고 건강함)',
            'timeline': '유지형 + 생애주기 적응',
            'expected': '효율적이고 지속가능한 건강 식단'
        },
        {
            'group': '8. 여성 중년층 MetS(+) [758명]',
            'network': '복잡 (7개 연결선, 10.6% 밀도)',
            'hub_pattern': 'Processed→Fried→Protein (호르몬 변화 + MetS)',
            'primary_target': '🚨 호르몬 변화 + MetS 동시 관리',
            'strategy': '폐경기 고려한 집중 네트워크 관리',
            'actions': [
                '1순위: Processed-Fried 허브 동시 차단 (호르몬 균형)',
                '2순위: 단백질 섭취 충분히 유지 (근육량 보존)',
                '3순위: 칼슘/마그네슘 고려한 뼈 건강 패턴',
                '4순위: 염분 엄격 관리 (갱년기 부종 예방)',
                '5순위: 주 2회 집중 상담 + 호르몬 수치 모니터링'
            ],
            'intensity': '🔴 고강도 (MetS + 호르몬 변화)',
            'timeline': '3개월 집중 → 9개월 안정화',
            'expected': '폐경기 건강한 전환, MetS 개선'
        },
        {
            'group': '9. 여성 중년층 MetS(-) [5,629명] ⭐ 최대 여성 그룹',
            'network': '복잡 (7개 연결선, 10.6% 밀도)',
            'hub_pattern': 'Processed→Protein→Vegetables (전환기 패턴)',
            'primary_target': '🔄 Vegetables 허브로 건강 전환',
            'strategy': '호르몬 변화 대비 예방적 패턴 구축',
            'actions': [
                '1순위: Vegetables를 새로운 핵심 허브로 전환',
                '2순위: Protein-Vegetables (0.318) 관계 극대화',
                '3순위: 폐경 대비 항산화/파이토에스트로겐 강화',
                '4순위: 가공식품 허브 약화 지속 추진',
                '5순위: 월 2회 호르몬 변화 고려한 식단 조정'
            ],
            'intensity': '🟡 중강도 (호르몬 변화 대비)',
            'timeline': '6개월 전환 → 장기 유지',
            'expected': '건강한 폐경기 준비, 평생 건강 기반'
        },
        {
            'group': '10. 여성 장년층 MetS(+) [680명]',
            'network': '중간 (6개 연결선, 9.1% 밀도)',
            'hub_pattern': 'Vegetables→Processed→Protein (전환 중)',
            'primary_target': '🥬 Vegetables 허브 절대 우위 확립',
            'strategy': '단순함 속 최대 영양밀도 (노화 + MetS)',
            'actions': [
                '1순위: 채소를 모든 식사의 절대 중심으로',
                '2순위: 6개 연결선을 최고 품질 식품으로만',
                '3순위: 소화 흡수율 고려한 부드러운 조리',
                '4순위: 항염/항산화 중심 식품 선택',
                '5순위: 2주마다 간단명료한 목표 점검'
            ],
            'intensity': '🟡 중강도 (연령 + MetS)',
            'timeline': '4개월 집중 → 장기 유지',
            'expected': '건강한 노화 지원, 만성질환 관리'
        },
        {
            'group': '11. 여성 장년층 MetS(-) [1,084명]',
            'network': '극도 단순 (3개 연결선, 4.5% 밀도) - 최저 복잡성',
            'hub_pattern': 'Vegetables→Protein→Processed (최적 단순화)',
            'primary_target': '✨ 완벽한 단순성 유지 + 품질 극대화',
            'strategy': '최소 변화로 최대 건강 효과',
            'actions': [
                '1순위: 현재 Vegetables 허브 패턴 완벽 유지',
                '2순위: 3개 연결선만 최고 영양밀도로 최적화',
                '3순위: 소화 부담 절대 최소화',
                '4순위: 항노화 영양소 집중 공급',
                '5순위: 월 1회 만족도 중심 점검'
            ],
            'intensity': '🟢 저강도 (이미 최적 단순성)',
            'timeline': '현상 유지 + 미세 최적화',
            'expected': '지속가능한 건강 장수 패턴'
        }
    ]
    
    for i, strategy in enumerate(strategies):
        print(f"{'='*80}")
        print(f"🔍 {strategy['group']}")
        print(f"{'='*80}")
        print(f"📊 네트워크 특성: {strategy['network']}")
        print(f"🌐 허브 패턴: {strategy['hub_pattern']}")
        print(f"🎯 주요 타겟: {strategy['primary_target']}")
        print(f"📋 전략: {strategy['strategy']}")
        print(f"⚡ 강도: {strategy['intensity']}")
        print(f"⏰ 일정: {strategy['timeline']}")
        print(f"📈 기대효과: {strategy['expected']}")
        print()
        print("📝 구체적 실행 계획:")
        for action in strategy['actions']:
            print(f"   {action}")
        print()
    
    # 요약 분석
    print("="*80)
    print("📊 전체 요약 분석")
    print("="*80)
    
    print("\n🎯 중재 강도별 그룹 분포:")
    print("   🔴 고강도 (3개 그룹): 남청MetS+, 남중MetS+, 여중MetS+")
    print("   🟡 중강도 (4개 그룹): 남청MetS-, 남장MetS+, 여중MetS-, 여장MetS+")  
    print("   🟢 저강도 (4개 그룹): 남중MetS-, 남장MetS-, 여청MetS-, 여장MetS-")
    
    print("\n🌟 핵심 발견:")
    print("   1️⃣ 성별 > 연령 > MetS 순서의 영향력")
    print("   2️⃣ 남성: 복잡한 네트워크 → 종합적 접근 필요")
    print("   3️⃣ 여성: 단순한 네트워크 → 효율적 타겟팅 가능")
    print("   4️⃣ 연령 증가 → 네트워크 단순화 → 핵심 허브 집중")
    print("   5️⃣ MetS(+): 허브 차단 우선, MetS(-): 건강 허브 강화")
    
    print("\n🚀 개인맞춤형 영양의 혁신적 접근:")
    print("   • 기존: 일률적 영양소 권장량")
    print("   • 신규: 네트워크 기반 맞춤형 허브 전략")
    print("   • 효과: 개인별 최적화된 최소 변화로 최대 건강 효과")
    
    print("\n💡 실용적 적용 방안:")
    print("   1. AI 기반 개인별 네트워크 분석")
    print("   2. 층화 그룹별 맞춤형 앱 알고리즘")
    print("   3. 허브 식품 중심 식단 추천 시스템")
    print("   4. 네트워크 복잡성 기반 중재 강도 결정")
    print("   5. 생애주기 고려한 동적 전략 업데이트")

if __name__ == '__main__':
    print_personalized_coaching_strategies()