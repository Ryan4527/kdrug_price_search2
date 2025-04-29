# 버전 1
# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="성분별 약가 검색 필터", layout="wide")

# # 데이터 로딩
# @st.cache_data
# def load_data():
#     return pd.read_excel("약가.xlsx")

# df = load_data()

# # 제형코드 로딩 및 병합
# form_df = pd.read_excel("제형코드.xlsx")
# df["제형구분코드"] = df["주성분코드"].astype(str).str[7:9]
# df = df.merge(form_df.rename(columns={"제형구분코드": "제형구분코드", "제형": "제형명"}), on="제형구분코드", how="left")

# # 투여경로 추출
# route_map = {"A": "내복제", "B": "주사제", "C": "외용제", "D": "기타"}
# df["투여경로코드"] = df["주성분코드"].astype(str).str[6]
# df["투여경로"] = df["투여경로코드"].map(route_map)

# # 약효분류 병합
# efficacy_df = pd.read_csv("의약품_분류표.csv")
# efficacy_df = efficacy_df.rename(columns={"분류번호": "분류코드"})
# df["분류코드"] = df["분류"]
# df = df.merge(efficacy_df, on="분류코드", how="left")

# # --- 필터 UI ---
# st.title("💊 약가 검색 - 투여경로/제형/분류")
# st.markdown("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")

# st.sidebar.header("🔍 필터 선택")

# # 투여경로 필터
# route_options = df["투여경로"].dropna().unique().tolist()
# selected_route = st.sidebar.selectbox("투여경로", ["전체"] + sorted(route_options))

# # 제형 필터
# form_options = df["제형명"].dropna().unique().tolist()
# selected_form = st.sidebar.selectbox("제형", ["전체"] + sorted(form_options))

# # 약효분류 필터
# efficacy_options = df["약효분류"].dropna().unique().tolist()
# selected_efficacy = st.sidebar.selectbox("약효분류", ["전체"] + sorted(efficacy_options))

# # 약가 개수 필터
# count_option = st.sidebar.radio(
#     "약가 개수 기준",
#     ("전체", "1~5개", "10개 이하", "20개 이하")
# )

# # --- 필터링 적용 ---
# filtered_df = df.copy()

# if selected_route != "전체":
#     filtered_df = filtered_df[filtered_df["투여경로"] == selected_route]

# if selected_form != "전체":
#     filtered_df = filtered_df[filtered_df["제형명"] == selected_form]

# if selected_efficacy != "전체":
#     filtered_df = filtered_df[filtered_df["약효분류"] == selected_efficacy]

# if count_option == "1~5개":
#     filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) <= 5)
# elif count_option == "10개 이하":
#     filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) <= 10)
# elif count_option == "20개 이하":
#     filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) <= 20)

# # --- 결과 출력 항목 제한 ---
# selected_columns = [
#     "주성분코드", "제품코드", "제품명", "업체명", "규격", "단위", "상한금액", "전일", "약효분류"
# ]
# result_df = filtered_df[selected_columns]

# # --- 결과 출력 ---
# st.subheader("📋 검색 결과")
# st.write(f"총 {len(result_df)}개 항목이 검색되었습니다.")
# st.dataframe(result_df)

# # --- 다운로드 옵션 ---
# st.download_button(
#     label="📥 결과 다운로드 (CSV)",
#     data=result_df.to_csv(index=False, encoding="utf-8-sig"),
#     file_name="성분_약가_검색결과.csv",
#     mime="text/csv"
# )

# # https://cafe.naver.com/aipharma
# st.markdown("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")
# # st.subheader("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")

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
st.markdown("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")

st.sidebar.header("🔍 필터 선택")

# 투여경로 필터 (다중선택)
route_options = df["투여경로"].dropna().unique().tolist()
selected_routes = st.sidebar.multiselect("투여경로(중복선택 가능)", sorted(route_options))

# 제형 필터 (다중선택)
form_options = df["제형명"].dropna().unique().tolist()
selected_forms = st.sidebar.multiselect("제형(중복선택 가능)", sorted(form_options))

# 약효분류 필터 (다중선택)
efficacy_options = df["약효분류"].dropna().unique().tolist()
selected_efficacies = st.sidebar.multiselect("약효분류(중복선택 가능)", sorted(efficacy_options))

# 약가 개수 필터
count_option = st.sidebar.radio(
    "약가 개수 기준",
    ("전체", "1개", "2개", "3개", "4개", "5개", "6~10개", "11~15개", "16~20개")
)

# --- 필터링 적용 ---
filtered_df = df.copy()

if selected_routes:
    filtered_df = filtered_df[filtered_df["투여경로"].isin(selected_routes)]

if selected_forms:
    filtered_df = filtered_df[filtered_df["제형명"].isin(selected_forms)]

if selected_efficacies:
    filtered_df = filtered_df[filtered_df["약효분류"].isin(selected_efficacies)]

if count_option == "1개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) == 2)
elif count_option == "2개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) == 3)
elif count_option == "3개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) == 4)
elif count_option == "4개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) == 5)
elif count_option == "5개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: len(x) == 6)
elif count_option == "6~10개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: 7 <= len(x) <= 11)
elif count_option == "11~15개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: 12 <= len(x) <= 16)
elif count_option == "16~20개":
    filtered_df = filtered_df.groupby("주성분코드").filter(lambda x: 17 <= len(x) <= 21)

# --- 결과 출력 항목 제한 ---
selected_columns = [
    "주성분코드", "제품코드", "제품명", "업체명", "규격", "단위", "상한금액", "전일", "약효분류"
]
result_df = filtered_df[selected_columns]

# --- 검색 요약 통계 ---
st.subheader("📈 검색 요약")
st.write(f"총 품목 수: {len(result_df):,}개")
st.write(f"총 성분 수: {result_df['주성분코드'].nunique():,}개")

# 상한금액 관련 통계 처리 (비어 있거나 숫자 아닌 경우 대비)
if not result_df.empty:
    try:
        result_df["상한금액"] = pd.to_numeric(result_df["상한금액"], errors="coerce")
        valid_prices = result_df["상한금액"].dropna()
        if not valid_prices.empty:
            st.write(f"상한금액 평균: {valid_prices.mean():,.0f} 원")
            st.write(f"상한금액 최대: {valid_prices.max():,} 원")
            st.write(f"상한금액 최소: {valid_prices.min():,} 원")
        else:
            st.warning("상한금액에 유효한 숫자 데이터가 없습니다.")
    except Exception as e:
        st.error(f"상한금액 통계 계산 중 오류 발생: {e}")

# --- 검색 결과 출력 ---
st.subheader("📋 검색 결과")
st.dataframe(result_df, use_container_width=True)

# --- 다운로드 옵션 ---
st.download_button(
    label="📥 결과 다운로드 (CSV)",
    data=result_df.to_csv(index=False, encoding="utf-8-sig"),
    file_name="성분_약가_검색결과.csv",
    mime="text/csv"
)


st.markdown("[👉 AI Pharma 네이버 카페 바로가기](https://cafe.naver.com/aipharma)")
