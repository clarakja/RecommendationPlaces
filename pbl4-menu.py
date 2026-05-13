import streamlit as st
import pandas as pd


def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df


def intro_page():
    st.subheader("앱 설명")
    st.write("""
    이 앱은 엑셀 파일을 업로드한 뒤, 장소 데이터를 확인하고,
    조건에 맞는 장소를 검색하고, 데이터를 차트로 시각화하는 앱입니다.
    """)

    st.write("엑셀 파일에는 최소한 다음 열이 있어야 합니다.")

    example_columns = ["이름", "지역", "유형", "실내여부", "예산", "평점"]
    st.write(example_columns)


def show_data_page(df):
    st.subheader("전체 장소 데이터")
    st.dataframe(df)

    st.write("데이터 행 개수:", len(df))
    st.write("데이터 열 이름:", list(df.columns))


def search_page(df):
    st.subheader("조건 검색")

    selected_region = st.selectbox(
        "지역을 선택하세요",
        df["지역"].unique()
    )

    selected_budget = st.number_input(
        "사용 가능한 예산을 입력하세요",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["예산"] <= selected_budget)
    ]

    result = result.sort_values("평점", ascending=False)

    st.subheader("추천 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다. 조건을 바꿔보세요.")


def chart_page(df):
    st.subheader("데이터 시각화")

    st.write("지역별 장소 개수")
    region_count = df["지역"].value_counts()
    st.bar_chart(region_count)

    st.write("유형별 장소 개수")
    type_count = df["유형"].value_counts()
    st.bar_chart(type_count)


st.title("강원생활도우미앱 2.0")

st.sidebar.title("메뉴")

menu = st.sidebar.radio(
    "원하는 기능을 선택하세요",
    ["홈", "데이터 확인", "조건 검색", "데이터 시각화"]
)

uploaded_file = st.sidebar.file_uploader(
    "장소 데이터 엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if menu == "홈":
    intro_page()

else:
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        if menu == "데이터 확인":
            show_data_page(df)

        elif menu == "조건 검색":
            search_page(df)

        elif menu == "데이터 시각화":
            chart_page(df)

    else:
        st.info("왼쪽 사이드바에서 엑셀 파일을 먼저 업로드해주세요.")
