# NiftyUpstoxDashboard/modules/styles.py

def get_option_chain_styles():
    """Returns CSS styles for the option chain table."""
    return """
        <style>
            .dataframe-container { font-size: 14px; border-collapse: collapse; width: 100%; }
            .dataframe-container th {
                background-color: #262730; color: #fafafa; text-align: center !important;
                font-weight: bold; padding: 8px; border: 1px solid #444;
            }
            .dataframe-container td { text-align: center !important; border: 1px solid #444; padding: 6px; }
            .call-bg { background-color: rgba(0, 100, 0, 0.2); }
            .put-bg { background-color: rgba(100, 0, 0, 0.2); }
            .itm { font-weight: bold; }
            .strike-col { font-weight: bold; background-color: #333; color: #ffab00; }
            .trend-long-buildup { color: #28a745; font-weight: bold; }
            .trend-short-buildup { color: #dc3545; font-weight: bold; }
            .trend-short-covering { color: #ffc107; }
            .trend-long-unwinding { color: #fd7e14; }
        </style>
    """