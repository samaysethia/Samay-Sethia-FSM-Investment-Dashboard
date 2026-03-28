import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Geopolitical Financial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Bloomberg-style
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-card: #111827;
    --bg-card2: #1a2235;
    --accent-gold: #f0b429;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #1e293b;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp { background-color: var(--bg-primary); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #111827 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent-gold);
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--text-secondary);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.metric-delta-pos { color: var(--accent-green); font-size: 13px; font-family: 'IBM Plex Mono', monospace; }
.metric-delta-neg { color: var(--accent-red); font-size: 13px; font-family: 'IBM Plex Mono', monospace; }

/* Section headers */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--accent-gold);
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin-bottom: 20px;
    margin-top: 10px;
}

/* Traffic light badges */
.badge-buy { background: #064e3b; color: #10b981; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.badge-neutral { background: #451a03; color: #f59e0b; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.badge-reduce { background: #450a0a; color: #ef4444; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    color: var(--text-secondary) !important;
    background: transparent;
    border-radius: 6px;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-gold) !important;
    color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY DARK TEMPLATE
# ─────────────────────────────────────────────
TEMPLATE = go.layout.Template()
TEMPLATE.layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='IBM Plex Sans', color='#94a3b8', size=12),
    title_font=dict(family='IBM Plex Mono', color='#f1f5f9', size=13),
    xaxis=dict(gridcolor='#1e293b', linecolor='#1e293b', tickcolor='#1e293b', zerolinecolor='#1e293b'),
    yaxis=dict(gridcolor='#1e293b', linecolor='#1e293b', tickcolor='#1e293b', zerolinecolor='#1e293b'),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1e293b'),
    colorway=['#f0b429','#10b981','#3b82f6','#8b5cf6','#ef4444','#06b6d4','#f97316'],
    margin=dict(l=10, r=10, t=40, b=10),
)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
gdp_data = pd.DataFrame({
    'Country': ['India','China','Indonesia','Brazil','United States','Mexico','Saudi Arabia','World','Euro Area','Germany','Japan','UK'],
    'GDP_2026': [7.3, 4.5, 5.1, 2.2, 2.7, 1.4, 2.5, 3.3, 1.3, 0.2, 1.1, 1.5],
    'GDP_2025': [6.8, 4.8, 5.0, 2.1, 2.8, 1.6, 2.6, 3.3, 0.9, 0.0, 0.2, 0.9],
    'Region': ['Asia','Asia','Asia','Americas','Americas','Americas','Middle East','Global','Europe','Europe','Asia','Europe']
})
gdp_data['color'] = gdp_data['GDP_2026'].apply(
    lambda x: '#10b981' if x >= 5 else ('#f0b429' if x >= 2 else '#ef4444')
)

oil_months = ['Jan 26','Feb 26','Mar 26 (est)']
oil_prices = [60.2, 85.4, 119.0]

sector_data = pd.DataFrame({
    'Sector': ['Energy (XLE)','Defense','Gold (GLD)','Materials','Healthcare','S&P 500','Technology','Consumer Disc.','Airlines','Utilities'],
    'YTD_Return': [34.0, 22.5, 18.3, 12.1, 5.4, 3.2, -4.1, -7.8, -18.5, 1.2],
    'Signal': ['BUY','BUY','BUY','BUY','NEUTRAL','NEUTRAL','NEUTRAL','REDUCE','REDUCE','NEUTRAL']
})
sector_data['color'] = sector_data['YTD_Return'].apply(
    lambda x: '#10b981' if x > 10 else ('#f0b429' if x >= 0 else '#ef4444')
)

asset_heatmap = pd.DataFrame({
    'Asset': ['Brent Crude','Gold','US Defense ETF','Energy Equities','DXY Dollar','EM Bonds','Shipping (BDRY)','Tech Growth','EM Currencies','High Yield'],
    'Performance': [97.7, 18.3, 22.5, 34.0, 6.2, -3.1, -14.2, -4.1, -11.3, -2.0],
    'Geopolitical_Sensitivity': [9.5, 8.7, 9.2, 8.9, 7.5, 7.0, 8.5, 4.2, 7.8, 5.0],
    'Category': ['Commodity','SafeHaven','Equity','Equity','Currency','Bond','Commodity','Equity','Currency','Bond']
})

country_vuln = pd.DataFrame({
    'Country': ['India','Brazil','Indonesia','Germany','Japan','Turkey','South Africa','Vietnam','Mexico','Egypt'],
    'Trade_Openness': [22, 25, 38, 71, 32, 52, 60, 185, 68, 35],
    'Energy_Import_Dep': [30, -5, 45, 62, 88, 75, 25, 70, -10, 88],
    'GDP_Size': [3.9, 2.1, 1.4, 4.7, 4.2, 1.1, 0.4, 0.4, 1.4, 0.4],
    'Risk_Score': [3, 4, 6, 7, 8, 9, 8, 7, 4, 9]
})

scenario_data = {
    'Base Case (60%)': {'Oil': '$105–$115', 'Equities': 'Range-bound +2–5%', 'Inflation': '3.5–4.0%', 'EM': 'Selective positive', 'Color': '#f0b429'},
    'Bull Case (20%)': {'Oil': '$80–$95', 'Equities': 'Rally +10–15%', 'Inflation': '2.8–3.2%', 'EM': 'Broad positive', 'Color': '#10b981'},
    'Bear Case (20%)': {'Oil': '$130–$160+', 'Equities': 'Correction –10–20%', 'Inflation': '5.0–6.5%', 'EM': 'Severe outflows', 'Color': '#ef4444'},
}

portfolio_alloc = pd.DataFrame({
    'Asset': ['Energy','Defense','Commodities','Gold','Technology','EM Equities','Bonds','Cash'],
    'Weight': [25, 15, 12, 10, 15, 10, 8, 5],
    'Stance': ['OW','OW','OW','OW','UW','UW','N','N']
})

sector_signals = [
    ("Energy", "BUY", "+34% YTD, structural risk premium"),
    ("Defense", "BUY", "NATO spending mandate, $2T pipeline"),
    ("Gold", "BUY", "Safe haven + inflation hedge"),
    ("Commodities", "BUY", "Supply disruption, EM demand"),
    ("Healthcare", "NEUTRAL", "Defensive, rate-resilient"),
    ("Utilities", "NEUTRAL", "Dividend yield supportive"),
    ("Technology", "NEUTRAL", "Valuation compressed, selective"),
    ("Financials", "NEUTRAL", "Rate environment mixed"),
    ("Consumer Disc.", "REDUCE", "Demand squeeze, high fuel costs"),
    ("Airlines", "REDUCE", "Fuel cost -18% YTD, margin risk"),
    ("Real Estate", "REDUCE", "Rate sensitivity, dollar pressure"),
    ("EM ex-India", "REDUCE", "Dollar strength, trade fragmentation"),
]

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px 0'>
        <div style='font-family:IBM Plex Mono;font-size:10px;letter-spacing:3px;color:#f0b429;text-transform:uppercase'>Investment Intelligence</div>
        <div style='font-size:18px;font-weight:700;margin-top:4px'>Geopolitical<br>Market Monitor</div>
        <div style='font-family:IBM Plex Mono;font-size:10px;color:#475569;margin-top:4px'>Q1 2026 | Samay Sethia</div>
    </div>
    <hr style='border-color:#1e293b;margin:12px 0'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-family:IBM Plex Mono;font-size:10px;letter-spacing:2px;color:#94a3b8;text-transform:uppercase;margin-bottom:8px'>Live Data Points</div>", unsafe_allow_html=True)

    for label, val, delta, pos in [
        ("Brent Crude", "$119.0", "▲ +97.7% YTD", True),
        ("World GDP", "3.3%", "— Stable vs 2025", True),
        ("Global Inflation", "3.8%", "▼ -0.3pp from 2025", True),
        ("DXY Dollar", "106.4", "▲ +6.2% YTD", True),
        ("Gold", "$3,124", "▲ +18.3% YTD", True),
        ("India GDP (FY26)", "7.3%", "▲ +0.5pp upgrade", True),
    ]:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{val}</div>
            <div class='{"metric-delta-pos" if pos else "metric-delta-neg"}'>{delta}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <hr style='border-color:#1e293b;margin:12px 0'>
    <div style='font-family:IBM Plex Mono;font-size:9px;color:#334155;letter-spacing:1px'>
    SOURCES: IMF WEO Jan 2026 · Reuters · World Bank · EIA<br>
    Dashboard: Samay Sethia · MS25GF129<br>
    Subject: Financial Systems & Markets<br>
    Advisor: Dr. Nathaniel Christopher
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style='padding: 24px 0 8px 0'>
    <div style='font-family:IBM Plex Mono;font-size:11px;letter-spacing:3px;color:#f0b429;text-transform:uppercase'>Investment Research Memo — Q1 2026</div>
    <h1 style='font-size:36px;font-weight:700;margin:4px 0 4px 0;line-height:1.1'>Global Geopolitical Impact<br>on Financial Markets</h1>
    <div style='color:#94a3b8;font-size:14px'>Structural fragmentation analysis • Cross-asset implications • 3–6 month forward outlook</div>
</div>
<hr style='border-color:#1e293b;margin:4px 0 20px 0'>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 MACRO OVERVIEW",
    "⚡ ENERGY & COMMODITIES",
    "🌐 CROSS-ASSET",
    "🗺️ COUNTRY DIVERGENCE",
    "🎯 STRATEGY & OUTLOOK"
])

# ═══════════════════════════════════════════
# TAB 1 — MACRO OVERVIEW
# ═══════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>01 — Macroeconomic Environment 2026</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("World GDP Growth", "3.3%", "▲ Stable vs 2025", "IMF WEO Jan 2026"),
        ("Global Inflation", "3.8%", "▼ Easing from 4.1%", "IMF 2026 Projection"),
        ("Oil Risk Premium", "$10–25/bbl", "▲ Structural", "Reuters / Allianz 2026"),
        ("India Growth (FY26)", "7.3%", "▲ Fastest Major Economy", "Reuters / IMF Upgrade"),
    ]
    for col, (label, val, delta, src) in zip([col1,col2,col3,col4], kpis):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{val}</div>
                <div class='metric-delta-pos'>{delta}</div>
                <div style='font-size:9px;color:#334155;margin-top:6px;font-family:IBM Plex Mono'>{src}</div>
            </div>
            """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        gdp_sorted = gdp_data.sort_values('GDP_2026', ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=gdp_sorted['Country'], x=gdp_sorted['GDP_2025'],
            name='2025 Actual', orientation='h',
            marker_color='#1e293b', marker_line=dict(color='#334155', width=1)
        ))
        fig.add_trace(go.Bar(
            y=gdp_sorted['Country'], x=gdp_sorted['GDP_2026'],
            name='2026 Forecast', orientation='h',
            marker_color=gdp_sorted['color'].values,
            marker_line=dict(color='rgba(0,0,0,0)', width=0)
        ))
        fig.add_vline(x=3.3, line_dash="dot", line_color="#f0b429",
                     annotation_text="World Avg 3.3%",
                     annotation_font=dict(color="#f0b429", size=10))
        fig.update_layout(template=TEMPLATE, title="GDP Growth Forecast 2026 (%) — IMF WEO",
                         barmode='overlay', height=420, legend=dict(orientation='h', y=1.05))
        fig.update_xaxes(title_text="GDP Growth (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        inflation_data = pd.DataFrame({
            'Year': ['2022','2023','2024','2025','2026F','2027F'],
            'Global': [8.7, 6.9, 5.7, 4.1, 3.8, 3.4],
            'Advanced': [7.3, 4.6, 2.8, 2.2, 2.0, 1.9],
            'Emerging': [9.9, 8.5, 7.8, 5.6, 4.9, 4.2],
        })
        fig2 = go.Figure()
        for col_name, color, dash in [('Global','#f0b429','solid'),('Advanced','#10b981','dot'),('Emerging','#ef4444','dash')]:
            fig2.add_trace(go.Scatter(x=inflation_data['Year'], y=inflation_data[col_name],
                mode='lines+markers', name=col_name, line=dict(color=color, width=2, dash=dash),
                marker=dict(size=7)))
        fig2.update_layout(template=TEMPLATE, title="Global Inflation Trajectory (%)", height=200,
                          legend=dict(orientation='h', y=1.08), margin=dict(l=10,r=10,t=40,b=10))
        st.plotly_chart(fig2, use_container_width=True)

        geo_drivers = pd.DataFrame({'Factor': ['Energy Shock','Trade Fragmentation','Defense Spend','Supply Chain','Currency Risk'],
                                    'Intensity': [9.2, 8.1, 7.5, 7.8, 6.9]})
        fig3 = go.Figure(go.Bar(x=geo_drivers['Intensity'], y=geo_drivers['Factor'],
            orientation='h', marker_color=['#ef4444','#f0b429','#f0b429','#f97316','#3b82f6'],
            text=geo_drivers['Intensity'], textposition='outside', textfont=dict(color='#94a3b8', size=10)))
        fig3.update_layout(template=TEMPLATE, title="Geopolitical Risk Intensity (0–10)", height=200,
                          xaxis=dict(range=[0,11], showgrid=False))
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='section-header'>Transmission Channels — Geopolitics → Markets</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    channels = [
        ("💥 Inflation Channel", "Energy price shocks → CPI surge. +10% oil = +0.4pp inflation (IMF)", "#ef4444"),
        ("📉 Growth Channel", "Trade fragmentation → Productivity loss. Supply chain rewiring = permanent cost tax", "#f97316"),
        ("🏛️ Fiscal Channel", "Defense + subsidies → Deficits → Higher sovereign yields → Crowding out private capex", "#f0b429"),
        ("💱 Currency Channel", "Uncertainty → USD safe haven flows → EM currency pressure → External debt stress", "#3b82f6"),
    ]
    for col, (title, desc, color) in zip([c1,c2,c3,c4], channels):
        with col:
            st.markdown(f"""
            <div style='background:{color}15;border:1px solid {color}40;border-radius:8px;padding:16px;height:140px'>
                <div style='font-size:13px;font-weight:700;color:{color};margin-bottom:8px'>{title}</div>
                <div style='font-size:12px;color:#94a3b8;line-height:1.5'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# TAB 2 — ENERGY & COMMODITIES
# ═══════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>02 — Energy Markets & Geopolitical Risk Premium</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])
    with col1:
        months_ext = ['Jan 26','Feb 26','Mar 26']
        brent = [60.2, 85.4, 119.0]
        fundamental = [58.0, 62.0, 66.0]
        geo_premium = [b - f for b, f in zip(brent, fundamental)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_ext, y=fundamental, fill='tozeroy',
            name='Fundamental Value', line=dict(color='#3b82f6', width=2),
            fillcolor='rgba(59,130,246,0.15)'))
        fig.add_trace(go.Scatter(x=months_ext, y=brent, fill='tonexty',
            name='Brent Crude (Actual)', line=dict(color='#f0b429', width=3),
            fillcolor='rgba(240,180,41,0.2)'))
        fig.add_trace(go.Scatter(x=months_ext, y=[80,90,104],
            name='Bear Scenario', line=dict(color='#10b981', width=1, dash='dot'), mode='lines'))
        fig.add_trace(go.Scatter(x=months_ext+['Apr 26','May 26','Jun 26'],
            y=[60.2,85.4,119.0,130,145,160],
            name='Bull Escalation', line=dict(color='#ef4444', width=1, dash='dash'), mode='lines'))
        for i, (m, b, g) in enumerate(zip(months_ext, brent, geo_premium)):
            fig.add_annotation(x=m, y=b+3, text=f"${b} (+${g:.0f} geo)", showarrow=False,
                             font=dict(size=10, color='#f0b429'), bgcolor='rgba(0,0,0,0.6)')
        fig.update_layout(template=TEMPLATE, title="Brent Crude: Actual vs Fundamental Value ($/bbl)",
                         height=360, yaxis_title="$/bbl",
                         legend=dict(orientation='h', y=1.05))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        waterfall_x = ['Supply/Demand\nFundamental','OPEC+\nDiscipline','Strait of\nHormuz Risk','Russia\nExport Risk','Iran\nSanctions','Current\nBrent Price']
        waterfall_y = [66, 10, 15, 12, 16, 0]
        measures = ['absolute','relative','relative','relative','relative','total']
        fig_wf = go.Figure(go.Waterfall(
            name="Oil Price Build", orientation="v",
            measure=measures, x=waterfall_x, y=waterfall_y,
            connector=dict(line=dict(color='#334155')),
            decreasing=dict(marker=dict(color='#ef4444')),
            increasing=dict(marker=dict(color='#10b981')),
            totals=dict(marker=dict(color='#f0b429')),
            text=[f"${v}" for v in [66,10,15,12,16,119]],
            textposition='outside', textfont=dict(color='#94a3b8', size=10)
        ))
        fig_wf.update_layout(template=TEMPLATE, title="Oil Price Decomposition ($/bbl)",
                            height=360, showlegend=False,
                            yaxis=dict(range=[0,140]))
        st.plotly_chart(fig_wf, use_container_width=True)

    col3, col4 = st.columns([3,2])
    with col3:
        sector_sorted = sector_data.sort_values('YTD_Return')
        fig_sec = go.Figure(go.Bar(
            x=sector_sorted['YTD_Return'], y=sector_sorted['Sector'],
            orientation='h', marker_color=sector_sorted['color'].tolist(),
            text=[f"{v:+.1f}%" for v in sector_sorted['YTD_Return']],
            textposition='outside', textfont=dict(color='#94a3b8', size=11)
        ))
        fig_sec.add_vline(x=0, line_color='#334155', line_width=1)
        fig_sec.update_layout(template=TEMPLATE, title="YTD Sector Performance 2026 (%)",
                             height=380, xaxis=dict(range=[-25,45], title="YTD Return (%)"))
        st.plotly_chart(fig_sec, use_container_width=True)

    with col4:
        supply_chain_data = pd.DataFrame({
            'Route': ['Strait of Hormuz','Suez Canal','Red Sea','Panama Canal','Malacca Strait'],
            'Disruption_Risk': [9.5, 8.2, 9.0, 5.5, 6.0],
            'Oil_Flow_MBPD': [21, 5, 4, 0.2, 15],
            'Status': ['Critical','High','High','Moderate','Moderate']
        })
        fig_sc = go.Figure()
        colors_sc = {'Critical':'#ef4444','High':'#f0b429','Moderate':'#3b82f6'}
        for status, group in supply_chain_data.groupby('Status'):
            fig_sc.add_trace(go.Scatter(
                x=group['Disruption_Risk'], y=group['Oil_Flow_MBPD'],
                mode='markers+text', name=status,
                marker=dict(size=(group['Oil_Flow_MBPD']*1.5).tolist(), color=colors_sc[status], opacity=0.85,
                           line=dict(color='#0a0e1a', width=2)),
                text=group['Route'], textposition='top center',
                textfont=dict(size=9, color='#94a3b8')
            ))
        fig_sc.update_layout(template=TEMPLATE, title="Supply Chain Chokepoints",
                            xaxis_title="Disruption Risk (0–10)", yaxis_title="Oil Flow (mln bbl/day)",
                            height=380)
        st.plotly_chart(fig_sc, use_container_width=True)

# ═══════════════════════════════════════════
# TAB 3 — CROSS ASSET
# ═══════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>03 — Cross-Asset Market Implications</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        fig_scatter = go.Figure()
        cat_colors = {'Commodity':'#f0b429','SafeHaven':'#10b981','Equity':'#3b82f6','Currency':'#8b5cf6','Bond':'#94a3b8'}
        for cat, group in asset_heatmap.groupby('Category'):
            fig_scatter.add_trace(go.Scatter(
                x=group['Geopolitical_Sensitivity'], y=group['Performance'],
                mode='markers+text', name=cat,
                marker=dict(size=18, color=cat_colors[cat], opacity=0.85,
                           line=dict(color='#0a0e1a', width=2)),
                text=group['Asset'], textposition='top center',
                textfont=dict(size=9, color='#94a3b8')
            ))
        fig_scatter.add_hline(y=0, line_dash="dot", line_color="#334155")
        fig_scatter.add_vrect(x0=7, x1=10, fillcolor="rgba(239,68,68,0.06)", line_width=0,
                             annotation_text="High Geo Risk Zone",
                             annotation_font=dict(color="#ef4444", size=9))
        fig_scatter.update_layout(template=TEMPLATE,
            title="Asset Class: Geopolitical Sensitivity vs YTD Performance",
            xaxis_title="Geopolitical Sensitivity (0–10)",
            yaxis_title="YTD Performance (%)", height=420,
            legend=dict(orientation='h', y=1.05))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        gold_oil_months = ['Jan','Feb','Mar']
        gold_prices = [2640, 2890, 3124]
        oil_prices_go = [60.2, 85.4, 119.0]
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        fig_dual.add_trace(go.Scatter(x=gold_oil_months, y=gold_prices, name='Gold ($/oz)',
            line=dict(color='#f0b429', width=2.5), mode='lines+markers', marker=dict(size=8)), secondary_y=False)
        fig_dual.add_trace(go.Scatter(x=gold_oil_months, y=oil_prices_go, name='Brent ($/bbl)',
            line=dict(color='#ef4444', width=2.5, dash='dash'), mode='lines+markers', marker=dict(size=8)), secondary_y=True)
        fig_dual.update_layout(template=TEMPLATE, title="Gold vs Brent: Safe Haven Correlation",
                            height=200, legend=dict(orientation='h', y=1.08))
        fig_dual.update_yaxes(title_text="Gold ($/oz)", secondary_y=False, title_font=dict(color='#f0b429'))
        fig_dual.update_yaxes(title_text="Brent ($/bbl)", secondary_y=True, title_font=dict(color='#ef4444'))
        st.plotly_chart(fig_dual, use_container_width=True)

        risk_on = ['Equities','EM Assets','High Yield','Commodities']
        risk_off = ['Gold','USD','US Treasuries','Defense Stocks']
        st.markdown("""
        <div style='background:#111827;border:1px solid #1e293b;border-radius:8px;padding:16px;margin-top:4px'>
            <div style='font-family:IBM Plex Mono;font-size:9px;letter-spacing:2px;color:#94a3b8;text-transform:uppercase;margin-bottom:10px'>Capital Rotation Map</div>
            <div style='display:flex;gap:12px'>
                <div style='flex:1'>
                    <div style='color:#ef4444;font-size:11px;font-weight:600;margin-bottom:6px'>⬇ RISK-OFF OUTFLOWS</div>
                    """ + "".join([f"<div style='font-size:11px;color:#94a3b8;padding:3px 0;border-bottom:1px solid #1e293b'>{r}</div>" for r in risk_on]) + """
                </div>
                <div style='width:1px;background:#1e293b'></div>
                <div style='flex:1'>
                    <div style='color:#10b981;font-size:11px;font-weight:600;margin-bottom:6px'>⬆ SAFE HAVEN INFLOWS</div>
                    """ + "".join([f"<div style='font-size:11px;color:#94a3b8;padding:3px 0;border-bottom:1px solid #1e293b'>{r}</div>" for r in risk_off]) + """
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Equity Risk Premium — Valuation Regime Shift</div>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        erp_years = ['2018','2019','2020','2021','2022','2023','2024','2025','2026F']
        erp_values = [3.2, 3.4, 4.8, 2.9, 5.8, 4.9, 4.2, 5.1, 6.0]
        rfr_values = [2.8, 2.1, 0.6, 1.5, 4.5, 5.2, 4.8, 4.3, 4.5]
        fig_erp = go.Figure()
        fig_erp.add_trace(go.Scatter(x=erp_years, y=rfr_values, fill='tozeroy', name='Risk Free Rate',
            line=dict(color='#3b82f6',width=2), fillcolor='rgba(59,130,246,0.15)'))
        fig_erp.add_trace(go.Scatter(x=erp_years, y=[e+r for e,r in zip(erp_values, rfr_values)],
            fill='tonexty', name='+ Equity Risk Premium', line=dict(color='#f0b429',width=2),
            fillcolor='rgba(240,180,41,0.2)'))
        fig_erp.update_layout(template=TEMPLATE, title="Equity Risk Premium: Expanding in 2026",
                             height=250, yaxis_title="Required Return (%)",
                             legend=dict(orientation='h', y=1.08))
        st.plotly_chart(fig_erp, use_container_width=True)

    with col4:
        pe_sectors = ['Energy','Defense','Tech','Consumer','Utilities','Healthcare']
        pe_2021 = [18, 22, 42, 35, 24, 28]
        pe_2026 = [12, 18, 26, 22, 21, 24]
        fig_pe = go.Figure()
        fig_pe.add_trace(go.Bar(name='2021 Peak (Low Rate)', x=pe_sectors, y=pe_2021,
            marker_color='#334155'))
        fig_pe.add_trace(go.Bar(name='2026 (High Rate + Geo Risk)', x=pe_sectors, y=pe_2026,
            marker_color='#f0b429'))
        fig_pe.update_layout(template=TEMPLATE, title="P/E Multiple Compression by Sector",
                            height=250, barmode='group', yaxis_title="P/E Ratio",
                            legend=dict(orientation='h', y=1.08))
        st.plotly_chart(fig_pe, use_container_width=True)

# ═══════════════════════════════════════════
# TAB 4 — COUNTRY DIVERGENCE
# ═══════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>04 — Country-Level Divergence & Regional Alpha</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        world_gdp = pd.DataFrame({
            'country': ['India','China','United States','Indonesia','Brazil','Mexico','Saudi Arabia','Germany','Japan','United Kingdom','France','Turkey','South Africa','Vietnam','Egypt'],
            'gdp_growth': [7.3, 4.5, 2.7, 5.1, 2.2, 1.4, 2.5, 0.2, 1.1, 1.5, 1.2, 2.8, 1.1, 6.5, 3.5],
            'color_text': ['High Growth','Moderate','Moderate','High Growth','Low','Low','Low','Stagnant','Low','Low','Low','Low','Low','High Growth','Low']
        })
        fig_map = px.choropleth(world_gdp, locations='country', locationmode='country names',
                               color='gdp_growth', color_continuous_scale=['#ef4444','#f97316','#f0b429','#10b981','#059669'],
                               range_color=[0, 8],
                               title='GDP Growth Forecast 2026 (%) — IMF WEO')
        fig_map.update_layout(template=TEMPLATE, height=380, geo=dict(
            bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)',
            landcolor='#1e293b', showframe=False, showcoastlines=True,
            coastlinecolor='#334155', projection_type='natural earth'),
            coloraxis_colorbar=dict(title='GDP %', tickfont=dict(color='#94a3b8')))
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        india_metrics = dict(
            r=[7.3, 8.5, 7.0, 6.0, 4.0, 8.0],
            theta=['GDP Growth','Domestic Demand','Supply Chain Score','FDI Attractiveness','Geopolitical Neutrality','Digital Economy']
        )
        fig_india = go.Figure(go.Scatterpolar(
            r=india_metrics['r'], theta=india_metrics['theta'],
            fill='toself', fillcolor='rgba(16,185,129,0.2)',
            line=dict(color='#10b981', width=2),
            marker=dict(color='#10b981', size=7),
            name='India 2026'
        ))
        fig_india.update_layout(template=TEMPLATE, title="India: Multi-Dimensional Scorecard",
            polar=dict(radialaxis=dict(visible=True, range=[0,10], gridcolor='#1e293b',
                                      tickfont=dict(size=8, color='#334155')),
                      angularaxis=dict(tickfont=dict(size=9, color='#94a3b8')),
                      bgcolor='rgba(0,0,0,0)'),
            height=380, showlegend=False)
        st.plotly_chart(fig_india, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_vuln = go.Figure()
        risk_colors = {1:'#10b981',2:'#10b981',3:'#10b981',4:'#f0b429',5:'#f0b429',
                      6:'#f97316',7:'#f97316',8:'#ef4444',9:'#ef4444',10:'#ef4444'}
        fig_vuln.add_trace(go.Scatter(
            x=country_vuln['Trade_Openness'], y=country_vuln['Energy_Import_Dep'],
            mode='markers+text', text=country_vuln['Country'],
            textposition='top center', textfont=dict(size=9, color='#94a3b8'),
            marker=dict(size=(country_vuln['GDP_Size']*8+12).tolist(),
                       color=[risk_colors[r] for r in country_vuln['Risk_Score'].tolist()],
                       opacity=0.8, line=dict(color='#0a0e1a', width=2)),
        ))
        fig_vuln.add_hrect(y0=60, y1=100, fillcolor='rgba(239,68,68,0.05)',
                          annotation_text="High Energy Import Risk",
                          annotation_font=dict(color='#ef4444', size=9))
        fig_vuln.update_layout(template=TEMPLATE,
            title="EM Vulnerability Matrix<br><sup>Bubble size = GDP | Color = Risk Score</sup>",
            xaxis_title="Trade Openness (% GDP)", yaxis_title="Energy Import Dependency (%)",
            height=360)
        st.plotly_chart(fig_vuln, use_container_width=True)

    with col4:
        radar_categories = ['GDP Growth','Energy Security','Trade Balance','Currency Stability','Defense Capacity','Innovation']
        us_vals = [7, 9, 5, 9, 10, 9]
        eu_vals = [3, 3, 6, 7, 6, 7]
        china_vals = [6, 5, 9, 5, 8, 7]
        india_vals = [9, 6, 5, 6, 6, 6]
        fig_radar = go.Figure()
        def hex_to_rgba(hex_color, alpha=0.12):
            h = hex_color.lstrip('#')
            r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
            return f'rgba({r},{g},{b},{alpha})'

        for name, vals, color in [('USA',us_vals,'#3b82f6'),('Euro Area',eu_vals,'#8b5cf6'),
                                   ('China',china_vals,'#ef4444'),('India',india_vals,'#10b981')]:
            fig_radar.add_trace(go.Scatterpolar(
                r=vals+[vals[0]], theta=radar_categories+[radar_categories[0]],
                name=name, line=dict(color=color, width=2),
                fill='toself', fillcolor=hex_to_rgba(color)))
        fig_radar.update_layout(template=TEMPLATE, title="Major Economy Comparison — 6 Dimensions",
            polar=dict(radialaxis=dict(visible=True, range=[0,10], gridcolor='#1e293b',
                                      tickfont=dict(size=7, color='#334155')),
                      angularaxis=dict(tickfont=dict(size=9, color='#94a3b8')),
                      bgcolor='rgba(0,0,0,0)'),
            height=360, legend=dict(orientation='h', y=1.05))
        st.plotly_chart(fig_radar, use_container_width=True)

# ═══════════════════════════════════════════
# TAB 5 — STRATEGY & OUTLOOK
# ═══════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-header'>05 — Investment Strategy & 3–6 Month Outlook</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,3])
    with col1:
        fig_port = go.Figure(go.Pie(
            labels=portfolio_alloc['Asset'], values=portfolio_alloc['Weight'],
            hole=0.6,
            marker=dict(colors=['#f0b429','#ef4444','#f97316','#10b981','#3b82f6','#8b5cf6','#94a3b8','#334155'],
                       line=dict(color='#0a0e1a', width=3)),
            textinfo='label+percent', textfont=dict(size=11, color='#f1f5f9'),
            hovertemplate='<b>%{label}</b><br>Weight: %{value}%<extra></extra>'
        ))
        fig_port.update_layout(template=TEMPLATE, title="Recommended Portfolio Allocation",
                              height=380,
                              annotations=[dict(text='<b>Portfolio</b><br>Allocation', x=0.5, y=0.5,
                                              font_size=13, showarrow=False, font_color='#f1f5f9')])
        st.plotly_chart(fig_port, use_container_width=True)

        st.markdown("""
        <div style='background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px'>
            <div style='font-family:IBM Plex Mono;font-size:9px;letter-spacing:2px;color:#f0b429;text-transform:uppercase;margin-bottom:8px'>Positioning Legend</div>
            <div style='display:flex;gap:12px'>
                <span style='background:#064e3b;color:#10b981;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600'>OW Overweight</span>
                <span style='background:#451a03;color:#f59e0b;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600'>N Neutral</span>
                <span style='background:#450a0a;color:#ef4444;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600'>UW Underweight</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='font-family:IBM Plex Mono;font-size:10px;letter-spacing:2px;color:#94a3b8;text-transform:uppercase;margin-bottom:12px'>3–6 Month Scenario Analysis</div>", unsafe_allow_html=True)
        for scenario, data in scenario_data.items():
            color = data['Color']
            st.markdown(f"""
            <div style='background:{color}10;border:1px solid {color}40;border-radius:8px;padding:14px;margin-bottom:10px'>
                <div style='font-weight:700;color:{color};font-size:13px;margin-bottom:8px'>{scenario}</div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:6px'>
                    <div style='font-size:11px'><span style='color:#475569'>Oil: </span><span style='color:#f1f5f9'>{data['Oil']}</span></div>
                    <div style='font-size:11px'><span style='color:#475569'>Equities: </span><span style='color:#f1f5f9'>{data['Equities']}</span></div>
                    <div style='font-size:11px'><span style='color:#475569'>Inflation: </span><span style='color:#f1f5f9'>{data['Inflation']}</span></div>
                    <div style='font-size:11px'><span style='color:#475569'>EM: </span><span style='color:#f1f5f9'>{data['EM']}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        prob_fig = go.Figure(go.Bar(
            x=[60, 20, 20], y=['Base Case','Bull Case','Bear Case'],
            orientation='h',
            marker_color=['#f0b429','#10b981','#ef4444'],
            text=['60%','20%','20%'], textposition='outside',
            textfont=dict(color='#94a3b8', size=12)
        ))
        prob_fig.update_layout(template=TEMPLATE, title="Scenario Probability Weights",
                              height=170, xaxis=dict(range=[0,80], showgrid=False, showticklabels=False),
                              margin=dict(l=10,r=60,t=40,b=10))
        st.plotly_chart(prob_fig, use_container_width=True)

    st.markdown("<div class='section-header'>Sector Signal Dashboard — Buy / Neutral / Reduce</div>", unsafe_allow_html=True)
    badge_map = {'BUY': 'badge-buy', 'NEUTRAL': 'badge-neutral', 'REDUCE': 'badge-reduce'}
    signal_html = "<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:10px'>"
    for sector, signal, rationale in sector_signals:
        badge_class = badge_map[signal]
        signal_html += f"""
        <div style='background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
                <div style='font-weight:600;font-size:13px'>{sector}</div>
                <span class='{badge_class}'>{signal}</span>
            </div>
            <div style='font-size:11px;color:#475569'>{rationale}</div>
        </div>"""
    signal_html += "</div>"
    st.markdown(signal_html, unsafe_allow_html=True)

    st.markdown("<div class='section-header' style='margin-top:20px'>Thesis Validation — Memo Predictions vs Market Reality</div>", unsafe_allow_html=True)
    thesis_checks = [
        ("Energy outperforms", "✅ Confirmed", "XLE +34% YTD, Brent +98%", "#10b981"),
        ("Gold as hedge", "✅ Confirmed", "Gold +18.3%, ATH $3,124", "#10b981"),
        ("Defense sector beneficiary", "✅ Confirmed", "Defense ETF +22.5% YTD", "#10b981"),
        ("India as supply chain winner", "✅ Confirmed", "GDP 7.3%, FDI inflows up", "#10b981"),
        ("Tech valuation compression", "✅ Confirmed", "P/E contracted, growth sold off", "#10b981"),
        ("USD safe haven strength", "✅ Confirmed", "DXY +6.2%, EM currency stress", "#10b981"),
        ("EM differentiation", "⚠️ Partial", "India outperforms; other EMs under pressure", "#f0b429"),
        ("Stagflation risk contained", "⚠️ Monitoring", "Inflation easing but oil spike threatens", "#f0b429"),
    ]
    tv_html = "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px'>"
    for thesis, status, evidence, color in thesis_checks:
        tv_html += f"""
        <div style='background:{color}10;border:1px solid {color}30;border-radius:8px;padding:12px'>
            <div style='font-size:11px;color:#94a3b8;margin-bottom:4px'>{thesis}</div>
            <div style='font-weight:700;color:{color};font-size:12px;margin-bottom:4px'>{status}</div>
            <div style='font-size:10px;color:#475569'>{evidence}</div>
        </div>"""
    tv_html += "</div>"
    st.markdown(tv_html, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#111827;border:1px solid #1e293b;border-radius:8px;padding:16px;margin-top:20px'>
        <div style='font-family:IBM Plex Mono;font-size:9px;letter-spacing:2px;color:#f0b429;text-transform:uppercase;margin-bottom:8px'>Data Sources & Verification</div>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:11px;color:#475569'>
            <div>📊 IMF World Economic Outlook Jan 2026<br><span style='color:#334155'>imf.org/en/publications/weo</span></div>
            <div>📰 Reuters Energy & Inflation Reports 2026<br><span style='color:#334155'>reuters.com/world/</span></div>
            <div>🏦 World Bank Global Economic Prospects<br><span style='color:#334155'>worldbank.org/en/publication/global-economic-prospects</span></div>
            <div>⛽ EIA Weekly Petroleum Reports<br><span style='color:#334155'>eia.gov/petroleum/supply/weekly</span></div>
            <div>🔬 Allianz Research Iran Scenarios 2026<br><span style='color:#334155'>allianz.com/economic-research</span></div>
            <div>📈 IMF Oil Price Shock Analysis 2026<br><span style='color:#334155'>oilprice.com / IMF Research</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
