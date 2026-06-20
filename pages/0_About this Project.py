import streamlit as st

def render_about_this_project():
    # ============================================================
    # 1. PREMIUM STYLE CONFIG (Theme: Flavour United)
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

    /* Hero Header */
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
    .hero-title { margin-top: 15px; color: #FFF8E9; font-size: 48px; font-weight: 950; letter-spacing: -2px; }
    
    .section-title { margin: 40px 0 12px 0; color: #00492C; font-size: 28px; font-weight: 950; letter-spacing: -.4px; }
    
    /* Issue Box */
    .ultra-premium-box {
        background: linear-gradient(135deg, #00492C 0%, #083823 40%, #1e3a1e 100%);
        border-left: 7px solid #FBBA16;
        border-radius: 28px;
        padding: 28px 32px;
        box-shadow: 0 22px 60px rgba(0,73,44,.18);
        color: #FFF8E9;
        font-size: 18px;
        font-weight: 700;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    .ultra-premium-box b { color: #FBBA16; font-weight: 950; }

    /* Solution Card */
    .solution-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(0,73,44,.15);
        border-radius: 30px;
        padding: 35px;
        box-shadow: 0 20px 58px rgba(0,73,44,0.08);
        margin-top: 10px;
        animation: fadeIn 0.4s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card-topic { color:#00492C; font-size: 24px; font-weight: 950; margin-bottom: 20px; border-bottom: 2px solid rgba(0,73,44,.1); padding-bottom: 12px; }
    
    .method-item { margin-bottom: 20px; }
    .method-item b { color: #00492C; font-size: 17px; }
    .method-desc { font-weight: 600; color: #17342A; line-height: 1.7; margin-top: 5px; }

    .story-card { border-radius: 26px; padding: 24px; background: #00492C; color: #FFF8E9; min-height: 130px; box-shadow: 0 18px 54px rgba(0,73,44,.12); }
    .story-card.yellow { background:#FBBA16; color:#00492C; }
    
    /* Step Navigator Tags */
    .step-tag {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        background: #EAF7EF;
        color: #00492C;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        margin-right: 8px;
        border: 1px solid rgba(0,73,44,.2);
    }
    
    .pres-guide {
        background: rgba(0, 73, 44, 0.05);
        padding: 12px 20px;
        border-radius: 14px;
        color: #00492C;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 15px;
        display: inline-block;
    }
    
    hr { margin: 2rem 0; border: none; height: 1px; background: rgba(0,73,44,0.1); }
    </style>
    """, unsafe_allow_html=True)

    # 1. HERO
    st.markdown('<div class="hero-wrap"><div class="hero-title">About This Project</div></div>', unsafe_allow_html=True)

    # 2. ISSUES & MOTIVATION
    st.markdown('<div class="section-title">Issues & Motivation</div>', unsafe_allow_html=True)
    st.markdown('<div class="ultra-premium-box">🚀 แรงบันดาลใจจากการเติบโตของ<b>เทรนด์รักสุขภาพ</b> ท่ามกลาง<b>ข้อจำกัดของคนเมืองกรุง</b></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="story-card"><h4>📌 1) สวนหลักหนาแน่นมาก</h4><p>แต่ยังมีพื้นที่สีเขียวทางเลือกอีกหลายแห่งกระจายอยู่ทั่วกรุงเทพฯ ที่ประชาชนยังเข้าไม่ถึงหรือยังไม่รู้จัก</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="story-card yellow"><h4>🎯 2) ปัจจัยหลักในการเข้าถึงสวน</h4><p>• Amenities (สิ่งอำนวยความสะดวก)<br>• Connectivity (การเชื่อมต่อ BTS/MRT)<br>• Health Safety (ความปลอดภัยจากฝุ่น)</p></div>', unsafe_allow_html=True)

    # 3. OBJECTIVE
    st.markdown('<div class="section-title">Objective</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-card"><p style="font-size: 16px; line-height: 1.8; color: #17342A; font-weight: 650; margin: 0;">วัตถุประสงค์ของโปรเจกต์ จึงเป็นการสร้างระบบค้นหาและคัดกรองสวนสาธารณะในกรุงเทพฯ หรือ <b>Interactive Park Finder</b> ขึ้นมา เพื่อเป็นเครื่องมือให้ผู้ใช้งานสามารถเลือกและคัดกรองสวนตามเงื่อนไขความสะดวกของตัวเอง ระยะห่างจากรถไฟฟ้า พร้อมเช็กค่าฝุ่น PM2.5 ล่าสุด เพื่อส่งเสริมให้คนกรุงออกไปใช้พื้นที่สีเขียวได้อย่างมั่นใจและปลอดภัยที่สุด</p></div>', unsafe_allow_html=True)

    # 4. SOLUTION (METHODOLOGY) - Interactive Slide
    st.markdown('<div class="section-title">Solution (Methodology)</div>', unsafe_allow_html=True)
    st.markdown('<div class="pres-guide">💡 คลิกเลือกหัวข้อด้านล่างเพื่อแสดงสไลด์เจาะลึกทีละข้อระหว่างพรีเซนต์:</div>', unsafe_allow_html=True)
    
    # แท็บปุ่มกดแบบ Segmented Control สวยๆ เหมือนเวอร์ชันก่อนหน้า
    step_options = [
        "🗄️ 1) Database Architecture", 
        "⚡ 2) Processing & DuckDB Engine", 
        "🤖 3) AI Integration"
    ]
    current_step = st.segmented_control(
        "Select Methodology Step", 
        options=step_options, 
        default=step_options[0],
        label_visibility="collapsed"
    )

    st.write("") # เว้นระยะช่องไฟ

    # --- หัวข้อที่ 1 ---
    if current_step == "🗄️ 1) Database Architecture":
        st.markdown("""
<div class="solution-card">
    <div class="card-topic">🗄️ 1) Database Architecture (Hybrid Strategy)</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div style="background: #f0f7f3; padding: 25px; border-radius: 20px; border-left: 6px solid #00492C;">
            <span class="step-tag">❄️ Snowflake</span>
            <div class="method-desc">ใช้จัดเก็บ <b>ข้อมูลที่มีโครงสร้างชัดเจน (Static Data)</b> เช่น มิติของสวนสาธารณะ รายชื่อสิ่งอำนวยความสะดวก และพิกัดสถานีรถไฟฟ้า BTS/MRT ทั้งหมด</div>
        </div>
        <div style="background: #f0f4f7; padding: 25px; border-radius: 20px; border-left: 6px solid #1E4380;">
            <span class="step-tag" style="background:#e1eef6; color:#1E4380;">🍃 MongoDB</span>
            <div class="method-desc">ใช้จัดเก็บ <b>ข้อมูลค่าฝุ่น PM2.5 (Dynamic Data)</b> จากสถานีตรวจวัดต่างๆ ซึ่งมีลักษณะเป็น JSON ที่เปลี่ยนแปลงตามเวลาแบบ Real-time</div>
        </div>
    </div>
</div>
        """, unsafe_allow_html=True)

    # --- หัวข้อที่ 2 ---
    elif current_step == "⚡ 2) Processing & DuckDB Engine":
        st.markdown("""
<div class="solution-card">
    <div class="card-topic">⚡ 2) Processing & DuckDB Engine</div>
    <div class="method-item">
        <span class="step-tag">🔄 Real-time Pipeline</span>
        <div class="method-desc"><b>Dynamic JSON Management:</b> เมื่อเปิดหน้าเว็บ Streamlit จะยิง API Air4Thai ดึงค่าฝุ่นสดใหม่ และบันทึกลง MongoDB ทันทีด้วยวิธี <code>replace_one</code> อัปเดตทับข้อมูลเดิม 90 สถานีเพื่อให้ข้อมูลสดใหม่เสมอ</div>
    </div>
    <div class="method-item">
        <span class="step-tag">📍 Geospatial Match</span>
        <div class="method-desc"><b>Geospatial Matrix:</b> ระบบดึงพิกัดสวนจาก Snowflake มาคำนวณเปรียบเทียบกับพิกัดสถานีฝุ่นใน MongoDB โดยใช้ฟังก์ชัน <code>cdist</code> จาก SciPy เพื่อจับคู่สวนเข้ากับสถานีวัดฝุ่นที่ใกล้ที่สุด</div>
    </div>
    <div class="method-item">
        <span class="step-tag">🚀 Performance Boost</span>
        <div class="method-desc"><b>DuckDB In-Memory SQL:</b> Register ตารางที่รวมเสร็จแล้วเข้าสู่ DuckDB เพื่อทำหน้าที่เป็นตัวประมวลผลคำสั่งคัดกรองในหน่วยความจำแทน Pandas ทำให้การ Filter ข้อมูลทำได้รวดเร็วระดับวินาที</div>
    </div>
</div>
        """, unsafe_allow_html=True)

    # --- หัวข้อที่ 3 ---
    else:
        st.markdown("""
<div class="solution-card">
    <div class="card-topic">🤖 3) AI Integration (Urban Wellness)</div>
    <div class="method-item">
        <span class="step-tag">🧠 Gemini Brain</span>
        <div class="method-desc"><b>Core Engine:</b> ใช้ Gemini 2.5 Flash API ผ่าน Google AI Studio เพื่อความเร็วและความแม่นยำในการวิเคราะห์ข้อมูลสุขภาพ</div>
    </div>
    <div class="method-item">
        <span class="step-tag">⛓️ Context-Aware</span>
        <div class="method-desc"><b>Smart Prompting:</b> ดีไซน์ระบบให้ AI ทำงานร่วมกับฐานข้อมูลจริงผ่านกระบวนการ Context-Aware Prompt Engineering เพื่อควบคุมคำตอบให้เหมาะสมกับหัวข้อสุขภาพและการออกกำลังกาย</div>
    </div>
    <div class="method-item">
        <span class="step-tag">🛡️ Ground Truth</span>
        <div class="method-desc"><b>Rule-based Logic:</b> ระบบจะดึงข้อมูลจริงของสวนจาก Snowflake มาวิเคราะห์เข้าเงื่อนไขก่อน แล้วจึงนำโครงสร้างข้อมูลจริงใส่ลงใน Prompt เพื่อให้ Gemini ให้คำแนะนำที่อ้างอิงจากฐานข้อมูลจริง</div>
    </div>
</div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("DADS 5001 · BKK Urban Green Spaces & Connectivity")

# EXECUTE
render_about_this_project()
