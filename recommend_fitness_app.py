import streamlit as st
import random

# 운동 프로그램 및 가격(단위: 원)
programs = {
    "수영": {"1회권": 7000, "정기권": 62000, "패키지": 136000},
    "헬스": {"1회권": 9000, "정기권": 79000, "패키지": 105000},
    "스쿼시": {"1회권": 10000, "정기권": 82000},
    "체형 교정 발레": {"정기권": 90000},
    "방송댄스": {"정기권": 90000},
    "골프": {"1회권": 10000, "정기권": 119000}
}

mbti_recommendations = {
    "ISTJ": "스쿼시", "ISFJ": "체형 교정 발레", "INFJ": "수영", "INTJ": "골프",
    "ISTP": "스쿼시", "ISFP": "방송댄스", "INFP": "체형 교정 발레", "INTP": "골프",
    "ESTP": "헬스", "ESFP": "방송댄스", "ENFP": "방송댄스", "ENTP": "골프",
    "ESTJ": "헬스", "ESFJ": "수영", "ENFJ": "방송댄스", "ENTJ": "골프"
}

mbti_explanations = {
    "ISTJ": "규칙적이고 체계적인 스쿼시의 명확한 룰이 당신의 성향과 잘 맞습니다.",
    "ISFJ": "세심한 동작 교정이 필요한 발레가 내성적이면서 완벽주의적인 성향에 적합합니다.",
    "INFJ": "혼자서 집중할 수 있는 수영이 내향적이면서도 통찰력 있는 성격과 조화롭습니다.",
    "INTJ": "전략적 사고가 필요한 골프가 비전을 중시하는 당신의 성향에 부합합니다.",
    "ISTP": "순간 판단과 기계적 움직임이 중요한 스쿼시가 분석적 성향과 잘 맞습니다.",
    "ISFP": "예술적 표현이 자유로운 방송댄스가 감성적인 성격에 최적화되어 있습니다.",
    "INFP": "아름다움과 조화를 추구하는 발레가 이상주의적 성향과 잘 어울립니다.",
    "INTP": "물리학적 원리 분석이 가능한 골프가 논리적 사고를 가진 분에게 적합합니다.",
    "ESTP": "에너지 발산이 가능한 고강도 헬스가 활동적인 성격에 맞습니다.",
    "ESFP": "사교적이고 활기찬 방송댄스가 사람을 즐겁게 하는 성향과 조화롭습니다.",
    "ENFP": "창의력 발휘가 가능한 자유로운 댄스가 열정적인 성격에 어울립니다.",
    "ENTP": "다양한 전략 시도가 가능한 골프가 혁신적인 사고를 가진 분에게 추천됩니다.",
    "ESTJ": "목표 달성을 위한 체계적인 헬스 루틴이 조직적인 성향에 부합합니다.",
    "ESFJ": "그룹 수영이 사교적이면서도 타인을 배려하는 성격과 잘 맞습니다.",
    "ENFJ": "팀워크가 중요한 방송댄스가 리더십 있는 성향에 적합합니다.",
    "ENTJ": "경쟁적 요소가 있는 골프가 목표 지향적인 성격과 잘 어울립니다."
}

purpose_recommendations = {
    "체중 감량": ["수영", "헬스", "방송댄스"],
    "근육 증가": ["헬스", "스쿼시"],
    "자세 개선": ["체형 교정 발레", "수영"],
    "스트레스 해소": ["수영", "방송댄스", "골프"],
    "재활 훈련": ["수영", "체형 교정 발레"],
    "심폐 기능 향상": ["수영", "헬스", "스쿼시"],
    "사교 활동": ["방송댄스", "헬스"]
}

sport_tips = {
    "수영": ["목 통증: 접형 영법(나비수영)은 목에 부담을 줄 수 있음",
             "어깨 통증: 과도한 팔 동작은 회전근개 손상 유발 가능",
             "허리 통증: 배영이 허리에 가장 부담이 적은 영법",
             "무릎 통증: 평영 발차기 시 무릎에 과도한 스트레스 주의"],
    "헬스": ["목 통증: 목 근육 긴장 상태에서의 머리 숙임 동작 금지",
             "어깨 통증: 벤치 프레스 시 어깨 각도 75도 유지",
             "허리 통증: 데드리프트 시 허리 곡선 유지 필수",
             "무릎 통증: 스쿼트 시 무릎이 발끝 넘어가지 않도록"],
    "스쿼시": ["목 통증: 공을 쫓을 때 목의 급격한 회전 피하기",
               "어깨 통증: 백핸드 스트로크 시 어깨 관절 과신전 주의",
               "허리 통증: 전방 굽힘 자세 지속 시 요추 디스크 압력 ↑",
               "무릎 통증: 갑작스러운 방향 전환 시 무릎 충격 조심"],
    "체형 교정 발레": ["목 통증: 아라베스크 자세에서 목 과도한 신전 금지",
                     "어깨 통증: 포르 드 브라 동작 시 어깨 라인 유지",
                     "허리 통증: 플리에 동작에서 과도한 요추 전만 방지",
                     "무릎 통증: 턴아웃 각도 무리하게 확대하지 말 것"],
    "방송댄스": ["목 통증: 헤드뱅잉 동작은 경추 추간판 손상 위험",
               "어깨 통증: 파트너 리프팅 시 회전근개 부상 주의",
               "허리 통증: 힙합 동작 시 척추의 비정상적 회전 금지",
               "무릎 통증: 점프 후 착지 시 충격 흡수 필수"],
    "골프": ["목 통증: 스윙 시 목의 과도한 회전 반복 금지",
             "어깨 통증: 백스윙 탑 위치에서 어깨 관절 압력 ↑",
             "허리 통증: 티샷 시 전방 굽힘 자세 유지 시간 최소화",
             "무릎 통증: 다운스윙 시 앞무릎의 외회전 스트레스 주의"]
}

st.set_page_config(page_title="SNU 운동 추천기", page_icon="🏋️")
st.title(":muscle: 더 건강한 캠퍼스를 위한 운동 추천 프로그램")
st.markdown("서울대학교 구성원 전용 서비스입니다.")

is_member = st.radio("서울대학교 구성원이신가요?", ["예", "아니오"])
if is_member == "아니오":
    st.warning("※ 본 추천 시스템은 서울대 기준 가격으로 구성되어 있습니다.")
    if not st.checkbox("그래도 계속하겠습니다."):
        st.stop()

method = st.selectbox("운동 추천 방식", ["완전 무작위", "MBTI 기반", "운동 목적 기반", "직접 선택"])
budget = st.slider("운동 예산을 입력하세요 (단위: 원)", 5000, 200000, 7000, step=1000)

selected_sport = ""
reason = ""

if method == "완전 무작위":
    affordable_sports = []
    for sport, price_dict in programs.items():
        if any(price <= budget for price in price_dict.values()):
            affordable_sports.append(sport)
    if not affordable_sports:
        st.error(f"예산 {budget:,}원으로 가능한 운동이 없습니다.")
        st.stop()
    selected_sport = random.choice(affordable_sports)
    reason = "무작위 추천입니다."
elif method == "MBTI 기반":
    mbti = st.text_input("당신의 MBTI를 입력해주세요 (예: INFJ)").strip().upper()
    if mbti in mbti_recommendations:
        selected_sport = mbti_recommendations[mbti]
        reason = mbti_explanations.get(mbti, "")
    elif mbti:
        st.error("알 수 없는 MBTI입니다. 정확히 입력해주세요.")
elif method == "운동 목적 기반":
    purpose = st.selectbox("운동 목적 또는 증상", list(purpose_recommendations.keys()))
    selected_sport = random.choice(purpose_recommendations[purpose])
    reason = "해당 목적에 기반한 추천입니다."
elif method == "직접 선택":
    selected_sport = st.selectbox("운동 직접 선택", list(programs.keys()))
    reason = "사용자 직접 선택입니다."

if selected_sport:
    st.subheader(":trophy: 추천 결과")
    st.write(f"**운동 프로그램:** {selected_sport}")
    st.write(f"**추천 사유:** {reason}")

    prices = programs[selected_sport]
    available_options = {k: v for k, v in prices.items() if v <= budget}

    if not available_options:
        st.error(f"예산 {budget:,}원으로는 {selected_sport} 프로그램의 이용권이 없습니다.")
        st.stop()

    # 가장 비싼 이용권 추천
    sorted_options = sorted(available_options.items(), key=lambda x: -x[1])
    ticket, price = sorted_options[0]

    st.success(f"추천 이용권: {ticket} ({price:,}원)")

    st.markdown("### 💰 이용권 가격표")
    for key, value in prices.items():
        st.write(f"- {key}: {value:,}원")

    if selected_sport in sport_tips:
        st.markdown("### ⚠️ 운동 시 주의사항")
        for tip in sport_tips[selected_sport]:
            st.markdown(f"- {tip}")
