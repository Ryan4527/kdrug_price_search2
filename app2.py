import streamlit as st
import pandas as pd

st.set_page_config(page_title="성분별 약가 검색 필터", layout="wide")

# 데이터 로딩
@st.cache_data
def load_data():
    return pd.read_excel("약가.xlsx")

df = load_data()

# 제형코드 로딩 및 병합
form_df = pd.read_excel("제형코드.xlsx")
df["제형구분코드"] = df["주성분코드"].astype(str).str[7:9]
df = df.merge(form_df.rename(columns={"제형구분코드": "제형구분코드", "제형": "제형명"}), on="제형구분코드", how="left")

# 투여경로 추출
route_map = {"A": "내복제", "B": "주사제", "C": "외용제", "D": "기타"}
df["투여경로코드"] = df["주성분코드"].astype(str).str[6]
df["투여경로"] = df["투여경로코드"].map(route_map)

# 약효분류 병합
efficacy_df = pd.read_csv("의약품_분류표.csv")
efficacy_df = efficacy_df.rename(columns={"분류번호": "분류코드"})
df["분류코드"] = df["분류"]
df = df.merge(efficacy_df, on="분류코드", how="left")

# --- 필터 UI ---
st.title("💊 약가 검색 - 투여경로/제형/분류")
st.sidebar.header("🔍 필터 선택")

# 투여경로 필터
route_options = df["투여경로"].dropna().unique().tolist()
selected_route = st.sidebar.selectbox("투여경로", ["전체"] + sorted(route_options))

# 제형 필터
form_options = df["제형명"].dropna().unique().tolist()
selected_form = st.sidebar.selectbox("제형", ["전체"] + sorted(form_options))

# 약효분류 필터
efficacy_options = df["약효분류"].dropna().unique().tolist()
selected_efficacy = st.sidebar.selectbox("약효분류", ["전체"] + sorted(efficacy_options))

# 약가 개수 필터
count_option = st.sidebar.radio(
    "약가 개수 기준",
    ("전체", "1~5개", "10개 이하", "20개 이하")
)

# --- 필터링 적용 ---
filtered_df = df.copy()

if selected_route != "전체":
    filtered_df = filtered_df[filtered_df["투여경로"] == selected_route]

if selected_form != "전체":
    filtered_df = filtered_df[filtered_df["제형명"] == selected_form]

if selected_efficacy != "전체":
    filtered_df = filtered_df[filtered_df["약효분류"] == selected_efficacy]

if count_option == "1~5개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) <= 5)
elif count_option == "10개 이하":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) <= 10)
elif count_option == "20개 이하":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) <= 20)

# --- 결과 출력 항목 제한 ---
selected_columns = [
    "주성분코드", "제품코드", "제품명", "업체명", "규격", "단위", "상한금액", "전일", "약효분류"
]
result_df = filtered_df[selected_columns]

# --- 결과 출력 ---
st.subheader("📋 검색 결과")
st.write(f"총 {len(result_df)}개 항목이 검색되었습니다.")
st.dataframe(result_df)

# --- 다운로드 옵션 ---
st.download_button(
    label="📥 결과 다운로드 (CSV)",
    data=result_df.to_csv(index=False, encoding="utf-8-sig"),
    file_name="성분_약가_검색결과.csv",
    mime="text/csv"
)

# https://cafe.naver.com/aipharma
st.markdown("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")
# st.subheader("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")