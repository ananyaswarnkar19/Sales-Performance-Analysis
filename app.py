import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}

.metric-container {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/Sample - Superstore.csv",
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df

df = load_data()

# =========================
# HEADER
# =========================
st.title("📊 Sales Performance Analysis Dashboard")
st.markdown("Interactive Business Intelligence Dashboard")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

# =========================
# KPI SECTION
# =========================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

st.subheader("📌 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    label="💰 Total Sales",
    value=f"${total_sales:,.0f}"
)

kpi2.metric(
    label="📈 Total Profit",
    value=f"${total_profit:,.0f}"
)

kpi3.metric(
    label="🛒 Total Orders",
    value=f"{total_orders:,}"
)

kpi4.metric(
    label="👥 Customers",
    value=f"{total_customers:,}"
)

st.divider()

# =========================
# MONTHLY SALES TREND
# =========================
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = (
    monthly_sales["Order Date"].astype(str)
)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# REGION ANALYSIS
# =========================
col1, col2 = st.columns(2)

with col1:

    st.subheader("🌎 Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Regional Sales"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# CATEGORY PIE CHART
# =========================
with col2:

    st.subheader("📦 Category Distribution")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.4,
        title="Sales by Category"
    )

    st.plotly_chart(fig3, use_container_width=True)

# =========================
# TOP PRODUCTS
# =========================
col3, col4 = st.columns(2)

with col3:

    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top Products"
    )

    st.plotly_chart(fig4, use_container_width=True)

# =========================
# TOP CUSTOMERS
# =========================
with col4:

    st.subheader("👤 Top 10 Customers")

    top_customers = (
        filtered_df
        .groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig5 = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Top Customers"
    )

    st.plotly_chart(fig5, use_container_width=True)

# =========================
# PROFIT VS DISCOUNT
# =========================
st.subheader("💹 Profit vs Discount Analysis")

fig6 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    hover_data=["Product Name"],
    title="Discount Impact on Profit"
)

st.plotly_chart(fig6, use_container_width=True)

# =========================
# SHIPPING MODE ANALYSIS
# =========================
st.subheader("🚚 Shipping Mode Analysis")

shipping_sales = (
    filtered_df
    .groupby("Ship Mode")["Sales"]
    .sum()
    .reset_index()
)

fig7 = px.bar(
    shipping_sales,
    x="Ship Mode",
    y="Sales",
    title="Sales by Shipping Mode"
)

st.plotly_chart(fig7, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "Developed by Ananya Kumari | Sales Performance Analysis Dashboard"
)