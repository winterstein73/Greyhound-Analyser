import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="The Regulr - Greyhound Analyzer",
    page_icon="🐾",
    layout="wide"
)

st.image("regulr_logo.png", width=200)
st.markdown("## 🏁 The Regulr: Greyhound Race Analyzer")
st.markdown("---")

uploaded_file = st.file_uploader("📤 Upload your race form Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Load Race Summary
    summary_df = pd.read_excel(uploaded_file, sheet_name="Race 8 Summary")
    st.subheader("📊 Race 8 Summary")
    st.dataframe(summary_df)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚡ Fastest Early Speed")
        st.dataframe(summary_df.nsmallest(3, 'Split Rank')[["Dog", "Box", "Best Split (s)", "Split Rank"]])
    with col2:
        st.markdown("### 🏁 Fastest Overall Time")
        st.dataframe(summary_df.nsmallest(3, 'Speed Rank')[["Dog", "Box", "Best Time (s)", "Speed Rank"]])

    ev_df = pd.read_excel(uploaded_file, sheet_name="EV Calculator")
    ev_df["Your Win Probability"] = ev_df["Your Estimated Win %"] / 100
    ev_df["Bookie Probability"] = 1 / ev_df["Last SP (Odds)"]
    ev_df["EV"] = (ev_df["Your Win Probability"] - ev_df["Bookie Probability"]) * ev_df["Last SP (Odds)"]
    st.subheader("💰 EV Calculator")
    st.dataframe(ev_df.sort_values("EV", ascending=False)[["Dog", "Last SP (Odds)", "Your Estimated Win %", "EV"]])

    multi_df = pd.read_excel(uploaded_file, sheet_name="Same Race Multi")
    st.subheader("🎯 Same Race Multi Helper")
    st.dataframe(multi_df)
else:
    st.info("Please upload an Excel file.")
