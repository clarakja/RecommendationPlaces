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

 region_count = df["지역"].value_counts()

st.subheader("지역별 장소 개수")
st.bar_chart(region_count)
