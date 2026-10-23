import streamlit as st
import pandas as pd

st.set_page_config(page_title="Niger Engagement App", page_icon="🇳🇬", layout="wide")

st.title("Niger Engagement App")
st.caption("Upload a spreadsheet and explore engagement insights quickly.")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"Loaded {len(df)} rows successfully.")

        st.subheader("Preview")
        st.dataframe(df.head(20), use_container_width=True)

        if df.empty:
            st.warning("The uploaded file is empty.")
            st.stop()

        st.subheader("Data Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Duplicate Rows", int(df.duplicated().sum()))

        st.subheader("Column Explorer")
        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        text_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

        if numeric_columns:
            selected_metric = st.selectbox("Select a numeric metric", numeric_columns)
            st.bar_chart(df[selected_metric].value_counts().head(10))

        if text_columns:
            selected_group = st.selectbox("Select a text column to group by", text_columns)
            grouped = df[selected_group].value_counts().head(10)
            st.bar_chart(grouped)

    except Exception as e:
        st.error(f"Could not read the file. Please upload a valid Excel or CSV file. Error: {e}")
else:
    st.info("Please upload a file to begin.")

    sample = pd.DataFrame(
        {
            "Region": ["North", "South", "East", "West", "Central"],
            "Engagement Score": [82, 74, 89, 76, 91],
            "Active Users": [1200, 980, 1430, 1100, 1650],
        }
    )

    st.subheader("Sample Dashboard")
    st.dataframe(sample, use_container_width=True)
    st.bar_chart(sample.set_index("Region")["Engagement Score"])

    st.caption("This app is ready to be deployed on Streamlit Cloud.")
