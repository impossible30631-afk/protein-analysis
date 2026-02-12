import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import sqlalchemy
from sqlalchemy import create_engine

# 1. 세션 상태 초기화 (사이드바 상태와 메뉴 인덱스 관리)
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if 'menu_index' not in st.session_state:
    st.session_state.menu_index = 0

st.set_page_config(page_title="Protein AI Platform", layout="wide", initial_sidebar_state="expanded")

# 2. 본문 클릭 시 사이드바 닫기 JavaScript 주입
# 이 스크립트는 본문 영역을 클릭하면 사이드바 닫기 버튼을 자동으로 찾아 클릭합니다.
components.html("""
    <script>
    const doc = window.parent.document;
    const body = doc.querySelector('.main');
    body.addEventListener('click', function() {
        const closeButton = doc.querySelector('button[data-testid="stSidebarCollapseButton"]');
        if (closeButton) {
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            // 사이드바가 화면에 보이는 상태(expanded)일 때만 클릭하여 닫음
            const isVisible = window.getComputedStyle(sidebar).getPropertyValue('left') === '0px';
            if (isExpanded) {
                closeButton.click();
            }
        }
    });
    </script>
""", height=0)

# 2. 페이지 설정
st.set_page_config(
    page_title="Protein AI Platform", 
    layout="wide", 
    initial_sidebar_state=st.session_state.sidebar_state
)

# 3. DB 연결 정보 및 함수
db_user = "root"
db_pass = "your_password"  # <-- 실제 비밀번호로 수정하세요
db_name = "my-review-db"
db_host = "34.64.195.191"

def get_db_connection():
    engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
    return engine

# 4. 메뉴 이동 함수 (클릭 시 사이드바 접힘 상태로 변경)
def move_menu(target_index):
    st.session_state.menu_index = target_index
    st.session_state.sidebar_state = "collapsed"  # 버튼 클릭 시 접힘으로 변경
    st.rerun()

# 5. 강력한 CSS 주입 (화살표 시인성 및 카드 디자인)
st.markdown("""
    <style>
        .stApp { background-color: #ffffff !important; }
        
        /* 화살표 아이콘 강제 고정 (색상 및 위치) */
        button[data-testid="stSidebarCollapseButton"] {
            color: #000000 !important;
            background-color: transparent !important;
            z-index: 999999;
        }
        button[data-testid="stSidebarCollapseButton"] svg {
            fill: #000000 !important;
            width: 30px !important;
            height: 30px !important;
        }
        
        [data-testid="stSidebar"] { 
            background-color: #f8f9fa !important; 
            border-right: 1px solid #e0e0e0;
        }
        
        /* 사이드바 모든 텍스트 강제 검정 */
        [data-testid="stSidebar"] * {
            color: #000000 !important; 
            font-weight: 700 !important;
        }
        
        /* 메뉴 선택 효과 */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] input:checked + div {
            background-color: #e8f0fe !important;
            border-radius: 8px !important;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] input:checked + div p {
            color: #1a73e8 !important; 
            font-weight: 800 !important;
        }
        
        /* 카드 디자인 및 내부 글자색 강화 */
        .gs-card {
            background: #ffffff; border: 1px solid #e0e0e0; border-radius: 12px;
            padding: 22px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); margin-bottom: 20px;
        }
        .gs-card h3, .gs-card p, .gs-card b {
            color: #000000 !important;
        }
        .persona-tag {
            display: inline-block; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 12px;
        }
        .stMarkdown li, .stMarkdown p { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 6. 사이드바 메뉴 구성
menu_list = ["🏠 프로틴 제품 검색", "🚀 실시간 리뷰 엔진", "👥 맞춤형 페르소나", "📈 핵심 개선 인사이트"]

with st.sidebar:
    st.markdown("<br><h1 style='color: #4285f4; font-size: 26px; margin-bottom:0;'>Protein AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px; font-weight:bold;'>Market Intelligent Platform</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = st.radio(
        "NAVIGATION", 
        menu_list,
        index=st.session_state.menu_index,
        key="nav_radio",
        label_visibility="collapsed"
    )
    
    # 사이드바에서 수동 클릭 시에도 인덱스 동기화
    st.session_state.menu_index = menu_list.index(menu)
    
    st.write("---")
    # st.markdown("### 🚦 System Status")
    # st.caption("🔒 DB: 🟢 Connected")
    # st.caption("🧠 AI: 🔵 Model Engine Active")
    st.caption("📅 Sync: 2026-02-12")

# --- 공통 레이아웃 함수 ---
def content_layout(title, subtitle):
    st.markdown(f"<div style='padding: 20px 40px;'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: #000000; font-weight: 800;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #333333; font-size: 17px;'>{subtitle}</p>", unsafe_allow_html=True)

# --- 메뉴별 화면 구현 ---
if menu == "🏠 프로틴 제품 검색":
    content_layout("프로틴 제품 검색", "최적의 제품을 찾기 위한 AI 검색 엔진입니다.")
    genspark_url = "https://www.genspark.ai/api/code_sandbox_light/preview/8d73fd93-0037-4011-be71-2ec88dda37cc/product-search.html"
    components.iframe(genspark_url, height=850, scrolling=True)
    
    st.markdown("<div style='padding: 0 40px;'>", unsafe_allow_html=True)
    # if st.button("🚀 실제 소비자 리뷰 확인하기", use_container_width=True):
    #     move_menu(1)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚀 실시간 리뷰 엔진":
    content_layout("실시간 리뷰 엔진", "데이터베이스에서 직접 불러온 실시간 데이터 현황입니다.")
    try:
        engine = get_db_connection()
        df = pd.read_sql("SELECT * FROM reviews LIMIT 10", engine)
        st.success("✅ 실시간 DB 연결 성공")
        st.dataframe(df, use_container_width=True)
    except:
        st.info("💡 (Sample Data) 미리 보기 데이터를 표시합니다.")
        st.dataframe(pd.DataFrame({"제품명": ["테이크핏 맥스"], "별점": [5], "리뷰": ["목넘김이 깔끔합니다."]}), use_container_width=True)
    
    st.markdown("<br><div style='padding: 0 40px;'>", unsafe_allow_html=True)
    # if st.button("📊 시장 포지셔닝 분석 보기", use_container_width=True):
    #     move_menu(2)
    st.markdown("</div>", unsafe_allow_html=True)

# elif menu == "📊 시장 포지셔닝 맵":
#     content_layout("시장 포지셔닝 맵", "함량 및 품질 지수 기반 군집 분석 결과입니다.")
#     st.markdown("""
#     <div style='padding: 0 40px;'>
#     * **Cluster 1 (Premium Elite):** 함량 0.81, 품질 0.78 이상의 최상위 그룹<br>
#     * **Cluster 2 (Efficiency Focus):** 고단백·저당 밸런스의 실속 그룹<br>
#     * **Cluster 3 (Market Standard):** 대중적인 데일리 제품군<br>
#     * **Cluster 0 (Entry/Value):** 입문용 및 가벼운 일상 섭취용 그룹
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("<br><div style='padding: 0 40px;'>", unsafe_allow_html=True)
#     if st.button("👥 타겟 페르소나 확인하기", use_container_width=True):
#         move_menu(3)
#     st.markdown("</div>", unsafe_allow_html=True)

elif menu == "👥 맞춤형 페르소나":
    content_layout("맞춤형 페르소나", "4가지 핵심 소비자 유형 리포트입니다.")
    st.markdown("""
    <div style='padding: 0 40px; color: #000000 !important; line-height: 1.6;'>
        <ul style='list-style-type: none; padding-left: 0;'>
            <li style='margin-bottom: 8px;'>• <b>Cluster 1 (Premium Elite):</b> 함량 0.81, 품질 0.78 이상의 최상위 그룹</li>
            <li style='margin-bottom: 8px;'>• <b>Cluster 2 (Efficiency Focus):</b> 고단백·저당 밸런스의 실속 그룹</li>
            <li style='margin-bottom: 8px;'>• <b>Cluster 3 (Market Standard):</b> 대중적인 데일리 제품군</li>
            <li style='margin-bottom: 8px;'>• <b>Cluster 0 (Entry/Value):</b> 입문용 및 가벼운 일상 섭취용 그룹</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='gs-card'>
            <span class='persona-tag' style='background:#e7f5ed; color:#0d904f;'>Persona 1: 프리미엄 운동인</span>
            <h3>💪 Premium Performance</h3>
            <p><b>Goal:</b> 근성장 극대화, BCAA 섭취</p>
            <hr><b>추천: 테이크핏 몬스터, 테이크핏 맥스</b>
        </div>
        <div class='gs-card'>
            <span class='persona-tag' style='background:#fef7e0; color:#b06000;'>Persona 3: 데일리 영양보충</span>
            <h3>🤝 Daily Nutrition</h3>
            <p><b>Goal:</b> 근감소증 예방, 영양보충용</p>
            <hr><b>추천: 연세두유 고단백, 마이밀 뉴프로틴</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='gs-card'>
            <span class='persona-tag' style='background:#e8f0fe; color:#1a73e8;'>Persona 2: 실속형 입문자</span>
            <h3>👍 Smart Starter</h3>
            <p><b>Goal:</b> 고단백·저당·맛 균형</p>
            <hr><b>추천: 테이크핏 맥스, 더:단백</b>
        </div>
        <div class='gs-card'>
            <span class='persona-tag' style='background:#f1f3f4; color:#202124;'>Persona 4: 라이트 일상용</span>
            <h3>🏃 Light Wellness</h3>
            <p><b>Goal:</b> 음료수 대신 단백질 챙기기</p>
            <hr><b>추천: 베지밀 고단백두유, 셀렉스 프로틴음료</b>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
    # if st.button("📈 핵심 개선 전략 확인", use_container_width=True):
    #     move_menu(4)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📈 핵심 개선 인사이트":
    content_layout("핵심 개선 인사이트", "데이터 분석을 통한 브랜드 성장 및 제품 개선 전략 리포트입니다.")

# 1. [해결] 지표 카드 (Metric) - 글자색 검정 강제 주입
    st.markdown("""
        <style>
            /* 지표 카드의 숫자와 라벨 색상을 검정으로 강제 */
            [data-testid="stMetricValue"] > div { color: #000000 !important; font-weight: 800 !important; }
            [data-testid="stMetricLabel"] > div > p { color: #333333 !important; font-weight: 600 !important; }
            [data-testid="stMetricDelta"] > div { font-weight: bold !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding: 0 40px;'>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 리뷰", "1,240건", "↑12%")
    with m2:
        st.metric("평균 별점", "4.8", "↑ High")
    with m3:
        st.metric("긍정비율", "92%", "↑ Excellent")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 1. 상단 핵심 요약 (글자색 검정 강제)
    st.markdown("""
    <div style='padding: 0 40px; color: #000000 !important; line-height: 1.8; background-color: #f8f9fa; border-radius: 10px; padding: 25px; margin: 0 40px 30px 40px;'>
        <h3 style='color: #000000 !important; margin-top: 0;'>💡 데이터 기반 핵심 요약</h3>
        <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
            <li style='margin-bottom: 12px;'>✅ <b>R&D 전략:</b> 텍스처(목넘김) 만족도는 높으나, 인공적인 향료에 대한 거부감을 줄이는 '천연 향료 대체' 연구 시급</li>
            <li style='margin-bottom: 12px;'>✅ <b>차별화 전략:</b> 고관여 운동인을 위한 '고함량 라인'과 일반인을 위한 '저칼로리 에이드 라인'으로 이원화 필요</li>
            <li style='margin-bottom: 0;'>✅ <b>패키징 혁신:</b> 1회용 파우치의 '이지컷(Easy-cut)' 불량 이슈 해결을 위한 공정 개선 제언</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # 2. 시각화 지표 (Metric)
    st.markdown("<div style='padding: 0 40px;'>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("리뷰 긍정 수치", "89.2%", "+2.4%")
    with m2:
        st.metric("재구매 의사", "76.5%", "High")
    with m3:
        st.metric("핵심 불만 키워드", "패키지/캡", "-5.0%")
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. 상세 개선 로드맵
    st.write("---")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class='gs-card'>
            <h3 style='color: #4285f4 !important;'>🎯 단기 개선 과제 (1~3개월)</h3>
            <p><b>1. 맛의 밸런스 조정</b><br>초코맛의 잔여 단맛이 너무 강하다는 피드백 수용, 스테비아 함량 최적화.</p>
            <p><b>2. 배송 안정성 확보</b><br>파우치 터짐 방지를 위한 박스 내부 완충 구조 변경 및 물류 파트너사 관리 강화.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style='padding: 20px 40px; color: #000000 !important; background-color: #f8f9fa; border-radius: 10px; margin: 20px 40px;'>
            <h3 style='color: #000000 !important;'>💡 전략적 제언</h3>
            <p style='color: #000000 !important;'><b>1. R&D 전략:</b> 목넘김 개선을 위한 미세 여과 공정 도입 및 천연 향료 비중 확대.</p>
            <p style='color: #000000 !important;'><b>2. 패키징:</b> 캡(뚜껑) 밀봉 강도 최적화를 통해 노약자 및 여성 사용자 편의성 증대.</p>
            <p style='color: #000000 !important;'><b>3. 마케팅:</b> '락토프리' 속성을 강조하여 유당불내증 타겟 신규 유입 유도.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><div style='padding: 0 40px;'>", unsafe_allow_html=True)
    # if st.button("🏠 처음으로 돌아가기 (사이드바 다시 열림)", use_container_width=True):
    #     st.session_state.sidebar_state = "expanded"  # 홈으로 갈 땐 다시 열기
    #     move_menu(0)
    st.markdown("</div>", unsafe_allow_html=True)
