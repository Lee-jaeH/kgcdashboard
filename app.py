import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date

# ----------------------------------------------------
# 📌 구글 스프레드시트 '웹에 게시(CSV)' URL
# ----------------------------------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTwIslWTmsfiT6UsKDFdvnNiPaCe-AlG4BR5qZI8-eRm6VHUg2NU0rCQrTdDAJN9TpsSd02EG2LwtN6/pub?output=csv" 

# 데이터 불러오기 함수 (캐싱 적용: 60초마다 새로고침)
@st.cache_data(ttl=60)
def load_gsheet_data(url):
    try:
        if not url or url == "":
            return pd.DataFrame({
                "지표명": ["수도권 판매량", "지방 판매량", "AI 인사이트"],
                "값": ["+15%", "-2%", "분석중"],
                "증감량": ["15% 상승", "-2% 하락", "-"],
                "메모": ["🏪 편의점 채널 강세", "🛒 대형마트 정체", "데이터를 불러오는 중입니다..."]
            })
        
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

# 1. 페이지 설정
st.set_page_config(
    page_title="제품 분석 대시보드 리포트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS
st.html("""
<style>
    .highlight-text { background: linear-gradient(135deg, #dc2626, #991b1b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .header-badge { background: linear-gradient(to right, #fbe8e8, #ffe4e6); color: #991b1b; padding: 6px 16px; border-radius: 9999px; font-size: 0.9rem; font-weight: bold; display: inline-block; margin-bottom: 10px; border: 1px solid #fecdd3; }
    div[data-testid="metric-container"] { background-color: white; border: 1px solid #f3f4f6; padding: 5% 10%; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); transition: transform 0.2s ease, box-shadow 0.2s ease; }
    div[data-testid="metric-container"]:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .insight-card { background: linear-gradient(135deg, #7f1d1d, #111827); color: white; padding: 20px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); margin-top: 20px; }
    .insight-highlight { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 10px; border-left: 4px solid #ef4444; }
</style>
""")

# 구글 시트 데이터 로드
df_metrics = load_gsheet_data(CSV_URL)

# 기본값 세팅
sudo_val, sudo_delta, sudo_memo = "+15%", "15% 상승", "🏪 편의점 채널 강세"
local_val, local_delta, local_memo = "-2%", "-2% 하락", "🛒 대형마트 정체"
ai_comment = "스프레드시트에서 'AI 인사이트' 행의 '메모' 컬럼을 확인해주세요."

# 구글 시트 데이터 매핑
if df_metrics is not None and not df_metrics.empty:
    try:
        sudo_row = df_metrics[df_metrics['지표명'] == '수도권 판매량'].iloc[0]
        sudo_val, sudo_delta, sudo_memo = sudo_row['값'], sudo_row['증감량'], sudo_row['메모']
        
        local_row = df_metrics[df_metrics['지표명'] == '지방 판매량'].iloc[0]
        local_val, local_delta, local_memo = local_row['값'], local_row['증감량'], local_row['메모']
        
        if 'AI 인사이트' in df_metrics['지표명'].values:
            ai_row = df_metrics[df_metrics['지표명'] == 'AI 인사이트'].iloc[0]
            ai_comment = ai_row['메모']
    except Exception as e:
        pass

# 3. 사이드바
with st.sidebar:
    st.markdown("### 🎛️ 대시보드 필터")
    st.date_input("조회 기간", value=(date(2026, 3, 22), date(2026, 3, 28)))
    st.multiselect("분석 채널", options=["편의점", "대형마트", "온라인(자사몰)", "백화점"], default=["편의점", "대형마트"])
    st.button("필터 적용", use_container_width=True)

# 4. 상단 헤더
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.html('<div class="header-badge">📊 주간 인사이트 리포트 | Gemini AI 연동</div>')
    st.html('<h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0;">정관장 에브리타임 밸런스 <span class="highlight-text">(리뉴얼)</span></h1>')
with col_header2:
    st.info("**AI 분석 엔진:** Gemini 1.5 Flash\n\n**동기화:** 1분 주기 자동 반영", icon="🤖")

st.markdown("---")

# 5. KPI 지표 영역
col_kpi1, col_kpi2, col_kpi3 = st.columns([1, 1, 2])
with col_kpi1:
    st.metric(label="수도권 판매량 (전주 대비)", value=sudo_val, delta=sudo_delta)
    st.caption(f"**{sudo_memo}**")
with col_kpi2:
    st.metric(label="지방 판매량 (전주 대비)", value=local_val, delta=local_delta, delta_color="inverse")
    st.caption(f"**{local_memo}**")
with col_kpi3:
    age_col1, age_col2 = st.columns([1.2, 1])
    with age_col1:
        st.markdown("##### 핵심 타겟 고객층")
        st.html("<h2 style='margin: 0; padding: 0;'>2030 사회초년생</h2>")
        st.markdown("전체 구매자의 **45%** 차지")
    with age_col2:
        fig = go.Figure(data=[go.Pie(labels=['2030', '기타'], values=[45, 55], hole=0.75, marker=dict(colors=['#ef4444', '#f1f5f9']), textinfo='none')])
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=140)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.html("<br>")

# 6. 리뷰 영역 및 AI 인사이트 통합
col_main, col_sub = st.columns([2, 1])

with col_main:
    st.markdown("### 💬 고객 리뷰 및 AI 핵심 인사이트")
    
    # 상단: 긍정/부정 리뷰 2컬럼
    rev_col1, rev_col2 = st.columns(2)
    with rev_col1:
        st.success("**✓ 긍정적 피드백**\n* 포장 디자인 만족도 높음\n* 맛의 밸런스 개선", icon="✅")
    with rev_col2:
        st.error("**! 개선 필요 사항**\n* 가격 저항감 존재\n* 패키지 개봉 편의성", icon="⚠️")
    
    # 하단: Gemini AI 인사이트 카드 (리뷰 영역 내부로 이동)
    insight_html = f"""
    <div class="insight-card">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="background: #ef4444; color: white; font-size: 0.7em; padding: 2px 8px; border-radius: 4px; font-weight: bold;">Gemini AI 분석</span>
            <strong style="color: white;">종합 데이터 인사이트</strong>
        </div>
        <div class="insight-highlight">
            <span style="font-size: 1.0rem; line-height: 1.6; color: #fecdd3; font-weight: 600;">💡 핵심 요약</span><br>
            <span style="font-size: 0.95em; line-height: 1.6; color: white;">{ai_comment}</span>
        </div>
    </div>
    """
    st.html(insight_html)

with col_sub:
    # 오른쪽 사이드 영역: 기타 트렌드나 보조 지표
    st.markdown("### 🔥 마켓 트렌드")
    st.info("**2030 등산/테니스족** 유입 급증\n\n휴대용 스틱 제형이 야외 활동 시 필수 아이템으로 자리 잡으며 판매량 견인 중", icon="📈")
    
    # 추가적인 미니 차트나 지표 등을 넣을 수 있는 공간입니다.
    st.divider()
    st.markdown("##### 📅 다음 주 예측")
    st.write("벚꽃 시즌 야외 활동 증가로 인해 수도권 편의점 채널 판매량 **8~12% 추가 상승** 예상")

st.markdown("---")

# 7. 원본 데이터 확인
with st.expander("📁 스프레드시트 연동 데이터 상세 보기"):
    if df_metrics is not None:
        st.dataframe(df_metrics, use_container_width=True, hide_index=True)
