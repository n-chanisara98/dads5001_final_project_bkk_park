import streamlit as st

st.set_page_config(
    page_title="BKK Park Finder - Home",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STYLE ONLY: ปรับเฉพาะหน้าตา/เลย์เอาต์ ไม่แตะ logic เชื่อมข้อมูลหน้าอื่น
# Color palette from reference image:
# #FBBA16 Yellow | #00492C Green | #9BCCDO Light Blue | #E22028 Red
# #E2B2B4 Pink | #1E4380 Blue | #B1D8B8 Mint | #B1D8B8 Orange/Red
# =========================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700;800&display=swap');

        :root {
            --yellow: #FBBA16;
            --green: #00492C;
            --blue-light: #9BCCDO;
            --red: #E22028;
            --pink: #E2B2B4;
            --blue: #1E4380;
            --mint: #B1D8B8;
            --orange: #B1D8B8;
            --cream: #FFF7E6;
            --ink: #17332A;
            --muted: #5E6F68;
            --card: rgba(255, 255, 255, 0.78);
            --line: rgba(0, 73, 44, 0.14);
        }

        html, body, [class*="css"]  {
            font-family: 'Noto Sans Thai', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(251, 186, 22, 0.28), transparent 28%),
                radial-gradient(circle at 75% 10%, rgba(155, 204, 208, 0.50), transparent 26%),
                linear-gradient(135deg, #FFF7E6 0%, #F7FBF2 42%, #EAF6EE 100%);
            color: var(--ink);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #00492C 0%, #17332A 100%);
            border-right: 1px solid rgba(255,255,255,0.10);
        }
        section[data-testid="stSidebar"] * {
            color: #FFF7E6 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            padding-top: 1.5rem;
        }

        .block-container {
            padding-top: 2.1rem;
            padding-bottom: 2.5rem;
            max-width: 1380px;
        }

        h1, h2, h3, h4 {
            color: var(--green);
            letter-spacing: -0.02em;
        }

        .hero {
            min-height: 420px;
            border-radius: 34px;
            padding: 46px 48px;
            background:
                linear-gradient(90deg, rgba(0,73,44,0.88) 0%, rgba(0,73,44,0.64) 44%, rgba(0,73,44,0.10) 100%),
                url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1800&q=85');
            background-size: cover;
            background-position: center;
            box-shadow: 0 26px 70px rgba(0, 73, 44, 0.24);
            position: relative;
            overflow: hidden;
        }
        .hero:after {
            content: "";
            position: absolute;
            inset: auto -80px -100px auto;
            width: 340px;
            height: 340px;
            border-radius: 50%;
            background: rgba(251, 186, 22, 0.50);
            filter: blur(8px);
        }
        .hero-kicker {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(251, 186, 22, 0.92);
            color: var(--green);
            font-weight: 800;
            font-size: 0.95rem;
            margin-bottom: 18px;
        }
        .hero-title {
            max-width: 850px;
            color: #FFF7E6;
            font-size: clamp(2.2rem, 5vw, 4.9rem);
            line-height: 1.04;
            font-weight: 900;
            margin: 0 0 14px 0;
        }
        .hero-title span { color: var(--yellow); }
        .hero-subtitle {
            max-width: 780px;
            color: rgba(255, 247, 230, 0.94);
            font-size: 1.22rem;
            line-height: 1.75;
            font-weight: 500;
            margin-bottom: 26px;
        }
        .hero-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            max-width: 900px;
        }
        .tag {
            padding: 9px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.25);
            color: #FFFFFF;
            font-weight: 700;
            backdrop-filter: blur(10px);
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 34px 0 16px 0;
        }
        .section-icon {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: grid;
            place-items: center;
            background: var(--yellow);
            color: var(--green);
            font-size: 1.35rem;
            box-shadow: 0 10px 24px rgba(251, 186, 22, 0.30);
        }
        .section-title h2 {
            margin: 0;
            font-size: 1.72rem;
            font-weight: 900;
        }
        .section-note {
            margin-top: -8px;
            color: var(--muted);
            font-size: 1.02rem;
        }

        .metric-card, .content-card, .page-card, .tech-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 16px 44px rgba(0, 73, 44, 0.10);
            backdrop-filter: blur(12px);
            height: 100%;
        }
        .metric-card {
            min-height: 175px;
            transition: transform .18s ease, box-shadow .18s ease;
        }
        .metric-card:hover, .page-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 22px 54px rgba(0, 73, 44, 0.16);
        }
        .metric-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 18px;
        }
        .metric-icon {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            display: grid;
            place-items: center;
            font-size: 1.45rem;
            background: #EAF6EE;
        }
        .metric-label {
            color: var(--muted);
            font-size: .96rem;
            font-weight: 800;
        }
        .metric-value {
            color: var(--green);
            font-size: 2.05rem;
            line-height: 1.05;
            font-weight: 900;
            margin-bottom: 8px;
        }
        .metric-delta {
            display: inline-block;
            padding: 6px 11px;
            border-radius: 999px;
            background: rgba(177, 216, 184, 0.48);
            color: var(--green);
            font-weight: 800;
            font-size: .86rem;
        }

        .quote-box {
            border-left: 8px solid var(--yellow);
            background: rgba(255,247,230,0.85);
            padding: 20px 22px;
            border-radius: 18px;
            color: var(--green);
            font-weight: 800;
            font-size: 1.18rem;
            margin-bottom: 18px;
        }
        .body-text {
            color: #2F463D;
            font-size: 1.04rem;
            line-height: 1.9;
        }

        .tech-card {
            display: flex;
            gap: 15px;
            align-items: flex-start;
            margin-bottom: 14px;
            padding: 18px 20px;
        }
        .tech-badge {
            min-width: 40px;
            height: 40px;
            border-radius: 13px;
            display: grid;
            place-items: center;
            font-size: 1.15rem;
            font-weight: 900;
        }
        .tech-title {
            font-weight: 900;
            color: var(--green);
            margin-bottom: 3px;
        }
        .tech-desc {
            color: var(--muted);
            font-size: .94rem;
            line-height: 1.6;
        }

        .page-card {
            border-top: 8px solid var(--green);
        }
        .page-no {
            display: inline-block;
            color: var(--green);
            background: rgba(251, 186, 22, 0.84);
            border-radius: 999px;
            padding: 7px 12px;
            font-weight: 900;
            font-size: .86rem;
            margin-bottom: 12px;
        }
        .page-title {
            color: var(--green);
            font-size: 1.25rem;
            line-height: 1.35;
            font-weight: 900;
            margin-bottom: 12px;
        }
        .page-desc {
            color: #415A50;
            line-height: 1.75;
            font-size: .98rem;
        }
        .page-chip {
            display: inline-block;
            margin-top: 16px;
            padding: 7px 11px;
            border-radius: 999px;
            font-size: .82rem;
            font-weight: 800;
            color: white;
            background: var(--blue);
        }

        .workflow {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        .step {
            background: rgba(255,255,255,0.70);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 20px;
            min-height: 140px;
        }
        .step-number {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            background: var(--green);
            color: var(--yellow);
            font-weight: 900;
            margin-bottom: 12px;
        }
        .step-title {
            color: var(--green);
            font-weight: 900;
            margin-bottom: 6px;
        }
        .step-desc {
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.55;
        }

        .footer {
            margin-top: 34px;
            padding: 18px 24px;
            border-radius: 22px;
            color: rgba(255,255,255,0.88);
            background: linear-gradient(90deg, #00492C 0%, #1E4380 100%);
            font-weight: 700;
        }

        div[data-testid="stHorizontalBlock"] { gap: 1.1rem; }

        @media (max-width: 900px) {
            .hero { padding: 34px 26px; min-height: 430px; }
            .workflow { grid-template-columns: 1fr; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# SIDEBAR BRANDING
# =========================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 24px 8px 26px 8px; text-align:center;">
            <div style="font-size:3rem; line-height:1;">🌳</div>
            <div style="font-size:1.55rem; font-weight:900; color:#FFF7E6; margin-top:10px; line-height:1.15;">
                BKK Green<br>Navigator
            </div>
            <div style="color:#B1D8B8; font-weight:700; margin-top:8px; font-size:.92rem;">
                Parks • Transit • Air Quality
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# HERO SECTION
# =========================
st.markdown(
    """
    <section class="hero">
        <div class="hero-kicker">🌿 Bangkok Urban Data Project</div>
        <h1 class="hero-title">BKK Urban <span>Green Spaces</span> & Connectivity</h1>
        <div class="hero-subtitle">
            ระบบบูรณาการข้อมูลพื้นที่สีเขียว โครงข่ายรถไฟฟ้า และคุณภาพอากาศ
            เพื่อช่วยให้คนกรุงเทพฯ เลือกสวนที่เหมาะกับการเดินทางและสุขภาพได้ง่ายขึ้น
        </div>
        <div class="hero-tags">
            <span class="tag">🍀 30+ Public Parks</span>
            <span class="tag">🚊 BTS & MRT Access</span>
            <span class="tag">😷 Real-time PM2.5</span>
            <span class="tag">🗺️ Spatial Analytics</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# =========================
# DATA ARCHITECTURE / KPI
# =========================
st.markdown(
    """
    <div class="section-title">
        <div class="section-icon">🛠️</div>
        <h2>Data Architecture</h2>
    </div>
    <div class="section-note">โปรเจกต์นี้เชื่อมโยง 3 แกนข้อมูลหลัก เพื่อเปลี่ยนข้อมูลเมืองให้เป็นเครื่องมือช่วยตัดสินใจ</div>
    """,
    unsafe_allow_html=True,
)

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-top">
                <div>
                    <div class="metric-label">สวนสาธารณะ · Snowflake</div>
                </div>
                <div class="metric-icon" style="background:#B1D8B8;">🍀</div>
            </div>
            <div class="metric-value">30+ สวน</div>
            <span class="metric-delta">↑ คัดกรองพิกัดจริง</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-top">
                <div>
                    <div class="metric-label">โครงข่ายรถไฟฟ้า · Snowflake</div>
                </div>
                <div class="metric-icon" style="background:#9BCCDO;">🚊</div>
            </div>
            <div class="metric-value">BTS & MRT</div>
            <span class="metric-delta">↑ คำนวณระยะทางเดินเท้า</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-top">
                <div>
                    <div class="metric-label">ดัชนีฝุ่น · MongoDB</div>
                </div>
                <div class="metric-icon" style="background:#E2B2B4;">😷</div>
            </div>
            <div class="metric-value">Real-time</div>
            <span class="metric-delta">↑ Air4Thai API ล่าสุด</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# PROBLEM / TECH STACK
# =========================
st.markdown(
    """
    <div class="section-title">
        <div class="section-icon">💡</div>
        <h2>Project Concept</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.05, 0.95])

with col_left:
    st.markdown(
        """
        <div class="content-card">
            <div class="quote-box">“จะออกไปวิ่งทั้งที ต้องเดินทางสะดวก และอากาศต้องปลอดภัย”</div>
            <div class="body-text">
                กรุงเทพฯ มีพื้นที่สีเขียวจำกัด และมักประสบปัญหาฝุ่น <b>PM2.5</b> บ่อยครั้ง
                แอปพลิเคชันนี้จึงออกแบบมาเพื่อรวมข้อมูลเชิงพื้นที่ การเดินทาง และคุณภาพอากาศไว้ในที่เดียว
                เพื่อให้ผู้ใช้งานค้นหาสถานที่ออกกำลังกายหรือพักผ่อนที่เหมาะกับชีวิตประจำวันได้จริง
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown(
        """
        <div class="tech-card">
            <div class="tech-badge" style="background:#B1D8B8; color:#00492C;">S</div>
            <div>
                <div class="tech-title">Snowflake</div>
                <div class="tech-desc">จัดเก็บข้อมูลโครงสร้างหลักของสวนสาธารณะและสถานีรถไฟฟ้า</div>
            </div>
        </div>
        <div class="tech-card">
            <div class="tech-badge" style="background:#FBBA16; color:#00492C;">M</div>
            <div>
                <div class="tech-title">MongoDB</div>
                <div class="tech-desc">จัดเก็บข้อมูลฝุ่นดิบรูปแบบ JSON ที่ดึงมาจาก API เพื่อใช้งานแบบล่าสุด</div>
            </div>
        </div>
        <div class="tech-card">
            <div class="tech-badge" style="background:#9BCCDO; color:#1E4380;">Py</div>
            <div>
                <div class="tech-title">Pandas & Scipy</div>
                <div class="tech-desc">คำนวณระยะห่างทางภูมิศาสตร์ระหว่างสวน สถานีรถไฟฟ้า และจุดตรวจวัดอากาศ</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# USER FLOW
# =========================
st.markdown(
    """
    <div class="section-title">
        <div class="section-icon">🧭</div>
        <h2>How Users Read This Dashboard</h2>
    </div>
    <div class="workflow">
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-title">ดูภาพรวมสวน</div>
            <div class="step-desc">เข้าใจจำนวนสวน ขนาดพื้นที่ และความพร้อมของสิ่งอำนวยความสะดวก</div>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-title">เลือกสวนบนแผนที่</div>
            <div class="step-desc">ค้นหาสวนที่ต้องการตามขนาด พื้นที่ และตำแหน่งที่เดินทางสะดวก</div>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-title">เช็กคุณภาพอากาศ</div>
            <div class="step-desc">ดูค่าฝุ่นจากสถานีตรวจวัดที่ใกล้ที่สุดก่อนออกจากบ้าน</div>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <div class="step-title">วิเคราะห์การเชื่อมต่อ</div>
            <div class="step-desc">เปรียบเทียบระยะห่างสวนกับสถานีรถไฟฟ้า เพื่อประเมินการเข้าถึงพื้นที่สีเขียว</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# APP DIRECTORY
# =========================
st.markdown(
    """
    <div class="section-title">
        <div class="section-icon">🖥️</div>
        <h2>App Directory</h2>
    </div>
    <div class="section-note">เลือกหน้าใช้งานตามคำถามที่ต้องการตอบจากข้อมูล</div>
    """,
    unsafe_allow_html=True,
)

page_col1, page_col2, page_col3 = st.columns(3)

with page_col1:
    st.markdown(
        """
        <div class="page-card">
            <span class="page-no">PAGE 01</span>
            <div class="page-title">🏠 Overview & Park Analytics</div>
            <div class="page-desc">
                วิเคราะห์ภาพรวมขนาดพื้นที่สีเขียวรวมรายเขต พฤติกรรมการใช้งาน
                และความพร้อมเชิงสันทนาการของสวนสาธารณะ
            </div>
            <span class="page-chip">Park Overview</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with page_col2:
    st.markdown(
        """
        <div class="page-card" style="border-top-color:#FBBA16;">
            <span class="page-no">PAGE 02</span>
            <div class="page-title">🔍 Park Finder & Air Quality</div>
            <div class="page-desc">
                ระบบ Map-Based สำหรับค้นหาสวน คัดกรองขนาดพื้นที่
                และจับคู่สถานีตรวจฝุ่นที่อยู่ใกล้ที่สุดโดยอัตโนมัติ
            </div>
            <span class="page-chip" style="background:#E22028;">Air Quality</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with page_col3:
    st.markdown(
        """
        <div class="page-card" style="border-top-color:#1E4380;">
            <span class="page-no">PAGE 03</span>
            <div class="page-title">📊 Analytics & Connectivity</div>
            <div class="page-desc">
                วิเคราะห์ความสัมพันธ์เชิงสถิติระหว่างขนาดสวนกับระยะห่างสถานีรถไฟฟ้า
                พร้อมดูสัดส่วนการเข้าถึงระบบราง
            </div>
            <span class="page-chip" style="background:#00492C;">Connectivity</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="footer">
        DADS 5001 - Data Analytics and Data Science Tools and Programming Project | 2026<br>
        Designed for BKK Park Finder: Urban Green Space, Transit Connectivity & Air Quality Monitoring
    </div>
    """,
    unsafe_allow_html=True,
)
