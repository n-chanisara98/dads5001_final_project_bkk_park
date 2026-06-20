import streamlit as st

def render_about_this_project():
    # ============================================================
    # 1. SETUP THEME STYLES (ก๊อปปี้สไตล์จากหน้า Home มาทั้งหมด)
    # ============================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;700;800;900&display=swap');

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
        min-height: 200px;
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
        margin-top: 15px;
        color: #FFF8E9;
        font-size: 48px;
        font-weight: 950;
        letter-spacing: -2px;
    }
    .section-title { margin: 30px 0 8px 0; color: #00492C; font-size: 28px; font-weight: 950; letter-spacing: -.4px; }
    
    .insight-box {
        background: linear-gradient(135deg, rgba(251,186,22,.38), rgba(177,216,184,.60));
        border: 1px solid rgba(0,73,44,.16);
        border-radius: 26px;
        padding: 20px 24px;
        box-shadow: 0 18px 54px rgba(0,73,44,.08);
        color: #17342A;
        font-size: 16px;
        line-height: 1.8;
    }
    .chart-card {
        background: rgba(255,255,255,.84);
        border: 1px solid rgba(0,73,44,.10);
        border-radius: 28px;
        padding: 24px;
        box-shadow: 0 18px 54px rgba(0,73,44,.09);
        margin-bottom: 18px;
    }
    .chart-title { color:#00492C; font-size: 19px; font-weight: 950; margin-bottom: 10px; }
    
    .story-card { border-radius: 26px; padding: 22px; background: #00492C; color: #FFF8E9; min-height: 120px; box-shadow: 0 18px 54px rgba(0,73,44,.14); }
    .story-card.yellow { background:#FBBA16; color:#00492C; }
    .story-card h4 { margin: 0 0 8px 0; font-size: 20px; font-weight: 950; }
    .story-card p { margin: 0; line-height: 1.7; font-weight: 650; }
    
    hr { margin: 2rem 0; border: none; height: 1px; background: rgba(0,73,44,.14); }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================
    # 2. HERO HEADER
    # ============================================================
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-kicker">🌳 Project Overview</div>
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
    
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="story-card">
            <h4>1) สวนหลักหนาแน่นมาก</h4>
            <p>แต่ยังมีพื้นที่สีเขียวทางเลือกอีกหลายแห่งกระจายอยู่ทั่วกรุงเทพฯ ที่ประชาชนยังเข้าไม่ถึงหรือยังไม่รู้จัก</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="story-card yellow">
            <h4>2) การใช้สวนของคนเมืองขับเคลื่อนด้วย 3 ปัจจัยหลัก ได้แก่</h4>
            <p style="margin-bottom: 4px;">• Amenities (สิ่งอำนวยความสะดวก)</p>
            <p style="margin-bottom: 4px;">• Connectivity (ความสะดวกในการเชื่อมต่อ BTS/MRT)</p>
            <p>• Health Safety (ความปลอดภัยจากฝุ่น PM2.5)</p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # 4. OBJECTIVE
    # ============================================================
    st.markdown('<div class="section-title">Objective</div>', unsafe_allow_html=True)
    
    with st.container():
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
    with st.container():
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">1) Database Architecture</div>
            <p style="font-size: 15px; color: #17342A; font-weight: 650; margin-bottom: 12px;">
            สถาปัตยกรรมข้อมูลเป็นแบบ Hybrid โดยจัดเก็บข้อมูลแยกเป็น 2 ส่วนหลัก
            </p>
            <p style="font-weight: 650; color: #17342A; margin-bottom: 6px;">
                <b style="color: #00492C;">- Snowflake:</b> ใช้จัดเก็บ ข้อมูลที่มีโครงสร้างชัดเจนอย่าง มิติของสวนสาธารณะ รายชื่อสิ่งอำนวยความสะดวก และพิกัดสถานีรถไฟฟ้า BTS/MRT
            </p>
            <p style="font-weight: 650; color: #17342A; margin: 0;">
                <b style="color: #00492C;">- MongoDB:</b> ใช้จัดเก็บข้อมูลค่าฝุ่น PM2.5 จากสถานีตรวจวัดในเขตต่างๆ ซึ่งมีลักษณะเป็น Dynamic JSON จากภายนอก
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- 5.2 Processing & DuckDB Engine ---
    with st.container():
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">2) Processing & DuckDB Engine</div>
            <p style="font-weight: 650; color: #17342A; line-height: 1.7; margin-bottom: 12px;">
                <b style="color: #00492C;">- Dynamic JSON Management:</b> สำหรับข้อมูลค่าฝุ่น PM2.5 การทำงานของระบบคือ ทันทีที่มีผู้ใช้เปิดหน้าเว็บแอปพลิเคชันขึ้นมา Streamlit จะวิ่งตรงไปยิง API ของทาง Air4Thai เพื่อดึงค่าฝุ่น ที่มีอยู่ ณ วินาทีนั้นลงมาทันทีเป็น JSON และ บันทึกลงไปในฐานข้อมูล MongoDB แบบเรียลไทม์ โดยใช้วิธี replace_one หรือเอาข้อมูลใหม่ล่าสุด 90 สถานีไปอัปเดตทับข้อมูลเดิมเรื่อยๆ ทำให้ MongoDB รักษาประสิทธิภาพการทำงานได้ดี และได้ข้อมูลที่เป็นปัจจุบันที่สุดเสมอ
            </p>
            <p style="font-weight: 650; color: #17342A; line-height: 1.7; margin-bottom: 12px;">
                <b style="color: #00492C;">- Geospatial Matrix:</b> ระบบจะทำการดึงข้อมูลพิกัด ละติจูด (Latitude) และลองจิจูด (Longitude) ของสวนจาก Snowflake มาคำนวณเปรียบเทียบกับพิกัดสถานีของ Air4Thai ใน MongoDB โดย ใช้ฟังก์ชัน cdist จาก SciPy ในการคำนวณระยะทาง เพื่อจับคู่สวนสาธารณะเข้ากับสถานีตรวจวัดฝุ่นที่อยู่ใกล้ที่สุด
            </p>
            <p style="font-weight: 650; color: #17342A; line-height: 1.7; margin: 0;">
                <b style="color: #00492C;">- DuckDB In-Memory SQL Engine:</b> Register ตารางผลลัพธ์ที่ Merge แล้วเข้าสู่ DuckDB เพื่อทำหน้าที่เป็น Space ประมวลผลคำสั่งคัดกรองในหน่วยความจำ เปลี่ยนจากการพึ่งพา Pandas มาใช้พลังของ SQL บน DuckDB
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- 5.3 AI Integration ---
    with st.container():
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">3) AI Integration</div>
            <p style="font-weight: 650; color: #17342A; margin-bottom: 12px;">
                <b style="color: #1E4380;">- Core Engine:</b> Gemini 2.5 Flash API ผ่านไลบรารีของกูเกิล
            </p>
            <p style="font-weight: 650; color: #17342A; line-height: 1.7; margin-bottom: 12px;">
                - ดีไซน์ระบบให้ทำงานร่วมกับฐานข้อมูลจริง ผ่านกระบวนการที่เรียกว่า Context-Aware Prompt Engineering เพื่อ control ให้คำตอบเกี่ยวข้องและเหมาะสมกับหัวข้อการออกกำลังกาย และสุขภาพ
            </p>
            <p style="font-weight: 650; color: #17342A; line-height: 1.7; margin: 0;">
                - สำหรับ function ที่ต้องมีการนำ database สวนสาธารณะมาใช้วิเคราะห์ร่วมด้วย ระบบหลังบ้านจะวิ่งไปดึงข้อมูลจริงของสวนนั้นจาก Snowflake นำมาเข้าเงื่อนไขหรือ Rule-based Logic ก่อน จากนั้น ระบบจะนำโครงสร้างข้อมูลบริบทจริงตรงนี้ ใส่เข้าไปในตัว Prompt เพื่อส่งให้ Gemini
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("DADS 5001 · BKK Urban Green Spaces & Connectivity")

# รันหน้าเว็บ
render_about_this_project()
