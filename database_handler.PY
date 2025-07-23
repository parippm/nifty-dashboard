# NiftyUpstoxDashboard/modules/database_handler.py

import sqlite3
import pandas as pd
from datetime import date
import streamlit as st

def init_db(db_path):
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_pivots (
        date TEXT PRIMARY KEY,
        high REAL,
        low REAL,
        close REAL,
        R3 REAL,
        R2 REAL,
        R1 REAL,
        Pivot REAL,
        S1 REAL,
        S2 REAL,
        S3 REAL
    )
    """)
    conn.commit()
    conn.close()

def save_pivots_to_db(db_path, pivot_data):
    """Save the calculated pivot points for the current date."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    
    # Use INSERT OR REPLACE to avoid duplicate date entries
    cursor.execute("""
    INSERT OR REPLACE INTO daily_pivots (date, high, low, close, R3, R2, R1, Pivot, S1, S2, S3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        today_str,
        pivot_data.get('High'), pivot_data.get('Low'), pivot_data.get('Close'),
        pivot_data.get('R3'), pivot_data.get('R2'), pivot_data.get('R1'),
        pivot_data.get('Pivot'), pivot_data.get('S1'), pivot_data.get('S2'), pivot_data.get('S3')
    ))
    conn.commit()
    conn.close()

@st.cache_data(ttl=3600) # Cache for 1 hour
def get_historical_pivots(db_path):
    """Retrieve all historical pivot points from the database."""
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM daily_pivots ORDER BY date DESC", conn)
        return df
    except pd.io.sql.DatabaseError:
        return pd.DataFrame() # Return empty if table doesn't exist yet
    finally:
        conn.close()