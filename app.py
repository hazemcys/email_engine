import streamlit as st
import pandas as pd
from engine import load_and_parse, write_outputs
from classifier import run_ai_classification
import plotly.express as px
import os
import time

st.set_page_config(page_title="Email Engine", layout="centered")

# ── THEME LOADING (graceful fallback) ──
# If ultra_theme.py exists → premium UI
# If you delete it → old default UI loads, nothing crashes
_FALLBACK_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    * {
        font-family: 'Cairo', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top left, #0d1117, #161b22);
    }

    [data-testid="stSidebar"] {
        background: rgba(22, 27, 34, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #007cf0, #00dfd8);
        color: white;
        border: none;
        padding: 15px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 124, 240, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 124, 240, 0.5);
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.3s;
    }

    .metric-card:hover {
        border-color: #00dfd8;
        background: rgba(255, 255, 255, 0.08);
    }

    .stDataFrame {
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
        transition: 0.3s;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background: #007cf0 !important;
        border-radius: 10px;
    }
    </style>
    """

try:
    from ultra_theme import get_ultra_css, get_ultra_header, get_stage_icon
    st.markdown(get_ultra_css(), unsafe_allow_html=True)
    st.markdown(get_ultra_header(), unsafe_allow_html=True)
except ImportError:
    st.markdown(_FALLBACK_CSS, unsafe_allow_html=True)
    # Define fallback if theme is missing so app doesn't crash
    def get_stage_icon(stage_num):
        return f"<h3>Stage {stage_num}</h3>"

st.title("🚀 Email Categorization Engine")
st.write("Upload Your MBOX File To Start The Classification.")

# UI Settings for AI
with st.sidebar:
    st.header("Settings")
    enable_ai = st.checkbox("Enable AI Classification", value=False, help="Uses Gemini AI to categorize emails (real_user, ad, etc.)")
    spam_val = st.number_input("Spam Threshold", min_value=1, value=5, help="Number of occurrences to flag a sender in Stage 1")

uploaded_file = st.file_uploader("Choose MBOX File")

temp_path = "temp_data.mbox"

if uploaded_file is not None:
    if st.button("Start The Classification"):
        with st.spinner("Processing... Please Wait"):
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 1. Core Parsing
            all_rows, phone_tracker = load_and_parse(temp_path)
            
            # 2. Optional AI Classification
            if enable_ai:
                st.info("🧠 AI Classification active. Processing in batches...")
                batch_size = 20
                ai_failed = False
                for i in range(0, len(all_rows), batch_size):
                    if ai_failed: break
                    
                    chunk = all_rows[i : i + batch_size]
                    results = run_ai_classification(chunk)
                    
                    if results and results[0] == "RATE_LIMIT_HIT":
                        st.warning("⚠️ AI Rate Limit Hit! Continuing without AI.")
                        ai_failed = True
                        continue

                    for j, category in enumerate(results):
                        if i + j < len(all_rows):
                            all_rows[i + j]['category'] = category
                    time.sleep(0.5)

            # 3. Pipeline Filtering
            write_outputs("output", all_rows, phone_tracker, spam_threshold=spam_val)
            st.session_state['all_results'] = pd.DataFrame(all_rows)
            st.success("Done! Emails classified successfully.")

    if 'all_results' in st.session_state:
        all_results = st.session_state['all_results']
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "1️⃣ Most Occurred",
            "2️⃣ Legal Keywords",
            "3️⃣ Report Pattern",
            "4️⃣ Detected Phones",
            "5️⃣ Unprocessed",
            "📈 Intelligence Summary"
        ])
        
        with tab1:
            st.markdown(get_stage_icon(1), unsafe_allow_html=True)
            df1 = all_results[all_results['stage'] == 1]
            st.metric("Flagged Senders", len(df1))
            st.dataframe(df1, use_container_width=True)
            if not df1.empty:
                st.download_button("Download Stage 1", df1.to_csv(index=False).encode('utf-8'), "most_occurred.csv", "text/csv")

        with tab2:
            st.markdown(get_stage_icon(2), unsafe_allow_html=True)
            df2 = all_results[all_results['stage'] == 2]
            st.metric("Legal Matches", len(df2))
            st.dataframe(df2, use_container_width=True)
            if not df2.empty:
                st.download_button("Download Stage 2", df2.to_csv(index=False).encode('utf-8'), "legal_keywords.csv", "text/csv")

        with tab3:
            st.markdown(get_stage_icon(3), unsafe_allow_html=True)
            df3 = all_results[all_results['stage'] == 3] 
            st.metric("Reports Detected", len(df3))
            st.dataframe(df3, use_container_width=True)
            if not df3.empty:
                st.download_button("Download Stage 3", df3.to_csv(index=False).encode('utf-8'), "report_entries.csv", "text/csv")

        with tab4:
            st.markdown(get_stage_icon(4), unsafe_allow_html=True)
            df4 = all_results[all_results['stage'] == 4]
            st.metric("Valid Phone Hits", len(df4))
            st.dataframe(df4, use_container_width=True)
            if not df4.empty:
                st.download_button("Download Stage 4", df4.to_csv(index=False).encode('utf-8'), "detected_phones.csv", "text/csv")

        with tab5:
            st.markdown(get_stage_icon(5), unsafe_allow_html=True)
            df5 = all_results[all_results['stage'] == 5]
            st.metric("Unprocessed Junk", len(df5))
            st.dataframe(df5, use_container_width=True)
            if not df5.empty:
                st.download_button("Download Stage 5", df5.to_csv(index=False).encode('utf-8'), "unprocessed.csv", "text/csv")

        with tab6:
            st.markdown("<h3 style='margin-bottom: 25px;'>📊 Data Intelligence Dashboard</h3>", unsafe_allow_html=True)
            
            # --- TOP METRICS ---
            total = len(all_results)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Processed", total)
            with m2:
                spam_count = len(all_results[all_results['stage'] == 1])
                st.metric("Spam Volume", f"{(spam_count/total*100 if total > 0 else 0):.1f}%")
            with m3:
                useful_count = len(all_results[all_results['stage'].isin([2,3,4])])
                st.metric("Intelligence Yield", f"{(useful_count/total*100 if total > 0 else 0):.1f}%")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- CHARTS ---
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Stage Distribution")
                fig_pie = px.pie(
                    all_results, 
                    names='stage', 
                    hole=0.6,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    font_color="white", 
                    showlegend=True,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with c2:
                st.subheader("Volume by Pipeline Stage")
                stage_counts = all_results['stage'].value_counts().reset_index()
                stage_counts.columns = ['Stage', 'Count']
                fig_bar = px.bar(
                    stage_counts, 
                    x='Stage', 
                    y='Count',
                    color='Count',
                    color_continuous_scale='Viridis'
                )
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    font_color="white",
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # --- EXPORT ---
            st.markdown("<br>", unsafe_allow_html=True)
            full_csv = all_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DOWNLOAD MASTER INTELLIGENCE REPORT",
                data=full_csv,
                file_name="Intelligence_Report.csv",
                mime="text/csv",
                use_container_width=True
            )

    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except:
            pass