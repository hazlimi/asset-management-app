"""Aviation Asset Management Portal — Azure App Service / Streamlit.

Keep reports.json alongside this file. Edit only its embed_url fields to
connect additional reports. No external frontend assets or paid components.
"""

import html
import base64
import json
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Asset Management Dashboard Portal",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CONFIG_FILE = Path(__file__).with_name("reports.json")
try:
    reports = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    if not isinstance(reports, list):
        raise ValueError("reports.json must contain a JSON list")
    reports = [r for r in reports if isinstance(r, dict) and r.get("name")]
except (OSError, json.JSONDecodeError, ValueError) as exc:
    st.error(f"Unable to read reports.json: {exc}")
    st.stop()

REPORT_TYPES = {
    "shipment": ("LOGISTICS", "🚚", "#0ea5e9"),
    "aog": ("PRIORITY ORDERS", "✈️", "#3b82f6"),
    "oss": ("INVENTORY", "📦", "#14b8a6"),
    "oem": ("SUPPLIER PERFORMANCE", "📈", "#8b5cf6"),
    "cabin": ("CABIN OPERATIONS", "🛠️", "#f59e0b"),
    "repair": ("REPAIR OPERATIONS", "🔧", "#ef7188"),
}


def meta(name):
    for term, data in REPORT_TYPES.items():
        if term in name.lower():
            return data
    return ("OPERATIONS", "📊", "#3b82f6")


def valid_embed(url):
    if not url:
        return False
    parsed = urlparse(url)
    return (
        parsed.scheme == "https"
        and parsed.hostname == "app.powerbi.com"
        and parsed.path.rstrip("/") == "/reportEmbed"
    )


def navigate(page):
    st.session_state["selected_page"] = page


def safe(value):
    return html.escape(str(value), quote=True)


connected = sum(bool(r.get("embed_url", "").strip()) for r in reports)
pending = len(reports) - connected
pages = ["Home"] + [r["name"] for r in reports]
if st.session_state.get("selected_page") not in pages:
    st.session_state["selected_page"] = "Home"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root { --navy:#0b1d36; --ink:#11243f; --muted:#62748b; --line:#e2eaf4; --blue:#2563eb; }
html,body,.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family:'DM Sans',Arial,sans-serif!important;
    background-color:#f5f8fc!important;
    color:var(--ink)!important;
}
[data-testid="stMain"] .block-container {
    padding:2rem 2.5rem 3.5rem;
    max-width:1540px;
}
[data-testid="stMain"] h1,[data-testid="stMain"] h2,
[data-testid="stMain"] h3 { color:var(--ink)!important; }
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0d2441 0%,#07172b 100%)!important;
    border-right:1px solid #173656;
    min-width:278px;
}
[data-testid="stSidebar"] .block-container {padding-top:1.5rem!important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color:#d7e5f6!important;
}
[data-testid="stSidebar"] [role="radiogroup"] {gap:.25rem;}
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding:.72rem .8rem!important;
    border-radius:11px!important;
    transition:background .18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#1a3a5b!important;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background:#1f4674!important;
    box-shadow:inset 3px 0 0 #5db5ff;
}
[data-testid="stSidebar"] [role="radiogroup"] label p {
    color:#e9f3ff!important;font-size:0.87rem;font-weight:600;
}
[data-testid="stSidebar"] [role="radiogroup"] [data-testid="stWidgetLabel"] {display:none;}
[data-testid="stSidebar"] hr {border-color:#2a4460;}
[data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color:#e3ebf6;
    background:#ffffff;
    border-radius:18px;
    box-shadow:0 9px 28px rgba(24,56,93,.045);
}
[data-testid="stMain"] .stButton button {
    border-radius:10px;
    border:1px solid #dae5f4;
    background:#eef5ff;
    color:#1854a7;
    font-weight:700;
    transition:all .2s ease;
}
[data-testid="stMain"] .stButton button:hover {
    background:#dfeeff;color:#0e417f;border-color:#aecfff;
}
[data-testid="stMain"] [data-testid="stLinkButton"] a {
    border-radius:10px!important;
    background:#1d5fc8!important;
    color:white!important;
    border:none!important;
}
[data-testid="stMain"] [data-testid="stTextInput"] input {
    color:#14304f!important;background:white!important;
    border-color:#dce7f3!important;border-radius:12px!important;
}
.brand{display:flex;flex-direction:column;align-items:center;justify-content:center;
    gap:7px;padding:9px 2px 21px;text-align:center;}
.brand-logo{display:block;width:100%;max-width:226px;height:auto;object-fit:contain;}
.brand-fallback{color:#fff;font-size:18px;font-weight:800;line-height:1.2;}
.brand small{display:block;color:#9dbad3;letter-spacing:1.7px;font-size:10px;margin-top:3px;}
.side-section{color:#7898b5;font-size:10px;letter-spacing:2.2px;font-weight:800;margin:14px 0 9px;}
.side-foot{border-top:1px solid #2a4460;margin-top:30px;padding-top:18px;color:#9db7d1;font-size:11px;line-height:1.8;}
.side-pulse{display:inline-block;width:7px;height:7px;border-radius:50%;background:#43ceb1;margin-right:7px;}
.eyebrow {font-size:11px;letter-spacing:2.1px;font-weight:800;color:#50769f;text-transform:uppercase;}
.topline{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px;}
.topbadge{display:inline-flex;align-items:center;gap:7px;padding:8px 12px;border-radius:30px;
    color:#2e668e;background:#e8f1fb;border:1px solid #d2e4f7;font-size:11px;font-weight:800;}
.hero{position:relative;overflow:hidden;display:flex;align-items:center;min-height:245px;
    border-radius:22px;padding:38px 42px;background:linear-gradient(115deg,#0b2748 2%,#144679 60%,#2169a4 100%);
    box-shadow:0 20px 38px rgba(22,62,106,.14);}
.hero:before{content:"";position:absolute;width:460px;height:460px;border:1px solid rgba(255,255,255,.09);
    border-radius:50%;right:-90px;top:-190px;box-shadow:0 0 0 62px rgba(255,255,255,.03),0 0 0 124px rgba(255,255,255,.025);}
.hero:after{content:"";position:absolute;right:19%;top:-40px;width:230px;height:350px;
    background:linear-gradient(130deg,transparent 5%,rgba(255,255,255,.06) 50%,transparent 85%);transform:rotate(25deg);}
.hero-text{position:relative;z-index:2;max-width:650px;}
.hero-chip{display:inline-block;color:#bfe5ff;font-size:10px;font-weight:800;letter-spacing:1.55px;
    background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.21);
    border-radius:50px;padding:8px 12px;margin-bottom:15px;}
.hero h1{font-size:clamp(30px,3vw,43px)!important;font-weight:800;line-height:1.14;letter-spacing:-1.6px;
    color:white!important;margin:0 0 12px!important;}
.hero h1 em{font-style:normal;color:#90d7ff;}
.hero p{max-width:480px;color:#d7eaff!important;margin:0;font-size:14px;line-height:1.7;}
.hero-mark{position:absolute;right:10%;top:65px;color:rgba(207,238,255,.65);font-size:88px;
    transform:rotate(-23deg);text-shadow:0 15px 40px rgba(0,0,0,.12);z-index:1;}
.hero-coordinate{position:absolute;right:33px;bottom:26px;color:#b3dbfa;
    font-size:10px;letter-spacing:2px;z-index:1;}
.stat{background:#fff;padding:23px 24px;border:1px solid var(--line);border-radius:16px;
    box-shadow:0 7px 22px rgba(20,55,92,.035);min-height:109px;}
.stat-head{display:flex;align-items:center;justify-content:space-between;font-size:11px;font-weight:800;
    text-transform:uppercase;letter-spacing:.7px;color:#74869e;margin-bottom:12px;}
.stat-icon{font-size:20px;}
.stat-value{font-size:31px;line-height:1;font-weight:800;color:#172d4c;letter-spacing:-1px;}
.stat-note{font-size:11px;color:#7690a9;margin-top:6px;}
.section-title{display:flex;align-items:center;justify-content:space-between;margin:10px 0 3px;gap:10px;}
.section-title h2{font-size:21px!important;letter-spacing:-.5px;margin:0!important;}
.section-title p{font-size:12px;color:#7b8ca1;margin:4px 0 0;}
.section-count{background:#e5eef9;border-radius:30px;padding:6px 11px;color:#2c6ca3;
    font-size:11px;font-weight:800;}
.report-intro{min-height:155px;}
.report-top{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:17px;}
.report-icon{width:48px;height:48px;border-radius:13px;display:flex;align-items:center;justify-content:center;
    background:#ecf4ff;font-size:23px;}
.report-category{font-size:10px;color:#7b8da2;letter-spacing:1.15px;font-weight:800;margin-bottom:6px;}
.report-name{font-size:16px;font-weight:800;color:#18304f;margin:0 0 7px;}
.report-description{min-height:40px;font-size:12px;line-height:1.6;color:#6c7f95;margin:0 0 14px;}
.pill{display:inline-flex;align-items:center;gap:7px;border-radius:50px;padding:6px 9px;font-weight:800;font-size:10px;}
.pill.ready{background:#e5f8f1;color:#0e8664;}
.pill.waiting{background:#f0f4f8;color:#72859a;}
.pill-dot{height:6px;width:6px;border-radius:50%;background:currentColor;}
.detail-head{background:white;border:1px solid #e3ebf6;border-radius:17px;
    padding:23px 27px;margin:4px 0 17px;}
.detail-head h1{margin:7px 0 6px!important;font-size:31px!important;letter-spacing:-.8px;}
.detail-head p{color:#6a7d91;font-size:13px;margin:0;}
.viewbar{background:#eaf3ff;border:1px solid #d2e6ff;border-radius:12px;
    padding:12px 16px;color:#2d6399;font-size:12px;margin:8px 0 16px;}
.viewbar strong{color:#16466c;}
.blank-state{text-align:center;padding:58px 12px 38px;}
.blank-icon{font-size:37px;margin-bottom:13px;}
.blank-state h3{font-size:20px!important;}
.blank-state p{color:#73859a;max-width:500px;margin:0 auto 10px;line-height:1.8;}
.portal-footer{border-top:1px solid #e2eaf3;margin-top:29px;padding-top:17px;
    color:#8092a9;font-size:11px;display:flex;justify-content:space-between;gap:12px;}
@media(max-width:1000px){.hero{padding:27px;min-height:220px}.hero-mark{right:4%;opacity:.3}.hero h1{font-size:30px!important}}
@media(max-width:700px){[data-testid="stMain"] .block-container{padding:1.15rem .8rem 2rem;}
  .hero{padding:26px 22px}.hero-mark{display:none}.hero h1{font-size:27px!important}
  .topbadge{display:none}.portal-footer{display:block}}
</style>
""",
    unsafe_allow_html=True,
)

# Embed the uploaded Asset Management logo into the Streamlit sidebar.
# Keep logo_sidebar.png alongside app.py in the Azure deployment folder.
LOGO_FILE = Path(__file__).with_name("logo_sidebar.png")
if LOGO_FILE.is_file():
    logo_encoded = base64.b64encode(LOGO_FILE.read_bytes()).decode("ascii")
    brand_image_html = (
        f'<img class="brand-logo" '
        f'src="data:image/png;base64,{logo_encoded}" '
        'alt="Asset Management logo">'
    )
else:
    brand_image_html = '<div class="brand-fallback">ASSET MANAGEMENT</div>'

with st.sidebar:
    st.markdown(
        f'<div class="brand">{brand_image_html}'
        '<small>AVIATION INTELLIGENCE</small></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-section">WORKSPACE</div>', unsafe_allow_html=True)

    def nav_label(page):
        if page == "Home":
            return "⌂  Overview"
        return f'{meta(page)[1]}  {page}'

    st.radio(
        "Navigation",
        pages,
        key="selected_page",
        label_visibility="collapsed",
        format_func=nav_label,
    )
    st.markdown(
        '<div class="side-foot"><span class="side-pulse"></span>'
        'Internal reporting portal<br>Azure App Service + Power BI<br>'
        'Access controlled by your organization</div>',
        unsafe_allow_html=True,
    )

selected = st.session_state["selected_page"]

if selected == "Home":
    st.markdown(
        '<div class="topline"><div class="eyebrow">Asset Management / Reporting Hub</div>'
        '<span class="topbadge">🔒 &nbsp; INTERNAL OPERATIONS PORTAL</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<section class="hero"><div class="hero-text">'
        '<span class="hero-chip">✦ &nbsp; AVIATION OPERATIONS COMMAND CENTER</span>'
        '<h1>Every operational insight.<br><em>One connected workspace.</em></h1>'
        '<p>Explore purchasing, inventory, supplier performance, cabin defects, repairs, '
        'and shipment priorities — without switching between reporting sites.</p>'
        '</div><div class="hero-mark">✈</div>'
        '<div class="hero-coordinate">OPERATIONS  /  ANALYTICS  /  INSIGHTS</div></section>',
        unsafe_allow_html=True,
    )
    st.write("")
    metric_cols = st.columns(3, gap="medium")
    metric_data = [
        ("Dashboards", str(len(reports)), "Sections in this portal", "▦"),
        ("Links configured", str(connected), "Power BI embed URLs added", "↗"),
        ("Pending setup", str(pending), "Awaiting secure embed links", "◷"),
    ]
    for col, (label, value, detail, icon) in zip(metric_cols, metric_data):
        with col:
            st.markdown(
                f'<div class="stat"><div class="stat-head"><span>{safe(label)}</span>'
                f'<span class="stat-icon">{icon}</span></div>'
                f'<div class="stat-value">{value}</div>'
                f'<div class="stat-note">{safe(detail)}</div></div>',
                unsafe_allow_html=True,
            )
    st.write("")
    st.markdown(
        f'<div class="section-title"><div><h2>Explore dashboards</h2>'
        '<p>Select any dashboard to explore its embedded report or setup information.</p>'
        f'</div><span class="section-count">{len(reports)} REPORTS</span></div>',
        unsafe_allow_html=True,
    )
    search = st.text_input(
        "Search dashboards",
        placeholder="🔎  Search dashboards — e.g. AOG, shipment, OSS...",
        label_visibility="collapsed",
    )
    filtered = [
        r for r in reports
        if search.strip().lower() in (
            r.get("name", "") + " " + r.get("description", "")
        ).lower()
    ]
    if not filtered:
        st.info("No dashboard matches your search. Try a different keyword.")

    for i in range(0, len(filtered), 3):
        cols = st.columns(3, gap="medium")
        for col, r in zip(cols, filtered[i:i + 3]):
            with col:
                with st.container(border=True):
                    name = r["name"]
                    category, icon, _color = meta(name)
                    configured = bool(r.get("embed_url", "").strip())
                    badge = (
                        '<span class="pill ready"><span class="pill-dot"></span> LINK CONFIGURED</span>'
                        if configured else
                        '<span class="pill waiting"><span class="pill-dot"></span> NOT CONFIGURED</span>'
                    )
                    st.markdown(
                        '<div class="report-intro">'
                        f'<div class="report-top"><div class="report-icon">{icon}</div>{badge}</div>'
                        f'<div class="report-category">{safe(category)}</div>'
                        f'<div class="report-name">{safe(name)}</div>'
                        f'<p class="report-description">{safe(r.get("description", ""))}</p>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                    st.button(
                        "Open dashboard  →" if configured else "View setup  →",
                        key=f"report_{safe(name)}",
                        use_container_width=True,
                        on_click=navigate,
                        args=(name,),
                    )
else:
    report = next(r for r in reports if r["name"] == selected)
    category, icon, _color = meta(selected)
    url = report.get("embed_url", "").strip()
    st.markdown(
        '<div class="topline"><div class="eyebrow">Asset Management / Dashboard Viewer</div>'
        '<span class="topbadge">🔒 &nbsp; POWER BI SECURE EMBED</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="detail-head">'
        f'<div class="eyebrow">{icon} &nbsp; {safe(category)}</div>'
        f'<h1>{safe(selected)}</h1>'
        f'<p>{safe(report.get("description", ""))}</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([1, 4], gap="small")
    with left:
        st.button("← All dashboards", on_click=navigate, args=("Home",),
                  use_container_width=True)
    if not url:
        st.markdown(
            '<div class="blank-state"><div class="blank-icon">📎</div>'
            '<h3>This dashboard is ready for its embed link</h3>'
            '<p>Publish the report to Power BI Service, copy its secure '
            '<b>Website or portal</b> embed URL, add it to the matching '
            '<code>embed_url</code> in <code>reports.json</code>, then redeploy the App.</p></div>',
            unsafe_allow_html=True,
        )
    elif not valid_embed(url):
        st.error(
            "The embed URL is invalid. Use the Power BI Service secure 'Website or portal' "
            "link beginning with https://app.powerbi.com/reportEmbed"
        )
    else:
        with right:
            st.link_button("↗ Open directly in Power BI", url)
        st.markdown(
            '<div class="viewbar"><strong>Report viewer:</strong> '
            'This dashboard is embedded from Power BI Service. '
            'Your Power BI permissions and licence still apply.</div>',
            unsafe_allow_html=True,
        )
        view_height = st.select_slider(
            "Report viewing height",
            options=[650, 800, 950, 1150],
            value=650,
            format_func=lambda h: f"{h}px",
        )
        components.iframe(src=url, height=view_height, scrolling=True)
        st.caption(
            "If Microsoft authentication is blocked inside the embedded window, "
            "use 'Open directly in Power BI'. The app does not bypass Power BI security."
        )

st.markdown(
    '<div class="portal-footer"><span>© Asset Management · Operations Reporting Hub</span>'
    '<span>Powered by Azure App Service + Microsoft Power BI</span></div>',
    unsafe_allow_html=True,
)
