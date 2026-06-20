"""
╔══════════════════════════════════════════════════════════════════════════╗
║          NeuroBro Crypto Signal Engine v3.0                             ║
║          Real trading compass — scalping, intraday, swing               ║
║          Data: Bybit REST (no key, no geo-block)                        ║
║          News: CryptoPanic + Google News RSS fallback                   ║
║          Deploy: Streamlit Cloud compatible                             ║
╚══════════════════════════════════════════════════════════════════════════╝

pip install streamlit requests pandas numpy
streamlit run neurobro_crypto.py
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime
import time, random, math

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroBro · Crypto Signal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────
# CSS — terminal-trading-desk aesthetic
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
  background: #080b10 !important;
  color: #dce3ec !important;
  font-family: 'Space Grotesk', sans-serif;
}

/* ── TOP BAR ── */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  background: #0d1117;
  border-bottom: 1px solid #1a2233;
  padding: 12px 24px;
  margin: -20px -28px 24px -28px;
}
.topbar-brand {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1rem; font-weight: 700;
  color: #e2e8f0; letter-spacing: -0.3px;
}
.topbar-brand span { color: #3b82f6; }
.topbar-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem; color: #4a5568;
  display: flex; align-items: center; gap: 16px;
}
.live-pill {
  background: #0f2918; border: 1px solid #166534;
  color: #4ade80; font-size: 0.62rem;
  padding: 2px 10px; border-radius: 20px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px; text-transform: uppercase;
}
.live-dot {
  display: inline-block; width: 6px; height: 6px;
  background: #4ade80; border-radius: 50%;
  margin-right: 5px; animation: blink 1.4s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── COIN SELECTOR TABS ── */
.coin-tab-row {
  display: flex; gap: 8px; margin-bottom: 20px;
}
.coin-tab {
  flex: 1; padding: 10px 0; text-align: center;
  background: #0d1117; border: 1px solid #1a2233;
  border-radius: 8px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem; font-weight: 500;
  color: #64748b; transition: all 0.15s;
}
.coin-tab.active {
  background: #0f1f3d; border-color: #3b82f6;
  color: #93c5fd;
}

/* ── PRICE HERO ── */
.price-hero {
  background: #0d1117;
  border: 1px solid #1a2233;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
}
.price-hero::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
}
.price-coin-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem; color: #4a5568;
  text-transform: uppercase; letter-spacing: 2px;
  margin-bottom: 6px;
}
.price-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2.4rem; font-weight: 700;
  color: #f1f5f9; letter-spacing: -1px;
  line-height: 1;
}
.price-change-pos { color: #4ade80; font-size: 1rem; font-weight: 600; margin-left: 12px; }
.price-change-neg { color: #f87171; font-size: 1rem; font-weight: 600; margin-left: 12px; }
.price-meta-row {
  display: flex; gap: 20px; margin-top: 12px;
  padding-top: 12px; border-top: 1px solid #1a2233;
}
.price-meta-item { flex: 1; }
.price-meta-label {
  font-size: 0.62rem; color: #4a5568;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 3px;
}
.price-meta-val {
  font-size: 0.82rem; font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
  color: #cbd5e1;
}

/* ── MODE SELECTOR ── */
.mode-row { display: flex; gap: 8px; margin-bottom: 16px; }
.mode-chip {
  padding: 6px 16px;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem; font-weight: 500;
  border: 1px solid #1a2233;
  background: #0d1117; color: #4a5568;
  cursor: pointer; transition: all 0.15s;
  white-space: nowrap;
}
.mode-chip.scalping.active  { background:#1a0f2e;border-color:#8b5cf6;color:#c4b5fd; }
.mode-chip.intraday.active  { background:#0f1f3d;border-color:#3b82f6;color:#93c5fd; }
.mode-chip.swing.active     { background:#0f2918;border-color:#22c55e;color:#86efac; }

/* ── SIGNAL BOX ── */
.signal-box {
  border-radius: 12px; padding: 22px 24px;
  margin-bottom: 16px; position: relative; overflow: hidden;
}
.signal-box.buy  { background:#0a1f12; border: 2px solid #22c55e; }
.signal-box.sell { background:#1f0a0a; border: 2px solid #ef4444; }
.signal-box.wait { background:#1a1500; border: 2px solid #eab308; }
.signal-box.buy::after  { content:'BUY';  position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:5rem;font-weight:900;color:#22c55e08;font-family:'JetBrains Mono',monospace;line-height:1; }
.signal-box.sell::after { content:'SELL'; position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:5rem;font-weight:900;color:#ef444408;font-family:'JetBrains Mono',monospace;line-height:1; }
.signal-box.wait::after { content:'WAIT'; position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:5rem;font-weight:900;color:#eab30808;font-family:'JetBrains Mono',monospace;line-height:1; }
.signal-badge {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 2px;
  padding: 3px 10px; border-radius: 4px;
  margin-bottom: 8px;
}
.badge-buy  { background:#14532d; color:#4ade80; }
.badge-sell { background:#7f1d1d; color:#fca5a5; }
.badge-wait { background:#713f12; color:#fde047; }
.signal-decision {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem; font-weight: 700; letter-spacing: 1px;
  margin-bottom: 4px;
}
.signal-decision.buy  { color: #4ade80; }
.signal-decision.sell { color: #f87171; }
.signal-decision.wait { color: #facc15; }
.signal-subtitle {
  font-size: 0.8rem; color: #64748b; margin-bottom: 16px;
}
.confidence-bar-wrap {
  margin-bottom: 16px;
}
.confidence-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; color: #64748b;
  text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 5px; display: flex;
  justify-content: space-between;
}
.confidence-track {
  background: #1a2233; border-radius: 4px; height: 6px; overflow: hidden;
}
.confidence-fill-buy  { background: linear-gradient(90deg,#16a34a,#4ade80); height:6px; border-radius:4px; transition: width 0.5s; }
.confidence-fill-sell { background: linear-gradient(90deg,#dc2626,#f87171); height:6px; border-radius:4px; transition: width 0.5s; }
.confidence-fill-wait { background: linear-gradient(90deg,#ca8a04,#facc15); height:6px; border-radius:4px; transition: width 0.5s; }

/* ── LEVEL GRID ── */
.level-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 12px; }
.level-card {
  background: #080b10; border: 1px solid #1a2233;
  border-radius: 8px; padding: 10px 12px; text-align: center;
}
.level-card-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.58rem; text-transform: uppercase;
  letter-spacing: 1.5px; margin-bottom: 5px;
}
.lc-entry { color: #60a5fa; }
.lc-tp1   { color: #4ade80; }
.lc-tp2   { color: #86efac; }
.lc-sl    { color: #f87171; }
.lc-rr    { color: #c084fc; }
.level-card-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem; font-weight: 700; color: #e2e8f0;
}
.level-grid-5 { grid-template-columns: 1fr 1fr 1fr 1fr 1fr; }

/* ── REASON TAGS ── */
.reason-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.rtag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; padding: 3px 10px;
  border-radius: 4px; font-weight: 500;
}
.rtag-bull { background:#0f2918; color:#4ade80; border:1px solid #166534; }
.rtag-bear { background:#1f0a0a; color:#f87171; border:1px solid #991b1b; }
.rtag-neut { background:#111827; color:#94a3b8; border:1px solid #1e293b; }

/* ── INDICATOR TABLE ── */
.ind-section-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem; color: #4a5568;
  text-transform: uppercase; letter-spacing: 2px;
  margin: 14px 0 8px 0;
  padding-bottom: 6px; border-bottom: 1px solid #1a2233;
}
.ind-table { width: 100%; border-collapse: collapse; }
.ind-table td {
  padding: 6px 8px;
  border-bottom: 1px solid #0d1117;
  font-size: 0.78rem;
}
.ind-table td:first-child {
  font-family: 'JetBrains Mono', monospace;
  color: #475569; font-size: 0.7rem;
}
.ind-table td:last-child { text-align: right; }
.ind-table tr:last-child td { border-bottom: none; }
.v-bull { color: #4ade80; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.v-bear { color: #f87171; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.v-neut { color: #94a3b8; font-weight: 600; font-family: 'JetBrains Mono', monospace; }

/* ── MTF PANEL ── */
.mtf-row {
  display: flex; gap: 8px; margin-bottom: 8px;
}
.mtf-card {
  flex: 1; background: #0d1117; border: 1px solid #1a2233;
  border-radius: 8px; padding: 10px 12px; text-align: center;
}
.mtf-tf {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem; color: #4a5568;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;
}
.mtf-bias {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem; font-weight: 700;
}
.mtf-bull { color: #4ade80; }
.mtf-bear { color: #f87171; }
.mtf-neut { color: #94a3b8; }

/* ── NEWS ── */
.news-card {
  background: #0d1117; border: 1px solid #1a2233;
  border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;
}
.news-headline { font-size: 0.78rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 6px; }
.news-foot { display: flex; align-items: center; gap: 8px; }
.news-time { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #4a5568; }
.nbadge-bull {
  font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 700;
  background: #0f2918; color: #4ade80; border: 1px solid #166534;
  padding: 1px 8px; border-radius: 3px; letter-spacing: 1px;
}
.nbadge-bear {
  font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 700;
  background: #1f0a0a; color: #f87171; border: 1px solid #991b1b;
  padding: 1px 8px; border-radius: 3px; letter-spacing: 1px;
}
.sentiment-meter {
  background: #0d1117; border: 1px solid #1a2233;
  border-radius: 10px; padding: 14px 16px; margin-bottom: 14px;
}
.sm-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem; color: #4a5568;
  text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;
}
.sm-bar-track {
  background: #1a2233; border-radius: 4px; height: 8px;
  overflow: hidden; margin-bottom: 6px;
}
.sm-bar-bull { background: #22c55e; height: 8px; border-radius: 4px 0 0 4px; display: inline-block; }
.sm-bar-bear { background: #ef4444; height: 8px; border-radius: 0 4px 4px 0; display: inline-block; }
.sm-counts {
  display: flex; justify-content: space-between;
  font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
}

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
  background: #0d1117 !important; border: 1px solid #1a2233 !important;
  color: #94a3b8 !important; border-radius: 8px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.75rem !important; transition: all 0.15s !important;
}
.stButton > button:hover {
  border-color: #3b82f6 !important; color: #93c5fd !important;
  background: #0f1f3d !important;
}
.stSelectbox > div > div {
  background: #0d1117 !important; border: 1px solid #1a2233 !important;
  border-radius: 8px !important;
}
section[data-testid="stSidebar"] { display: none; }
footer, #MainMenu { display: none !important; }
.block-container { padding: 0 24px 40px 24px !important; max-width: 100% !important; }
div[data-testid="stHorizontalBlock"] { gap: 12px; }
.stMetric { background: #0d1117 !important; border: 1px solid #1a2233 !important;
  border-radius: 8px !important; padding: 10px 14px !important; }
.stMetric label { font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.62rem !important; color: #4a5568 !important; }
hr { border-color: #1a2233 !important; margin: 16px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═════════════════════════════════════════════════════════════════════
COINS = {
    "BTC": {"bybit": "BTCUSDT", "cg": "bitcoin",  "name": "Bitcoin",  "emoji": "₿"},
    "ETH": {"bybit": "ETHUSDT", "cg": "ethereum", "name": "Ethereum", "emoji": "Ξ"},
    "SOL": {"bybit": "SOLUSDT", "cg": "solana",   "name": "Solana",   "emoji": "◎"},
}

# Bybit interval codes
BYBIT_INTERVALS = {
    "1":   "1m",  "3":  "3m",  "5": "5m",
    "15":  "15m", "60": "1H",  "240": "4H", "D": "1D",
}

TRADING_MODES = {
    "Scalping":  {"htf": "15",  "ltf": "1",   "label": "15m/1m",  "color": "#8b5cf6", "candles": 100},
    "Intraday":  {"htf": "60",  "ltf": "15",  "label": "1H/15m",  "color": "#3b82f6", "candles": 100},
    "Swing":     {"htf": "240", "ltf": "60",  "label": "4H/1H",   "color": "#22c55e", "candles": 100},
}

HEADERS = {"User-Agent": "Mozilla/5.0 NeuroBro/3.0", "Accept": "application/json"}


# ═════════════════════════════════════════════════════════════════════
# DATA LAYER — BYBIT REST API
# ═════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=15)
def fetch_bybit_ticker(symbol: str) -> dict:
    """Real-time ticker dari Bybit — update tiap 15 detik."""
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        r   = requests.get(url, headers=HEADERS, timeout=8)
        r.raise_for_status()
        d   = r.json()
        if d.get("retCode") != 0 or not d["result"]["list"]:
            return {"ok": False, "error": d.get("retMsg", "No data")}
        t = d["result"]["list"][0]
        price    = float(t["lastPrice"])
        open_    = float(t.get("prevPrice24h", t["lastPrice"]))
        high     = float(t["highPrice24h"])
        low      = float(t["lowPrice24h"])
        chg_pct  = float(t.get("price24hPcnt", 0)) * 100
        vol      = float(t.get("volume24h", 0))
        vol_usd  = float(t.get("turnover24h", 0))
        return {
            "price": price, "open": open_, "high": high, "low": low,
            "change_pct": chg_pct, "volume": vol, "volume_usd": vol_usd,
            "source": "Bybit", "ok": True,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@st.cache_data(ttl=30)
def fetch_bybit_klines(symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
    """OHLCV klines dari Bybit."""
    try:
        url = (
            f"https://api.bybit.com/v5/market/kline"
            f"?category=spot&symbol={symbol}&interval={interval}&limit={limit}"
        )
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        d = r.json()
        if d.get("retCode") != 0 or not d["result"]["list"]:
            return pd.DataFrame()
        raw = d["result"]["list"]
        df  = pd.DataFrame(raw, columns=["timestamp","open","high","low","close","volume","turnover"])
        df  = df.iloc[::-1].reset_index(drop=True)  # chronological order
        for col in ["open","high","low","close","volume","turnover"]:
            df[col] = df[col].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception:
        return pd.DataFrame()


# ═════════════════════════════════════════════════════════════════════
# TECHNICAL INDICATORS
# ═════════════════════════════════════════════════════════════════════
def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()

def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(window=period).mean()

def rsi(series: pd.Series, period: int = 14) -> float:
    delta    = series.diff().dropna()
    gain     = delta.clip(lower=0).rolling(period).mean()
    loss     = (-delta).clip(lower=0).rolling(period).mean()
    rs       = gain / (loss + 1e-10)
    rsi_val  = 100 - (100 / (1 + rs))
    return round(float(rsi_val.iloc[-1]), 1)

def macd(series: pd.Series):
    e12  = ema(series, 12)
    e26  = ema(series, 26)
    line = e12 - e26
    sig  = ema(line, 9)
    hist = line - sig
    return float(line.iloc[-1]), float(sig.iloc[-1]), float(hist.iloc[-1])

def bollinger(series: pd.Series, window: int = 20):
    m   = sma(series, window)
    sd  = series.rolling(window).std()
    return float((m + 2*sd).iloc[-1]), float(m.iloc[-1]), float((m - 2*sd).iloc[-1])

def atr(df: pd.DataFrame, period: int = 14) -> float:
    h, l, c = df["high"], df["low"], df["close"]
    prev_c   = c.shift(1)
    tr       = pd.concat([h-l, (h-prev_c).abs(), (l-prev_c).abs()], axis=1).max(axis=1)
    return float(tr.rolling(period).mean().iloc[-1])

def volume_spike(df: pd.DataFrame, lookback: int = 20) -> tuple:
    avg_vol = df["volume"].rolling(lookback).mean().iloc[-1]
    cur_vol = df["volume"].iloc[-1]
    ratio   = cur_vol / (avg_vol + 1e-10)
    return round(ratio, 2), ratio >= 1.5

def detect_structure(df: pd.DataFrame, lookback: int = 10) -> dict:
    """Deteksi Higher High / Lower Low / struktur tren sederhana."""
    if len(df) < lookback * 2:
        return {"trend": "RANGING", "hh": False, "ll": False, "hl": False, "lh": False}
    highs = df["high"].rolling(lookback).max()
    lows  = df["low"].rolling(lookback).min()
    hh    = float(highs.iloc[-1]) > float(highs.iloc[-lookback-1])
    ll    = float(lows.iloc[-1])  < float(lows.iloc[-lookback-1])
    hl    = float(lows.iloc[-1])  > float(lows.iloc[-lookback-1])
    lh    = float(highs.iloc[-1]) < float(highs.iloc[-lookback-1])
    if hh and hl:   trend = "UPTREND"
    elif ll and lh: trend = "DOWNTREND"
    else:           trend = "RANGING"
    return {"trend": trend, "hh": hh, "ll": ll, "hl": hl, "lh": lh}

def swing_levels(df: pd.DataFrame, lookback: int = 15):
    """Cari swing high/low terdekat untuk TP dan SL berbasis struktur."""
    if len(df) < lookback * 2:
        return None, None
    recent  = df.tail(lookback * 3)
    swing_h = recent["high"].rolling(lookback, center=True).max()
    swing_l = recent["low"].rolling(lookback, center=True).min()
    sh_vals = swing_h.dropna().unique()
    sl_vals = swing_l.dropna().unique()
    price   = float(df["close"].iloc[-1])
    above   = sorted([v for v in sh_vals if v > price])
    below   = sorted([v for v in sl_vals if v < price], reverse=True)
    nearest_above = above[0]  if above  else price * 1.015
    nearest_below = below[0]  if below  else price * 0.985
    return nearest_above, nearest_below

def rsi_divergence(df: pd.DataFrame, period: int = 14) -> str:
    """Deteksi divergence bullish/bearish sederhana."""
    if len(df) < period * 3:
        return "NONE"
    close = df["close"]
    delta = close.diff().dropna()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta).clip(lower=0).rolling(period).mean()
    rs    = gain / (loss + 1e-10)
    rsi_s = 100 - (100 / (1 + rs))
    # Bandingkan 2 lembah/puncak terakhir (lookback 20 bar)
    lb = 20
    if len(rsi_s) < lb * 2:
        return "NONE"
    price_now   = float(close.iloc[-1])
    price_prev  = float(close.iloc[-lb])
    rsi_now     = float(rsi_s.iloc[-1])
    rsi_prev    = float(rsi_s.iloc[-lb])
    if price_now < price_prev and rsi_now > rsi_prev:
        return "BULLISH_DIV"
    if price_now > price_prev and rsi_now < rsi_prev:
        return "BEARISH_DIV"
    return "NONE"


# ═════════════════════════════════════════════════════════════════════
# SIGNAL ENGINE — MULTI-TIMEFRAME CONFLUENCE
# ═════════════════════════════════════════════════════════════════════
def analyze(symbol: str, mode: str) -> dict:
    """
    Core signal engine.
    HTF → bias (trend direction)
    LTF → entry timing (confluence)
    Output: signal, confidence, entry zone, TP1, TP2, SL, reasons
    """
    cfg      = TRADING_MODES[mode]
    htf_int  = cfg["htf"]
    ltf_int  = cfg["ltf"]
    candles  = cfg["candles"]

    # ── Fetch klines ──────────────────────────────────────────────
    df_htf = fetch_bybit_klines(symbol, htf_int, candles)
    df_ltf = fetch_bybit_klines(symbol, ltf_int, candles)
    ticker = fetch_bybit_ticker(symbol)

    if not ticker["ok"] or df_htf.empty or df_ltf.empty:
        return {"ok": False, "error": ticker.get("error", "Data error")}

    price   = ticker["price"]
    score   = 0          # + = bullish, - = bearish
    reasons = []
    ind_data = {}

    # ── HTF Analysis (Bias) ──────────────────────────────────────
    # 1. Struktur tren HTF
    struct_htf = detect_structure(df_htf, lookback=10)
    htf_trend  = struct_htf["trend"]
    if htf_trend == "UPTREND":
        score += 3; reasons.append(("HTF Uptrend Structure", "bull"))
    elif htf_trend == "DOWNTREND":
        score -= 3; reasons.append(("HTF Downtrend Structure", "bear"))
    else:
        reasons.append(("HTF Ranging / No Clear Bias", "neut"))

    # 2. EMA Stack HTF (21 > 50 > 200 = bullish)
    c_htf   = df_htf["close"]
    ema21h  = float(ema(c_htf, 21).iloc[-1])
    ema50h  = float(ema(c_htf, 50).iloc[-1])
    ema200h = float(ema(c_htf, min(200, len(c_htf)-1)).iloc[-1])
    ind_data["EMA21 (HTF)"] = (f"{ema21h:,.2f}", "bull" if price > ema21h else "bear")
    ind_data["EMA50 (HTF)"] = (f"{ema50h:,.2f}", "bull" if price > ema50h else "bear")
    ind_data["EMA200 (HTF)"]= (f"{ema200h:,.2f}","bull" if price > ema200h else "bear")
    if ema21h > ema50h > ema200h:
        score += 2; reasons.append(("EMA Stack Bullish (21>50>200)", "bull"))
    elif ema21h < ema50h < ema200h:
        score -= 2; reasons.append(("EMA Stack Bearish (21<50<200)", "bear"))

    # 3. RSI HTF
    rsi_htf = rsi(c_htf)
    ind_data["RSI (HTF)"] = (
        f"{rsi_htf}",
        "bull" if rsi_htf < 40 else ("bear" if rsi_htf > 60 else "neut")
    )
    if rsi_htf < 35:
        score += 2; reasons.append((f"RSI HTF Oversold ({rsi_htf})", "bull"))
    elif rsi_htf > 65:
        score -= 2; reasons.append((f"RSI HTF Overbought ({rsi_htf})", "bear"))

    # ── LTF Analysis (Entry Timing) ──────────────────────────────
    c_ltf   = df_ltf["close"]
    struct_ltf = detect_structure(df_ltf, lookback=8)

    # 4. LTF Structure alignment
    if struct_ltf["trend"] == htf_trend:
        score += 2; reasons.append(("LTF Structure Confirms HTF Bias", "bull" if htf_trend=="UPTREND" else "bear"))
    elif struct_ltf["trend"] != "RANGING" and struct_ltf["trend"] != htf_trend:
        score -= 1; reasons.append(("LTF vs HTF Structure Divergence", "neut"))

    # 5. RSI LTF
    rsi_ltf = rsi(c_ltf)
    ind_data["RSI (LTF)"] = (
        f"{rsi_ltf}",
        "bull" if rsi_ltf < 40 else ("bear" if rsi_ltf > 60 else "neut")
    )
    if rsi_ltf < 30:
        score += 2; reasons.append((f"RSI LTF Extreme Oversold ({rsi_ltf})", "bull"))
    elif rsi_ltf > 70:
        score -= 2; reasons.append((f"RSI LTF Extreme Overbought ({rsi_ltf})", "bear"))

    # 6. MACD LTF
    macd_l, macd_s, macd_h = macd(c_ltf)
    ind_data["MACD (LTF)"] = (
        f"{'▲' if macd_h > 0 else '▼'} {macd_h:+.4f}",
        "bull" if macd_h > 0 else "bear"
    )
    if macd_h > 0 and macd_l > macd_s:
        score += 1; reasons.append(("MACD Bullish Crossover (LTF)", "bull"))
    elif macd_h < 0 and macd_l < macd_s:
        score -= 1; reasons.append(("MACD Bearish Crossover (LTF)", "bear"))

    # 7. Bollinger Bands LTF
    bb_up, bb_mid, bb_low = bollinger(c_ltf)
    bb_pct = (price - bb_low) / (bb_up - bb_low + 1e-10) * 100
    ind_data["BB Position"] = (
        f"{bb_pct:.1f}%",
        "bull" if bb_pct < 25 else ("bear" if bb_pct > 75 else "neut")
    )
    if bb_pct < 20:
        score += 2; reasons.append(("Price at Lower Bollinger Band", "bull"))
    elif bb_pct > 80:
        score -= 2; reasons.append(("Price at Upper Bollinger Band", "bear"))

    # 8. Volume Spike
    vol_ratio, is_spike = volume_spike(df_ltf)
    ind_data["Volume Ratio"] = (
        f"{vol_ratio:.1f}x",
        "bull" if (is_spike and score > 0) else ("bear" if (is_spike and score < 0) else "neut")
    )
    if is_spike:
        if score > 0:
            score += 1; reasons.append((f"Volume Spike Confirms Buying ({vol_ratio:.1f}x avg)", "bull"))
        elif score < 0:
            score -= 1; reasons.append((f"Volume Spike Confirms Selling ({vol_ratio:.1f}x avg)", "bear"))

    # 9. RSI Divergence LTF
    div = rsi_divergence(df_ltf)
    ind_data["RSI Divergence"] = (
        div.replace("_", " "),
        "bull" if div == "BULLISH_DIV" else ("bear" if div == "BEARISH_DIV" else "neut")
    )
    if div == "BULLISH_DIV":
        score += 2; reasons.append(("Bullish RSI Divergence Detected", "bull"))
    elif div == "BEARISH_DIV":
        score -= 2; reasons.append(("Bearish RSI Divergence Detected", "bear"))

    # ── ATR for levels ────────────────────────────────────────────
    atr_val = atr(df_ltf)
    ind_data["ATR (LTF)"] = (f"{atr_val:.4f}", "neut")

    # Swing levels untuk TP/SL berbasis struktur
    swing_top, swing_bot = swing_levels(df_htf, lookback=15)

    # ── Decision ─────────────────────────────────────────────────
    max_score = 17  # total maksimal score teoritis
    conf_raw  = abs(score) / max_score * 100

    if score >= 5:
        signal     = "BUY"
        confidence = min(95, round(40 + conf_raw * 0.6, 1))
        # Entry: harga saat ini atau EMA21 LTF (mana yang lebih murah)
        ema21_ltf  = float(ema(c_ltf, 21).iloc[-1])
        entry      = min(price, ema21_ltf) if price > ema21_ltf * 0.99 else price
        # TP berbasis swing high atau ATR
        tp1 = swing_top if swing_top and swing_top < price * 1.05 else round(price + 1.5 * atr_val, _dp(price))
        tp2 = round(price + 3.0 * atr_val, _dp(price))
        sl  = swing_bot if swing_bot and swing_bot > price * 0.95 else round(price - 1.2 * atr_val, _dp(price))
        subtitle = "Confluence bullish terkonfirmasi. Entry di zona demand."

    elif score <= -5:
        signal     = "SELL"
        confidence = min(95, round(40 + conf_raw * 0.6, 1))
        ema21_ltf  = float(ema(c_ltf, 21).iloc[-1])
        entry      = max(price, ema21_ltf) if price < ema21_ltf * 1.01 else price
        tp1 = swing_bot if swing_bot and swing_bot > price * 0.95 else round(price - 1.5 * atr_val, _dp(price))
        tp2 = round(price - 3.0 * atr_val, _dp(price))
        sl  = swing_top if swing_top and swing_top < price * 1.05 else round(price + 1.2 * atr_val, _dp(price))
        subtitle = "Tekanan jual dominan. Entry di zona supply."

    else:
        signal     = "WAIT"
        confidence = round(60 - conf_raw * 0.4, 1)
        entry      = price
        tp1        = round(price + atr_val, _dp(price))
        tp2        = round(price + 2 * atr_val, _dp(price))
        sl         = round(price - atr_val, _dp(price))
        subtitle   = "Belum ada confluence cukup. Tunggu konfirmasi."

    rr = abs(tp1 - entry) / (abs(sl - entry) + 1e-10)

    # HTF + LTF bias label for MTF panel
    ltf_bias = struct_ltf["trend"]

    return {
        "ok": True,
        "signal": signal,
        "confidence": confidence,
        "score": score,
        "subtitle": subtitle,
        "entry": round(entry, _dp(price)),
        "tp1": round(tp1, _dp(price)),
        "tp2": round(tp2, _dp(price)),
        "sl": round(sl, _dp(price)),
        "rr": round(rr, 2),
        "atr": round(atr_val, _dp(price)),
        "reasons": reasons,
        "indicators": ind_data,
        "htf_bias": htf_trend,
        "ltf_bias": ltf_bias,
        "htf_tf": cfg["label"].split("/")[0],
        "ltf_tf": cfg["label"].split("/")[1],
        "rsi_htf": rsi_htf,
        "rsi_ltf": rsi_ltf,
    }


def _dp(price: float) -> int:
    if price >= 10000: return 1
    if price >= 100:   return 2
    if price >= 1:     return 4
    return 6


# ═════════════════════════════════════════════════════════════════════
# NEWS ENGINE
# ═════════════════════════════════════════════════════════════════════
BULL_KW = ["surge","rally","gain","rise","bull","buy","growth","record","boost","breakout",
           "recovery","strong","upside","profit","soar","adoption","institutional","all-time"]
BEAR_KW = ["fall","drop","crash","sell","bear","decline","recession","fear","loss","plunge",
           "weak","risk","concern","warning","inflation","hawkish","dump","liquidation","hack","ban"]

def sentiment_score(text: str) -> tuple:
    t = text.lower()
    b = sum(1 for w in BULL_KW if w in t)
    s = sum(1 for w in BEAR_KW if w in t)
    return ("BULLISH" if b >= s else "BEARISH"), b, s

@st.cache_data(ttl=180)
def fetch_news(coin_name: str) -> list:
    """
    Coba CryptoPanic → Google News RSS → simulated fallback.
    """
    articles = []

    # 1. CryptoPanic public feed (no key needed for basic)
    try:
        url = f"https://cryptopanic.com/api/free/v1/posts/?auth_token=&public=true&currencies={coin_name[:3].upper()}"
        r   = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            data = r.json().get("results", [])
            for item in data[:10]:
                title = item.get("title", "")
                pub   = item.get("published_at", "")[:16].replace("T", " ")
                sent, _, _ = sentiment_score(title)
                # CryptoPanic punya votes
                votes = item.get("votes", {})
                bull_votes = votes.get("positive", 0)
                bear_votes = votes.get("negative", 0)
                if bull_votes > bear_votes:   sent = "BULLISH"
                elif bear_votes > bull_votes: sent = "BEARISH"
                articles.append({"title": title, "pub": pub, "sentiment": sent, "src": "CryptoPanic"})
    except Exception:
        pass

    # 2. Google News RSS fallback
    if not articles:
        try:
            q   = f"{coin_name}+crypto+price"
            url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
            r   = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            root = ET.fromstring(r.content)
            for item in root.findall(".//item")[:10]:
                title = (item.findtext("title") or "").strip()
                pub   = (item.findtext("pubDate") or "")[:22]
                desc  = (item.findtext("description") or "")
                sent, _, _ = sentiment_score(title + " " + desc)
                articles.append({"title": title, "pub": pub, "sentiment": sent, "src": "Google News"})
        except Exception:
            pass

    # 3. Simulated fallback
    if not articles:
        articles = _sim_news(coin_name)

    return articles[:10]

def _sim_news(coin: str) -> list:
    pool = [
        (f"{coin} tests key resistance — bulls defend critical support zone", "BULLISH"),
        (f"Institutional buying accelerates as {coin} consolidates above EMA200", "BULLISH"),
        (f"{coin} spot ETF inflows hit weekly record, demand outpacing supply", "BULLISH"),
        (f"Derivatives data shows {coin} shorts being squeezed at current levels", "BULLISH"),
        (f"{coin} sell-off intensifies as macro fears weigh on risk assets", "BEARISH"),
        (f"Large {coin} wallets spotted moving funds to exchanges — sell signal?", "BEARISH"),
        (f"Fed minutes spark {coin} dip; traders await CPI data for direction", "BEARISH"),
        (f"{coin} liquidations spike $200M as price breaks below key support", "BEARISH"),
    ]
    random.shuffle(pool)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    return [{"title": t, "pub": now, "sentiment": s, "src": "Simulated"} for t, s in pool[:8]]


# ═════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═════════════════════════════════════════════════════════════════════
if "coin" not in st.session_state:
    st.session_state.coin = "BTC"
if "mode" not in st.session_state:
    st.session_state.mode = "Intraday"


# ═════════════════════════════════════════════════════════════════════
# TOP BAR
# ═════════════════════════════════════════════════════════════════════
ts = datetime.utcnow().strftime("%d %b %Y · %H:%M UTC")
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">🧠 Neuro<span>Bro</span> · Crypto Signal Engine</div>
  <div class="topbar-meta">
    <span><span class="live-dot"></span><span class="live-pill">LIVE</span></span>
    <span>{ts}</span>
    <span>Bybit · v3.0</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════
# COIN + MODE SELECTOR (inline buttons)
# ═════════════════════════════════════════════════════════════════════
col_btns = st.columns([1, 1, 1, 0.3, 1, 1, 1])
coins_list = list(COINS.keys())
modes_list = list(TRADING_MODES.keys())

for i, coin in enumerate(coins_list):
    with col_btns[i]:
        if st.button(f"{COINS[coin]['emoji']} {coin}", key=f"c_{coin}", use_container_width=True):
            st.session_state.coin = coin

with col_btns[3]:
    st.markdown("<div style='border-left:1px solid #1a2233;height:36px;margin:0 auto;'></div>", unsafe_allow_html=True)

for i, mode in enumerate(modes_list):
    with col_btns[i + 4]:
        mode_colors = {"Scalping": "#8b5cf6", "Intraday": "#3b82f6", "Swing": "#22c55e"}
        active_style = f"border-color:{mode_colors[mode]} !important;color:{mode_colors[mode]} !important;" if st.session_state.mode == mode else ""
        if st.button(f"{'⚡' if mode=='Scalping' else ('📊' if mode=='Intraday' else '🌊')} {mode}", key=f"m_{mode}", use_container_width=True):
            st.session_state.mode = mode

coin  = st.session_state.coin
mode  = st.session_state.mode
cfg   = COINS[coin]
mcfg  = TRADING_MODES[mode]

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════
# FETCH DATA
# ═════════════════════════════════════════════════════════════════════
with st.spinner(f"Fetching {coin} data from Bybit..."):
    ticker  = fetch_bybit_ticker(cfg["bybit"])
    result  = analyze(cfg["bybit"], mode)
    news    = fetch_news(cfg["name"])

if not ticker["ok"]:
    st.error(f"⚠️ Bybit API error: {ticker.get('error')}. Coba refresh dalam 15 detik.")
    st.stop()

if not result["ok"]:
    st.error(f"⚠️ Analysis error: {result.get('error')}")
    st.stop()

price = ticker["price"]
dp    = _dp(price)

# ═════════════════════════════════════════════════════════════════════
# LAYOUT: 3 COLUMNS
# ═════════════════════════════════════════════════════════════════════
col_l, col_c, col_r = st.columns([1, 1.6, 1], gap="medium")


# ─── LEFT: Price + Indicators ────────────────────────────────────────
with col_l:

    # Price Hero
    chg     = ticker["change_pct"]
    chg_cls = "price-change-pos" if chg >= 0 else "price-change-neg"
    chg_str = f"{'▲' if chg >= 0 else '▼'} {abs(chg):.2f}%"
    vol_b   = ticker["volume_usd"]
    vol_str = f"${vol_b/1e9:.2f}B" if vol_b >= 1e9 else f"${vol_b/1e6:.1f}M"

    st.markdown(f"""
    <div class="price-hero">
      <div class="price-coin-label">{cfg['emoji']} {coin} / USDT · {mode} Mode · {mcfg['label']}</div>
      <div style="display:flex;align-items:baseline;gap:4px;">
        <div class="price-value">${price:,.{dp}f}</div>
        <span class="{chg_cls}">{chg_str}</span>
      </div>
      <div class="price-meta-row">
        <div class="price-meta-item">
          <div class="price-meta-label">24H HIGH</div>
          <div class="price-meta-val">${ticker['high']:,.{dp}f}</div>
        </div>
        <div class="price-meta-item">
          <div class="price-meta-label">24H LOW</div>
          <div class="price-meta-val">${ticker['low']:,.{dp}f}</div>
        </div>
        <div class="price-meta-item">
          <div class="price-meta-label">VOLUME</div>
          <div class="price-meta-val">{vol_str}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Multi-Timeframe Bias
    htf_col = "mtf-bull" if result["htf_bias"] == "UPTREND" else ("mtf-bear" if result["htf_bias"] == "DOWNTREND" else "mtf-neut")
    ltf_col = "mtf-bull" if result["ltf_bias"] == "UPTREND" else ("mtf-bear" if result["ltf_bias"] == "DOWNTREND" else "mtf-neut")

    st.markdown(f"""
    <div class="ind-section-title">MULTI-TIMEFRAME BIAS</div>
    <div class="mtf-row">
      <div class="mtf-card">
        <div class="mtf-tf">HTF · {result['htf_tf']}</div>
        <div class="mtf-bias {htf_col}">{result['htf_bias']}</div>
      </div>
      <div class="mtf-card">
        <div class="mtf-tf">LTF · {result['ltf_tf']}</div>
        <div class="mtf-bias {ltf_col}">{result['ltf_bias']}</div>
      </div>
      <div class="mtf-card">
        <div class="mtf-tf">ATR</div>
        <div class="mtf-bias mtf-neut">{result['atr']:,.{dp}f}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Indicators table
    st.markdown('<div class="ind-section-title">TECHNICAL INDICATORS</div>', unsafe_allow_html=True)
    rows_html = ""
    for name, (val, sig) in result["indicators"].items():
        icon = "▲" if sig == "bull" else ("▼" if sig == "bear" else "◆")
        css  = f"v-{sig}"
        rows_html += f"<tr><td>{name}</td><td class='{css}'>{icon} {val}</td></tr>"
    st.markdown(f'<table class="ind-table">{rows_html}</table>', unsafe_allow_html=True)

    # Refresh button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown(f"""
    <div style="text-align:center;margin-top:6px;font-family:'JetBrains Mono',monospace;
         font-size:0.6rem;color:#2d3748;">
      Auto cache: ticker 15s · klines 30s · news 3min
    </div>
    """, unsafe_allow_html=True)


# ─── CENTER: Signal + Levels + Reasons ───────────────────────────────
with col_c:

    sig     = result["signal"]
    sig_l   = sig.lower()
    conf    = result["confidence"]
    conf_l  = sig_l if sig_l != "wait" else "wait"

    badge_map    = {"BUY": "badge-buy", "SELL": "badge-sell", "WAIT": "badge-wait"}
    badge_label  = {"BUY": "● LONG SIGNAL", "SELL": "● SHORT SIGNAL", "WAIT": "◆ STAND BY"}
    score_color  = "#4ade80" if result["score"] > 0 else ("#f87171" if result["score"] < 0 else "#94a3b8")

    st.markdown(f"""
    <div class="signal-box {sig_l}">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;">
        <div>
          <span class="signal-badge {badge_map[sig]}">{badge_label[sig]}</span>
          <div class="signal-decision {sig_l}">{sig}</div>
          <div class="signal-subtitle">{result['subtitle']}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#4a5568;margin-bottom:2px;">SCORE</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:700;color:{score_color};line-height:1;">{result['score']:+d}</div>
        </div>
      </div>
      <div class="confidence-bar-wrap">
        <div class="confidence-label">
          <span>Signal Confidence</span>
          <span style="color:{'#4ade80' if sig=='BUY' else ('#f87171' if sig=='SELL' else '#facc15')}">{conf}%</span>
        </div>
        <div class="confidence-track">
          <div class="confidence-fill-{conf_l}" style="width:{conf}%;"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Level Grid (Entry, TP1, TP2, SL, R:R)
    st.markdown('<div class="ind-section-title">EXECUTION LEVELS</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="level-grid level-grid-5">
      <div class="level-card">
        <div class="level-card-label lc-entry">ENTRY</div>
        <div class="level-card-val">${result['entry']:,.{dp}f}</div>
      </div>
      <div class="level-card">
        <div class="level-card-label lc-tp1">TP 1</div>
        <div class="level-card-val">${result['tp1']:,.{dp}f}</div>
      </div>
      <div class="level-card">
        <div class="level-card-label lc-tp2">TP 2</div>
        <div class="level-card-val">${result['tp2']:,.{dp}f}</div>
      </div>
      <div class="level-card">
        <div class="level-card-label lc-sl">STOP LOSS</div>
        <div class="level-card-val">${result['sl']:,.{dp}f}</div>
      </div>
      <div class="level-card">
        <div class="level-card-label lc-rr">R : R</div>
        <div class="level-card-val">1 : {result['rr']:.1f}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Confluence Reasons
    st.markdown('<div class="ind-section-title">CONFLUENCE FACTORS</div>', unsafe_allow_html=True)
    tags_html = '<div class="reason-tags">'
    for reason, rtype in result["reasons"]:
        css = f"rtag-{rtype}"
        icon = "▲" if rtype == "bull" else ("▼" if rtype == "bear" else "◆")
        tags_html += f'<span class="rtag {css}">{icon} {reason}</span>'
    tags_html += "</div>"
    st.markdown(tags_html, unsafe_allow_html=True)

    # Price chart
    st.markdown('<div class="ind-section-title">PRICE CHART (LTF)</div>', unsafe_allow_html=True)
    df_chart = fetch_bybit_klines(cfg["bybit"], mcfg["ltf"], 80)
    if not df_chart.empty:
        chart_data = df_chart[["close"]].copy()
        chart_data["EMA21"]  = ema(df_chart["close"], 21)
        chart_data["EMA50"]  = ema(df_chart["close"], 50)
        st.line_chart(chart_data.tail(60), height=180, use_container_width=True)

    # Disclaimer
    st.markdown("""
    <div style="margin-top:10px;padding:10px 14px;background:#0d1117;border:1px solid #1a2233;
         border-radius:8px;font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#374151;line-height:1.6;">
      ⚠️ Output ini adalah alat bantu analisis, bukan sinyal finansial resmi.
      Selalu konfirmasi di chart pribadi kamu. DYOR. Manage risk.
    </div>
    """, unsafe_allow_html=True)


# ─── RIGHT: News + Sentiment ──────────────────────────────────────────
with col_r:

    bull_n = sum(1 for n in news if n["sentiment"] == "BULLISH")
    bear_n = len(news) - bull_n
    bull_p = int(bull_n / max(len(news), 1) * 100)
    bear_p = 100 - bull_p
    overall_sent = "BULLISH" if bull_n >= bear_n else "BEARISH"
    sent_color   = "#22c55e" if overall_sent == "BULLISH" else "#ef4444"

    st.markdown(f"""
    <div class="sentiment-meter">
      <div class="sm-title">Market Sentiment · {coin}</div>
      <div style="font-size:1.1rem;font-weight:700;font-family:'JetBrains Mono',monospace;
           color:{sent_color};margin-bottom:8px;">{overall_sent}</div>
      <div class="sm-bar-track">
        <div style="display:flex;height:8px;">
          <div style="background:#22c55e;width:{bull_p}%;border-radius:4px 0 0 4px;"></div>
          <div style="background:#ef4444;width:{bear_p}%;border-radius:0 4px 4px 0;"></div>
        </div>
      </div>
      <div class="sm-counts">
        <span style="color:#22c55e;">▲ BULL {bull_n} ({bull_p}%)</span>
        <span style="color:#ef4444;">▼ BEAR {bear_n} ({bear_p}%)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="ind-section-title">LATEST NEWS · {coin}</div>', unsafe_allow_html=True)

    for item in news:
        sent  = item["sentiment"]
        badge = f'<span class="nbadge-{"bull" if sent=="BULLISH" else "bear"}">{sent}</span>'
        src   = item.get("src", "")
        title = item["title"]
        title = title[:100] + "…" if len(title) > 100 else title
        st.markdown(f"""
        <div class="news-card">
          <div class="news-headline">{title}</div>
          <div class="news-foot">
            {badge}
            <span class="news-time">{item['pub']}</span>
            <span class="news-time" style="color:#1e293b;">· {src}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Auto refresh toggle
    st.markdown("<br>", unsafe_allow_html=True)
    auto = st.checkbox("⚡ Auto-refresh (30s)", value=False)
    if auto:
        st.markdown('<div style="font-family:monospace;font-size:0.65rem;color:#4ade80;">● Aktif — refresh tiap 30 detik</div>', unsafe_allow_html=True)
        time.sleep(30)
        st.cache_data.clear()
        st.rerun()


# ═════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#1e293b;padding:8px;">
  NeuroBro Crypto Signal Engine v3.0 · Data: Bybit REST API (15s) ·
  News: CryptoPanic + Google News RSS · Score: {result['score']:+d}/17 ·
  <span style="color:#166534;">NO API KEY · WORKS IN INDONESIA</span>
</div>
""", unsafe_allow_html=True)
