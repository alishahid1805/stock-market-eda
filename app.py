
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Stock Market EDA", layout="wide")
st.title("Stock Market EDA Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.subheader("Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        missing.plot(kind="bar", ax=ax, color="tomato")
        ax.set_ylabel("Missing Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.success("No missing values found!")

    st.subheader("Category Distribution")
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    if cat_cols:
        selected_col = st.selectbox("Select column", cat_cols)
        counts = df[selected_col].fillna("Missing").value_counts().head(15)

        fig, ax = plt.subplots(figsize=(10, 4))
        counts.plot(kind="bar", ax=ax, color="steelblue")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include="all").T)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "stock_market_data.csv",
        "text/csv"
    )
else:
    st.info("Please upload symbols_valid_meta.csv to start EDA.")
