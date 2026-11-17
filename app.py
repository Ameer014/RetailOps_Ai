import streamlit as st
import pandas as pd

from utils.data_loader import (
    load_dataset,
    get_dataset_summary
)

from database.db import save_dataframe

from analytics.sales import calculate_sales_metrics

from components.charts import create_category_chart

from agent.graph import ask_agent


st.set_page_config(
    page_title="RetailOps AI",
    page_icon="📊",
    layout="wide"
)


st.title("📊 RetailOps AI")

st.caption(
    "Agentic AI-powered Business Intelligence Platform"
)


# Sidebar

st.sidebar.title("RetailOps AI")

st.sidebar.write("Business Intelligence Assistant")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)


if uploaded_file:

    try:

        df = load_dataset(uploaded_file)

        save_dataframe(df)

        st.sidebar.success("Dataset uploaded successfully!")

        st.session_state["dataset"] = df

    except Exception as e:

        st.error(str(e))


if "dataset" not in st.session_state:

    st.info("Upload a CSV dataset to begin.")

    st.stop()


df = st.session_state["dataset"]


# Dashboard

st.subheader("Business Overview")

metrics = calculate_sales_metrics(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{metrics['total_records']:,}"
)

col2.metric(
    "Total Revenue",
    f"₹{metrics.get('total_revenue', 0):,.2f}"
)

col3.metric(
    "Average Price",
    f"₹{metrics.get('average_price', 0):,.2f}"
)

col4.metric(
    "Total Orders",
    f"{metrics.get('total_orders', 0):,}"
)


st.divider()


# Dataset Explorer

st.subheader("Dataset Explorer")

st.dataframe(
    df.head(100),
    use_container_width=True
)


with st.expander("Dataset Information"):

    st.json(get_dataset_summary(df))


# Charts

st.subheader("Business Analytics")

chart = create_category_chart(df)

if chart:

    st.plotly_chart(
        chart,
        use_container_width=True
    )

else:

    st.info(
        "Category chart requires product_category_name and price columns."
    )


st.divider()


# AI Analyst

st.subheader("🤖 Ask RetailOps AI")

question = st.chat_input(
    "Ask a business question about your dataset..."
)


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


for role, message in st.session_state.chat_history:

    with st.chat_message(role):

        st.markdown(message)


if question:

    st.session_state.chat_history.append(
        ("user", question)
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analysing your business data..."):

            try:

                answer = ask_agent(question)

                st.markdown(answer)

                st.session_state.chat_history.append(
                    ("assistant", answer)
                )

            except Exception as e:

                st.error(f"Agent error: {e}")