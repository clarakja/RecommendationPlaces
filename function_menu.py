import streamlit as st
import pandas as pd


def load_data():
    uploaded_file = st.sidebar.file_uploader(
        "장소 데이터 엑셀 파일을 업로드해주세요.",
        type=["xlsx"]
    )

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    else:
        st.info("데이터를 저장한 엑셀(.xlsx) 파일을 업로드하세요.")
        return None


def show_uploaded_data(df):
    st.subheader("업로드한 장소 목록")
    st.dataframe(df)


def get_filter_options(df):
    selected_region = st.selectbox("지역 선택", df["지역"].unique())
    selected_budget = st.number_input("가용예산", min_value=0, value=10000, step=500)
    return selected_region, selected_budget


def show_search_result(df, selected_region, selected_budget):
    result = df[
        (df["지역"] == selected_region) &
        (df["예산"] <= selected_budget)
    ]

    st.subheader("추천 결과 목록")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다.")


def show_charts(df):
    st.subheader("지역별 장소 개수")
    st.bar_chart(df["지역"].value_counts())

    st.subheader("유형별 장소 개수")
    st.bar_chart(df["유형"].value_counts())

    st.subheader("지역별 평균 평점")
    st.bar_chart(df.groupby("지역")["평점"].mean())


st.title("강원생활도우미 앱 2.0")
st.write("엑셀 파일을 업로드하고 원하는 기능을 메뉴에서 선택할 수 있습니다.")

df = load_data()

menu = st.sidebar.radio(
    "메뉴 선택",
    ["데이터 확인", "조건 검색", "차트 보기"]
)

if df is not None:
    if menu == "데이터 확인":
        show_uploaded_data(df)

    elif menu == "조건 검색":
        selected_region, selected_budget = get_filter_options(df)
        show_search_result(df, selected_region, selected_budget)

    elif menu == "차트 보기":
        show_charts(df)
