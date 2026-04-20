import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta

# 1. 페이지 설정
st.set_page_config(
    page_title="제품 분석 대시보드 리포트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 디자인 (최신 st.html 방식 적용)
st.html("""
<style>
    /* 상단 헤더 타이틀 그라데이션 */
    .highlight-text {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .header-badge {
        background: linear-gradient(to right, #fbe8e8, #ffe4e6);
        color: #991b1b;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
        border: 1px solid #fecdd3;
    }
    
    /* 메트릭 카드 디자인 변경 */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #f3f4f6;
        padding: 5% 10%;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* 인사이트 카드 (어두운 테마) */
    .insight-card {
        background: linear-gradient(135deg, #7f1d1d, #111827);
        color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
    }
    .insight-highlight {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        margin-top: 15px;
        border-left: 4px solid #ef4444;
    }
</style>
""")

# 3. 사이드바 (데이터 필터 컨트롤)
with st.sidebar:
    st.markdown("### 🎛️ 대시보드 필터")
    st.date_input(
        "조회 기간",
        value=(date(2026, 3, 22), date(2026, 3, 28)),
        min_value=date(2026, 1, 1),
        max_value=date(2026, 12, 31)
    )
    st.multiselect(
        "분석 채널",
        options=["편의점", "대형마트", "온라인(자사몰)", "백화점"],
        default=["편의점", "대형마트"]
    )
    st.multiselect(
        "연령대",
        options=["10대", "2030 (사회초년생)", "4050", "60대 이상"],
        default=["2030 (사회초년생)", "4050"]
    )
    st.button("필터 적용", use_container_width=True)

# 4. 상단 헤더 영역
col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.html('<div class="header-badge">📊 주간 인사이트 리포트 | 2026년 3월 4주차</div>')
    st.html('<h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0;">정관장 에브리타임 밸런스 <span class="highlight-text">(리뉴얼)</span></h1>')

with col_header2:
    st.info("**데이터 기준일:** 2026. 03. 22 ~ 03. 28\n\n**분석 대상:** 온/오프라인 채널 및 리뷰 500건", icon="ℹ️")

st.markdown("---")

# 5. KPI 지표 영역 (4개 컬럼 그리드 활용)
col_kpi1, col_kpi2, col_kpi3 = st.columns([1, 1, 2])

with col_kpi1:
    st.metric(label="수도권 판매량 (전주 대비)", value="+15%", delta="15% 상승")
    st.caption("🏪 **편의점 채널 강세**")

with col_kpi2:
    st.metric(label="지방 판매량 (전주 대비)", value="-2%", delta="-2% 하락", delta_color="inverse")
    st.caption("🛒 **대형마트 정체**")

with col_kpi3:
    age_col1, age_col2 = st.columns([1.2, 1])
    with age_col1:
        st.markdown("##### 핵심 타겟 고객층")
        st.html("<h2 style='margin: 0; padding: 0;'>2030 사회초년생</h2>")
        st.markdown("전체 구매자의 **45%** 차지")
        
    with age_col2:
        fig = go.Figure(data=[go.Pie(
            labels=['2030 (사회초년생)', '기타 연령층'], 
            values=[45, 55], 
            hole=0.75,
            marker=dict(colors=['#ef4444', '#f1f5f9']),
            textinfo='none',
            hoverinfo='label+percent'
        )])
        fig.update_layout(
            showlegend=False, 
            margin=dict(t=0, b=0, l=0, r=0), 
            height=140
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.html("<br>")

# 6. 리뷰 및 특이사항 영역
col_rev, col_ins = st.columns([2, 1])

with col_rev:
    st.markdown("### 💬 고객 리뷰 핵심 요약 `분석 대상: 500건`")
    rev_col1, rev_col2 = st.columns(2)
    
    with rev_col1:
        st.success("""
        **✓ 긍정적 피드백**
        * 포장이 세련되어 선물용으로 좋다
        * 기존보다 쓴맛이 덜해 먹기 편하다
        """, icon="✅")
        
    with rev_col2:
        st.error("""
        **! 개선 필요 사항**
        * 가격이 작년보다 오른 느낌이다
        * 박스 개봉이 가끔 뻑뻑하다
        """, icon="⚠️")

with col_ins:
    insight_html = """
    <div class="insight-card">
        <h3 style="margin-top: 0; color: white;">🔥 라이프스타일 트렌드 <span style="background: #ef4444; font-size: 0.6em; padding: 2px 6px; border-radius: 4px; vertical-align: middle;">HOT</span></h3>
        <p style="color: #d1d5db; font-size: 0.9em; border-bottom: 1px solid #4b5563; padding-bottom: 10px;">최근 소셜 및 리뷰 내 동시 언급 키워드</p>
        
        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
            <strong>⛰️ 등산 / 🎾 테니스</strong>
            <span style="color: #fca5a5; font-weight: bold;">↑ 30% 급증</span>
        </div>
        
        <div class="insight-highlight">
            <span style="color: #fca5a5; font-weight: 900;">💡 핵심 인사이트</span><br>
            <span style="font-size: 0.9em;">야외 활동 및 아웃도어 스포츠(등산, 테니스 등)를 즐길 때 간편하게 섭취할 수 있는 휴대성이 <b style="color:white;">2030 세대에게 강점</b>으로 작용하고 있습니다.</span>
        </div>
    </div>
    """
    st.html(insight_html)

st.markdown("---")

# 7. 원본 데이터 및 다운로드 기능
with st.expander("📁 원본 데이터 및 상세 분석 내역 보기 (클릭하여 펼치기)"):
    st.markdown("##### 최근 1주일 주요 채널별 판매 추이 (가상 데이터)")
    
    df = pd.DataFrame({
        "일자": pd.date_range(start="2026-03-22", periods=7).strftime("%Y-%m-%d"),
        "수도권(편의점)": [120, 135, 140, 150, 180, 210, 195],
        "지방(대형마트)": [85, 80, 78, 82, 90, 85, 83],
        "온라인(자사몰)": [200, 210, 205, 230, 250, 300, 280]
    })
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 전체 데이터 다운로드 (CSV)",
        data=csv,
        file_name='sales_data_202603.csv',
        mime='text/csv',
    )
