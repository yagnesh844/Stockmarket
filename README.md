# 📈 Indian Stock Market AI Candle & Trend Analyzer

An interactive technical analysis web application built with **Python**, **Streamlit**, and **Plotly** to evaluate Indian equities (NSE/BSE). The application scans historical candlestick patterns, moving averages, and momentum oscillators to determine whether a stock is **RISING (Uptrend)** or **DROPPING (Downtrend)** and provides rule-based **Buy / Sell** signals with defined risk management levels.

---

## 🌟 Key Features

* **Price Range Filtering**: Quickly filter stocks by price brackets (*Under ₹100*, *₹100–₹500*, *₹500–₹2,000*, *Above ₹2,000*) or use a custom price slider.
* **Full NSE Equity Search**: Easily search any Indian stock by company name or exchange ticker symbol.
* **Candle Trend & Momentum Detection**: Evaluates historical candles for:
  * Green vs. Red candle dominance over the last 20 trading sessions.
  * Price slope (linear regression angle).
  * Higher-High/Higher-Low vs. Lower-High/Lower-Low structure.
* **Defined Risk Management**: Calculates a **Take-Profit Target** (~+8%) and a **Defensive Stop-Loss** (~-4%) on valid Buy signals.
* **Candlestick Pattern Recognition**: Automatically flags classic reversal patterns such as *Hammers*, *Shooting Stars*, and *Engulfing Candles*.
* **Auto-Refresh Capability**: Silently re-fetches latest price action and updates indicators on a regular interval.

---

## 🖥️ User Interface (UX) Breakdown

1. **Sidebar Navigation**:
   * **Price Range Filter**: Categorizes stocks into budget, growth, and large-cap segments.
   * **Stock Search**: Autocomplete search box across equities.
   * **Timeframe Selector**: Adjust candle depth (3 months, 6 months, 1 year).
   * **Auto-Refresh Toggle**: Updates price and candles on a 60-second timer.

2. **Top Trend & Action Banner**:
   * 🟢 **RISING (UPTREND) — Action: BUY**: Buyers dominate; indicators confirm upward momentum.
   * 🔴 **DROPPING (DOWNTREND) — Action: SELL / DO NOT BUY**: Sellers dominate; downward momentum detected.
   * 🟡 **SIDEWAYS — Action: WAIT**: Range-bound price action; wait for a breakout.

3. **Key Metric Cards**:
   * **Current Price**: Latest traded price (LTP) in INR (₹).
   * **20-Day Candle Bias**: Ratio of Green (bullish) to Red (bearish) closing sessions.
   * **Trend Slope**: Daily percentage rate of price change.
   * **Take-Profit Target**: Planned exit price to book profit.
   * **Defensive Stop-Loss**: Planned exit price to limit downside exposure.

4. **Interactive Charting Pane**:
   * **Candlestick Chart**: Daily open, high, low, and close bars.
   * **Trend Moving Averages**: 20-day Exponential Moving Average (Orange) and 50-day EMA (Blue).
   * **RSI (14) Subplot**: Overbought (70) and oversold (30) momentum thresholds.

5. **Past Candle Analysis Breakdown**:
   * Detailed checklist of all detected **Bullish Signals (✅)** and **Bearish Risks (❌)**.
   * Volume ratio comparing buying volume to selling volume.
   * Tactical trading guidance.

---

## 🛠️ Tech Stack

* **Language**: Python 3.9+
* **Frontend / Framework**: Streamlit
* **Market Data**: `yfinance` (NSE / BSE daily and intraday feeds)
* **Data Processing**: Pandas, NumPy
* **Data Visualization**: Plotly (Interactive Candlestick and Multi-panel Subplots)

---

## 🚀 Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Stockmarket.git](https://github.com/YOUR_USERNAME/Stockmarket.git)
   cd Stockmarket



## 🔰 New to Trading? Simple Step-by-Step Guide

If you are completely new to the stock market and don't know complex technical analysis, follow these 4 simple steps to use this dashboard:

1. **Pick a Stock Within Your Budget**:
   * Use the **Price Range Filter** on the sidebar to find stocks matching your available capital (e.g., *Under ₹100*, *₹100–₹500*, etc.).
   * Only invest money you can comfortably afford—never risk money you need for daily essentials.

2. **Check the Status Banner**:
   * **🟢 Green (PRICE IS RISING — BUY)**: The stock is in a healthy upward trend.
   * **🔴 Red (PRICE IS DROPPING)** or **🟡 Yellow (SIDEWAYS)**: Do **NOT** buy. Wait for better market conditions.

3. **Check the Profit & Risk Levels**:
   * Look at the **Take-Profit Target** and **Defensive Stop-Loss** values shown at the top of the screen.

4. **Follow the Exit Rule (Protect Your Capital)**:
   * **Rule 1 (Take Profit)**: When the stock rises and hits the **Take-Profit Target**, sell your shares to lock in your profit.
   * **Rule 2 (Cut Losses)**: If the market drops and the price falls to the **Stop-Loss amount**, sell immediately to exit safely and avoid larger losses.




   
# ==============================================================================
# LEGAL & REGULATORY DISCLAIMER
# ==============================================================================
st.markdown("---")
st. caption(
    "⚠️ **Disclaimer:** This application is an automated technical analysis tool built strictly for "
    "educational, research, and algorithmic demonstration purposes. It does not provide financial advice, "
    "stock recommendations, or SEBI-registered investment advisory services. Stock trading involves "
    "substantial risk of loss. Always perform your own independent analysis and consult a certified financial
    "advisor before making any investment or trading decisions."
)


    
