import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(
    page_title="NSE Market AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Indian Stock Market: Full Candle & Trend Analyzer")
st.caption("Includes price range filtering, historical candle analysis, and automatic Rising vs. Dropping detection.")

# Safe Fragment Decorator (compatible with all Streamlit versions)
def safe_fragment(run_every=None):
    if hasattr(st, "fragment"):
        return st.fragment(run_every=run_every)
    elif hasattr(st, "experimental_fragment"):
        return st.experimental_fragment(run_every=run_every)
    else:
        def decorator(func):
            return func
        return decorator

# Stock Database with Price Brackets
stock_catalog = [
    # Under ₹100 (Budget / Small-caps)
    {"SYMBOL": "IDEA", "NAME": "Vodafone Idea Ltd", "PRICE_TIER": "Under ₹100", "APPROX": 15},
    {"SYMBOL": "YESBANK", "NAME": "Yes Bank Ltd", "PRICE_TIER": "Under ₹100", "APPROX": 24},
    {"SYMBOL": "SOUTHBANK", "NAME": "South Indian Bank Ltd", "PRICE_TIER": "Under ₹100", "APPROX": 28},
    {"SYMBOL": "TRIDENT", "NAME": "Trident Ltd", "PRICE_TIER": "Under ₹100", "APPROX": 38},
    {"SYMBOL": "UCOBANK", "NAME": "UCO Bank", "PRICE_TIER": "Under ₹100", "APPROX": 45},
    {"SYMBOL": "SUZLON", "NAME": "Suzlon Energy Ltd", "PRICE_TIER": "Under ₹100", "APPROX": 75},
    {"SYMBOL": "NHPC", "NAME": "NHPC Ltd", "PRICE_TIER": "Under ₹100", "APPROX": 95},

    # ₹100 - ₹500 (Mid-caps)
    {"SYMBOL": "IOC", "NAME": "Indian Oil Corporation Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 170},
    {"SYMBOL": "IRFC", "NAME": "Indian Railway Finance Corp", "PRICE_TIER": "₹100 - ₹500", "APPROX": 175},
    {"SYMBOL": "FEDERALBNK", "NAME": "Federal Bank Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 195},
    {"SYMBOL": "GAIL", "NAME": "GAIL (India) Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 210},
    {"SYMBOL": "ZOMATO", "NAME": "Zomato Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 260},
    {"SYMBOL": "BEL", "NAME": "Bharat Electronics Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 290},
    {"SYMBOL": "TATAPOWER", "NAME": "Tata Power Co Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 430},
    {"SYMBOL": "ITC", "NAME": "ITC Ltd", "PRICE_TIER": "₹100 - ₹500", "APPROX": 490},

    # ₹500 - ₹2,000 (Core Large-caps)
    {"SYMBOL": "WIPRO", "NAME": "Wipro Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 540},
    {"SYMBOL": "SBIN", "NAME": "State Bank of India", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 810},
    {"SYMBOL": "TATAMOTORS", "NAME": "Tata Motors Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 980},
    {"SYMBOL": "AXISBANK", "NAME": "Axis Bank Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 1180},
    {"SYMBOL": "ICICIBANK", "NAME": "ICICI Bank Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 1220},
    {"SYMBOL": "BHARTIARTL", "NAME": "Bharti Airtel Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 1550},
    {"SYMBOL": "HDFCBANK", "NAME": "HDFC Bank Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 1650},
    {"SYMBOL": "INFY", "NAME": "Infosys Ltd", "PRICE_TIER": "₹500 - ₹2,000", "APPROX": 1850},

    # Above ₹2,000 (High-Priced Equities)
    {"SYMBOL": "RELIANCE", "NAME": "Reliance Industries Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 2980},
    {"SYMBOL": "ASIANPAINT", "NAME": "Asian Paints Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 3150},
    {"SYMBOL": "LT", "NAME": "Larsen & Toubro Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 3600},
    {"SYMBOL": "TITAN", "NAME": "Titan Company Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 3650},
    {"SYMBOL": "TCS", "NAME": "Tata Consultancy Services Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 4250},
    {"SYMBOL": "BAJFINANCE", "NAME": "Bajaj Finance Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 7100},
    {"SYMBOL": "MARUTI", "NAME": "Maruti Suzuki India Ltd", "PRICE_TIER": "Above ₹2,000", "APPROX": 12400}
]

df_stocks = pd.DataFrame(stock_catalog)
df_stocks["DISPLAY"] = df_stocks["NAME"] + " (" + df_stocks["SYMBOL"] + ") - ~₹" + df_stocks["APPROX"].astype(str)

# Sidebar: Filters
st.sidebar.header("🎚️ 1. Price Range Filter")
price_choice = st.sidebar.radio(
    "Select Budget / Price Tier:",
    ["All Prices", "Under ₹100", "₹100 - ₹500", "₹500 - ₹2,000", "Above ₹2,000"]
)

if price_choice != "All Prices":
    filtered_stocks = df_stocks[df_stocks["PRICE_TIER"] == price_choice]
else:
    filtered_stocks = df_stocks

st.sidebar.header("🔍 2. Select Stock")
selected_display = st.sidebar.selectbox(
    "Choose Stock from List:",
    options=list(filtered_stocks["DISPLAY"].values),
    index=0
)

selected_row = filtered_stocks[filtered_stocks["DISPLAY"] == selected_display].iloc[0]
ticker_symbol = f"{selected_row['SYMBOL']}.NS"
company_name = selected_row["NAME"]

# Manual Ticker Override
manual_entry = st.sidebar.text_input("Or type any NSE/BSE symbol manually:", "")
if manual_entry.strip():
    ticker_symbol = manual_entry.strip().upper()
    if not ticker_symbol.endswith(".NS") and not ticker_symbol.endswith(".BO"):
        ticker_symbol += ".NS"
    company_name = ticker_symbol

# Timeframe and Auto-Refresh
st.sidebar.header("⏱️ 3. Settings")
timeframe = st.sidebar.selectbox("Historical Candle Depth:", ["3mo", "6mo", "1y"], index=1)
auto_refresh = st.sidebar.checkbox("Auto-refresh every minute", value=True)
refresh_timer = 60 if auto_refresh else None

# Full Candlestick & Indicator Analyzer Function
def analyze_market_candles(df):
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["Is_Green"] = df["Close"] >= df["Open"]
    df["Body"] = (df["Close"] - df["Open"]).abs()
    df["Upper_Wick"] = df["High"] - df[["Open", "Close"]].max(axis=1)
    df["Lower_Wick"] = df[["Open", "Close"]].min(axis=1) - df["Low"]

    # RSI (14)
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = (100 - (100 / (1 + rs))).fillna(50)

    # 20-Day Window Statistics
    recent_20 = df.tail(20)
    green_count = int(recent_20["Is_Green"].sum())
    red_count = 20 - green_count

    # Trend Slope
    x = np.arange(len(recent_20))
    slope, _ = np.polyfit(x, recent_20["Close"].values, 1)
    slope_pct = (slope / recent_20["Close"].mean()) * 100

    # Volume Ratio (Buying vs Selling Volume)
    buy_vol = recent_20[recent_20["Is_Green"]]["Volume"].sum()
    sell_vol = recent_20[~recent_20["Is_Green"]]["Volume"].sum()
    vol_ratio = round(buy_vol / sell_vol, 2) if sell_vol > 0 else 1.0

    latest = df.iloc[-1]
    prev = df.iloc[-2]
    price = round(float(latest["Close"]), 2)

    # Candlestick Patterns
    patterns = []
    if latest["Lower_Wick"] > 2 * latest["Body"] and latest["Upper_Wick"] < latest["Body"]:
        patterns.append("Hammer (Bullish rejection of lower prices)")
    if latest["Upper_Wick"] > 2 * latest["Body"] and latest["Lower_Wick"] < latest["Body"]:
        patterns.append("Shooting Star (Bearish rejection of higher prices)")
    if not prev["Is_Green"] and latest["Is_Green"] and latest["Close"] > prev["Open"]:
        patterns.append("Bullish Engulfing (Buyers overpowered previous red candle)")
    if prev["Is_Green"] and not latest["Is_Green"] and latest["Close"] < prev["Open"]:
        patterns.append("Bearish Engulfing (Sellers overpowered previous green candle)")

    # Trend Proof Points
    bullish_proof = []
    bearish_proof = []

    if slope_pct > 0.1:
        bullish_proof.append(f"Positive Price Slope: Rising at {slope_pct:+.2f}% per session.")
    elif slope_pct < -0.1:
        bearish_proof.append(f"Negative Price Slope: Dropping at {slope_pct:+.2f}% per session.")

    if green_count >= 11:
        bullish_proof.append(f"Green Candle Dominance: {green_count} Green vs {red_count} Red in last 20 days.")
    elif red_count >= 11:
        bearish_proof.append(f"Red Candle Dominance: {red_count} Red vs {green_count} Green in last 20 days.")

    if price > latest["EMA_20"] > latest["EMA_50"]:
        bullish_proof.append("Price is trading above both 20-day and 50-day EMAs.")
    elif price < latest["EMA_20"] < latest["EMA_50"]:
        bearish_proof.append("Price is trading below both 20-day and 50-day EMAs.")

    # High / Low Structure (Last 5 days vs Prior 5 days)
    if df["High"].tail(5).max() > df["High"].iloc[-10:-5].max() and df["Low"].tail(5).min() > df["Low"].iloc[-10:-5].min():
        bullish_proof.append("Price Structure: Making Higher Highs and Higher Lows.")
    elif df["High"].tail(5).max() < df["High"].iloc[-10:-5].max() and df["Low"].tail(5).min() < df["Low"].iloc[-10:-5].min():
        bearish_proof.append("Price Structure: Making Lower Highs and Lower Lows.")

    # Direction Decision
    if len(bullish_proof) > len(bearish_proof) and slope_pct >= 0:
        direction = "RISING"
        signal = "BUY" if latest["RSI"] < 68 else "HOLD (Wait for a minor pullback)"
        target = round(price * 1.08, 2)
        stop_loss = round(price * 0.96, 2)
    elif len(bearish_proof) > len(bullish_proof) and slope_pct < 0:
        direction = "DROPPING"
        signal = "SELL / DO NOT BUY"
        target = round(price * 0.92, 2)
        stop_loss = round(price * 1.04, 2)
    else:
        direction = "SIDEWAYS"
        signal = "WAIT (Neutral Range)"
        target = None
        stop_loss = None

    return {
        "price": price,
        "direction": direction,
        "signal": signal,
        "target": target,
        "stop_loss": stop_loss,
        "green_count": green_count,
        "red_count": red_count,
        "slope_pct": round(slope_pct, 2),
        "vol_ratio": vol_ratio,
        "rsi": round(float(latest["RSI"]), 2),
        "ema20": round(float(latest["EMA_20"]), 2),
        "ema50": round(float(latest["EMA_50"]), 2),
        "bullish_proof": bullish_proof,
        "bearish_proof": bearish_proof,
        "patterns": patterns
    }

# Render Component
@safe_fragment(run_every=refresh_timer)
def render_full_dashboard(sym, name, tf):
    try:
        data = yf.Ticker(sym).history(period=tf)
        if data.empty or len(data) < 15:
            st.error(f"Could not load data for '{sym}'. Please check symbol.")
            return

        res = analyze_market_candles(data)

        # Header Title
        st.subheader(f"{name} ({sym})")
        st.caption(f"Last updated: {pd.Timestamp.now().strftime('%H:%M:%S IST')} | Auto-refresh: {'On (60s)' if auto_refresh else 'Off'}")

        # Top Big Direction Banner
        if res["direction"] == "RISING":
            st.success(f"### 🟢 PRICE IS RISING (UPTREND) — Action: {res['signal']}")
        elif res["direction"] == "DROPPING":
            st.error(f"### 🔴 PRICE IS DROPPING (DOWNTREND) — Action: {res['signal']}")
        else:
            st.warning(f"### 🟡 PRICE IS SIDEWAYS (CONSOLIDATION) — Action: {res['signal']}")

        # 5 Top Metric Cards
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Current Price", f"₹{res['price']}")
        m2.metric("20-Day Candles", f"{res['green_count']} Green / {res['red_count']} Red")
        m3.metric("Trend Slope", f"{res['slope_pct']:+}% / day")
        m4.metric("Take-Profit Target", f"₹{res['target']}" if res['target'] else "Wait")
        m5.metric("Defensive Stop-Loss", f"₹{res['stop_loss']}" if res['stop_loss'] else "N/A")

        st.markdown("---")

        # Two Column Layout: Chart (Left) and Detailed Reasons (Right)
        col_chart, col_reasons = st.columns([2, 1])

        with col_chart:
            st.markdown("#### Candlestick Chart & Moving Averages")
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_width=[0.28, 0.72])

            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"],
                name="Candles"
            ), row=1, col=1)

            fig.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], line=dict(color="orange", width=1.5), name="20 EMA"), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data["EMA_50"], line=dict(color="blue", width=1.5), name="50 EMA"), row=1, col=1)

            fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], line=dict(color="purple", width=1.5), name="RSI"), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

            fig.update_layout(height=520, margin=dict(l=10, r=10, t=10, b=10), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_reasons:
            st.markdown("#### Why is the Stock Rising or Dropping?")
            if res["bullish_proof"]:
                st.markdown("**Bullish Signals Detected:**")
                for item in res["bullish_proof"]:
                    st.write(f"✅ {item}")

            if res["bearish_proof"]:
                st.markdown("**Bearish Signals Detected:**")
                for item in res["bearish_proof"]:
                    st.write(f"❌ {item}")

            if res["patterns"]:
                st.markdown("**Recent Candlestick Patterns:**")
                for p in res["patterns"]:
                    st.info(f"🕯️ {p}")

            st.markdown("---")
            st.markdown("#### Technical Snapshot")
            st.write(f"- **RSI (14)**: `{res['rsi']}`")
            st.write(f"- **Volume Ratio (Up/Down)**: `{res['vol_ratio']}x`")
            st.write(f"- **20-Day EMA**: `₹{res['ema20']}`")
            st.write(f"- **50-Day EMA**: `₹{res['ema50']}`")

            if res["direction"] == "RISING":
                st.info("💡 **Trade Tip:** Buyers dominate. If you enter on BUY, keep your stop-loss active at the displayed price.")
            elif res["direction"] == "DROPPING":
                st.warning("⚠️ **Risk Alert:** Sellers dominate. Avoid buying until confirmed green reversal candles emerge.")

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

# Run Dashboard
render_full_dashboard(ticker_symbol, company_name, timeframe)