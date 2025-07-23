# NiftyUpstoxDashboard/pages/2_Live_Charts.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from modules.api_handler import get_historical_data
from modules.analysis import calculate_pivot_points, calculate_msv
from modules.data_handler import load_instrument_data, get_current_nifty_futures_key
from modules.database_handler import init_db, save_pivots_to_db, get_historical_pivots
from modules.config import INSTRUMENT_CSV_PATH, DATABASE_PATH

st.set_page_config(page_title="Live Charts", page_icon="📈", layout="wide")
st.title("📈 Live NIFTY Futures & MSV Chart")

# Initialize the database
init_db(DATABASE_PATH)

# Dynamically find the current futures key
instrument_df = load_instrument_data(INSTRUMENT_CSV_PATH)
current_fut_key = get_current_nifty_futures_key(instrument_df)

if not current_fut_key:
    st.error("Could not determine the current NIFTY Futures instrument key from the CSV file.")
    st.stop()

st.info(f"Displaying chart for the current active contract: **{current_fut_key}**")

candle_data = get_historical_data(current_fut_key, "1minute")
if not candle_data:
    st.warning("Could not fetch historical data. It might be off-market hours.")
    st.stop()

df = pd.DataFrame(candle_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'oi'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

df_first_15min = df.between_time('09:15', '09:30')
pivots = calculate_pivot_points(df_first_15min)
df['msv'] = calculate_msv(df['close'], window=14)

# Save pivots to database if calculated
if pivots:
    pivot_data_to_save = pivots.copy()
    pivot_data_to_save['High'] = df_first_15min['high'].max()
    pivot_data_to_save['Low'] = df_first_15min['low'].min()
    pivot_data_to_save['Close'] = df_first_15min['close'].iloc[-1]
    save_pivots_to_db(DATABASE_PATH, pivot_data_to_save)

# --- Price Chart with Pivot Points ---
st.subheader("NIFTY Futures Chart (1-Min) with Pivot Points")
fig_price = go.Figure(go.Candlestick(
    x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'], name='NIFTY Future'
))

if pivots:
    colors = {'R3':'#FF0000','R2':'#FF5733','R1':'#FFC300','Pivot':'#808080','S1':'#DAF7A6','S2':'#00FF00','S3':'#008000'}
    for level, value in pivots.items():
        fig_price.add_hline(y=value, line_dash="dash", line_color=colors.get(level),
                            annotation_text=f"{level}: {value:,.2f}", annotation_position="bottom right")
fig_price.update_layout(yaxis_title='Price (₹)', xaxis_rangeslider_visible=False, height=600)
st.plotly_chart(fig_price, use_container_width=True)

# --- MSV Chart ---
st.subheader("MSV (Moving Standard Deviation) - Volatility")
fig_msv = go.Figure(go.Scatter(x=df.index, y=df['msv'], mode='lines', name='MSV', line=dict(color='purple', width=2)))
fig_msv.update_layout(yaxis_title='Volatility', xaxis_title='Time', height=300)
st.plotly_chart(fig_msv, use_container_width=True)

# --- Historical Pivots Display ---
st.subheader("Historical Pivot Points")
df_pivots = get_historical_pivots(DATABASE_PATH)
if not df_pivots.empty:
    st.dataframe(df_pivots, use_container_width=True)
else:
    st.info("No historical pivot data found. It will be saved at the end of the first 15 minutes of the next trading day.")

# Auto-refresh logic
st.caption("Page refreshes automatically.")
time.sleep(60)
st.rerun() # FIX: Use the correct rerun function