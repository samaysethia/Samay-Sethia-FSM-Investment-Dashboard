# 📊 Global Geopolitical Impact on Financial Markets
### Investment Intelligence Dashboard — Q1 2026

> **Author:** Samay Sethia · MS25GF129  
> **Subject:** Financial Systems and Markets  
> **Advisor:** Dr. Nathaniel Christopher

---

## Overview

A Bloomberg-style, multi-panel financial intelligence dashboard that visualises the structural impact of geopolitical fragmentation on global financial markets in 2026. Built on the investment memo's thesis: *geopolitical risk has become a structural — not cyclical — market force.*

**Live Demo →** *(Deploy to Streamlit Cloud — see below)*

---

## Dashboard Structure

| Tab | Coverage |
|-----|----------|
| 📈 Macro Overview | GDP forecasts, inflation trajectory, transmission channels |
| ⚡ Energy & Commodities | Brent crude decomposition, sector performance, supply chain chokepoints |
| 🌐 Cross-Asset | Asset class heatmap, safe-haven flows, ERP expansion, P/E compression |
| 🗺️ Country Divergence | Choropleth map, India scorecard, EM vulnerability matrix, radar comparison |
| 🎯 Strategy & Outlook | Portfolio allocation, scenario analysis, sector signals, thesis validation |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/geopolitical-financial-dashboard.git
cd geopolitical-financial-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo → `app.py` → Deploy
5. Your dashboard will be live at `https://YOUR_USERNAME-geopolitical-dashboard.streamlit.app`

---

## Data Sources

All data points are sourced from peer-reviewed, institutional, or major financial sources:

- **IMF World Economic Outlook** — Jan 2026 · [imf.org](https://www.imf.org/en/publications/weo/issues/2026/01/19/world-economic-outlook-update-january-2026)
- **IMF Oil Price Shock Analysis** · [oilprice.com / IMF](https://oilprice.com/Latest-Energy-News/World-News/IMF-Oil-Price-Shock-Tests-Global-Economic-Resilience.html)
- **Reuters — Energy & Inflation** · [reuters.com](https://www.reuters.com/world/imf-says-prolonged-increase-energy-prices-could-boost-inflation-lower-growth-2026-03-19/)
- **Reuters — India GDP Forecast** · [reuters.com](https://www.reuters.com/world/india/imf-raises-india-fy26-growth-forecast-73-sees-slower-pace-next-two-years-2026-01-19/)
- **Reuters — Middle East Economic Impact** · [reuters.com](https://www.reuters.com/world/middle-east/middle-east-war-economic-impact-depend-duration-damage-energy-costs-imf-official-2026-03-03/)
- **World Bank Global Economic Prospects** · [worldbank.org](https://www.worldbank.org/en/publication/global-economic-prospects)
- **Allianz Research — Iran Scenarios** · [allianz.com](https://www.allianz.com/content/dam/onemarketing/azcom/Allianz_com/economic-research/publications/specials/en/2026/march/2026_03_03_IranScenarios.pdf)
- **EIA Petroleum Supply Weekly** · [eia.gov](https://www.eia.gov/petroleum/supply/weekly/)

---

## Tech Stack

- **Framework:** [Streamlit](https://streamlit.io)
- **Visualisations:** [Plotly](https://plotly.com/python/)
- **Data Processing:** [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/)
- **Fonts:** IBM Plex Sans + IBM Plex Mono (Google Fonts)

---

## License

Academic use only. Data sourced from public institutional publications.
