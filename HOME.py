import streamlit as st

st.set_page_config(
    page_title="BKK Park Finder - Home",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLE ONLY: Dashboard Template แบบภาพตัวอย่าง
# - ไม่แก้ logic / data connection
# - ปรับเฉพาะ Layout, CSS, Card, Sidebar, Metric UI
# ============================================================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Noto Sans Thai', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #0b3d3a 0%, #0f6b5c 42%, #0b355f 100%);
        }

        .block-container {
            padding-top: 1.3rem;
            padding-bottom: 1.6rem;
            max-width: 1280px;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #073b4c 0%, #072f41 58%, #052330 100%);
            border-right: 1px solid rgba(255,255,255,0.12);
        }

        section[data-testid="stSidebar"] * {
            color: #ecfeff !important;
        }

        .dashboard-shell {
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 28px;
            padding: 22px;
            box-shadow: 0 22px 70px rgba(0,0,0,0.28);
            backdrop-filter: blur(14px);
        }

        .hero-card {
            background: linear-gradient(135deg, rgba(6,182,212,0.95), rgba(34,197,94,0.92));
            border-radius: 24px;
            padding: 26px 28px;
            color: white;
            box-shadow: 0 18px 40px rgba(0,0,0,0.22);
            min-height: 170px;
        }

        .hero-card h1 {
            font-size: 2.35rem;
            line-height: 1.15;
            margin: 0 0 10px 0;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .hero-card p {
            margin: 0;
            font-size: 1.02rem;
            opacity: 0.93;
        }

        .mini-card {
            background: linear-gradient(145deg, rgba(20,184,166,0.95), rgba(14,116,144,0.94));
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 20px;
            padding: 18px 18px;
            min-height: 118px;
            color: white;
            box-shadow: 0 12px 28px rgba(0,0,0,0.20);
        }

        .mini-label {
            font-size: 0.82rem;
            font-weight: 700;
            opacity: 0.86;
            margin-bottom: 8px;
        }

        .mini-value {
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1;
        }

        .mini-delta {
            margin-top: 8px;
            font-size: 0.78rem;
            opacity: 0.90;
        }

        .glass-card {
            background: rgba(255,255,255,0.94);
            border-radius: 22px;
            padding: 22px 24px;
            border: 1px solid rgba(255,255,255,0.72);
            box-shadow: 0 16px 40px rgba(8,47,73,0.20);
            min-height: 100%;
        }

        .glass-card h3, .glass-card h4 {
            color: #073b4c;
            margin-top: 0;
            font-weight: 800;
        }

        .glass-card p, .glass-card li {
            color: #244154;
            font-size: 0.96rem;
        }

        .section-title {
            color: white;
            font-size: 1.12rem;
            font-weight: 800;
            margin: 18px 0 12px 2px;
        }

        .tech-pill {
            display: block;
            padding: 13px 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            color: #0f172a;
            font-weight: 600;
            border: 1px solid rgba(15,23,42,0.08);
        }

        .pill-green { background: #dcfce7; }
        .pill-yellow { background: #fef3c7; }
        .pill-blue { background: #dbeafe; }

        .page-card {
            background: rgba(255,255,255,0.95);
            border-radius: 21px;
            padding: 22px;
            border: 1px solid rgba(255,255,255,0.70);
            min-height: 210px;
            box-shadow: 0 14px 34px rgba(8,47,73,0.18);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .page-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 44px rgba(8,47,73,0.24);
        }

        .page-icon {
            width: 48px;
            height: 48px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #06b6d4, #22c55e);
            color: white;
            font-size: 1.45rem;
            margin-bottom: 14px;
        }

        .footer-text {
            color: rgba(255,255,255,0.72);
            text-align: center;
            font-size: 0.86rem;
            padding-top: 12px;
        }

        div[data-testid="stMetric"] {
            background: transparent;
        }

        div[data-testid="stMarkdownContainer"] > hr {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### 🌲 BKK Park Finder")
    st.caption("Urban Green Dashboard")
    st.markdown("---")
    st.markdown("🏠 **Dashboard**")
    st.markdown("🍀 **Overview & Park Analytics**")
    st.markdown("🔍 **Park Finder & Air Quality**")
    st.markdown("📊 **Analytics & Connectivity**")
    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("Snowflake · MongoDB · Air4Thai API")

# ---------------- Main Dashboard ----------------
st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)

# Header + Top Metrics
hero_col, kpi_col1, kpi_col2, kpi_col3 = st.columns([2.25, 1, 1, 1], gap="medium")

with hero_col:
    st.markdown(
        """
        <div class="hero-card">
            <h1>🌲 BKK Urban Green Spaces & Connectivity</h1>
            <p>ระบบบูรณาการฐานข้อมูลพื้นที่สีเขียว โครงข่ายรถไฟฟ้า และดัชนีคุณภาพอากาศกรุงเทพมหานคร</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col1:
    st.markdown(
        """
        <div class="mini-card">
            <div class="mini-label">🍀 สวนสาธารณะ</div>
            <div class="mini-value">30+</div>
            <div class="mini-delta">Snowflake · คัดกรองพิกัดจริง</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col2:
    st.markdown(
        """
        <div class="mini-card">
            <div class="mini-label">🚊 โครงข่ายรถไฟฟ้า</div>
            <div class="mini-value">BTS & MRT</div>
            <div class="mini-delta">คำนวณระยะทางเดินเท้า</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col3:
    st.markdown(
        """
        <div class="mini-card">
            <div class="mini-label">😷 ดัชนีฝุ่น</div>
            <div class="mini-value">Real-time</div>
            <div class="mini-delta">MongoDB · Air4Thai API ล่าสุด</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">🛠️ Data Architecture</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="glass-card">
        <p style="margin-bottom:0; font-weight:600; color:#0f172a;">
        โปรเจกต์นี้เกิดจากการเชื่อมโยง 3 แหล่งข้อมูลเพื่อตอบโจทย์คนเมือง และนำเสนอในรูปแบบ Dashboard ที่อ่านง่าย ใช้งานได้จริง และเหมาะกับการวิเคราะห์เชิงพื้นที่
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">❓ Why This App?</div>', unsafe_allow_html=True)
col_left, col_right = st.columns([5, 4], gap="medium")

with col_left:
    st.markdown(
        """
        <div class="glass-card">
            <h3>ออกไปวิ่งทั้งที ต้องเดินทางสะดวกและอากาศต้องปลอดภัย</h3>
            <p>
            กรุงเทพฯ มีพื้นที่สีเขียวจำกัด และมักประสบปัญหาฝุ่น <b>PM2.5</b> บ่อยครั้ง แอปพลิเคชันนี้จึงออกแบบมาเพื่อรวมข้อมูลเชิงพื้นที่ การเดินทาง และคุณภาพอากาศไว้ในที่เดียว เพื่อให้ทุกคนสามารถค้นหาสถานที่ออกกำลังกายที่ตอบโจทย์ชีวิตประจำวันได้จริง
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown(
        """
        <div class="glass-card">
            <h3>🗂️ เทคโนโลยีที่เลือกใช้</h3>
            <span class="tech-pill pill-green"><b>Snowflake</b>: จัดเก็บข้อมูลโครงสร้างหลักของสวนและสถานีรถไฟฟ้า</span>
            <span class="tech-pill pill-yellow"><b>MongoDB</b>: จัดเก็บข้อมูลฝุ่นดิบรูปแบบ JSON ที่ดึงมาจาก API</span>
            <span class="tech-pill pill-blue"><b>Pandas & Scipy</b>: คำนวณระยะห่างทางภูมิศาสตร์ระหว่างจุดต่อจุด</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">🖥️ App Directory</div>', unsafe_allow_html=True)
page_col1, page_col2, page_col3 = st.columns(3, gap="medium")

with page_col1:
    st.markdown(
        """
        <div class="page-card">
            <div class="page-icon">🏠</div>
            <h4>Page 1: Overview & Park Analytics</h4>
            <p>วิเคราะห์ภาพรวมขนาดพื้นที่สีเขียวรวมรายเขต พฤติกรรมการใช้งาน และความพร้อมเชิงสันทนาการ (Amenities)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with page_col2:
    st.markdown(
        """
        <div class="page-card">
            <div class="page-icon">🔍</div>
            <h4>Page 2: Park Finder & Air Quality</h4>
            <p>ระบบ Map-Based ค้นหาสวน คัดกรองขนาดพื้นที่ และจับคู่สถานีตรวจฝุ่นที่อยู่ใกล้ที่สุดโดยอัตโนมัติ เพื่อเช็กสภาพอากาศก่อนออกจากบ้าน</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with page_col3:
    st.markdown(
        """
        <div class="page-card">
            <div class="page-icon">📊</div>
            <h4>Page 3: Analytics & Connectivity</h4>
            <p>วิเคราะห์ความสัมพันธ์เชิงสถิติระหว่างขนาดสวนกับระยะห่างสถานีรถไฟฟ้า พร้อม Pie Chart ดูสัดส่วนการเข้าถึงระบบราง</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="footer-text">DADS 5001 - Data Analytics and Data Science Tools and Programming Project | 2026</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
