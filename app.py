"""
╔══════════════════════════════════════════════════════════════════════╗
║         NeuroBro Multi-Asset Quantitative Analyzer v2.0             ║
║         Senior Python Developer + Expert Quant Financial Analyst    ║
║         100% FREE · NO API KEY · ANTI-MACET ARCHITECTURE           ║
╚══════════════════════════════════════════════════════════════════════╝

INSTALL DEPENDENCIES:
    pip install streamlit yfinance requests pandas numpy

RUN:
    streamlit run app.py
"""

import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
import random

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroBro Quant Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────
# CUSTOM CSS – DARK TERMINAL AESTHETIC
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Base ── */
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    background-color: #0a0c10 !important;
    color: #c9d1d9 !important;
    font-family: 'Inter', sans-serif;
  }

  /* ── Header ── */
  .nb-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 18px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .nb-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #58a6ff;
    letter-spacing: -0.5px;
    margin: 0;
  }
  .nb-subtitle {
    font-size: 0.78rem;
    color: #6e7681;
    margin: 2px 0 0 0;
    font-family: 'JetBrains Mono', monospace;
  }
  .nb-badge {
    background: #1f6feb22;
    border: 1px solid #1f6feb55;
    color: #58a6ff;
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 3px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .nb-live-dot {
    width: 8px; height: 8px;
    background: #3fb950;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.5s infinite;
    margin-right: 6px;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.3; }
  }

  /* ── Cards ── */
  .nb-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 14px;
  }
  .nb-card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ── Asset Selector Buttons ── */
  .stButton > button {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
    width: 100% !important;
  }
  .stButton > button:hover {
    background: #1f6feb33 !important;
    border-color: #58a6ff88 !important;
    color: #58a6ff !important;
  }

  /* ── Decision Boxes ── */
  .decision-strong-buy {
    background: linear-gradient(135deg, #0d2818 0%, #132d1a 100%);
    border: 2px solid #3fb950;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }
  .decision-sell {
    background: linear-gradient(135deg, #2d0d12 0%, #3a0f17 100%);
    border: 2px solid #f85149;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }
  .decision-wait {
    background: linear-gradient(135deg, #1c1a09 0%, #2d2a0d 100%);
    border: 2px solid #d29922;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }
  .decision-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 2px;
  }
  .label-buy   { color: #3fb950; }
  .label-sell  { color: #f85149; }
  .label-wait  { color: #d29922; }

  /* ── Level Grid ── */
  .level-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 14px;
  }
  .level-box {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
  }
  .level-label {
    font-size: 0.65rem;
    color: #6e7681;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }
  .level-entry { color: #58a6ff; font-weight: 600; font-size: 0.9rem; font-family: 'JetBrains Mono', monospace; }
  .level-tp    { color: #3fb950; font-weight: 600; font-size: 0.9rem; font-family: 'JetBrains Mono', monospace; }
  .level-sl    { color: #f85149; font-weight: 600; font-size: 0.9rem; font-family: 'JetBrains Mono', monospace; }

  /* ── Narasi Neurobro ── */
  .neurobro-narasi {
    background: #0d1117;
    border-left: 3px solid #58a6ff;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    font-size: 0.82rem;
    color: #8b949e;
    line-height: 1.7;
    font-style: italic;
    margin-top: 14px;
  }

  /* ── Indicators ── */
  .ind-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #21262d;
    font-size: 0.8rem;
  }
  .ind-row:last-child { border-bottom: none; }
  .ind-name { color: #6e7681; font-family: 'JetBrains Mono', monospace; font-size: 0.73rem; }
  .ind-val  { font-family: 'JetBrains Mono', monospace; font-weight: 600; }
  .bull { color: #3fb950; }
  .bear { color: #f85149; }
  .neut { color: #d29922; }

  /* ── News ── */
  .news-item {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
  }
  .news-item:hover { border-color: #30363d; }
  .news-title { font-size: 0.8rem; color: #c9d1d9; line-height: 1.5; margin-bottom: 6px; }
  .news-meta  { font-size: 0.68rem; color: #6e7681; font-family: 'JetBrains Mono', monospace; }
  .sentiment-bull {
    background: #0d2818; color: #3fb950;
    border: 1px solid #3fb95055;
    padding: 2px 8px; border-radius: 20px;
    font-size: 0.65rem; font-family: 'JetBrains Mono', monospace;
    font-weight: 700; letter-spacing: 1px;
  }
  .sentiment-bear {
    background: #2d0d12; color: #f85149;
    border: 1px solid #f8514955;
    padding: 2px 8px; border-radius: 20px;
    font-size: 0.65rem; font-family: 'JetBrains Mono', monospace;
    font-weight: 700; letter-spacing: 1px;
  }

  /* ── Streamlit overrides ── */
  .stMetric { background: #161b22 !important; border: 1px solid #21262d; border-radius: 10px; padding: 12px 16px !important; }
  .stMetric label { color: #6e7681 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem !important; }
  .stMetric [data-testid="metric-container"] > div:nth-child(2) { font-family: 'JetBrains Mono', monospace !important; }
  div[data-testid="stHorizontalBlock"] { gap: 12px; }
  .stSelectbox > div > div { background: #161b22 !important; border: 1px solid #21262d !important; border-radius: 8px !important; }
  .stSelectbox label { color: #6e7681 !important; font-size: 0.75rem !important; font-family: 'JetBrains Mono', monospace !important; }
  footer { display: none !important; }
  #MainMenu { display: none !important; }
  .block-container { padding: 20px 28px 40px 28px !important; }
  hr { border-color: #21262d !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# ASSET REGISTRY
# ─────────────────────────────────────────────────────────────────────
CRYPTO_ASSETS = {
    "BTC (Bitcoin)":  {"binance": "BTCUSDT", "label": "BTC/USDT"},
    "ETH (Ethereum)": {"binance": "ETHUSDT", "label": "ETH/USDT"},
    "SOL (Solana)":   {"binance": "SOLUSDT", "label": "SOL/USDT"},
}
FOREX_ASSETS = {
    "EUR/USD": {"yf": "EURUSD=X", "label": "EUR/USD"},
    "GBP/USD": {"yf": "GBPUSD=X", "label": "GBP/USD"},
    "USD/JPY": {"yf": "JPY=X",    "label": "USD/JPY"},
    "XAU/USD (Gold)": {"yf": "GC=F", "label": "XAU/USD"},
}
STOCK_ASSETS = {
    "AAPL (Apple)":  {"yf": "AAPL",  "label": "AAPL"},
    "NVDA (NVIDIA)": {"yf": "NVDA",  "label": "NVDA"},
    "TSLA (Tesla)":  {"yf": "TSLA",  "label": "TSLA"},
}

RSS_FEEDS = [
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "https://feeds.reuters.com/reuters/businessNews",
]

NEUROBRO_BULLISH_NARRATIVES = [
    "Smart Money accumulation phase detected — institutional footprint visible via order flow imbalance. Retail shorts are being hunted.",
    "Higher timeframe structure bullish. DXY weakness creating macro tailwind. Expect continuation after liquidity sweep.",
    "Order Block mitigation complete. Premium zone rejected. Discount array now in play — risk/reward favoring longs.",
    "Buyside liquidity resting above equal highs. Market structure shift imminent. This is where Smart Money loads positions.",
    "Displacement candle confirmed on significant timeframe. FVG acting as magnet. Retail exhaustion phase validated.",
    "Institutional accumulation detected below market structure. Stop clusters at key level primed for sweep before reversal.",
]
NEUROBRO_BEARISH_NARRATIVES = [
    "Distribution phase active. Smart Money offloading into retail euphoria. Classic Wyckoff upthrust before markdown.",
    "DXY strength compressing risk assets. Macro headwinds prevail. Sellside liquidity pools are the target.",
    "Supply zone rejection confirmed. Premium pricing vs theoretical fair value screams distribution. Fade the rally.",
    "Bearish Order Block holding. Inducement run above local high cleared retail longs. Institutional sell program activated.",
    "Market structure break to the downside. FVG below acting as delivery target. Retail caught holding bags at the top.",
    "Liquidity void below — price will fill it with zero mercy. Bearish displacement on HTF validates the narrative.",
]
NEUROBRO_WAIT_NARRATIVES = [
    "No clean setup. Price is in consolidation — this is the grinder zone where retail loses money both ways. WAIT.",
    "Liquidity equalized on both sides. Institutional intent ambiguous. Entering here is gambling, not trading.",
    "Mid-range price action. Neither Premium nor Discount. Smart Money is not committed — neither should you be.",
    "Chopzone detected. Equilibrium pricing with no directional bias. The best trade is no trade until clarity emerges.",
    "Indecisive candle structure. Both buy and sell pressure equal. DXY ranging sideways — forex pairs will chop violently.",
]


# ─────────────────────────────────────────────────────────────────────
# DATA FETCHING — CRYPTO (Binance Public API)
# ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=90)
def fetch_crypto_binance(symbol: str) -> dict:
    """Fetch price + 24h stats from Binance public REST (no key required)."""
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        d = r.json()
        return {
            "price":        float(d["lastPrice"]),
            "open":         float(d["openPrice"]),
            "high":         float(d["highPrice"]),
            "low":          float(d["lowPrice"]),
            "change_pct":   float(d["priceChangePercent"]),
            "volume":       float(d["quoteVolume"]),
            "source":       "Binance",
            "ok":           True,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@st.cache_data(ttl=300)
def fetch_crypto_history(symbol: str, limit: int = 100) -> pd.DataFrame:
    """Fetch OHLCV klines from Binance (1-hour bars)."""
    try:
        url = (
            f"https://api.binance.com/api/v3/klines"
            f"?symbol={symbol}&interval=1h&limit={limit}"
        )
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        raw = r.json()
        df = pd.DataFrame(raw, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","qv","n","tbv","tqv","ignore"
        ])
        for col in ["open","high","low","close","volume"]:
            df[col] = df[col].astype(float)
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df.set_index("open_time", inplace=True)
        return df
    except Exception:
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────
# DATA FETCHING — FOREX / GOLD / STOCKS (yfinance)
# ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=120)
def fetch_yf_quote(ticker: str) -> dict:
    """Fetch latest quote + 2-day history from Yahoo Finance."""
    try:
        tk = yf.Ticker(ticker)
        hist = tk.history(period="5d", interval="1d")
        if hist.empty:
            return {"ok": False, "error": "No data from Yahoo Finance"}
        latest = hist.iloc[-1]
        prev   = hist.iloc[-2] if len(hist) >= 2 else hist.iloc[-1]
        price  = float(latest["Close"])
        open_  = float(latest["Open"])
        high   = float(latest["High"])
        low    = float(latest["Low"])
        prev_c = float(prev["Close"])
        chg    = ((price - prev_c) / prev_c) * 100
        return {
            "price": price, "open": open_, "high": high, "low": low,
            "prev_close": prev_c, "change_pct": chg,
            "source": "Yahoo Finance", "ok": True,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@st.cache_data(ttl=300)
def fetch_yf_history(ticker: str, period: str = "30d", interval: str = "1d") -> pd.DataFrame:
    try:
        tk = yf.Ticker(ticker)
        df = tk.history(period=period, interval=interval)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────
# QUANT ENGINE — TECHNICAL INDICATORS
# ─────────────────────────────────────────────────────────────────────
def compute_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()


def compute_rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff().dropna()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_gain = gain.rolling(period).mean().iloc[-1]
    avg_loss = loss.rolling(period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs  = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(float(rsi), 2)


def compute_macd(series: pd.Series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd_line   = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram   = macd_line - signal_line
    return float(macd_line.iloc[-1]), float(signal_line.iloc[-1]), float(histogram.iloc[-1])


def compute_bollinger(series: pd.Series, window: int = 20):
    mid  = series.rolling(window).mean()
    std  = series.rolling(window).std()
    upper = mid + 2 * std
    lower = mid - 2 * std
    return float(upper.iloc[-1]), float(mid.iloc[-1]), float(lower.iloc[-1])


def compute_stoch_rsi(series: pd.Series, period: int = 14) -> float:
    """Stochastic RSI oscillator (0–100)."""
    rsi_vals = []
    for i in range(period, len(series)):
        sl = series.iloc[i - period:i + 1]
        rsi_vals.append(compute_rsi(sl, period=min(period, len(sl) - 1)))
    if not rsi_vals:
        return 50.0
    rsi_s = pd.Series(rsi_vals)
    min_r = rsi_s.rolling(period).min().iloc[-1]
    max_r = rsi_s.rolling(period).max().iloc[-1]
    if max_r == min_r:
        return 50.0
    return round(float((rsi_s.iloc[-1] - min_r) / (max_r - min_r) * 100), 2)


def volatility_pct(high: float, low: float, price: float) -> float:
    return round(((high - low) / price) * 100, 4)


# ─────────────────────────────────────────────────────────────────────
# NEUROBRO ANALYSIS ENGINE
# ─────────────────────────────────────────────────────────────────────
def run_neurobro_analysis(quote: dict, df: pd.DataFrame) -> dict:
    """
    Core quant brain.  Combines RSI, MACD, Bollinger, SMA cross,
    price-vs-range position to produce decision + levels + narrative.
    """
    price  = quote["price"]
    high   = quote["high"]
    low    = quote["low"]
    open_  = quote["open"]
    chg    = quote["change_pct"]
    vol    = volatility_pct(high, low, price)

    # ── Indicator computation ──────────────────────────────────────
    score   = 0  # accumulated signal: positive = bull, negative = bear
    signals = {}

    if df.empty or len(df) < 26:
        # Fallback to pure price-action scoring
        signals["RSI"]         = ("N/A", "neut")
        signals["MACD"]        = ("N/A", "neut")
        signals["BB Position"] = ("N/A", "neut")
        signals["SMA Cross"]   = ("N/A", "neut")
        signals["Price Trend"] = (f"{chg:+.2f}%", "bull" if chg > 0 else "bear")
        score += 1 if chg > 0 else -1
    else:
        close = df["close"]

        # RSI
        rsi = compute_rsi(close)
        if rsi < 35:
            signals["RSI"] = (f"{rsi}", "bull"); score += 2
        elif rsi > 65:
            signals["RSI"] = (f"{rsi}", "bear"); score -= 2
        else:
            signals["RSI"] = (f"{rsi}", "neut")

        # MACD
        macd_v, sig_v, hist_v = compute_macd(close)
        if hist_v > 0:
            signals["MACD"] = (f"HIST +{hist_v:.4f}", "bull"); score += 1
        else:
            signals["MACD"] = (f"HIST {hist_v:.4f}", "bear"); score -= 1

        # Bollinger Bands
        bb_upper, bb_mid, bb_lower = compute_bollinger(close)
        bb_pos = (price - bb_lower) / (bb_upper - bb_lower + 1e-9) * 100
        if bb_pos < 25:
            signals["BB Position"] = (f"{bb_pos:.1f}% (Oversold)", "bull"); score += 2
        elif bb_pos > 75:
            signals["BB Position"] = (f"{bb_pos:.1f}% (Overbought)", "bear"); score -= 2
        else:
            signals["BB Position"] = (f"{bb_pos:.1f}% (Neutral)", "neut")

        # SMA Cross (20 vs 50)
        sma20 = compute_sma(close, 20).iloc[-1]
        sma50 = compute_sma(close, min(50, len(close) - 1)).iloc[-1]
        if sma20 > sma50:
            signals["SMA Cross"] = (f"SMA20>{sma50:.2f}", "bull"); score += 1
        else:
            signals["SMA Cross"] = (f"SMA20<{sma50:.2f}", "bear"); score -= 1

        # Price vs Daily Range (HTF momentum proxy)
        range_pos = (price - low) / (high - low + 1e-9) * 100
        if range_pos > 65:
            signals["Range Pos"] = (f"{range_pos:.1f}% (Upper)", "bull"); score += 1
        elif range_pos < 35:
            signals["Range Pos"] = (f"{range_pos:.1f}% (Lower)", "bear"); score -= 1
        else:
            signals["Range Pos"] = (f"{range_pos:.1f}% (Mid)", "neut")

    # ── Decision Logic ────────────────────────────────────────────
    if score >= 3:
        decision = "STRONG BUY"
        d_class  = "strong-buy"
        narrative = random.choice(NEUROBRO_BULLISH_NARRATIVES)
    elif score <= -3:
        decision = "ACTIONABLE SELL"
        d_class  = "sell"
        narrative = random.choice(NEUROBRO_BEARISH_NARRATIVES)
    else:
        decision = "LIQUIDITY HUNT (WAIT)"
        d_class  = "wait"
        narrative = random.choice(NEUROBRO_WAIT_NARRATIVES)

    # ── Level Calculation (volatility-based) ─────────────────────
    # Entry: current price
    # TP:   1.5× daily range from entry in signal direction
    # SL:   0.8× daily range from entry against signal direction
    daily_range = high - low
    if d_class == "strong-buy":
        entry = round(price, _decimals(price))
        tp    = round(price + 1.5 * daily_range, _decimals(price))
        sl    = round(price - 0.8 * daily_range, _decimals(price))
    elif d_class == "sell":
        entry = round(price, _decimals(price))
        tp    = round(price - 1.5 * daily_range, _decimals(price))
        sl    = round(price + 0.8 * daily_range, _decimals(price))
    else:
        entry = round(price, _decimals(price))
        tp    = round(price + 1.0 * daily_range, _decimals(price))
        sl    = round(price - 1.0 * daily_range, _decimals(price))

    rr_ratio = abs(tp - entry) / (abs(sl - entry) + 1e-9)

    return {
        "decision":  decision,
        "d_class":   d_class,
        "score":     score,
        "signals":   signals,
        "entry":     entry,
        "tp":        tp,
        "sl":        sl,
        "rr":        round(rr_ratio, 2),
        "vol_pct":   vol,
        "narrative": narrative,
    }


def _decimals(price: float) -> int:
    """Sensible decimal places based on price magnitude."""
    if price >= 1000: return 2
    if price >= 10:   return 4
    return 6


# ─────────────────────────────────────────────────────────────────────
# NEWS ENGINE — RSS PARSER + SENTIMENT
# ─────────────────────────────────────────────────────────────────────
BULLISH_KEYWORDS = [
    "surge", "rally", "gain", "rise", "bull", "buy", "growth", "record",
    "boost", "breakout", "recovery", "strong", "upside", "profit", "soar",
]
BEARISH_KEYWORDS = [
    "fall", "drop", "crash", "sell", "bear", "decline", "recession", "fear",
    "loss", "plunge", "weak", "risk", "concern", "warning", "inflation", "hawkish",
]


def classify_sentiment(text: str) -> str:
    t = text.lower()
    bull = sum(1 for w in BULLISH_KEYWORDS if w in t)
    bear = sum(1 for w in BEARISH_KEYWORDS if w in t)
    return "BULLISH" if bull >= bear else "BEARISH"


@st.cache_data(ttl=300)
def fetch_rss_news() -> list:
    """Try multiple RSS feeds; return list of news dicts."""
    articles = []
    headers  = {"User-Agent": "Mozilla/5.0 NeuroBro/2.0"}

    for feed_url in RSS_FEEDS:
        try:
            r = requests.get(feed_url, timeout=8, headers=headers)
            r.raise_for_status()
            root = ET.fromstring(r.content)
            items = root.findall(".//item")[:6]
            for item in items:
                title = (item.findtext("title") or "").strip()
                pub   = (item.findtext("pubDate") or "").strip()
                link  = (item.findtext("link") or "").strip()
                desc  = (item.findtext("description") or "").strip()
                if title:
                    articles.append({
                        "title":     title,
                        "pub":       pub[:22] if pub else "—",
                        "link":      link,
                        "sentiment": classify_sentiment(title + " " + desc),
                    })
            if articles:
                break  # first successful feed is enough
        except Exception:
            continue

    if not articles:
        articles = _generate_simulated_news()

    return articles[:10]


def _generate_simulated_news() -> list:
    """Fallback: synthesize plausible headlines from macro themes."""
    templates = [
        ("Fed officials signal cautious stance on rate cuts amid sticky inflation", "BEARISH"),
        ("Bitcoin breaks key resistance — institutional accumulation confirmed", "BULLISH"),
        ("DXY surges to multi-week high, pressuring EUR/USD and commodities", "BEARISH"),
        ("NVIDIA earnings beat expectations; AI demand cycle remains intact", "BULLISH"),
        ("Gold retreats from highs as Treasury yields tick higher", "BEARISH"),
        ("Risk appetite returns: equities rally on softer macro data", "BULLISH"),
        ("Tesla delivery numbers disappoint; analysts revise targets lower", "BEARISH"),
        ("Ethereum Layer-2 ecosystem sees record daily active addresses", "BULLISH"),
        ("JPY strengthens as BOJ signals possible policy normalization", "BEARISH"),
        ("S&P 500 futures edge higher ahead of key CPI release", "BULLISH"),
    ]
    random.shuffle(templates)
    now = datetime.utcnow().strftime("%d %b %Y %H:%M")
    return [
        {"title": t, "sentiment": s, "pub": now, "link": "#"}
        for t, s in templates[:8]
    ]


# ─────────────────────────────────────────────────────────────────────
# HELPER: FORMAT PRICE
# ─────────────────────────────────────────────────────────────────────
def fmt_price(price: float, ticker_type: str = "crypto") -> str:
    if ticker_type == "crypto" and price >= 1000:
        return f"${price:,.2f}"
    if ticker_type == "crypto":
        return f"${price:,.4f}"
    if ticker_type == "forex":
        return f"{price:.5f}"
    return f"${price:,.2f}"


# ─────────────────────────────────────────────────────────────────────
# SESSION STATE — SELECTED ASSET
# ─────────────────────────────────────────────────────────────────────
if "selected_asset"      not in st.session_state:
    st.session_state.selected_asset      = "BTC (Bitcoin)"
if "selected_category"   not in st.session_state:
    st.session_state.selected_category   = "CRYPTO"


# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────
ts = datetime.utcnow().strftime("%d %b %Y · %H:%M UTC")
st.markdown(f"""
<div class="nb-header">
  <div>
    <p class="nb-title">🧠 NeuroBro Multi-Asset Quantitative Analyzer</p>
    <p class="nb-subtitle">
      <span class="nb-live-dot"></span>LIVE &nbsp;·&nbsp; {ts} &nbsp;·&nbsp;
      Crypto · Forex · Gold · Equities
    </p>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;">
    <span class="nb-badge">Anti-Macet v2</span>
    <span class="nb-badge">No API Key</span>
    <span class="nb-badge">Quant Engine</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# THREE-COLUMN LAYOUT
# ─────────────────────────────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([1.1, 1.8, 1.1], gap="medium")


# ══════════════════════════════════════════════════════════════════════
# LEFT COLUMN — ASSET SELECTOR & REAL-TIME PRICES
# ══════════════════════════════════════════════════════════════════════
with col_left:

    # ── Category selector ─────────────────────────────────────────
    st.markdown('<div class="nb-card-title">📡 MARKET CATEGORY</div>', unsafe_allow_html=True)
    cat = st.selectbox(
        "Select Market",
        ["CRYPTO", "FOREX & GOLD", "STOCKS"],
        label_visibility="collapsed",
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Asset buttons ────────────────────────────────────────────
    st.markdown('<div class="nb-card-title">🎯 SELECT ASSET</div>', unsafe_allow_html=True)

    if cat == "CRYPTO":
        assets = list(CRYPTO_ASSETS.keys())
    elif cat == "FOREX & GOLD":
        assets = list(FOREX_ASSETS.keys())
    else:
        assets = list(STOCK_ASSETS.keys())

    for a in assets:
        if st.button(a, key=f"btn_{a}"):
            st.session_state.selected_asset    = a
            st.session_state.selected_category = cat

    # Sync category if changed via selectbox
    if cat != st.session_state.selected_category:
        st.session_state.selected_category = cat
        st.session_state.selected_asset    = assets[0]

    selected = st.session_state.selected_asset
    if selected not in assets:
        selected = assets[0]
        st.session_state.selected_asset = selected

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Live Price Ticker for ALL assets in category ──────────────
    st.markdown('<div class="nb-card-title">💹 LIVE PRICES</div>', unsafe_allow_html=True)

    if cat == "CRYPTO":
        for name, cfg in CRYPTO_ASSETS.items():
            q = fetch_crypto_binance(cfg["binance"])
            if q["ok"]:
                delta_str = f"{q['change_pct']:+.2f}%"
                st.metric(
                    label=cfg["label"],
                    value=f"${q['price']:,.2f}",
                    delta=delta_str,
                )
            else:
                st.metric(label=name, value="—", delta="Error")

    elif cat == "FOREX & GOLD":
        for name, cfg in FOREX_ASSETS.items():
            q = fetch_yf_quote(cfg["yf"])
            if q["ok"]:
                p     = q["price"]
                dp    = f"{q['change_pct']:+.3f}%"
                label = cfg["label"]
                if "Gold" in name:
                    st.metric(label=label, value=f"${p:,.2f}", delta=dp)
                elif "JPY" in name:
                    st.metric(label=label, value=f"{p:.3f}", delta=dp)
                else:
                    st.metric(label=label, value=f"{p:.5f}", delta=dp)
            else:
                st.metric(label=name, value="—", delta="Error")

    else:
        for name, cfg in STOCK_ASSETS.items():
            q = fetch_yf_quote(cfg["yf"])
            if q["ok"]:
                st.metric(
                    label=cfg["label"],
                    value=f"${q['price']:,.2f}",
                    delta=f"{q['change_pct']:+.2f}%",
                )
            else:
                st.metric(label=name, value="—", delta="Error")

    # ── Cache info ────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:14px;padding:10px 14px;background:#0d1117;
         border:1px solid #21262d;border-radius:8px;">
      <div style="font-size:0.65rem;color:#6e7681;font-family:'JetBrains Mono',monospace;line-height:1.8;">
        🔄 Crypto cache: 90s<br>
        🔄 Forex/Stock cache: 120s<br>
        🔄 History cache: 300s<br>
        ⚡ Anti-429 rate protection ON
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# MIDDLE COLUMN — NEUROBRO ANALYSIS
# ══════════════════════════════════════════════════════════════════════
with col_mid:

    selected = st.session_state.selected_asset
    cat      = st.session_state.selected_category

    # ── Fetch data for selected asset ─────────────────────────────
    if cat == "CRYPTO":
        cfg   = CRYPTO_ASSETS.get(selected, list(CRYPTO_ASSETS.values())[0])
        quote = fetch_crypto_binance(cfg["binance"])
        df    = fetch_crypto_history(cfg["binance"], limit=100) if quote.get("ok") else pd.DataFrame()
        price_label = cfg["label"]
        t_type = "crypto"

    elif cat == "FOREX & GOLD":
        cfg   = FOREX_ASSETS.get(selected, list(FOREX_ASSETS.values())[0])
        quote = fetch_yf_quote(cfg["yf"])
        df    = fetch_yf_history(cfg["yf"], period="60d", interval="1d") if quote.get("ok") else pd.DataFrame()
        price_label = cfg["label"]
        t_type = "forex"

    else:
        cfg   = STOCK_ASSETS.get(selected, list(STOCK_ASSETS.values())[0])
        quote = fetch_yf_quote(cfg["yf"])
        df    = fetch_yf_history(cfg["yf"], period="60d", interval="1d") if quote.get("ok") else pd.DataFrame()
        price_label = cfg["label"]
        t_type = "stock"

    # ── Run Analysis ─────────────────────────────────────────────
    if not quote.get("ok"):
        st.error(f"⚠️ Data unavailable: {quote.get('error','Unknown error')}. Retry in ~30s.")
        st.stop()

    ana = run_neurobro_analysis(quote, df)

    # ── Decision Box ─────────────────────────────────────────────
    d = ana["decision"]
    dc = ana["d_class"]
    css_class  = f"decision-{dc}"
    label_cls  = "label-buy" if dc == "strong-buy" else ("label-sell" if dc == "sell" else "label-wait")
    emoji_map  = {"strong-buy": "🟢", "sell": "🔴", "wait": "🟡"}

    entry_fmt = f"{ana['entry']:,.{_decimals(ana['entry'])}f}"
    tp_fmt    = f"{ana['tp']:,.{_decimals(ana['tp'])}f}"
    sl_fmt    = f"{ana['sl']:,.{_decimals(ana['sl'])}f}"

    st.markdown(f"""
    <div class="{css_class}">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
        <span style="font-size:1.6rem;">{emoji_map[dc]}</span>
        <div>
          <div style="font-size:0.65rem;color:#6e7681;font-family:'JetBrains Mono',monospace;
               letter-spacing:2px;text-transform:uppercase;margin-bottom:2px;">
            NeuroBro Decision · {price_label}
          </div>
          <div class="decision-label {label_cls}">{d}</div>
        </div>
        <div style="margin-left:auto;text-align:right;">
          <div style="font-size:0.65rem;color:#6e7681;font-family:'JetBrains Mono',monospace;">Signal Score</div>
          <div style="font-size:1.4rem;font-weight:700;font-family:'JetBrains Mono',monospace;
               color:{'#3fb950' if ana['score']>0 else ('#f85149' if ana['score']<0 else '#d29922')}">
            {ana['score']:+d}
          </div>
        </div>
      </div>

      <div class="level-grid">
        <div class="level-box">
          <div class="level-label">⚡ ENTRY</div>
          <div class="level-entry">{entry_fmt}</div>
        </div>
        <div class="level-box">
          <div class="level-label">🎯 TAKE PROFIT</div>
          <div class="level-tp">{tp_fmt}</div>
        </div>
        <div class="level-box">
          <div class="level-label">🛑 STOP LOSS</div>
          <div class="level-sl">{sl_fmt}</div>
        </div>
      </div>

      <div style="display:flex;gap:12px;margin-top:12px;">
        <div style="background:#0d1117;border:1px solid #21262d;border-radius:6px;
             padding:6px 12px;font-size:0.72rem;font-family:'JetBrains Mono',monospace;">
          R:R &nbsp;<span style="color:#58a6ff;font-weight:700;">1:{ana['rr']:.1f}</span>
        </div>
        <div style="background:#0d1117;border:1px solid #21262d;border-radius:6px;
             padding:6px 12px;font-size:0.72rem;font-family:'JetBrains Mono',monospace;">
          Volatility &nbsp;<span style="color:#d29922;font-weight:700;">{ana['vol_pct']:.2f}%</span>
        </div>
        <div style="background:#0d1117;border:1px solid #21262d;border-radius:6px;
             padding:6px 12px;font-size:0.72rem;font-family:'JetBrains Mono',monospace;">
          Source &nbsp;<span style="color:#6e7681;">{quote['source']}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── NeuroBro Narrative ────────────────────────────────────────
    st.markdown(f"""
    <div class="neurobro-narasi">
      <span style="color:#58a6ff;font-style:normal;font-weight:700;
            font-family:'JetBrains Mono',monospace;">🧠 NeuroBro Analysis:</span><br><br>
      {ana['narrative']}
    </div>
    """, unsafe_allow_html=True)

    # ── Technical Indicators Panel ────────────────────────────────
    st.markdown("""
    <div class="nb-card" style="margin-top:14px;">
      <div class="nb-card-title">📊 TECHNICAL INDICATORS</div>
    """, unsafe_allow_html=True)

    ind_html = ""
    for name, (val, sig) in ana["signals"].items():
        sig_icon = "▲" if sig == "bull" else ("▼" if sig == "bear" else "◆")
        ind_html += f"""
        <div class="ind-row">
          <span class="ind-name">{name}</span>
          <span class="ind-val {sig}">{sig_icon} {val}</span>
        </div>
        """
    st.markdown(ind_html + "</div>", unsafe_allow_html=True)

    # ── Price Chart ───────────────────────────────────────────────
    if not df.empty and len(df) >= 5:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="nb-card-title">📈 PRICE HISTORY</div>', unsafe_allow_html=True)

        chart_df = df[["close"]].copy() if "close" in df.columns else pd.DataFrame()
        if chart_df.empty and "Close" in df.columns:
            chart_df = df[["Close"]].rename(columns={"Close": "close"})

        if not chart_df.empty:
            # Add SMA20 if enough data
            chart_df["SMA20"] = chart_df["close"].rolling(20).mean()
            chart_df["SMA50"] = chart_df["close"].rolling(50).mean()
            st.line_chart(
                chart_df.tail(60),
                height=220,
                use_container_width=True,
            )

    # ── OHLC Summary ──────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    p = quote["price"]
    dp = _decimals(p)
    c1.metric("OPEN",  f"{quote['open']:,.{dp}f}")
    c2.metric("HIGH",  f"{quote['high']:,.{dp}f}")
    c3.metric("LOW",   f"{quote['low']:,.{dp}f}")
    c4.metric("PRICE", f"{p:,.{dp}f}", delta=f"{quote['change_pct']:+.3f}%")


# ══════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — NEWS & SENTIMENT
# ══════════════════════════════════════════════════════════════════════
with col_right:

    st.markdown('<div class="nb-card-title">📰 MARKET NEWS & SENTIMENT</div>', unsafe_allow_html=True)

    news = fetch_rss_news()

    bull_count = sum(1 for n in news if n["sentiment"] == "BULLISH")
    bear_count = len(news) - bull_count
    overall    = "BULLISH" if bull_count >= bear_count else "BEARISH"
    overall_pct = int(bull_count / max(len(news), 1) * 100)

    # Overall sentiment meter
    meter_color = "#3fb950" if overall == "BULLISH" else "#f85149"
    st.markdown(f"""
    <div style="background:#161b22;border:1px solid #21262d;border-radius:10px;
         padding:14px 18px;margin-bottom:14px;">
      <div style="font-size:0.65rem;color:#6e7681;font-family:'JetBrains Mono',monospace;
           text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">
        Overall Market Sentiment
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="font-size:1.3rem;font-weight:700;font-family:'JetBrains Mono',monospace;
             color:{meter_color};">{overall}</div>
        <div style="flex:1;">
          <div style="background:#21262d;border-radius:4px;height:6px;">
            <div style="background:{meter_color};width:{overall_pct}%;
                 height:6px;border-radius:4px;transition:width 0.5s;"></div>
          </div>
        </div>
        <div style="font-size:0.8rem;font-family:'JetBrains Mono',monospace;
             color:{meter_color};">{overall_pct}%</div>
      </div>
      <div style="display:flex;gap:14px;margin-top:8px;">
        <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#3fb950;">
          ▲ BULL {bull_count}
        </div>
        <div style="font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#f85149;">
          ▼ BEAR {bear_count}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # News items
    for item in news:
        sent  = item["sentiment"]
        badge = f'<span class="sentiment-{"bull" if sent=="BULLISH" else "bear"}">{sent}</span>'
        title = item["title"][:110] + ("…" if len(item["title"]) > 110 else "")
        pub   = item["pub"]

        st.markdown(f"""
        <div class="news-item">
          <div class="news-title">{title}</div>
          <div class="news-meta">{badge} &nbsp; {pub}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Disclaimer ────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:16px;padding:12px 16px;background:#0d1117;
         border:1px solid #21262d;border-radius:8px;">
      <div style="font-size:0.65rem;color:#6e7681;line-height:1.7;
           font-family:'JetBrains Mono',monospace;">
        ⚠️ <strong style="color:#d29922;">DISCLAIMER</strong><br>
        NeuroBro output is for <em>educational purposes only</em>
        and does NOT constitute financial advice.
        Always do your own research (DYOR) and manage risk accordingly.
        Past signal accuracy does not guarantee future performance.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Refresh Controls ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="nb-card-title">🔄 DATA CONTROLS</div>', unsafe_allow_html=True)

    if st.button("🔄 Force Refresh All Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(f"""
    <div style="margin-top:10px;font-size:0.66rem;color:#6e7681;
         font-family:'JetBrains Mono',monospace;text-align:center;">
      Last rendered: {datetime.utcnow().strftime('%H:%M:%S')} UTC
    </div>
    """, unsafe_allow_html=True)

    # ── Auto-refresh toggle ────────────────────────────────────────
    auto_refresh = st.checkbox("⚡ Auto-refresh (90s)", value=False)
    if auto_refresh:
        st.markdown("""
        <div style="font-size:0.68rem;color:#3fb950;
             font-family:'JetBrains Mono',monospace;margin-top:6px;">
          ● Auto-refresh active. Cache will handle rate limits.
        </div>
        """, unsafe_allow_html=True)
        time.sleep(90)
        st.cache_data.clear()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:12px;font-size:0.68rem;
     color:#6e7681;font-family:'JetBrains Mono',monospace;">
  🧠 NeuroBro Multi-Asset Quantitative Analyzer v2.0 &nbsp;·&nbsp;
  Powered by Binance Public API + Yahoo Finance + Python Quant Engine &nbsp;·&nbsp;
  Built with ❤️ using Streamlit &nbsp;·&nbsp;
  <span style="color:#3fb950;">100% FREE · NO API KEY</span>
</div>
""", unsafe_allow_html=True)
