import streamlit as st
import random
import json
import time

# 페이지 설정
st.set_page_config(
    page_title="오늘의 야식 큐레이터",
    page_icon="🍲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #2e1065 100%);
        color: #f8fafc;
    }
    .main-header {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .snack-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .snack-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(244, 63, 94, 0.2));
        border: 1px solid rgba(244, 63, 94, 0.3);
        color: #fde047;
    }
    .stButton > button {
        width: 100%;
        border-radius: 1rem;
        font-weight: 700;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, #f59e0b 0%, #f43f5e 50%, #9333ea 100%);
        color: white;
        border: none;
        box-shadow: 0 10px 20px -5px rgba(244, 63, 94, 0.3);
        cursor: pointer;
    }
    .stButton > button:hover {
        opacity: 0.95;
    }
</style>
""", unsafe_allow_html=True)

LOCAL_SNACK_DATABASE = [
    {
        "menuName": "따뜻한 계란들깨죽 & 두부전",
        "calorie": "약 280 kcal",
        "digestiveBurden": "하 (매우 편함)",
        "tasteCategory": ["담백"],
        "cookingCategory": ["직접 조리"],
        "digestiveFriendly": True,
        "reason": "속을 편안하게 감싸주는 들깨의 고소함과 계란의 부드러움이 잠들기 전 위장에 부담을 주지 않는 최적의 밤참입니다.",
        "pairingTip": "따뜻한 보리차나 둥굴레차 한 잔과 함께 드시면 숙면에 큰 도움이 됩니다."
    },
    {
        "menuName": "편의점 감동란 & 두유 콤보",
        "calorie": "약 220 kcal",
        "digestiveBurden": "하 (속 편함)",
        "tasteCategory": ["담백", "느끼/고소"],
        "cookingCategory": ["편의점"],
        "digestiveFriendly": True,
        "reason": "늦은 밤 조리 없이 바로 구매할 수 있으며, 짭조름한 반숙란과 고소한 무설탕 두유로 단백질을 알차게 채웁니다.",
        "pairingTip": "소금이 배어있는 감동란과 따뜻하게 데운 두유를 함께 드셔보세요."
    },
    {
        "menuName": "무설탕 요거트 & 견과류 바나나 볼",
        "calorie": "약 250 kcal",
        "digestiveBurden": "하 (속 편함)",
        "tasteCategory": ["달콤", "담백"],
        "cookingCategory": ["간단 조리", "편의점"],
        "digestiveFriendly": True,
        "reason": "달콤한 야식이 당길 때 혈당 폭발 걱정 없이 즐길 수 있는 건강한 단맛 조합입니다.",
        "pairingTip": "시나몬 가루를 살짝 뿌리면 풍미가 더욱 풍성해집니다."
    },
    {
        "menuName": "불닭 볶음면 & 스트링치즈 꿀조합",
        "calorie": "약 580 kcal",
        "digestiveBurden": "상 (자극적)",
        "tasteCategory": ["매콤", "자극적"],
        "cookingCategory": ["편의점"],
        "digestiveFriendly": False,
        "reason": "오늘 하루 스트레스를 단번에 날려버릴 매콤함! 치즈를 찢어 올려 매운맛을 중화한 최고의 인기 조합입니다.",
        "pairingTip": "시원한 쿨피스나 탄산수와 함께 먹으면 스트레스 해소에 특효입니다."
    },
    {
        "menuName": "직화 뼈없는 닭발 & 주먹밥",
        "calorie": "약 650 kcal",
        "digestiveBurden": "상 (매움)",
        "tasteCategory": ["매콤", "자극적"],
        "cookingCategory": ["배달"],
        "digestiveFriendly": False,
        "reason": "쫄깃한 식감과 매콤한 불향이 밤 정취와 딱 어우러지는 대표적인 최강 야식입니다.",
        "pairingTip": "고소한 김가루 마요네즈 주먹밥을 동글동글 만들어서 닭발 양념에 찍어드세요."
    },
    {
        "menuName": "바삭한 숯불 양념 지코바 치킨",
        "calorie": "약 750 kcal",
        "digestiveBurden": "중~상",
        "tasteCategory": ["매콤", "달콤", "자극적"],
        "cookingCategory": ["배달"],
        "digestiveFriendly": False,
        "reason": "튀기지 않고 숯불에 구워 불맛이 깊게 베어있으며, 남은 양념에 밥을 비벼먹는 밥반찬 겸 야식입니다.",
        "pairingTip": "치킨 무와 떡사리를 추가하고, 마지막에 햇반 하나 비벼 먹는 '치밥'이 국룰입니다."
    },
    {
        "menuName": "에어프라이어 버터 갈릭 새우 구이",
        "calorie": "약 320 kcal",
        "digestiveBurden": "중 (고소함)",
        "tasteCategory": ["느끼/고소", "담백"],
        "cookingCategory": ["직접 조리"],
        "digestiveFriendly": True,
        "reason": "새우의 탱글탱글한 식감과 버터, 마늘의 풍미가 어우러져 고급스러운 분위기를 내는 야식입니다.",
        "pairingTip": "레몬즙을 살짝 짜서 뿌려주면 느끼함 없이 깔끔하게 즐길 수 있습니다."
    },
    {
        "menuName": "편의점 족발 찰순대 세트",
        "calorie": "약 520 kcal",
        "digestiveBurden": "중",
        "tasteCategory": ["자극적", "느끼/고소"],
        "cookingCategory": ["편의점"],
        "digestiveFriendly": False,
        "reason": "전자레인지 1분 30초면 완성! 쫀득한 족발과 순대를 새우젓 양념에 찍어 먹는 고품격 간편 야식입니다.",
        "pairingTip": "초고추장이나 쌈장을 살짝 곁들이면 맛이 훨씬 다채로워집니다."
    },
    {
        "menuName": "따뜻한 시원어묵탕 & 곤약면",
        "calorie": "약 210 kcal",
        "digestiveBurden": "하 (매우 속편함)",
        "tasteCategory": ["담백", "자극적"],
        "cookingCategory": ["직접 조리", "편의점"],
        "digestiveFriendly": True,
        "reason": "곤약면을 활용해 칼로리 부담은 거의 없으면서도 따끈하고 깊은 어묵 국물로 속을 든든히 채워줍니다.",
        "pairingTip": "청양고추를 송송 썰어 넣으면 맑고 칼칼한 국물 맛을 즐길 수 있습니다."
    },
    {
        "menuName": "달콤 고소한 콘치즈 그라탕",
        "calorie": "약 410 kcal",
        "digestiveBurden": "중",
        "tasteCategory": ["달콤", "느끼/고소"],
        "cookingCategory": ["직접 조리", "편의점"],
        "digestiveFriendly": False,
        "reason": "옥수수 통조림과 모짜렐라 치즈, 마요네즈만 있으면 5분 만에 완성되는 입안 가득 행복해지는 맛입니다.",
        "pairingTip": "핫소스를 살짝 떨어뜨려 먹으면 단짠단짠 매력이 배가됩니다."
    }
]

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

st.markdown("""
<div style="text-align: center; padding: 1.5rem 0;">
    <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(to right, #f59e0b, #f43f5e, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🍲 오늘의 야식 큐레이터
    </h1>
    <p style="color: #94a3b8; font-size: 0.95rem;">당신의 입맛과 취침 시간에 딱 맞춘 완벽한 야식을 추천해 드립니다.</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        current_time = st.text_input("현재 시간", "23:00")
    with col2:
        bed_time = st.text_input("예상 취침 시간", "02:00")

    taste_options = ["매콤", "달콤", "담백", "느끼/고소", "자극적"]
    selected_taste = st.selectbox("선호하는 맛", taste_options)

    cooking_options = ["배달", "편의점", "직접 조리"]
    selected_cooking = st.selectbox("조리 방식", cooking_options)

    consider_digestive = st.checkbox("소화 부담 / 칼로리 고려 (속 편한 메뉴 우선)", value=True)

    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        submit_btn = st.button("✨ 맞춤 야식 추천 받기")
    with col_btn2:
        random_btn = st.button("🎲 랜덤 야식 뽑기")

def get_recommendations(is_random=False):
    filtered = list(LOCAL_SNACK_DATABASE)
    if is_random:
        random.shuffle(filtered)
    else:
        # 가중치 계산 정렬
        def score_item(item):
            score = 0
            if selected_taste in item["tasteCategory"]:
                score += 3
            if selected_cooking in item["cookingCategory"]:
                score += 2
            if consider_digestive and item["digestiveFriendly"]:
                score += 4
            return score
        
        filtered.sort(key=score_item, reverse=True)
    
    return filtered[:3]

if submit_btn or random_btn:
    with st.spinner("최적의 야식을 탐색 중입니다..."):
        time.sleep(0.4)
        st.session_state.recommendations = get_recommendations(is_random=random_btn)

if st.session_state.recommendations:
    st.markdown("---")
    st.markdown("### 🔥 추천 야식 TOP 3")
    
    for idx, item in enumerate(st.session_state.recommendations):
        st.markdown(f"""
        <div class="snack-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span class="badge">추천 {idx + 1}</span>
                <span style="color: #f43f5e; font-size: 0.85rem; font-weight: 600;">🔥 {item['calorie']}</span>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;">{item['menuName']}</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 1rem; background: rgba(15, 23, 42, 0.4); padding: 0.75rem; border-radius: 0.75rem; border: 1px solid rgba(51, 65, 85, 0.5);">
                {item['reason']}
            </p>
            <div style="border-top: 1px solid rgba(51, 65, 85, 0.6); pt-2;">
                <p style="color: #fbbf24; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.25rem;">💡 꿀조합 & 추천 팁</p>
                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">{item['pairingTip']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.75rem; margin-top: 3rem;">
    © 오늘의 야식 큐레이터. Built with Streamlit & Python.
</div>
""", unsafe_allow_html=True)
