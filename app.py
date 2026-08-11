import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("sales1_data.csv")

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        dayfirst=True
    )

    df = df.dropna(subset=["date"])
    df = df.drop_duplicates()

    df["revenue"] = df["revenue"].fillna(df["revenue"].median())
    df["region"] = df["region"].str.strip().str.title()

    return df

df = load_data()

st.title("Sales Performance Dashboard")
st.write("Interactive dashboard showing sales revenue by date, category, and region.")

col1, col2, col3 = st.columns(3)

total_revenue = df["revenue"].sum()
avg_order = df["revenue"].mean()
order_count = len(df)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Average Order Value", f"${avg_order:,.2f}")
col3.metric("Total Orders", f"{order_count:,}")

st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date)
)

regions = st.sidebar.multiselect(
    "Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered_df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date) &
    (df["region"].isin(regions))
]

monthly = filtered_df.groupby(
    filtered_df["date"].dt.to_period("M")
)["revenue"].sum().reset_index()

monthly["date"] = monthly["date"].astype(str)

fig_trend = px.line(
    monthly,
    x="date",
    y="revenue",
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig_trend, use_container_width=True)

col_a, col_b = st.columns(2)

cat_totals = filtered_df.groupby("category")["revenue"].sum().reset_index()

fig_bar = px.bar(
    cat_totals,
    x="category",
    y="revenue",
    color="category",
    title="Revenue by Category"
)

col_a.plotly_chart(fig_bar, use_container_width=True)

region_totals = filtered_df.groupby("region")["revenue"].sum().reset_index()

fig_pie = px.pie(
    region_totals,
    names="region",
    values="revenue",
    title="Revenue Share by Region",
    hole=0.4
)

col_b.plotly_chart(fig_pie, use_container_width=True)

st.caption("Data source: sales1_data.csv")
st.caption('Data source: sales1_data.csv | Last updated: 2026-07-28') 




