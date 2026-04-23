"""
Ultra Theme — Email Engine
==========================
Safe to delete: app.py falls back to its original CSS automatically.
"""


def get_ultra_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ─── RESET & FOUNDATION ─────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Fix: isolate Streamlit icon fonts from override */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    /* ─── BACKGROUND ─────────────────────────────────── */
    .stApp {
        background-color: #0a0a0a !important;
        background-image:
            radial-gradient(ellipse 60% 40% at 50% 0%, rgba(99,102,241,0.08) 0%, transparent 100%) !important;
    }

    /* ─── SIDEBAR ────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #0f0f0f !important;
        border-right: 1px solid #1a1a1a !important;
    }
    [data-testid="stSidebar"] * {
        color: #a1a1aa !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #e4e4e7 !important;
    }

    /* ─── MAIN CONTENT ───────────────────────────────── */
    .main .block-container {
        padding: 3rem 2.5rem !important;
        max-width: 860px !important;
    }

    /* ─── TYPOGRAPHY ─────────────────────────────────── */
    h1, h2, h3 {
        color: #ffffff !important;
        letter-spacing: -0.025em !important;
        font-weight: 700 !important;
    }

    p, span, label, div {
        color: #a1a1aa;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
    }

    /* ─── INPUTS & CONTROLS ──────────────────────────── */
    input[type="number"],
    input[type="text"] {
        background: #141414 !important;
        border: 1px solid #262626 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        outline: none !important;
    }

    /* ─── CHECKBOX ───────────────────────────────────── */
    [data-testid="stCheckbox"] label p {
        color: #d4d4d8 !important;
    }

    /* ─── FILE UPLOADER ──────────────────────────────── */
    [data-testid="stFileUploader"] {
        background: #111111 !important;
        border: 1px dashed #2d2d2d !important;
        border-radius: 12px !important;
        padding: 0 !important;
        transition: border-color 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1 !important;
    }
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: #71717a !important;
    }
    /* Hide the duplicated upload button label */
    [data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
        background: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 8px !important;
        color: #e4e4e7 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }

    /* ─── PRIMARY BUTTON ─────────────────────────────── */
    .stButton > button[kind="primary"],
    .stButton > button {
        background: #6366f1 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        height: 44px !important;
        letter-spacing: 0 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #4f46e5 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px rgba(99,102,241,0.3) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ─── DOWNLOAD BUTTON ────────────────────────────── */
    .stDownloadButton > button {
        background: transparent !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 8px !important;
        color: #a1a1aa !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: #6366f1 !important;
        color: #6366f1 !important;
        background: rgba(99,102,241,0.05) !important;
    }

    /* ─── METRIC CARDS ───────────────────────────────── */
    [data-testid="stMetric"] {
        background: #111111 !important;
        border: 1px solid #1d1d1d !important;
        border-radius: 10px !important;
        padding: 1.2rem 1.4rem !important;
        transition: border-color 0.2s ease !important;
    }
    [data-testid="stMetric"]:hover {
        border-color: #333333 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #71717a !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ─── TABS ───────────────────────────────────────── */
    [data-baseweb="tab-list"] {
        background: #111111 !important;
        border-radius: 10px !important;
        border: 1px solid #1d1d1d !important;
        padding: 4px !important;
        gap: 2px !important;
    }
    [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 7px !important;
        color: #71717a !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 8px 14px !important;
        transition: all 0.15s ease !important;
    }
    [data-baseweb="tab"]:hover {
        color: #e4e4e7 !important;
        background: #1a1a1a !important;
    }
    [aria-selected="true"][data-baseweb="tab"] {
        background: #1d1d1d !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-baseweb="tab-highlight"],
    [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ─── DATAFRAME ──────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border: 1px solid #1d1d1d !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* ─── ALERTS ─────────────────────────────────────── */
    [data-testid="stAlert"] {
        background: #111111 !important;
        border-radius: 10px !important;
        border: 1px solid #1d1d1d !important;
    }
    [data-testid="stAlert"] p {
        color: #e4e4e7 !important;
    }

    /* ─── SPINNER ────────────────────────────────────── */
    [data-testid="stSpinner"] > div {
        border-color: #6366f1 transparent transparent !important;
    }

    /* ─── SCROLLBAR ──────────────────────────────────── */
    * {
        scrollbar-width: thin;
        scrollbar-color: #2d2d2d transparent;
    }
    *::-webkit-scrollbar { width: 5px; height: 5px; }
    *::-webkit-scrollbar-thumb {
        background: #2d2d2d;
        border-radius: 10px;
    }
    </style>
    """


def get_ultra_header():
    return """
    <div style="
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #1a1a1a;
    ">
        <div style="
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #6366f1;
            margin-bottom: 0.75rem;
        ">Email Engine</div>
    </div>
    """


def get_stage_icon(stage_num):
    colors = {1: "#f87171", 2: "#fb923c", 3: "#a78bfa", 4: "#34d399", 5: "#94a3b8"}
    labels = {1: "Most Occurred", 2: "Legal Keywords", 3: "Report Pattern", 4: "Detected Phones", 5: "Unprocessed"}
    color = colors.get(stage_num, "#6366f1")
    label = labels.get(stage_num, "Stage")
    return f"""
    <span style="
        display: inline-block;
        padding: 3px 10px;
        border-radius: 5px;
        background: {color}15;
        border: 1px solid {color}40;
        color: {color};
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    ">STAGE {stage_num} · {label}</span>
    """
