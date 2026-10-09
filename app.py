import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

def ensure_database():
    """Build stocks.db from CSVs on first run."""
    if os.path.exists("stocks.db"):
        return
    
    FILES = {
        "bajaj_auto":    "Bajaj Auto.csv",
        "eicher_motors": "Eicher Motors.csv",
        "hero_motocorp": "Hero Motocorp.csv",
        "infosys":       "Infosys.csv",
        "tcs":           "TCS.csv",
        "tvs_motors":    "TVS Motors.csv",
    }
    COLS = ["date", "open_price", "high_price", "low_price", "close_price",
            "wap", "no_of_shares", "no_of_trades", "total_turnover",
            "deliverable_qty", "pct_deli_qty", "spread_high_low",
            "spread_close_open"]
    
    conn = sqlite3.connect("stocks.db")
    for table, fname in FILES.items():
        df = pd.read_csv(fname)
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%B-%Y").dt.strftime("%Y-%m-%d")
        df.columns = COLS
        df.to_sql(table, conn, if_exists="replace", index=False)
        conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_date ON {table}(date)")
        conn.commit()
    conn.close()

ensure_database()
# ============================================================
# CUSTOM CSS — the magic that makes it beautiful
# ============================================================
st.markdown("""
<style>
    /* ---------- Global ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
        @keyframes gradient {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0b1220, #1e1b4b);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    /* ---------- Hide default Streamlit chrome ---------- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1220 0%, #111c2f 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ---------- Headings ---------- */
    h1, h2, h3 {
        color: #f1f5f9 !important;
        letter-spacing: -0.02em;
    }
    h1 { font-weight: 800 !important; }

    /* ---------- Metric Cards ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(56,189,248,0.08));
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px;
        padding: 20px 22px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99,102,241,0.35);
    }
    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.5);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(99,102,241,0.15);
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background: transparent;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #3b82f6) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.4);
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #3b82f6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 4px 14px rgba(99,102,241,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99,102,241,0.5);
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 24px;
        box-shadow: 0 4px 14px rgba(16,185,129,0.3);
    }

    /* ---------- Dataframe ---------- */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(99,102,241,0.2);
    }

    /* ---------- Alerts ---------- */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #6366f1;
        background: rgba(99,102,241,0.08);
    }

    /* ---------- Hero banner ---------- */
    .hero {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #3b82f6 100%);
        border-radius: 20px;
        padding: 32px 36px;
        margin-bottom: 24px;
        box-shadow: 0 20px 60px rgba(99,102,241,0.3);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: "";
        position: absolute;
        top: -50%; right: -20%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero h1 {
        color: white !important;
        font-size: 2.2rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    .hero p {
        color: rgba(255,255,255,0.85);
        margin: 8px 0 0 0;
        font-size: 1rem;
        font-weight: 500;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 12px;
        backdrop-filter: blur(10px);
    }

    /* ---------- Section card ---------- */
    .card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 12px 0;
        backdrop-filter: blur(10px);
    }
    .card h3 {
        margin-top: 0;
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)



# ============================================================
# CONFIG
# ============================================================
import os
DB = "stocks.db"   # relative path — works everywhere
STOCKS = ["bajaj_auto", "eicher_motors", "hero_motocorp",
          "infosys", "tcs", "tvs_motors"]
NICE = {
    "bajaj_auto":    "Bajaj Auto",
    "eicher_motors": "Eicher Motors",
    "hero_motocorp": "Hero Motocorp",
    "infosys":       "Infosys",
    "tcs":           "TCS",
    "tvs_motors":    "TVS Motors",
}
TICKER = {
    "bajaj_auto":    "BAJAJ-AUTO",
    "eicher_motors": "EICHERMOT",
    "hero_motocorp": "HEROMOTOCO",
    "infosys":       "INFY",
    "tcs":           "TCS",
    "tvs_motors":    "TVSMOTOR",
}

# ============================================================
# DATA
# ============================================================
@st.cache_data
def load_stock(table):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(f"SELECT * FROM {table} ORDER BY date", conn, parse_dates=["date"])
    conn.close()
    df["ma20"] = df["close_price"].rolling(20).mean()
    df["ma50"] = df["close_price"].rolling(50).mean()
    df["prev_ma20"] = df["ma20"].shift(1)
    df["prev_ma50"] = df["ma50"].shift(1)
    df["signal"] = "Hold"
    df.loc[(df.prev_ma20 <= df.prev_ma50) & (df.ma20 > df.ma50), "signal"] = "Buy"
    df.loc[(df.prev_ma20 >= df.prev_ma50) & (df.ma20 < df.ma50), "signal"] = "Sell"
    return df

@st.cache_data
def load_all():
    conn = sqlite3.connect(DB)
    dfs = []
    for t in STOCKS:
        d = pd.read_sql(f"SELECT date, close_price FROM {t} ORDER BY date",
                        conn, parse_dates=["date"])
        d["stock"] = NICE[t]
        dfs.append(d)
    conn.close()
    return pd.concat(dfs, ignore_index=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding: 16px 0 8px 0;">
            <div style="font-size: 2.5rem;">📊</div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #f1f5f9;">Stock Analytics</div>
            <div style="font-size: 0.75rem; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 4px;">NSE · 2015–2018</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    stock_key = st.selectbox("Select Stock", STOCKS, format_func=lambda x: NICE[x])
    df = load_stock(stock_key)

    min_d, max_d = df["date"].min().date(), df["date"].max().date()
    date_range = st.slider(
        "Date Range",
        min_value=min_d, max_value=max_d,
        value=(min_d, max_d),
        format="YYYY-MM-DD"
    )
    mask = (df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])
    view = df[mask].copy()

    st.markdown("---")
    st.markdown(f"""
        <div style="padding: 12px 14px; background: rgba(99,102,241,0.1); border-radius: 10px; border: 1px solid rgba(99,102,241,0.25);">
            <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Database</div>
            <div style="font-size: 0.9rem; color: #e2e8f0; font-weight: 600; margin-top: 4px;">{len(df)} trading days</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 2px;">Viewing {len(view)} days</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# HERO HEADER
# ============================================================
buys  = (df["signal"] == "Buy").sum()
sells = (df["signal"] == "Sell").sum()
first_close = df["close_price"].iloc[0]
last_close  = df["close_price"].iloc[-1]
pct = (last_close - first_close) / first_close * 100

st.markdown(f"""
    <div class="hero">
        <h1>📈 {NICE[stock_key]}</h1>
        <p>Golden Cross Analysis · Moving Averages · Buy/Sell Signals</p>
        <span class="badge">{TICKER[stock_key]} · NSE</span>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# METRIC CARDS
# ============================================================
last_sig = df[df["signal"] != "Hold"].iloc[-1] if (df["signal"] != "Hold").any() else None

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Return", f"{pct:+.1f}%",
              f"₹{first_close:.0f} → ₹{last_close:.0f}")
with c2:
    st.metric("Buy Signals", int(buys), "▲")
with c3:
    st.metric("Sell Signals", int(sells), "▼")
with c4:
    if last_sig is not None:
        st.metric("Latest Signal", last_sig["signal"],
                  str(last_sig["date"].date()))
    else:
        st.metric("Latest Signal", "—", "")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Chart", "🧪 SQL Playground", "🔬 All Stocks", "💡 Insights"
])

# ---------- TAB 1: CHART ----------
with tab1:
    st.markdown("##### Candlestick · Moving Averages · Buy/Sell Markers")

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=view["date"], open=view["open_price"],
        high=view["high_price"], low=view["low_price"],
        close=view["close_price"], name="Price",
        increasing_line_color="#10b981", decreasing_line_color="#ef4444",
        increasing_fillcolor="#10b981", decreasing_fillcolor="#ef4444",
    ))
    fig.add_trace(go.Scatter(
        x=view["date"], y=view["ma20"], name="MA 20",
        line=dict(color="#3b82f6", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=view["date"], y=view["ma50"], name="MA 50",
        line=dict(color="#f59e0b", width=2),
    ))

    buy_pts  = view[view["signal"] == "Buy"]
    sell_pts = view[view["signal"] == "Sell"]

    fig.add_trace(go.Scatter(
        x=buy_pts["date"], y=buy_pts["close_price"] * 0.96,
        mode="markers", name="Buy",
        marker=dict(symbol="triangle-up", size=15, color="#10b981",
                    line=dict(color="#065f46", width=1.5)),
        hovertemplate="<b>BUY</b><br>%{x|%Y-%m-%d}<br>₹%{y:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=sell_pts["date"], y=sell_pts["close_price"] * 1.04,
        mode="markers", name="Sell",
        marker=dict(symbol="triangle-down", size=15, color="#ef4444",
                    line=dict(color="#7f1d1d", width=1.5)),
        hovertemplate="<b>SELL</b><br>%{x|%Y-%m-%d}<br>₹%{y:.2f}<extra></extra>",
    ))

    fig.update_layout(
        height=580,
        template="plotly_dark",
        paper_bgcolor="rgba(15,23,42,0)",
        plot_bgcolor="rgba(30,41,59,0.4)",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02, x=0,
                    bgcolor="rgba(15,23,42,0.6)", bordercolor="rgba(99,102,241,0.3)",
                    borderwidth=1),
        margin=dict(t=30, b=10, l=10, r=10),
        font=dict(family="Inter", color="#cbd5e1"),
    )
    st.plotly_chart(fig, use_container_width=True)

    csv = view.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download filtered data as CSV",
        csv, file_name=f"{stock_key}_{date_range[0]}_{date_range[1]}.csv",
        mime="text/csv",
    )

# ---------- TAB 2: SQL PLAYGROUND ----------
with tab2:
    st.markdown("##### Run live SQL against `stocks.db`")
    st.caption("Tables: `bajaj_auto`, `eicher_motors`, `hero_motocorp`, `infosys`, `tcs`, `tvs_motors`")

    default_q = """-- Try one of these:
-- SELECT COUNT(*) FROM bajaj_auto;
-- SELECT date, close_price FROM tcs ORDER BY close_price DESC LIMIT 5;
-- SELECT strftime('%Y', date) AS yr, ROUND(AVG(close_price),2) AS avg
--   FROM infosys GROUP BY yr ORDER BY yr;
SELECT date, close_price FROM bajaj_auto ORDER BY date DESC LIMIT 5;"""

    query = st.text_area("Query", default_q, height=180)

    col_a, col_b = st.columns([1, 5])
    with col_a:
        run = st.button("▶️ Run query", type="primary")

    if run:
        try:
            conn = sqlite3.connect(DB)
            result = pd.read_sql(query, conn)
            conn.close()
            st.success(f"✅ Returned {len(result)} rows")
            st.dataframe(result, use_container_width=True, height=380)
        except Exception as e:
            st.error(f"❌ SQL error: {e}")

# ---------- TAB 3: ALL STOCKS ----------
with tab3:
    st.markdown("##### Rebased to 100 — see how each stock grew over time")

    all_df = load_all()
    pivot = all_df.pivot(index="date", columns="stock", values="close_price").sort_index()
    rebased = pivot / pivot.iloc[0] * 100

    palette = {
        "Bajaj Auto":    "#3b82f6",
        "Eicher Motors": "#8b5cf6",
        "Hero Motocorp": "#ec4899",
        "Infosys":       "#10b981",
        "TCS":           "#f59e0b",
        "TVS Motors":    "#ef4444",
    }

    fig2 = go.Figure()
    for col in rebased.columns:
        fig2.add_trace(go.Scatter(
            x=rebased.index, y=rebased[col],
            mode="lines", name=col,
            line=dict(width=2.4, color=palette[col]),
        ))
    fig2.update_layout(
        height=520,
        template="plotly_dark",
        paper_bgcolor="rgba(15,23,42,0)",
        plot_bgcolor="rgba(30,41,59,0.4)",
        hovermode="x unified",
        yaxis_title="Index (first day = 100)",
        legend=dict(orientation="h", y=1.05, x=0),
        margin=dict(t=30, b=10, l=10, r=10),
        font=dict(family="Inter", color="#cbd5e1"),
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##### Headline numbers (unadjusted)")
    rows = []
    for t in STOCKS:
        d = load_stock(t)
        ret = (d["close_price"].iloc[-1] - d["close_price"].iloc[0]) / d["close_price"].iloc[0] * 100
        rows.append({
            "Stock": NICE[t],
            "Ticker": TICKER[t],
            "First Close": f"₹{d['close_price'].iloc[0]:.2f}",
            "Last Close": f"₹{d['close_price'].iloc[-1]:.2f}",
            "Return %": f"{ret:+.1f}%",
            "Buys": int((d["signal"] == "Buy").sum()),
            "Sells": int((d["signal"] == "Sell").sum()),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.warning("⚠️ Raw TCS and Infosys returns are misleading due to 1:1 bonus issues.")

# ---------- TAB 4: INSIGHTS ----------
with tab4:
    st.markdown("## 💡 Key Findings")

    st.markdown("### 🏆 Headline Results (Adjusted)")
    st.dataframe(pd.DataFrame([
        {"Stock": "TVS Motors",    "Return": "+86.9%", "Buys": 8,  "Sells": 8},
        {"Stock": "Eicher Motors", "Return": "+82.6%", "Buys": 6,  "Sells": 7},
        {"Stock": "TCS *",         "Return": "+52.4%", "Buys": 12, "Sells": 13},
        {"Stock": "Infosys *",     "Return": "+38.2%", "Buys": 9,  "Sells": 9},
        {"Stock": "Bajaj Auto",    "Return": "+10.0%", "Buys": 12, "Sells": 11},
        {"Stock": "Hero Motocorp", "Return": "+6.0%",  "Buys": 9,  "Sells": 9},
    ]), use_container_width=True, hide_index=True)
    st.caption("* Adjusted for 1:1 bonus issues")

    st.markdown("### 🚨 The Data Trap")
    st.error(
        "**TCS (2018-05-31)** and **Infosys (2015-06-15)** show apparent -50% "
        "single-day drops. These are **1:1 bonus issues**, not real losses. "
        "Unadjusted: TCS -23.8%, Infosys -30.9%. Adjusted: **+52.4% and +38.2%**."
    )

    st.markdown("### 🧹 Missing Data")
    st.info(
        "Six NULL `deliverable_qty` rows, all on just two dates: "
        "**2015-12-09** (4 stocks) and **2017-08-31** (2 stocks). "
        "This is an exchange-level reporting gap."
    )

    st.markdown("### ⚠️ Method Caveats")
    st.markdown("""
    - Moving averages are **lagging indicators**
    - The dataset excludes **dividends, brokerage costs, and taxes**
    - Golden-cross signals trigger many false positives in choppy markets
    - **Broader market context** (Nifty/Sensex) is missing
    """)