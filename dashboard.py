
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Breakout Scanner 5.5", layout="wide")

st.title("📈 Breakout Scanner v5.5 Dashboard")

scan_dir = "scans"
scans = sorted([f for f in os.listdir(scan_dir) if f.endswith(".csv")], reverse=True)

if scans:
    latest = scans[0]
    st.subheader(f"Latest Scan: {latest}")
    df = pd.read_csv(os.path.join(scan_dir, latest))
    df = df.sort_values(by="Vol Spike", ascending=False)
    st.dataframe(df)
else:
    st.warning("No scan results found.")
