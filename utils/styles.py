# utils/styles.py

def get_global_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Global font ───────────────────────────────── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Hide Streamlit chrome ─────────────────────── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

/* ── Page background ───────────────────────────── */
.stApp { background: #F0F4F8; }

/* ══════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D47A1 0%, #1565C0 40%, #1976D2 100%) !important;
    border-right: none !important;
}

/* Sidebar brand title block */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* All text in sidebar white */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: rgba(255,255,255,0.92) !important;
}

/* ── Nav links ─────────────────────────────────── */
[data-testid="stSidebarNav"] {
    padding: 0 12px !important;
}
[data-testid="stSidebarNav"] ul {
    padding: 0 !important;
}
[data-testid="stSidebarNav"] a {
    border-radius: 8px !important;
    padding: 9px 14px !important;
    color: rgba(255,255,255,0.82) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    transition: none !important;
    background: transparent !important;
    border: none !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255,255,255,0.22) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: inset 3px 0 0 #FFFFFF !important;
}

/* ── Sidebar divider ───────────────────────────── */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
    margin: 10px 0 !important;
}

/* ── Data Options section ──────────────────────── */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 6px !important;
    color: white !important;
}
[data-testid="stSidebar"] .stSelectbox svg { fill: white !important; }

/* ══════════════════════════════════════════════════
   HERO BANNER
══════════════════════════════════════════════════ */
.hero-banner {
    background: linear-gradient(135deg, #0D47A1 0%, #1976D2 55%, #42A5F5 100%);
    border-radius: 12px;
    padding: 26px 32px;
    margin-bottom: 22px;
    color: white;
    box-shadow: 0 4px 16px rgba(13,71,161,0.25);
}
.hero-banner h1 {
    color: white !important;
    font-size: 1.85rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    letter-spacing: -0.02em;
}
.hero-banner p {
    color: rgba(255,255,255,0.85);
    font-size: 0.97rem;
    margin: 0;
}

/* ══════════════════════════════════════════════════
   KPI CARDS
══════════════════════════════════════════════════ */
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 18px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border-top: 3px solid #1976D2;
    text-align: center;
    height: 100%;
}
.kpi-card .kpi-label {
    font-size: 0.72rem;
    color: #6B7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 8px;
}
.kpi-card .kpi-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #0D47A1;
    line-height: 1.15;
}
.kpi-card .kpi-sub {
    font-size: 0.73rem;
    color: #9CA3AF;
    margin-top: 4px;
}

/* ══════════════════════════════════════════════════
   SECTION CARD
══════════════════════════════════════════════════ */
.section-card {
    background: white;
    border-radius: 10px;
    padding: 20px 22px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}
.section-card h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #1A1A2E;
    margin: 0 0 14px 0;
}

/* ══════════════════════════════════════════════════
   ALERT BOXES
══════════════════════════════════════════════════ */
.info-box {
    background: #EFF6FF;
    border-left: 4px solid #1976D2;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #1E3A5F;
    font-size: 0.88rem;
}
.success-box {
    background: #F0FDF4;
    border-left: 4px solid #16A34A;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #14532D;
    font-size: 0.88rem;
}
.warning-box {
    background: #FFFBEB;
    border-left: 4px solid #F59E0B;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #78350F;
    font-size: 0.88rem;
}

/* ══════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════ */
div.stButton > button {
    background: #E53935 !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 10px 22px !important;
    letter-spacing: 0.02em !important;
    transition: background 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 2px 6px rgba(229,57,53,0.35) !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    background: #C62828 !important;
    box-shadow: 0 4px 12px rgba(229,57,53,0.45) !important;
}
div.stButton > button:active {
    background: #B71C1C !important;
    box-shadow: none !important;
}

/* Download buttons — blue */
[data-testid="stDownloadButton"] > button {
    background: #1565C0 !important;
    color: white !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 6px rgba(21,101,192,0.35) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #0D47A1 !important;
}

/* ══════════════════════════════════════════════════
   TABS
══════════════════════════════════════════════════ */
[data-baseweb="tab-list"] {
    gap: 4px !important;
    border-bottom: 2px solid #E0E7EF !important;
    background: transparent !important;
}
[data-baseweb="tab"] {
    border-radius: 7px 7px 0 0 !important;
    padding: 9px 20px !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    color: #6B7280 !important;
    background: transparent !important;
    border: none !important;
    transition: color 0.15s !important;
}
[data-baseweb="tab"]:hover { color: #1565C0 !important; }
[aria-selected="true"][data-baseweb="tab"] {
    color: #1565C0 !important;
    font-weight: 700 !important;
    border-bottom: 3px solid #1565C0 !important;
    background: transparent !important;
}

/* ══════════════════════════════════════════════════
   METRICS
══════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: white;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    border-top: 3px solid #1976D2;
}
[data-testid="stMetricLabel"] { font-size: 0.75rem !important; color: #6B7280 !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { color: #0D47A1 !important; font-weight: 700 !important; }

/* ══════════════════════════════════════════════════
   DATAFRAMES
══════════════════════════════════════════════════ */
[data-testid="stDataFrame"] { border-radius: 8px !important; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }

/* ══════════════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: white !important;
    border-radius: 10px !important;
    border: 1px solid #E0E7EF !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #1A1A2E !important;
    padding: 12px 16px !important;
}

/* ── Divider ───────────────────────────────────── */
hr { border: none; border-top: 1px solid #E0E7EF; margin: 18px 0; }

/* ── Inputs ────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border-radius: 6px !important;
    border: 1px solid #D1D5DB !important;
    font-size: 0.875rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #1976D2 !important;
    box-shadow: 0 0 0 3px rgba(25,118,210,0.12) !important;
}

/* Slider accent */
[data-testid="stSlider"] [role="slider"] {
    background: #1565C0 !important;
}
</style>
"""


def sidebar_brand():
    """Call this at the top of every page's sidebar block."""
    return """
<div style="
    background: rgba(0,0,0,0.18);
    border-radius: 10px;
    padding: 16px 14px 14px;
    margin: 0 0 14px 0;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.15);
">
  <div style="font-size:1.6rem; margin-bottom:4px;">📊</div>
  <div style="
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.03em;
    line-height: 1.2;
  ">Intelligent Sales</div>
  <div style="
    font-size: 0.7rem;
    color: rgba(255,255,255,0.65);
    font-weight: 400;
    margin-top: 2px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  ">Analytics Platform</div>
</div>
"""


def sidebar_data_options(df=None):
    """Renders the Data Options block for the sidebar."""
    active = f"`{len(df):,} rows × {len(df.columns)} cols`" if df is not None else "*No dataset loaded*"
    return f"""
<div style="
    background: rgba(0,0,0,0.15);
    border-radius: 8px;
    padding: 12px 14px;
    margin-top: 6px;
">
  <div style="
    font-size:0.7rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.08em;
    color:rgba(255,255,255,0.55);
    margin-bottom:8px;
  ">🗂️ Data Options</div>
  <div style="font-size:0.78rem;color:rgba(255,255,255,0.85);margin-bottom:6px;">
    <b>Active:</b> {active}
  </div>
</div>
"""


def hero(icon: str, title: str, subtitle: str) -> str:
    return f"""
<div class="hero-banner">
  <h1>{icon} {title}</h1>
  <p>{subtitle}</p>
</div>
"""


def kpi_card(label: str, value: str, sub: str = "") -> str:
    return f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-sub">{sub}</div>
</div>
"""


def info_box(text: str)    -> str: return f'<div class="info-box">ℹ️ {text}</div>'
def success_box(text: str) -> str: return f'<div class="success-box">✅ {text}</div>'
def warning_box(text: str) -> str: return f'<div class="warning-box">⚠️ {text}</div>'