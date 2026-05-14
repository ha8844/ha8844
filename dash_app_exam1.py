
import streamlit as st
import random
import time
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(page_title="점심 메뉴 룰렛", layout="wide")

# 메뉴 데이터
menu_options = {
    "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기", "제육볶음", "냉면", "갈비탕"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "양꼬치", "볶음밥"],
    "일식": ["초밥", "라멘", "돈까스", "우동", "회덮밥", "소바"],
    "양식": ["파스타", "피자", "스테이크", "리조또", "햄버거", "샐러드"],
    "분식": ["떡볶이", "김밥", "라면", "튀김", "순대"]
}

# 세션 상태 초기화
if 'selected_menus' not in st.session_state:
    st.session_state.selected_menus = []
if 'roulette_result' not in st.session_state:
    st.session_state.roulette_result = None
if 'spinning' not in st.session_state:
    st.session_state.spinning = False

# 룰렛 차트 생성 함수
def create_roulette_chart(menus, rotation=0, result_menu=None):
    if not menus:
        return go.Figure()

    n_menus = len(menus)
    values = [10] * n_menus
    
    fig = go.Figure(data=[go.Pie(
        labels=menus, 
        values=values, 
        hole=.3,
        textinfo='label',
        hoverinfo='none',
        marker=dict(colors=['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(n_menus)]),
        rotation=rotation
    )])
    
    fig.update_layout(
        showlegend=False,
        width=500,
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # 화살표 추가
    fig.add_shape(
        type="path",
        path=" M -0.5 -0.1 L -0.5 0.1 L -0.8 0 L -0.5 -0.1 Z",
        fillcolor="red",
        line_color="red",
        xref="paper",
        yref="paper",
        xanchor="center",
        yanchor="middle",
    )
    
    if result_menu:
        st.markdown(f"<h1 style='text-align: center; color: red;'>🎉 {result_menu} 🎉</h1>", unsafe_allow_html=True)

    return fig

# 사이드바
with st.sidebar:
    st.title("룰렛 메뉴 선택")
    
    current_selection = []
    for category, items in menu_options.items():
        with st.expander(f"**{category}**"):
            for item in items:
                if st.checkbox(item, key=f"{category}_{item}", value=(item in st.session_state.selected_menus)):
                    if item not in current_selection:
                        current_selection.append(item)
    
    if current_selection != st.session_state.selected_menus:
        st.session_state.selected_menus = current_selection
        st.rerun()

    st.markdown("---")
    st.write("##### 선택된 메뉴")
    if st.session_state.selected_menus:
        for menu in st.session_state.selected_menus:
            st.write(f"- {menu}")
    else:
        st.write("메뉴를 선택해주세요.")

# 메인 화면
st.title("점심 메뉴 룰렛")
st.markdown("사이드바에서 메뉴를 선택하고 룰렛을 돌려보세요!")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 룰렛 돌리기 버튼
    if st.button("룰렛 돌리기!", use_container_width=True, type="primary"):
        if len(st.session_state.selected_menus) > 1:
            st.session_state.spinning = True
            st.session_state.roulette_result = None
        elif len(st.session_state.selected_menus) == 1:
            st.session_state.roulette_result = st.session_state.selected_menus[0]
            st.session_state.spinning = False
        else:
            st.warning("룰렛을 돌리려면 2개 이상의 메뉴를 선택해야 합니다.")
            st.session_state.spinning = False

    chart_placeholder = st.empty()

    # 룰렛 애니메이션 및 결과 표시
    if st.session_state.spinning:
        start_time = time.time()
        duration = 3  # 3초 동안 스핀
        spin_speed = 360 * 3 # 초당 회전 속도

        while time.time() - start_time < duration:
            angle = (time.time() - start_time) * spin_speed
            chart = create_roulette_chart(st.session_state.selected_menus, rotation=angle)
            chart_placeholder.plotly_chart(chart, use_container_width=True)
            time.sleep(0.01)
        
        # 최종 결과 선택
        final_result = random.choice(st.session_state.selected_menus)
        st.session_state.roulette_result = final_result
        st.session_state.spinning = False

        # 최종 결과 위치로 회전
        result_index = st.session_state.selected_menus.index(final_result)
        n_menus = len(st.session_state.selected_menus)
        angle_per_item = 360 / n_menus
        final_angle = - (result_index * angle_per_item + angle_per_item / 2)
        
        # 최종 결과 차트 표시
        final_chart = create_roulette_chart(st.session_state.selected_menus, rotation=final_angle)
        chart_placeholder.plotly_chart(final_chart, use_container_width=True)
        st.markdown(f"<h1 style='text-align: center; color: red;'>🎉 {st.session_state.roulette_result} 🎉</h1>", unsafe_allow_html=True)
        st.balloons()

    elif st.session_state.roulette_result:
        result_index = st.session_state.selected_menus.index(st.session_state.roulette_result)
        n_menus = len(st.session_state.selected_menus)
        angle_per_item = 360 / n_menus
        final_angle = - (result_index * angle_per_item + angle_per_item / 2)
        
        chart = create_roulette_chart(st.session_state.selected_menus, rotation=final_angle)
        chart_placeholder.plotly_chart(chart, use_container_width=True)
        st.markdown(f"<h1 style='text-align: center; color: red;'>🎉 {st.session_state.roulette_result} 🎉</h1>", unsafe_allow_html=True)
    else:
        chart = create_roulette_chart(st.session_state.selected_menus)
        chart_placeholder.plotly_chart(chart, use_container_width=True)


st.markdown("---")
st.info("이 앱은 Streamlit으로 만들어졌습니다.")
