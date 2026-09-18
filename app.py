import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Finance Dashboard", layout="wide")

# Dark theme CSS
st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    .stMetric { background-color: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 8px; }
    .stMetricLabel { color: #8b949e !important; }
    .stMetricValue { color: #e6edf3 !important; }
    h1, h2, h3 { color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def fetch_data(ticker, days):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(1, axis=1)
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def sma(series, n):
    return series.rolling(window=n).mean()

st.title("Finance Dashboard")

# Sidebar
ticker = st.sidebar.text_input("Ticker", "AAPL").upper()
days = st.sidebar.selectbox("Period", [90, 180, 365, 730], index=1)

if not ticker:
    st.stop()

df = fetch_data(ticker, days)
if df is None or df.empty:
    st.error("No data found")
    st.stop()

df['50MA'] = sma(df['Close'], 50)
df['200MA'] = sma(df['Close'], 200)

# KPIs
current = df['Close'].iloc[-1]
start_price = df['Close'].iloc[0]
ytd_start = df[df['Date'] >= datetime(df['Date'].iloc[-1].year, 1, 1)]['Close'].iloc[0] if len(df[df['Date'] >= datetime(df['Date'].iloc[-1].year, 1, 1)]) > 0 else start_price

change_1d = df['Close'].pct_change().iloc[-1] * 100
change_1m = (df['Close'].iloc[-1] / df['Close'].iloc[-21] - 1) * 100 if len(df) > 21 else 0
change_ytd = (current / ytd_start - 1) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Price", f"${current:.2f}", f"{change_1d:+.2f}%")
col2.metric("1M Change", f"{change_1m:+.2f}%")
col3.metric("YTD Change", f"{change_ytd:+.2f}%")
col4.metric("Period High", f"${df['High'].max():.2f}")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Charts", "Export"])

with tab1:
    st.subheader(f"{ticker} Price & Moving Averages")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close', line=dict(color='#58a6ff', width=2)))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['50MA'], name='50MA', line=dict(color='#ffd700', width=1.5, dash='dash')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['200MA'], name='200MA', line=dict(color='#ff6b6b', width=1.5, dash='dot')))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font=dict(color='#c9d1d9'),
        xaxis=dict(gridcolor='#21262d'),
        yaxis=dict(gridcolor='#21262d'),
        margin=dict(l=40, r=20, t=40, b=40),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Volume")
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker_color='rgba(88,166,255,0.3)'))
    fig_vol.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font=dict(color='#c9d1d9'),
        xaxis=dict(gridcolor='#21262d'),
        yaxis=dict(gridcolor='#21262d'),
        margin=dict(l=40, r=20, t=40, b=40),
        height=300,
    )
    st.plotly_chart(fig_vol, use_container_width=True)

with tab3:
    st.subheader("Download Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, f"{ticker}_data.csv", "text/csv", key='download-csv')
    
    st.subheader("Download Chart")
    fig.write_image(f"{ticker}_chart.png")
    with open(f"{ticker}_chart.png", "rb") as f:
        st.download_button("Download PNG", f.read(), f"{ticker}_chart.png", "image/png", key='download-png')

st.sidebar.markdown("---")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
