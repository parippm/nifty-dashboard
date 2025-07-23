# NiftyUpstoxDashboard/pages/1_Option_Chain.py

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import time
from modules.api_handler import get_option_chain, get_live_price
from modules.analysis import get_option_trend
from modules.config import NIFTY_50_INSTRUMENT_KEY
from modules.styles import get_option_chain_styles

st.set_page_config(page_title="NIFTY Option Chain", page_icon="🚀", layout="wide")
st.markdown(get_option_chain_styles(), unsafe_allow_html=True)
st.title("🚀 Real-Time NIFTY Option Chain")

# --- Sidebar Controls ---
st.sidebar.header("Controls")
today = date.today()
# Find the next Thursday
thursday = today + timedelta(days=(3 - today.weekday() + 7) % 7)
expiry_dates = [(thursday + timedelta(days=i*7)).strftime("%Y-%m-%d") for i in range(8)]
expiry_date_str = st.sidebar.selectbox("Select Expiry Date", expiry_dates)

# --- Fetch Live Data ---
placeholder = st.empty()
nifty_spot = get_live_price(NIFTY_50_INSTRUMENT_KEY)

if nifty_spot:
    placeholder.metric("NIFTY 50 Spot Price", f"₹{nifty_spot:,.2f}")
else:
    placeholder.warning("Could not fetch NIFTY spot price. Retrying...")
    st.stop()

strike_range = st.sidebar.slider(
    "Select Strike Range",
    min_value=int(nifty_spot - 1000), max_value=int(nifty_spot + 1000),
    value=(int(nifty_spot - 400), int(nifty_spot + 400)), step=50
)

# --- Fetch and Process Data ---
option_data = get_option_chain(NIFTY_50_INSTRUMENT_KEY, expiry_date_str)
if not option_data:
    st.warning("No option chain data received. It might be off-market hours, a holiday, or an invalid expiry.")
    st.stop()

df = pd.DataFrame(option_data)
df_filtered = df[(df['strike_price'] >= strike_range[0]) & (df['strike_price'] <= strike_range[1])]

final_data = []
for _, row in df_filtered.iterrows():
    ce = row.get('ce', {})
    pe = row.get('pe', {})

    # Use the correct keys from Upstox API response for trend calculation
    ce_trend = get_option_trend(ce.get('ltp', 0), ce.get('last_close', 0), ce.get('oi', 0), ce.get('prev_day_oi', 0))
    pe_trend = get_option_trend(pe.get('ltp', 0), pe.get('last_close', 0), pe.get('oi', 0), pe.get('prev_day_oi', 0))
    
    final_data.append({
        'CALL_VOLUME': ce.get('volume', 0),
        'CALL_OI': ce.get('oi', 0),
        'CALL_CH_OI': ce.get('oi_change', 0),
        'CALL_LTP': ce.get('ltp', 0),
        'CALL_TREND': ce_trend,
        'CALL_SIGNAL': "BUY" if "Long" in ce_trend or "Covering" in ce_trend else "SELL",
        'STRIKE': row['strike_price'],
        'PUT_SIGNAL': "BUY" if "Long" in pe_trend or "Covering" in pe_trend else "SELL",
        'PUT_TREND': pe_trend,
        'PUT_LTP': pe.get('ltp', 0),
        'PUT_CH_OI': pe.get('oi_change', 0),
        'PUT_OI': pe.get('oi', 0),
        'PUT_VOLUME': pe.get('volume', 0),
    })

if not final_data:
    st.warning("No data available in the selected strike range.")
    st.stop()

df_final = pd.DataFrame(final_data)

# --- Function to Style and Render the Custom HTML Table ---
def create_option_chain_html(df, spot):
    html = "<table class='dataframe-container'>"
    html += "<thead><tr>"
    call_headers = ["VOLUME", "OI", "CHNG IN OI", "LTP", "TREND", "SIGNAL"]
    put_headers = ["SIGNAL", "TREND", "LTP", "CHNG IN OI", "OI", "VOLUME"]
    for h in call_headers: html += f"<th>{h}</th>"
    html += "<th>STRIKE</th>"
    for h in put_headers: html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"
    
    for _, row in df.iterrows():
        is_call_itm, is_put_itm = row['STRIKE'] < spot, row['STRIKE'] > spot
        call_bg, put_bg = "call-bg itm" if is_call_itm else "call-bg", "put-bg itm" if is_put_itm else "put-bg"
        
        html += f"""<tr>
            <td class='{call_bg}'>{row['CALL_VOLUME']:,}</td> <td class='{call_bg}'>{row['CALL_OI']:,}</td>
            <td class='{call_bg}'>{row['CALL_CH_OI']:,}</td> <td class='{call_bg}'>{row['CALL_LTP']}</td>
            <td class='{call_bg} trend-{row['CALL_TREND'].lower().replace(' ', '-')}'>{row['CALL_TREND']}</td>
            <td class='{call_bg}'>{row['CALL_SIGNAL']}</td>
            <td class='strike-col'>{row['STRIKE']}</td>
            <td class='{put_bg}'>{row['PUT_SIGNAL']}</td>
            <td class='{put_bg} trend-{row['PUT_TREND'].lower().replace(' ', '-')}'>{row['PUT_TREND']}</td>
            <td class='{put_bg}'>{row['PUT_LTP']}</td> <td class='{put_bg}'>{row['PUT_CH_OI']:,}</td>
            <td class='{put_bg}'>{row['PUT_OI']:,}</td> <td class='{put_bg}'>{row['PUT_VOLUME']:,}</td>
        </tr>"""
    html += "</tbody></table>"
    return html

st.write(create_option_chain_html(df_final, nifty_spot), unsafe_allow_html=True)

# Auto-refresh logic
st.caption("Page refreshes automatically.")
time.sleep(30)
st.rerun()