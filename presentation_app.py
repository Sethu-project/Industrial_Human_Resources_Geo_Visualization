import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv(r"D:\GUVI DS 2025\Industrial HR Geo Project\cleaned_data_final.csv")

# Clean district code safely
df["district_code"] = (
    df["district_code"]
    .astype(str)
    .str.replace("`", "", regex=False)
    .str.strip()
)

st.title(" Indian Workforce Industrial Analytics Dashboard ")

# =====================================================
# NATIONAL SUMMARY (NO FILTERING)
# =====================================================

col1, col2, col3, col4,col5 = st.columns(5)

col1.metric("Total Workers", f"{df['total_workers'].sum():,}")
col2.metric("Male Workers", f"{df['male_total'].sum():,}")
col3.metric("Female Workers", f"{df['female_total'].sum():,}")
col4.metric("Rural Workers", f"{df['rural_total'].sum():,}")
col5.metric("Urban Workers", f"{df['urban_total'].sum():,}")

st.markdown("---")

# =====================================================
# INDUSTRY DISTRIBUTION
# =====================================================

industry_summary = (
    df.groupby("industry_sector")["total_workers"]
    .sum()
    .reset_index()
    .sort_values(by="total_workers", ascending=False)
)

fig1 = px.bar(
    industry_summary,
    x="industry_sector",
    y="total_workers",
    text_auto=True,
    template="plotly_white",
    title="Industry-wise Workforce Distribution (India)"
)

fig1.update_layout(xaxis_tickangle=45)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# GENDER DOMINANT INDUSTRY
# =====================================================

st.subheader("👩‍💼 Gender-wise Dominant Industry")

gender_option = st.selectbox("Select Gender", ["Male", "Female"])

metric_column = "male_total" if gender_option == "Male" else "female_total"

gender_industry = (
    df.groupby("industry_sector")[metric_column]
    .sum()
    .reset_index()
    .sort_values(by=metric_column, ascending=False)
)

dominant = gender_industry.iloc[0]["industry_sector"]

st.write(f"🔎 Dominant Industry for {gender_option}: **{dominant}**")

fig2 = px.bar(
    gender_industry,
    x="industry_sector",
    y=metric_column,
    text_auto=True,
    template="plotly_white"
)

fig2.update_layout(xaxis_tickangle=45)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# INDUSTRY BREAKDOWN
# =====================================================

st.subheader("🏭 Industry Workforce Breakdown")

industry_selected = st.selectbox(
    "Select Industry",
    sorted(df["industry_sector"].unique())
)

industry_data = df[df["industry_sector"] == industry_selected]

col1, col2 = st.columns(2)

gender_df = pd.DataFrame({
    "Category": ["Male", "Female"],
    "Workers": [
        industry_data["male_total"].sum(),
        industry_data["female_total"].sum()
    ]
})

fig3 = px.bar(
    gender_df,
    x="Category",
    y="Workers",
    text_auto=True,
    template="plotly_white",
    title=f"{industry_selected} - Gender Distribution"
)

col1.plotly_chart(fig3, use_container_width=True)

geo_df = pd.DataFrame({
    "Category": ["Rural", "Urban"],
    "Workers": [
        industry_data["rural_total"].sum(),
        industry_data["urban_total"].sum()
    ]
})

fig4 = px.bar(
    geo_df,
    x="Category",
    y="Workers",
    text_auto=True,
    template="plotly_white",
    title=f"{industry_selected} - Rural vs Urban Distribution"
)

col2.plotly_chart(fig4, use_container_width=True)

# =====================================================
# STATE-WISE INDUSTRY ANALYSIS
# =====================================================

st.markdown("---")
st.subheader("📍 State & District-wise Industry Analysis")

# State dropdown
selected_state = st.selectbox(
    "Select State for Industry Analysis",
    sorted(df["state"].unique())
)

# Filter state data
state_data = df[df["state"] == selected_state]

if state_data.empty:
    st.warning("No data available for selected state.")
else:

    # Aggregate industry totals for that state
    state_industry = (
        state_data.groupby("industry_sector")["total_workers"]
        .sum()
        .reset_index()
        .sort_values(by="total_workers", ascending=False)
    )

    col1, col2 = st.columns(2)

    # ---------------- Bar Chart ----------------
    fig_bar = px.bar(
        state_industry,
        x="industry_sector",
        y="total_workers",
        text_auto=True,
        template="plotly_white",
        title=f"{selected_state} - Industry Distribution"
    )

    fig_bar.update_layout(xaxis_tickangle=45)

    col1.plotly_chart(fig_bar, use_container_width=True)

    # ---------------- Pie Chart ----------------
    fig_pie = px.pie(
        state_industry,
        names="industry_sector",
        values="total_workers",
        hole=0.5,
        template="plotly_white",
        title=f"{selected_state} - Industry Share (%)"
    )

    col2.plotly_chart(fig_pie, use_container_width=True)

    # ---------------- Dominant Industry Insight ----------------
    dominant_industry = state_industry.iloc[0]["industry_sector"]

    st.success(
        f"🔎 Dominant Industry in {selected_state}: {dominant_industry}"
    )