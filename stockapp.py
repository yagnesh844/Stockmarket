import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import io

# Page Setup
st.set_page_config(
    page_title="Indian Stock Market AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Indian Stock Market: Full Candle & Trend Analyzer")
st.caption("Default view displays all 2,000+ NSE stocks. Toggle the filter to isolate specific price ranges.")

# Beginner's Guide Expander
with st.expander("📖 New to Trading? Click here for a quick 4-step guide"):
    st.markdown("""
    **Follow these 4 simple steps to use this dashboard safely:**
    1. **Pick a stock matching your budget**: By default, search all stocks, or check the **Price Filter** box in the sidebar to view stocks within your exact budget.
    2. **Check the Status Banner**:
       * 🟢 **PRICE IS RISING (Action: BUY)**: Strong upward momentum and buyer dominance.
       * 🔴 **PRICE IS DROPPING** or 🟡 **SIDEWAYS**: Do **NOT** buy. Wait for better market conditions.
    3. **Note the Target & Stop-Loss**: Every stock has a planned exit price for both profit and capital defense.
    4. **The Golden Exit Rules**:
       * **Take Profit**: When the stock climbs to the **Take-Profit Target**, sell your shares to lock in your profit.
       * **Cut Losses**: If the stock falls to the **Defensive Stop-Loss**, sell immediately to protect your remaining capital.
    """)


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


# ==============================================================================
# 1. LOAD FULL MASTER NSE DIRECTORY (2,000+ STOCKS)
# ==============================================================================
@st.cache_data(ttl=86400)
def load_all_nse_equities() -> pd.DataFrame:
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            df = pd.read_csv(io.StringIO(res.text))
            df.columns = [c.strip() for c in df.columns]
            if "SERIES" in df.columns:
                df = df[df["SERIES"] == "EQ"]
            df = df[["SYMBOL", "NAME OF COMPANY"]].dropna()
            df["DISPLAY"] = df["NAME OF COMPANY"] + " (" + df["SYMBOL"] + ")"
            return df
    except Exception:
        pass

    # Built-in fallback
    fallback = [
        {"SYMBOL": "TATASTEEL", "NAME OF COMPANY": "Tata Steel Ltd"},
        {"SYMBOL": "IDEA", "NAME OF COMPANY": "Vodafone Idea Ltd"},
        {"SYMBOL": "YESBANK", "NAME OF COMPANY": "Yes Bank Ltd"},
        {"SYMBOL": "SUZLON", "NAME OF COMPANY": "Suzlon Energy Ltd"},
        {"SYMBOL": "SAIL", "NAME OF COMPANY": "Steel Authority of India Ltd"},
        {"SYMBOL": "IOC", "NAME OF COMPANY": "Indian Oil Corporation Ltd"},
        {"SYMBOL": "IRFC", "NAME OF COMPANY": "Indian Railway Finance Corp"},
        {"SYMBOL": "FEDERALBNK", "NAME OF COMPANY": "Federal Bank Ltd"},
        {"SYMBOL": "ZOMATO", "NAME OF COMPANY": "Zomato Ltd"},
        {"SYMBOL": "BEL", "NAME OF COMPANY": "Bharat Electronics Ltd"},
        {"SYMBOL": "TATAPOWER", "NAME OF COMPANY": "Tata Power Co Ltd"},
        {"SYMBOL": "ITC", "NAME OF COMPANY": "ITC Ltd"},
        {"SYMBOL": "SBIN", "NAME OF COMPANY": "State Bank of India"},
        {"SYMBOL": "TATAMOTORS", "NAME OF COMPANY": "Tata Motors Ltd"},
        {"SYMBOL": "INFY", "NAME OF COMPANY": "Infosys Ltd"},
        {"SYMBOL": "HDFCBANK", "NAME OF COMPANY": "HDFC Bank Ltd"},
        {"SYMBOL": "RELIANCE", "NAME OF COMPANY": "Reliance Industries Ltd"},
        {"SYMBOL": "TCS", "NAME OF COMPANY": "Tata Consultancy Services Ltd"},
        {"SYMBOL": "MRF", "NAME OF COMPANY": "MRF Ltd"}
    ]
    df_fb = pd.DataFrame(fallback)
    df_fb["DISPLAY"] = df_fb["NAME OF COMPANY"] + " (" + df_fb["SYMBOL"] + ")"
    return df_fb


df_all_nse = load_all_nse_equities()

# Price-Indexed Catalog for Budget Filtering
catalog_prices = [
    # Under ₹50
    {"SYMBOL": "IDEA", "NAME": "Vodafone Idea Ltd", "PRICE": 15.20},
    {"SYMBOL": "YESBANK", "NAME": "Yes Bank Ltd", "PRICE": 24.50},
    {"SYMBOL": "SOUTHBANK", "NAME": "South Indian Bank Ltd", "PRICE": 28.30},
    {"SYMBOL": "TRIDENT", "NAME": "Trident Ltd", "PRICE": 38.40},
    {"SYMBOL": "UCOBANK", "NAME": "UCO Bank", "PRICE": 46.10},

    # ₹50 to ₹100
    {"SYMBOL": "CENTRALBK", "NAME": "Central Bank of India", "PRICE": 58.20},
    {"SYMBOL": "IOB", "NAME": "Indian Overseas Bank", "PRICE": 62.50},
    {"SYMBOL": "IDFCFIRSTB", "NAME": "IDFC First Bank Ltd", "PRICE": 72.40},
    {"SYMBOL": "SUZLON", "NAME": "Suzlon Energy Ltd", "PRICE": 74.80},
    {"SYMBOL": "NHPC", "NAME": "NHPC Ltd", "PRICE": 92.50},
    {"SYMBOL": "PNB", "NAME": "Punjab National Bank", "PRICE": 98.30},

    # ₹100 to ₹200
    {"SYMBOL": "SAIL", "NAME": "Steel Authority of India Ltd", "PRICE": 134.50},
    {"SYMBOL": "TATASTEEL", "NAME": "Tata Steel Ltd", "PRICE": 153.20},
    {"SYMBOL": "IOC", "NAME": "Indian Oil Corporation Ltd", "PRICE": 172.40},
    {"SYMBOL": "IRFC", "NAME": "Indian Railway Finance Corp", "PRICE": 181.50},
    {"SYMBOL": "ASHOKLEY", "NAME": "Ashok Leyland Ltd", "PRICE": 188.40},
    {"SYMBOL": "FEDERALBNK", "NAME": "Federal Bank Ltd", "PRICE": 194.80},
    {"SYMBOL": "GAIL", "NAME": "GAIL (India) Ltd", "PRICE": 198.60},

    # ₹200 to ₹500
    {"SYMBOL": "BANKBARODA", "NAME": "Bank of Baroda", "PRICE": 235.00},
    {"SYMBOL": "ZOMATO", "NAME": "Zomato Ltd", "PRICE": 262.50},
    {"SYMBOL": "BHEL", "NAME": "Bharat Heavy Electricals Ltd", "PRICE": 285.40},
    {"SYMBOL": "BEL", "NAME": "Bharat Electronics Ltd", "PRICE": 292.10},
    {"SYMBOL": "NTPC", "NAME": "NTPC Ltd", "PRICE": 395.00},
    {"SYMBOL": "TATAPOWER", "NAME": "Tata Power Co Ltd", "PRICE": 435.00},
    {"SYMBOL": "COALINDIA", "NAME": "Coal India Ltd", "PRICE": 482.00},
    {"SYMBOL": "ITC", "NAME": "ITC Ltd", "PRICE": 492.00},

    # ₹500 to ₹1,000
    {"SYMBOL": "WIPRO", "NAME": "Wipro Ltd", "PRICE": 545.00},
    {"SYMBOL": "HINDALCO", "NAME": "Hindalco Industries Ltd", "PRICE": 670.00},
    {"SYMBOL": "SBIN", "NAME": "State Bank of India", "PRICE": 815.00},
    {"SYMBOL": "TATAMOTORS", "NAME": "Tata Motors Ltd", "PRICE": 985.00},
    {"SYMBOL": "CIPLA", "NAME": "Cipla Ltd", "PRICE": 995.00},

    # ₹1,000 to ₹2,000
    {"SYMBOL": "AXISBANK", "NAME": "Axis Bank Ltd", "PRICE": 1180.00},
    {"SYMBOL": "ICICIBANK", "NAME": "ICICI Bank Ltd", "PRICE": 1225.00},
    {"SYMBOL": "BHARTIARTL", "NAME": "Bharti Airtel Ltd", "PRICE": 1560.00},
    {"SYMBOL": "HDFCBANK", "NAME": "HDFC Bank Ltd", "PRICE": 1655.00},
    {"SYMBOL": "INFY", "NAME": "Infosys Ltd", "PRICE": 1860.00},

    # ₹2,000 to ₹10,000
    {"SYMBOL": "RELIANCE", "NAME": "Reliance Industries Ltd", "PRICE": 2980.00},
    {"SYMBOL": "ASIANPAINT", "NAME": "Asian Paints Ltd", "PRICE": 3150.00},
    {"SYMBOL": "LT", "NAME": "Larsen & Toubro Ltd", "PRICE": 3620.00},
    {"SYMBOL": "TITAN", "NAME": "Titan Company Ltd", "PRICE": 3670.00},
    {"SYMBOL": "TCS", "NAME": "Tata Consultancy Services Ltd", "PRICE": 4260.00},
    {"SYMBOL": "BAJFINANCE", "NAME": "Bajaj Finance Ltd", "PRICE": 7150.00},

    # ₹10,000 to ₹1.5 Lakhs+
    {"SYMBOL": "MARUTI", "NAME": "Maruti Suzuki India Ltd", "PRICE": 12450.00},
    {"SYMBOL": "SHREECEM", "NAME": "Shree Cement Ltd", "PRICE": 25800.00},
    {"SYMBOL": "BOSCHLTD", "NAME": "Bosch Ltd", "PRICE": 31200.00},
    {"SYMBOL": "PAGEIND", "NAME": "Page Industries Ltd", "PRICE": 38500.00},
    {"SYMBOL": "MRF", "NAME": "MRF Ltd", "PRICE": 134500.00}
]
df_price_catalog = pd.DataFrame(catalog_prices)
df_price_catalog["DISPLAY"] = df_price_catalog["NAME"] + " (" + df_price_catalog["SYMBOL"] + ") - ~₹" + \
                              df_price_catalog["PRICE"].astype(str)

# ==============================================================================
# 2. GUARANTEED TICKER INITIALIZATION (PREVENTS NameError)
# ==============================================================================
# Set initial defaults so variables are ALWAYS defined
ticker_symbol = "TATASTEEL.NS"
company_name = "Tata Steel Ltd"

st.sidebar.header("⚙️ Controls")

# The Filter Button / Checkbox
enable_filter = st.sidebar.checkbox("🔍 Filter by Price Range", value=False)

# Session State for Price Inputs
if "applied_min" not in st.session_state:
    st.session_state.applied_min = 100.0
if "applied_max" not in st.session_state:
    st.session_state.applied_max = 200.0

if enable_filter:
    st.sidebar.markdown("#### Set Price Range:")
    with st.sidebar.form(key="price_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            input_min = st.number_input("From (Min ₹):", min_value=0.0, max_value=500000.0,
                                        value=float(st.session_state.applied_min), step=10.0)
        with col_f2:
            input_max = st.number_input("To (Max ₹):", min_value=1.0, max_value=500000.0,
                                        value=float(st.session_state.applied_max), step=10.0)

        submit_btn = st.form_submit_button("Apply Filter", use_container_width=True)

        if submit_btn:
            st.session_state.applied_min = input_min
            st.session_state.applied_max = input_max

    # Filter is active
    min_p = st.session_state.applied_min
    max_p = st.session_state.applied_max
    filtered_stocks = df_price_catalog[(df_price_catalog["PRICE"] >= min_p) & (df_price_catalog["PRICE"] <= max_p)]

    st.sidebar.success(f"✅ Filter Active: ₹{min_p:,.0f} to ₹{max_p:,.0f} ({len(filtered_stocks)} stocks found)")

    if not filtered_stocks.empty:
        active_options = list(filtered_stocks["DISPLAY"].values)
        stock_choice = st.sidebar.selectbox("Select Filtered Stock:", options=active_options, index=0)
        matched = filtered_stocks[filtered_stocks["DISPLAY"] == stock_choice].iloc[0]
        ticker_symbol = f"{matched['SYMBOL']}.NS"
        company_name = matched["NAME"]
    else:
        st.sidebar.warning("No stocks in database match this range. Using default stock or type manual ticker below.")
        ticker_symbol = "TATASTEEL.NS"
        company_name = "Tata Steel Ltd"

else:
    # DEFAULT: Filter is OFF -> Show ALL 2,000+ NSE stocks
    st.sidebar.info(f"Showing all {len(df_all_nse):,} NSE stocks (Filter is OFF).")
    stock_choice = st.sidebar.selectbox(
        "Search Any Stock (Company Name or Symbol):",
        options=list(df_all_nse["DISPLAY"].values),
        index=0
    )
    matched = df_all_nse[df_all_nse["DISPLAY"] == stock_choice].iloc[0]
    ticker_symbol = f"{matched['SYMBOL']}.NS"
    company_name = matched["NAME OF COMPANY"]

# Manual Ticker Override
manual_input = st.sidebar.text_input("Or enter any symbol manually (e.g. SAIL.NS, MRF.NS):", "")
if manual_input.strip():
    ticker_symbol = manual_input.strip().upper()
    if not ticker_symbol.endswith(".NS") and not ticker_symbol.endswith(".BO"):
        ticker_symbol += ".NS"
    company_name = ticker_symbol

# Settings
timeframe = st.sidebar.selectbox("Historical Candle Depth:", ["3mo", "6mo", "1y"], index=1)
auto_refresh = st.sidebar.checkbox("Auto-refresh every 1 minute", value=True)
refresh_timer = 60 if auto_refresh else None


# ==============================================================================
# 3. PAST CANDLE & MOMENTUM ANALYSIS ENGINE
# ==============================================================================
def analyze_stock_candles(df):
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

    recent_20 = df.tail(20)
    green_count = int(recent_20["Is_Green"].sum())
    red_count = 20 - green_count

    x = np.arange(len(recent_20))
    slope, _ = np.polyfit(x, recent_20["Close"].values, 1)
    slope_pct = (slope / recent_20["Close"].mean()) * 100

    buy_vol = recent_20[recent_20["Is_Green"]]["Volume"].sum()
    sell_vol = recent_20[~recent_20["Is_Green"]]["Volume"].sum()
    vol_ratio = round(buy_vol / sell_vol, 2) if sell_vol > 0 else 1.0

    latest = df.iloc[-1]
    prev = df.iloc[-2]
    current_price = round(float(latest["Close"]), 2)

    patterns = []
    if latest["Lower_Wick"] > (2 * latest["Body"]) and latest["Upper_Wick"] < latest["Body"]:
        patterns.append("Hammer (Bullish price rejection from lower levels)")
    if latest["Upper_Wick"] > (2 * latest["Body"]) and latest["Lower_Wick"] < latest["Body"]:
        patterns.append("Shooting Star (Bearish price rejection from higher levels)")
    if not prev["Is_Green"] and latest["Is_Green"] and latest["Close"] > prev["Open"]:
        patterns.append("Bullish Engulfing (Buyers completely overpowered previous red candle)")
    if prev["Is_Green"] and not latest["Is_Green"] and latest["Close"] < prev["Open"]:
        patterns.append("Bearish Engulfing (Sellers completely overpowered previous green candle)")

    bullish_proof = []
    bearish_proof = []

    if slope_pct > 0.1:
        bullish_proof.append(f"Upward Price Slope: Gaining {slope_pct:+.2f}% per session on average.")
    elif slope_pct < -0.1:
        bearish_proof.append(f"Downward Price Slope: Falling {slope_pct:+.2f}% per session on average.")

    if green_count >= 11:
        bullish_proof.append(f"Buyer Dominance: {green_count} Green vs {red_count} Red candles in last 20 days.")
    elif red_count >= 11:
        bearish_proof.append(f"Seller Dominance: {red_count} Red vs {green_count} Green candles in last 20 days.")

    if current_price > latest["EMA_20"] > latest["EMA_50"]:
        bullish_proof.append("Price is trading above both 20-day and 50-day Moving Averages.")
    elif current_price < latest["EMA_20"] < latest["EMA_50"]:
        bearish_proof.append("Price is trading below both 20-day and 50-day Moving Averages.")

    if df["High"].tail(5).max() > df["High"].iloc[-10:-5].max() and df["Low"].tail(5).min() > df["Low"].iloc[
        -10:-5].min():
        bullish_proof.append("Structure confirms Higher Highs & Higher Lows (Classic Uptrend).")
    elif df["High"].tail(5).max() < df["High"].iloc[-10:-5].max() and df["Low"].tail(5).min() < df["Low"].iloc[
        -10:-5].min():
        bearish_proof.append("Structure confirms Lower Highs & Lower Lows (Classic Downtrend).")

    if len(bullish_proof) > len(bearish_proof) and slope_pct >= 0:
        direction = "RISING"
        signal = "BUY" if latest["RSI"] < 68 else "HOLD (Wait for a minor pullback)"
        target = round(current_price * 1.08, 2)
        stop_loss = round(current_price * 0.96, 2)
    elif len(bearish_proof) > len(bullish_proof) and slope_pct < 0:
        direction = "DROPPING"
        signal = "SELL / DO NOT BUY"
        target = round(current_price * 0.92, 2)
        stop_loss = round(current_price * 1.04, 2)
    else:
        direction = "SIDEWAYS"
        signal = "WAIT (Neutral Consolidation)"
        target = None
        stop_loss = None

    return {
        "price": current_price,
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


# ==============================================================================
# 4. RENDER DASHBOARD
# ==============================================================================
@safe_fragment(run_every=refresh_timer)
def render_dashboard(sym, name, tf):
    try:
        data = yf.Ticker(sym).history(period=tf)
        if data.empty or len(data) < 15:
            st.error(f"Could not load trading history for '{sym}'. Ensure the symbol is correct.")
            return

        res = analyze_stock_candles(data)

        st.subheader(f"{name} ({sym})")
        st.caption(
            f"Last updated: {pd.Timestamp.now().strftime('%H:%M:%S IST')} | Auto-refresh: {'On (60s)' if auto_refresh else 'Off'}")

        # Big Direction Banner
        if res["direction"] == "RISING":
            st.success(f"### 🟢 PRICE IS RISING (UPTREND) — Action: {res['signal']}")
        elif res["direction"] == "DROPPING":
            st.error(f"### 🔴 PRICE IS DROPPING (DOWNTREND) — Action: {res['signal']}")
        else:
            st.warning(f"### 🟡 PRICE IS SIDEWAYS (CONSOLIDATION) — Action: {res['signal']}")

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Current Price", f"₹{res['price']:,.2f}")
        m2.metric("20-Day Candles", f"{res['green_count']} Green / {res['red_count']} Red")
        m3.metric("Trend Slope", f"{res['slope_pct']:+}% / day")
        m4.metric("Take-Profit Target", f"₹{res['target']:,.2f}" if res['target'] else "Wait")
        m5.metric("Defensive Stop-Loss", f"₹{res['stop_loss']:,.2f}" if res['stop_loss'] else "N/A")

        st.markdown("---")

        col_chart, col_reasons = st.columns([2, 1])

        with col_chart:
            st.markdown("#### Candlestick Chart with 20 & 50 EMAs")
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_width=[0.28, 0.72])

            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"],
                name="Candles"
            ), row=1, col=1)

            fig.add_trace(
                go.Scatter(x=data.index, y=data["EMA_20"], line=dict(color="orange", width=1.5), name="20 EMA"), row=1,
                col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data["EMA_50"], line=dict(color="blue", width=1.5), name="50 EMA"),
                          row=1, col=1)

            fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], line=dict(color="purple", width=1.5), name="RSI"),
                          row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

            fig.update_layout(height=520, margin=dict(l=10, r=10, t=10, b=10), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_reasons:
            st.markdown("#### Why is the Stock Rising or Dropping?")
            if res["bullish_proof"]:
                st.markdown("**Bullish Proof Points:**")
                for item in res["bullish_proof"]:
                    st.write(f"✅ {item}")

            if res["bearish_proof"]:
                st.markdown("**Bearish Warning Points:**")
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
            st.write(f"- **20-Day EMA**: `₹{res['ema20']:,.2f}`")
            st.write(f"- **50-Day EMA**: `₹{res['ema50']:,.2f}`")

            if res["direction"] == "RISING":
                st.info(
                    "💡 **Trade Tip:** Buyers dominate. If entering on BUY, place your stop-loss order at the displayed defensive price.")
            elif res["direction"] == "DROPPING":
                st.warning(
                    "⚠️ **Risk Alert:** Sellers dominate. Avoid buying until clear green reversal candles emerge.")

    except Exception as e:
        st.error(f"Error evaluating stock: {e}")


# Run Dashboard (Safe execution in all cases)
render_dashboard(ticker_symbol, company_name, timeframe)

# Legal Footer
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** This application is an automated technical analysis tool built strictly for "
    "educational, research, and algorithmic demonstration purposes. It does not provide financial advice, "
    "stock recommendations, or SEBI-registered investment advisory services. Stock trading involves "
    "substantial risk of loss. Always perform your own independent research before trading."
)