import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 2.0")
st.write("엑셀 파일을 업로드하여 장소 데이터를 검색하고 시각화합니다.")

uploaded_file = st.file_uploader(
    "장소 데이터 엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("1. 전체 장소 데이터")
    st.dataframe(df)

    st.subheader("2. 조건 검색")

    selected_region = st.selectbox(
        "지역을 선택하세요",
        df["지역"].unique()
    )

    selected_indoor = st.selectbox(
        "실내/실외를 선택하세요",
        df["실내여부"].unique()
    )

    selected_budget = st.number_input(
        "사용 가능한 예산을 입력하세요",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["실내여부"] == selected_indoor) &
        (df["예산"] <= selected_budget)
    ]

    result = result.sort_values("평점", ascending=False)

    st.subheader("3. 추천 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다. 조건을 바꿔보세요.")

    st.subheader("4. 데이터 시각화")

    st.write("지역별 장소 개수")
    region_count = df["지역"].value_counts()
    st.bar_chart(region_count)

    st.write("유형별 장소 개수")
    type_count = df["유형"].value_counts()
    st.bar_chart(type_count)

else:
    st.info("엑셀 파일을 업로드하면 앱이 실행됩니다.")
