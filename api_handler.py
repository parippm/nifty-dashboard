# NiftyUpstoxDashboard/modules/api_handler.py

import requests
import streamlit as st
from datetime import date
from modules.config import UPSTOX_ACCESS_TOKEN

HEADERS = {
    "accept": "application/json",
    "Api-Version": "2.0",
    "Authorization": f"Bearer {UPSTOX_ACCESS_TOKEN}"
}

@st.cache_data(ttl=15) # Cache for 15 seconds for more real-time feel
def get_live_price(instrument_key):
    url = f"https://api.upstox.com/v2/market-quote/ltp?instrument_key={instrument_key}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            key_in_response = list(data["data"].keys())[0]
            return data["data"][key_in_response].get("last_price")
    except requests.RequestException as e:
        st.error(f"API Error fetching live price for {instrument_key}: {e}")
    return None

@st.cache_data(ttl=30) # Cache for 30 seconds
def get_option_chain(instrument_key, expiry_date):
    url = "https://api.upstox.com/v2/option/chain"
    params = {"instrument_key": instrument_key, "expiry_date": expiry_date}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data.get("data", [])
    except requests.RequestException as e:
        st.error(f"API Error fetching option chain: {e}")
    return []

@st.cache_data(ttl=60)
def get_historical_data(instrument_key, interval="1minute"):
    today_str = date.today().strftime("%Y-%m-%d")
    url = f"https://api.upstox.com/v2/historical-candle/{instrument_key}/{interval}/{today_str}/{today_str}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data["data"]["candles"]
    except requests.RequestException as e:
        st.error(f"API Error fetching historical data for {instrument_key}: {e}")
    return []