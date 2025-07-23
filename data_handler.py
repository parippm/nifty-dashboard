# NiftyUpstoxDashboard/modules/data_handler.py

import pandas as pd
import os
from datetime import datetime
import streamlit as st

@st.cache_data
def load_instrument_data(file_path):
    """Loads and caches the instrument data from the CSV file."""
    if not os.path.exists(file_path):
        st.error(f"FATAL ERROR: Instrument file not found at '{file_path}'")
        return None
    try:
        # --- FIX: Specify the date format to match your CSV ---
        df = pd.read_csv(file_path, parse_dates=['expiry'], dayfirst=True)
        return df
    except Exception as e:
        st.error(f"Error reading or processing CSV file: {e}")
        return None

def get_current_nifty_futures_key(df):
    """Dynamically finds the instrument key for the current month's Nifty futures."""
    if df is None:
        return None
    
    today = datetime.now()
    
    futures_df = df[
        (df['instrument_type'] == 'FUTIDX') & 
        (df['name'] == 'NIFTY') &
        (df['expiry'] >= today)
    ].copy()
    
    if futures_df.empty:
        st.error("No active NIFTY Futures contract found in the CSV for today or a future date.")
        return None
    
    # Sort by expiry to find the nearest contract
    futures_df = futures_df.sort_values(by='expiry')
    return futures_df.iloc[0]['instrument_key']