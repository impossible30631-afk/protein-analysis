import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
import os

# 1. 페이지 설정
st.set_page_config(page_title="Protein AI Platform", layout="wide", initial_sidebar_state="collapsed")

# 2. 강력한 CSS 주입 (글자색 및 화살표 가시성 해결)
st.markdown("""
    <style>
        /* 1. 전체 배경 및 본문 글자색 */
        .stApp {
            background-color: #ffffff !important;
            color: #202124 !important;
        }

        /* 2. 사이드바 글자색 강제 고정 (모든 하위 요소 포함) */
        [data-testid="stSidebar"] * {
            color: #202124 !important;
        }

        /* 3. 사이드바 라디오 버튼 텍스트 (더 구체적인 타겟팅) */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
            color: #202124 !important;
            font-weight: 600 !important;
        }

        /* 4. [핵심] 안 보이던 사이드바 열기/닫기 화살표 버튼 색상 변경 */
        [data-testid="stSidebarCollapseButton"] button svg {
            fill: #4285f4 !important; /* 화살표를 파란색으로 */
            width: 30px;
            height: 30px;
        }
        
        /* 접혔을 때 왼쪽 상단에 생기는 열기 버튼 화살표 */
        .st-emotion-cache-199v095 { 
            color: #4285f4 !important; 
        }
        
        /* 5. 사이드바 배경색 및 경계선 */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            border-right: 1px solid #e0e0e0;
        }

        /* 6. 카드 디자인 */
        .gs-card {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        
        /* 7. 메인 영역 패딩 제거 */
        .block-container { padding: 0rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 메뉴 구성
st.sidebar.markdown("<br><h2 style='text-align: center; color: #4285f4 !important;'>Protein AI</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "MENU", 
    [
        "🏠 프로젝트 개요 (Genspark)", 
        "🚀 실시간 리뷰 엔진", 
        "📊 시장 포지셔닝 맵", 
        "👥 맞춤형 페르소나"
    ]
)

# --- 공통 레이아웃 함수 ---
def content_layout(title, subtitle):
    st.markdown(f"<div style='padding: 40px 60px;'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: #202124 !important; margin-bottom: 5px;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f" <p style='color: #5f6368 !important; margin-bottom: 30px;'>{subtitle}</p>", unsafe_allow_html=True)

# --- 메뉴별 화면 구현 ---
if menu == "🏠 프로젝트 개요 (Genspark)":
    genspark_url = "https://www.genspark.ai/api/code_sandbox_light/preview/8d73fd93-0037-4011-be71-2ec88dda37cc/index.html"
    components.iframe(genspark_url, height=900, scrolling=True)

elif menu == "🚀 실시간 리뷰 엔진":
    content_layout("실시간 리뷰 엔진", "현재 수집 중인 날것의 리뷰 데이터를 실시간으로 모니터링합니다.")
    st.info("🔄 현재 데이터 재수집이 진행 중입니다.")
    st.dataframe(pd.DataFrame(columns=["제품명", "작성자", "별점", "리뷰내용"]), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📊 시장 포지셔닝 맵":
    content_layout("시장 포지셔닝 맵", "AI 분석 결과입니다.")
    sample_data = pd.DataFrame({'x': np.random.randn(50), 'y': np.random.randn(50), 'Cluster': np.random.choice(['A','B','C'], 50)})
    fig = px.scatter(sample_data, x='x', y='y', color='Cluster', template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    content_layout("맞춤형 페르소나", "소비자 유형별 최적의 프로틴 제품을 매칭해 드립니다.")
    col1, col2, col3 = st.columns(3)
    p_styles = [{"icon": "💪", "title": "벌크업 빌더"}, {"icon": "🏃", "title": "유지어터"}, {"icon": "🍃", "title": "비건 지향"}]
    for i, col in enumerate([col1, col2, col3]):
        with col:
            st.markdown(f"<div class='gs-card'><h3>{p_styles[i]['icon']} {p_styles[i]['title']}</h3><p>맞춤 추천 대기 중</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
