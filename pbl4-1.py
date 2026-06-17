# =====================================================================
# 강원생활도우미앱 3.1 — 가성비 추천 기능 확장본
#
# [확장 문서화]  (SDD 6단계 결과)
# - 더한 것   : add_value_score(), top_value() 함수 + '추천 검색'에 '가성비 추천 보기'
# - 건드리지 않은 것 : load_data, join_data, show_original_data, show_joined_data,
#                      search_recommendations의 기존 검색/경고, show_chart
# - 회귀 결과 : 기존 검색 결과는 그대로 (가성비는 결과를 '복사'해서 계산 → 원본 불변)
# - 접점     : 기존 검색 결과 DataFrame을 받아, '평점'·'예산' 열로 가성비를 매긴다
# =====================================================================

import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.1")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)


# =====================================================================
# === 확장: 가성비 추천 (새로 추가한 함수 — 기존 함수는 그대로) ===
# 가성비 = 평점 / (예산 + 1)   (예산 0 나눗셈 방지 +1)
# 입력(검색 결과)을 복사해서 사용하므로 원본은 바뀌지 않는다.
# =====================================================================
def add_value_score(result):
    out = result.copy()                                   # 원본 보호
    out["가성비"] = (out["평점"] / (out["예산"] + 1)).round(5)
    return out.sort_values("가성비", ascending=False)


def top_value(result, n=3):
    return add_value_score(result).head(n)
# =====================================================================


def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox("지역 선택", df["지역"].unique())
    selected_purpose = st.selectbox("추천목적 선택", df["추천목적"].unique())
    selected_situation = st.selectbox("추천상황 선택", df["추천상황"].unique())
    selected_target = st.selectbox("추천대상 선택", df["추천대상"].unique())

    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget)
    ]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)

        # === 확장: 가성비 추천 보기 (기존 결과는 위에 그대로 두고, 아래에 추가) ===
        if {"평점", "예산"}.issubset(result.columns):
            if st.checkbox("가성비 추천 보기 (평점 대비 예산)"):
                st.subheader("가성비 추천 TOP 3")
                st.caption("가성비 = 평점 ÷ (예산+1) — 값이 클수록 저렴하면서 평점이 높음")
                st.dataframe(top_value(result, 3))
        # =========================================================
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)
