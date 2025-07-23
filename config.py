# NiftyUpstoxDashboard/modules/config.py - FINAL VERSION FOR DEPLOYMENT

import streamlit as st

# Try to load from Streamlit's secrets manager first, otherwise use local strings
UPSTOX_API_KEY = st.secrets.get("UPSTOX_API_KEY", "YOUR_LOCAL_API_KEY_HERE")
UPSTOX_ACCESS_TOKEN = st.secrets.get("UPSTOX_ACCESS_TOKEN", "YOUR_LOCAL_ACCESS_TOKEN_HERE")

# --- Instrument Keys ---
NIFTY_50_INSTRUMENT_KEY = "NSE_INDEX|Nifty 50"

# --- Data File Path ---
INSTRUMENT_CSV_PATH = "data/NSE_cleaned.csv"
DATABASE_PATH = "data/market_data.db" # Note: This DB will reset on deployment restarts

# --- App Settings ---
APP_TITLE = "NIFTY Live Analysis Dashboard"
PAGE_ICON = "📊"