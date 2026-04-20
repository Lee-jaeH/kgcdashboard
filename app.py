import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date

# ----------------------------------------------------
# 📌 여기에 구글 스프레드시트 '웹에 게시(CSV)' URL을 넣으세요!
# 따옴표("") 안에 링크를 붙여넣으시면 됩니다.
# ----------------------------------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTwIslWTmsfiT6UsKDFdvnNiPaCe-AlG4BR5qZI8-eRm6VHUg2NU0rCQrTdDAJN9TpsSd02EG2LwtN6/pub?output=csv" 

# 데이터 불러오기 함수 (캐싱 적용: 60초마다 새로고침)
@st.cache_data(ttl=60)
def load_gsheet_data(url):
    try:
        if not url or url == "":
            # URL을 넣지 않았을 때 보여줄 기본 임시 데이터
            return pd.DataFrame({
                "지표명": ["수도권 판매량", "지방 판매량"],
                "값": ["+15%", "-2%"],
                "증감량": ["15% 상승", "-2% 하락"],
                "메모": ["🏪 편의점 채널 강세", "🛒 대형마트 정체"]
            })
        
        # 구글 시트 CSV 읽어오기
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다. 링크를 다시 확인해주세요: {e}")
        return None

# 1. 페이지 설정
st.set_page_config(
    page_title="제품 분석 대시보드 리포트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS (UI 깨짐 방지용 st.html 적용)
st.html("""
<style>
    .highlight-text { background: linear-gradient(135deg, #dc2626, #991b1b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .header-badge { background: linear-gradient(to right, #fbe8e8, #ffe4e6); color: #991b1b; padding: 6px 16px; border-radius: 9999px; font-size: 0.9rem; font-weight: bold; display: inline-block; margin-bottom: 10px; border: 1px solid #fecdd3; }
    div[data-testid="metric-container"] { background-color: white; border: 1px solid #f3f4f6; padding: 5% 10%; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); transition: transform 0.2s ease, box-shadow 0.2s ease; }
    div[data-testid="metric-container"]:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .insight-card { background: linear-gradient(135deg, #7f1d1d, #111827); color: white; padding: 20px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
    .insight-highlight { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #ef4444; }
</style>
""")

# 구글 시트 데이터 로드
df_metrics = load_gsheet_data(CSV_URL)

# 지표값 기본 세팅
sudo_val, sudo_delta, sudo_memo = "+15%", "15% 상승", "🏪 편의점 채널 강세"
local_val, local_delta, local_memo = "-2%", "-2% 하락", "🛒 대형마트 정체"

# 구글 시트 데이터가 정상적으로 불러와졌다면 값 덮어쓰기
if df_metrics is not None and not df_metrics.empty:
    try:
        sudo_row = df_metrics[df_metrics['지표명'] == '수도권 판매량'].iloc[0]
        sudo_val, sudo_delta, sudo_memo = sudo_row['값'], sudo_row['증감량'], sudo_row['메모']
        
        local_row = df_metrics[df_metrics['지표명'] == '지방 판매량'].iloc[0]
        local_val, local_delta, local_memo = local_row['값'], local_row['증감량'], local_row['메모']
    except IndexError:
        pass # 시트 형식이 다를 경우 기본값 유지

# 3. 사이드바 (데이터 필터 컨트롤)
with st.sidebar:
    st.markdown("### 🎛️ 대시보드 필터")
    st.date_input("조회 기간", value=(date(2026, 3, 22), date(2026, 3, 28)))
    st.multiselect("분석 채널", options=["편의점", "대형마트", "온라인(자사몰)", "백화점"], default=["편의점", "대형마트"])
    st.multiselect("연령대", options=["10대", "2030 (사회초년생)", "4050", "60대 이상"], default=["2030 (사회초년생)", "4050"])
    st.button("필터 적용", use_container_width=True)

# 4. 상단 헤더
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.html('<div class="header-badge">📊 주간 인사이트 리포트 | 실시간 연동</div>')
    st.html('<h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0;">정관장 에브리타임 밸런스 <span class="highlight-text">(리뉴얼)</span></h1>')
with col_header2:
    st.info("**데이터 소스:** 구글 스프레드시트\n\n**동기화:** 1분 주기 자동 반영", icon="🔄")

st.markdown("---")

# 5. KPI 지표 영역 (구글 시트 연동 데이터 반영)
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
        fig = go.Figure(data=[go.Pie(labels=['2030 (사회초년생)', '기타 연령층'], values=[45, 55], hole=0.75, marker=dict(colors=['#ef4444', '#f1f5f9']), textinfo='none', hoverinfo='label+percent')])
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=140)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.html("<br>")

# 6. 리뷰 영역 
col_rev, col_ins = st.columns([2, 1])
with col_rev:
    st.markdown("### 💬 고객 리뷰 핵심 요약 `분석 대상: 500건`")
    rev_col1, rev_col2 = st.columns(2)
    with rev_col1:
        st.success("**✓ 긍정적 피드백**\n* 포장이 세련되어 선물용으로 좋다\n* 기존보다 쓴맛이 덜해 먹기 편하다", icon="✅")
    with rev_col2:
        st.error("**! 개선 필요 사항**\n* 가격이 작년보다 오른 느낌이다\n* 박스 개봉이 가끔 뻑뻑하다", icon="⚠️")

with col_ins:
    insight_html = """
    <div class="insight-card">
        <h3 style="margin-top: 0; color: white;">🔥 라이프스타일 트렌드 <span style="background: #ef4444; font-size: 0.6em; padding: 2px 6px; border-radius: 4px;">HOT</span></h3>
        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
            <strong>⛰️ 등산 / 🎾 테니스</strong><span style="color: #fca5a5; font-weight: bold;">↑ 30% 급증</span>
        </div>
        <div class="insight-highlight">
            <span style="color: #fca5a5; font-weight: 900;">💡 핵심 인사이트</span><br>
            <span style="font-size: 0.9em;">아웃도어 스포츠 시 휴대성이 <b style="color:white;">2030 세대</b>에게 강점으로 작용합니다.</span>
        </div>
    </div>
    """
    st.html(insight_html)

st.markdown("---")

# 7. 원본 데이터 및 다운로드 
with st.expander("📁 원본 데이터 및 상세 분석 내역 보기 (클릭하여 펼치기)"):
    if df_metrics is not None and not df_metrics.empty:
        st.markdown("##### 📊 구글 스프레드시트 연동 원본 데이터")
        st.dataframe(df_metrics, use_container_width=True, hide_index=True)
    else:
        st.markdown("##### 최근 1주일 주요 채널별 판매 추이 (가상 데이터)")
        df_dummy = pd.DataFrame({
            "일자": pd.date_range(start="2026-03-22", periods=7).strftime("%Y-%m-%d"),
            "수도권(편의점)": [120, 135, 140, 150, 180, 210, 195],
            "지방(대형마트)": [85, 80, 78, 82, 90, 85, 83]
        })
        st.dataframe(df_dummy, use_container_width=True, hide_index=True)
