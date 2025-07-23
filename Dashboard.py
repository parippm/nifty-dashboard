# NiftyUpstoxDashboard/Dashboard.py

import streamlit as st
from modules.config import APP_TITLE, PAGE_ICON, NIFTY_50_INSTRUMENT_KEY
from modules.api_handler import get_live_price

st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")

st.title(f"📊 {APP_TITLE}")
st.markdown("Welcome to your personal NIFTY analysis dashboard, powered by the Upstox API.")
st.markdown("---")

nifty_price = get_live_price(NIFTY_50_INSTRUMENT_KEY)
if nifty_price:
    st.header(f"NIFTY 50 Live Price: ₹{nifty_price:,.2f}")
else:
    st.header("Fetching NIFTY 50 Live Price...")

st.info("Use the navigation panel on the left to explore the Option Chain and Live Charts.")
st.subheader("How to Get Started")
st.markdown("""
1.  **Navigate to a Page**: Use the sidebar on the left to select a tool.
    -   **Option Chain**: View real-time NIFTY option chain data with trend analysis.
    -   **Live Charts**: See the NIFTY Futures chart with live pivot points and the MSV volatility indicator.
2.  **Select Parameters**: On each page, use the sidebar controls to select the expiry date or chart settings.
3.  **Analyze**: The data will automatically refresh at regular intervals.
""")

st.markdown("---")
st.text("Built with Streamlit and Upstox API. This is an analysis tool, not for trading.")