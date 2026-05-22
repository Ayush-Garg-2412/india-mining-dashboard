import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('src')
from clean_data import load_and_clean

st.set_page_config(
    page_title="India Mining Intelligence Dashboard",
    page_icon="⛏️",
    layout="wide"
)

df = load_and_clean()

st.title("⛏️ India Mining Sector Intelligence Dashboard")
st.markdown("**Data:** Ministry of Statistics & Programme Implementation | **Period:** 2000-01 to 2015-16")
st.divider()

# ── KPI CARDS ───────────────────────────────────────────
st.subheader("Sector Overview")

col1, col2, col3, col4 = st.columns(4)

total_growth = ((df['All Minerals - Value'].iloc[-1] / df['All Minerals - Value'].iloc[0]) - 1) * 100
peak_year = df.loc[df['YoY_Growth_Pct'].idxmax(), 'Year_Label']
peak_growth = df['YoY_Growth_Pct'].max()
last_yoy = df['YoY_Growth_Pct'].iloc[-1]
coal_share = df['Coal_Share_Pct'].iloc[-1]

col1.metric("Total Value Growth (2000–2016)", f"{total_growth:.0f}%", "15-year period", delta_color="normal")
col2.metric("Peak Growth Year", peak_year, f"+{peak_growth:.1f}% YoY", delta_color="normal")
col3.metric("2015-16 YoY Growth", f"{last_yoy:.1f}%", "First decline in dataset", delta_color="inverse")
col4.metric("Coal Share of Fuel Value", f"{coal_share:.1f}%", "2015-16", delta_color="off")

st.divider()

# ── SECTION 1: TOTAL VALUE TREND ────────────────────────
st.subheader("Total Mining Value Trend (2000–2016)")

fig1 = px.line(
    df,
    x='Year_Label',
    y='All Minerals - Value',
    markers=True,
    labels={'Year_Label': 'Year', 'All Minerals - Value': 'Total Value (₹)'},
    color_discrete_sequence=['#1f77b4']
)
fig1.update_layout(xaxis_tickangle=-45, hovermode='x unified', height=420)

# Correct annotations pointing to actual data points
peak_val = df.loc[df['Year_Label']=='2008-09', 'All Minerals - Value'].values[0]
last_val = df.loc[df['Year_Label']=='2015-16', 'All Minerals - Value'].values[0]

fig1.add_annotation(
    x='2008-09', y=peak_val,
    text="Commodity Supercycle Peak<br>+43% YoY",
    showarrow=True, arrowhead=2, arrowcolor='orange',
    ax=40, ay=-60,
    bgcolor='orange', font=dict(color='white', size=11),
    bordercolor='orange'
)
fig1.add_annotation(
    x='2015-16', y=last_val,
    text="First Decline<br>-1.4% YoY",
    showarrow=True, arrowhead=2, arrowcolor='red',
    ax=40, ay=-60,
    bgcolor='red', font=dict(color='white', size=11),
    bordercolor='red'
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ── SECTION 2: SECTOR BREAKDOWN ─────────────────────────
st.subheader("Fuels vs Metallic Sector Value Over Time")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df['Year_Label'], y=df['Fuels_Total_Value'],
    name='Fuels', mode='lines+markers',
    line=dict(color='#ff7f0e', width=2)
))
fig2.add_trace(go.Scatter(
    x=df['Year_Label'], y=df['Metallic_Total_Value'],
    name='Metallic Minerals', mode='lines+markers',
    line=dict(color='#2ca02c', width=2)
))
fig2.update_layout(
    xaxis_tickangle=-45,
    hovermode='x unified',
    height=420,
    yaxis_title='Value (₹)',
    xaxis_title='Year'
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── SECTION 3: MINERAL SELECTOR ─────────────────────────
st.subheader("Mineral Production Explorer")

mineral_options = {
    'Coal (th. tonnes)': 'Fuels - Coal - Quantity (th.tonne)',
    'Iron Ore (th. tonnes)': 'Metallic - Iron Ore - Quantity (th.Tonne)',
    'Bauxite (th. tonnes)': 'Metallic - Bauxite - Quantity (th.tonne)',
    'Manganese Ore (th. tonnes)': 'Metallic - Manganese Ore - Quantity (th.tonne)',
    'Gold (kg)': 'Metallic - Gold - Quantity (Kilogram)',
    'Zinc Concentrates (tonnes)': 'Metallic - Zinc Concetrates - Quantity (tonne)',
    'Lead Concentrate (tonnes)': 'Metallic - Lead Concentrate - Quantity (tonne)',
}

selected_mineral = st.selectbox("Select a mineral to explore:", list(mineral_options.keys()))
col = mineral_options[selected_mineral]

fig3 = px.bar(
    df, x='Year_Label', y=col,
    labels={'Year_Label': 'Year', col: selected_mineral},
    color_discrete_sequence=['#9467bd']
)
fig3.update_layout(xaxis_tickangle=-45, height=420)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── SECTION 4: YOY GROWTH ───────────────────────────────
st.subheader("Year-over-Year Growth in Total Mining Value")

yoy_data = df.dropna(subset=['YoY_Growth_Pct'])
colors = ['#d62728' if x < 0 else '#1f77b4' for x in yoy_data['YoY_Growth_Pct']]

fig4 = go.Figure(go.Bar(
    x=yoy_data['Year_Label'],
    y=yoy_data['YoY_Growth_Pct'],
    marker_color=colors,
    text=yoy_data['YoY_Growth_Pct'].apply(lambda x: f"{x:.1f}%"),
    textposition='outside'
))
fig4.update_layout(
    xaxis_tickangle=-45,
    yaxis_title='YoY Growth (%)',
    xaxis_title='Year',
    height=420,
    yaxis=dict(range=[-10, 55])
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── SECTION 5: KEY INSIGHTS ─────────────────────────────
st.subheader("Key Analytical Insights")

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.info("**Fuel Dominance**\n\nFuels consistently account for ~70% of total mining value, with coal alone representing 48% of fuel value — highlighting India's heavy dependence on coal for energy security.")

with insight2:
    st.warning("**Supercycle Sensitivity**\n\nThe 2008-09 commodity supercycle drove a 43% YoY spike — the highest in the dataset. This sensitivity to global commodity cycles is a key strategic risk for India's mining sector.")

with insight3:
    st.error("**Post-2012 Slowdown**\n\nGrowth slowed sharply after 2012 and turned negative in 2015-16, coinciding with the global commodity downturn and domestic policy uncertainty in mining allocations.")

st.divider()
st.caption("Built by Ayush Garg | India Mining Sector Intelligence Dashboard | Data: data.gov.in / Ministry of Statistics & Programme Implementation")