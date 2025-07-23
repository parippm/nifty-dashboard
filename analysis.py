# NiftyUpstoxDashboard/modules/analysis.py

import pandas as pd

def calculate_pivot_points(df_15min):
    """Calculates classic pivot points based on the first 15min OHLC."""
    if df_15min.empty:
        return {}
    
    high = df_15min['high'].max()
    low = df_15min['low'].min()
    close = df_15min['close'].iloc[-1]
    
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2 * (pivot - low)
    s3 = low - 2 * (high - pivot)
    
    return {'R3': r3, 'R2': r2, 'R1': r1, 'Pivot': pivot, 'S1': s1, 'S2': s2, 'S3': s3}

def get_option_trend(ltp, prev_ltp, oi, prev_oi):
    """Determines the option trend based on price and Open Interest changes."""
    price_change = ltp - prev_ltp
    oi_change = oi - prev_oi
    
    if price_change > 0 and oi_change > 0:
        return "Long Buildup"
    elif price_change < 0 and oi_change > 0:
        return "Short Buildup"
    elif price_change > 0 and oi_change < 0:
        return "Short Covering"
    elif price_change < 0 and oi_change < 0:
        return "Long Unwinding"
    else:
        return "─" # Represents neutral or no change

def calculate_msv(price_series, window=14):
    """Calculates the Moving Standard Deviation (Volatility)."""
    return price_series.rolling(window=window).std()