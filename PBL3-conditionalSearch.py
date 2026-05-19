import streamlit as st
import pandas as pd


def load_file():
    uploaded_file = st.file_uploader(
        "장소 데이터 엑셀 파일을 업로드하세요",
        type=["xlsx"]
    )

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    else:
        st.info("엑셀 파일을 업로드하면 데이터가 표시됩니다.")
        return None


def print_table(table, table_name):
    st.subheader(table_name)

    if len(table) > 0:
        st.dataframe(table)
    else:
        st.warning("출력할 장소가 없습니다.")


def get_user_input(df):
    st.subheader("조건 검색")

    # 1. 검색할 열 선택
    search_key = st.selectbox(
        "검색 기준을 선택하세요",
        df.columns
    )

    # 2. 선택한 열이 숫자형인지 확인
    if pd.api.types.is_numeric_dtype(df[search_key]):
        condition = st.selectbox(
            "검색 조건을 선택하세요",
            ["이하", "이상", "같음"]
        )

        search_value = st.number_input(
            f"{search_key} 값을 입력하세요",
            value=float(df[search_key].mean())
        )

        if condition == "이하":
            result = df[df[search_key] <= search_value]
        elif condition == "이상":
            result = df[df[search_key] >= search_value]
        else:
            result = df[df[search_key] == search_value]

    # 3. 선택한 열이 문자형이면 목록에서 값 선택
    else:
        search_value = st.selectbox(
            "검색 값을 선택하세요",
            df[search_key].dropna().unique()
        )

        result = df[df[search_key] == search_value]

    return result


def show_filter_places(result):
    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다.")


def count_chart(df, key):
    key_count = df[key].value_counts()

    st.subheader(key + "별 장소 개수")
    st.bar_chart(key_count)


def average_chart(df, group, num):
    avg_score = df.groupby(group)[num].mean()

    st.subheader(group + "별 평균 " + num)
    st.bar_chart(avg_score)


st.title("강생도 2.0")
st.write("엑셀 파일을 업로드하면 장소 데이터를 확인할 수 있습니다.")

df = load_file()

if df is not None:
    print_table(df, "업로드한 장소 데이터")

    result = get_user_input(df)

    show_filter_places(result)

    count_chart(df, "지역")
    count_chart(df, "유형")
    average_chart(df, "지역", "평점")
