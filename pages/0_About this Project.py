import streamlit as st

def render_about_this_project():
    # ============================================================
    # 1. STYLE CONFIGURATION (ธีมสีสดใส สวนธรรมชาติ + Flavour United)
    # ============================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', 'Noto Sans Thai', sans-serif; }
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(251,186,22,.25), transparent 30%),
            radial-gradient(circle at top right, rgba(155,204,208,.42), transparent 32%),
            linear-gradient(135deg, #FFF8E9 0%, #F8FBF1 45%, #EAF7EF 100%);
    }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px; }

    .hero-wrap {
        position: relative;
        overflow: hidden;
        border-radius: 34px;
        min-height: 280px;
        padding: 42px 48px;
        background:
            linear-gradient(90deg, rgba(0,73,44,.94) 0%, rgba(0,73,44,.74) 42%, rgba(0,73,44,.12) 100%),
            url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=2200&q=85');
        background-size: cover;
        background-position: center;
        box-shadow: 0 26px 80px rgba(0,73,44,.22);
        border: 1px solid rgba(255,255,255,.40);
        margin-bottom: 25px;
    }
    .hero-kicker {
        display: inline-flex;
        padding: 9px 15px;
        background: #FBBA16;
        color: #00492C;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: .04em;
        text-transform: uppercase;
    }
    .hero-title {
        margin-top: 18px;
        max-width: 850px;
        color: #FFF8E9;
        font-size: clamp(38px, 4.5vw, 64px);
        line-height: .98;
        font-weight: 950;
        letter-spacing: -2px;
    }
    
    .section-title { margin: 35px 0 8px 0; color: #00492C; font-size: 28px; font-weight: 950; letter-spacing: -.4px; }
    
    /* Content Elements mapped with Home Theme classes */
    .insight-box {
        background: linear-gradient(135deg, rgba(251,186,22,.20), rgba(177,216,184,.45));
        border: 1px solid rgba(0,73,44,.14);
        border-radius: 26px;
        padding: 24px 28px;
        box-shadow: 0 14px 44px rgba(0,73,44,.05);
        color: #17342A;
        font-size: 15.5px;
        line-height: 1.8;
        margin-bottom: 20px;
    }
    .chart-card {
        background: rgba(255,255,255,.84);
        border: 1px solid rgba(0,73,44,.10);
        border-radius: 28px;
        padding: 26px 28px;
        box-shadow: 0 18px 54px rgba(0,73,44,.07);
        margin-bottom: 22px;
    }
    .chart-title { color:#00492C; font-size: 20px; font-weight: 950; margin-bottom: 12px; }

    .story-card { border-radius: 26px; padding: 24px; background: #00492C; color: #FFF8E9; min-height: 150px; box-shadow: 0 14px 40px rgba(0,73,44,.10); margin-bottom: 15px; }
    .story-card.yellow { background:#FBBA16; color:#00492C; }
    .story-card.aqua { background:#9BCCD0; color:#00492C; }
    
    .story-card h4 { margin: 0 0 8px 0; font-size: 19px; font-weight: 950; }
    .story-card p { margin: 0; line-height: 1.6; font-weight: 650; }
    
    ul.bullet-list { padding-left: 20px; margin-top: 8px; }
    ul.bullet-list li { margin-bottom: 8px; font-weight: 650; color: #17342A; }
    
    hr { margin: 2rem 0; border: none; height: 1px; background: rgba(0,73,44,.14); }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================
    # 2. HERO COMPONENT
    # ============================================================
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-kicker">ℹ️ Project Overview & Documentation</div>
        <div class="hero-title">About This Project</div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # 3. ISSUES & MOTIVATION
    # ============================================================
    st.markdown('<div class="section-title">Issues & Motivation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
        แรงบันดาลใจจากการเติบโตของเทรนด์รักสุขภาพ ท่ามกลางข้อจำกัดของคนเมืองกรุง
    </div>
    """, unsafe_allow_html=True)

    col_issue1, col_issue2 = st.columns(2)
    
    with col_issue1:
        st.markdown("""
        <div class="story-card">
            <h4>1) สวนหลักหนาแน่นมาก</h4>
            <p>แต่ยังมีพื้นที่สีเขียวทางเลือกอีกหลายแห่งกระจายอยู่ทั่วกรุงเทพฯ ที่ประชาชนยังเข้าไม่ถึงหรือยังไม่รู้จัก</p>
        </div>
        """, unsafe_allow_html=True)

    with col_issue2:
        st.markdown("""
        <div class="story-card yellow">
            <h4>2) การใช้สวนของคนเมืองขับเคลื่อนด้วย 3 ปัจจัยหลัก ได้แก่</h4>
            <ul class="bullet-list" style="color: #00492C;">
                <li>Amenities (สิ่งอำนวยความสะดวก)</li>
                <li>Connectivity (ความสะดวกในการเชื่อมต่อ BTS/MRT)</li>
                <li>Health Safety (ความปลอดภัยจากฝุ่น PM2.5)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # 4. OBJECTIVE
    # ============================================================
    st.markdown('<div class="section-title">Objective</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-card">
        <p style="font-size: 16px; line-height: 1.8; color: #17342A; font-weight: 650; margin: 0;">
        วัตถุประสงค์ของโปรเจกต์ จึงเป็นการสร้างระบบค้นหาและคัดกรองสวนสาธารณะในกรุงเทพฯ หรือ Interactive Park Finder ขึ้นมา
        เพื่อเป็นเครื่องมือให้ผู้ใช้งานสามารถ 'เลือกและคัดกรองสวน' ตามเงื่อนไขความสะดวกของตัวเอง
        ไม่ว่าจะเป็นสิ่งอำนวยความสะดวก ระยะห่างจากรถไฟฟ้า ควบคู่ไปกับการเช็กค่าฝุ่น PM2.5 ล่าสุด ณ สวนแห่งนั้นได้ทันทีในหน้าจอเดียว เพื่อช่วยในการตัดสินใจ
        และส่งเสริมให้คนกรุงออกไปใช้พื้นที่สีเขียวได้อย่างมั่นใจและปลอดภัยที่สุด
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # 5. SOLUTION (METHODOLOGY)
    # ============================================================
    st.markdown('<div class="section-title">Solution (Methodology)</div>', unsafe_allow_html=True)

    # --- 5.1 Database Architecture ---
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">1) Database Architecture</div>
        <p style="font-size: 15px; color: #17342A; font-weight: 650; margin-bottom: 15px;">
        สถาปัตยกรรมข้อมูลเป็นแบบ Hybrid โดยจัดเก็บข้อมูลแยกเป็น 2 ส่วนหลัก
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="background: rgba(0,73,44,.05); padding: 20px; border-radius: 18px; border-left: 5px solid #00492C;">
                <b style="color: #00492C; font-size: 16px;">• Snowflake:</b>
                <p style="margin: 8px 0 0 0; font-weight: 650; color: #17342A; font-size: 14.5px;">ใช้จัดเก็บ ข้อมูลที่มีโครงสร้างชัดเจนอย่าง มิติของสวนสาธารณะ รายชื่อสิ่งอำนวยความสะดวก และพิกัดสถานีรถไฟฟ้า BTS/MRT</p>
            </div>
            <div style="background: rgba(251,186,22,.08); padding: 20px; border-radius: 18px; border-left: 5px solid #FBBA16;">
                <b style="color: #b38000; font-size: 16px;">• MongoDB:</b>
                <p style="margin: 8px 0 0 0; font-weight: 650; color: #17342A; font-size: 14.5px;">ใช้จัดเก็บข้อมูลค่าฝุ่น PM2.5 จากสถานีตรวจวัดในเขตต่างๆ ซึ่งมีลักษณะเป็น Dynamic JSON จากภายนอก</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 5.2 Processing & DuckDB Engine ---
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">2) Processing & DuckDB Engine</div>
        <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 15px;">
            <div style="border-bottom: 1px solid rgba(0,73,44,.08); padding-bottom: 12px;">
                <b style="color: #00492C; font-size: 15.5px;">- Dynamic JSON Management:</b>
                <p style="margin: 6px 0 0 0; font-weight: 650; color: #17342A; line-height: 1.6;">
