import streamlit as st

def render_about_this_project():
    # ============================================================
    # 1. PREMIUM UX/UI STYLES (With Presentation Navigator Style)
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
    
    .section-title { margin: 40px 0 12px 0; color: #00492C; font-size: 28px; font-weight: 950; letter-spacing: -.4px; }
    
    /* กล่อง Issue & Motivation */
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
    .ultra-premium-box b { color: #FBBA16; font-weight: 900; }

    /* กล่องเนื้อหาหลัก */
    .chart-card {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(0,73,44,.12);
        border-radius: 30px;
        padding: 35px;
        box-shadow: 0 20px 58px rgba(0,73,44,.06);
        margin-bottom: 25px;
        animation: fadeIn 0.4s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chart-title { color:#00492C; font-size: 24px; font-weight: 950; margin-bottom: 20px; border-bottom: 2px solid rgba(0,73,44,.08); padding-bottom: 12px; }
    
    /* Tags / Badges Graphics */
    .inline-tag {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        background: #EAF7EF;
        color: #00492C;
        border-radius: 10px;
        font-size: 13.5px;
        font-weight: 800;
        margin-right: 8px;
        border: 1px solid rgba(0,73,44,.15);
    }
    .inline-tag.blue { background: #EBF3FC; color: #1E4380; border-color: rgba(30,67,128,.15); }
    .inline-tag.yellow { background: #FFF8E7; color: #B8860B; border-color: rgba(184,134,11,.15); }

    /* Story Cards */
    .story-card { border-radius: 26px; padding: 24px; background: #00492C; color: #FFF8E9; min-height: 130px; box-shadow: 0 18px 54px rgba(0,73,44,.12); }
    .story-card.yellow { background:#FBBA16; color:#00492C; }
    .story-card h4 { margin: 0 0 10px 0; font-size: 20px; font-weight: 950; }
    .story-card p { margin: 0; line-height: 1.7; font-weight: 650; }
    
    /* กล่อง Presentation Step Guide */
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
    <div class="ultra-premium-box">
        🚀 แรงบันดาลใจจากการเติบโตของ<b>เทรนด์รักสุขภาพ</b> ท่ามกลาง<b>ข้อจำกัดของคนเมืองกรุง</b>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="story-card">
            <h4>📌 1) สวนหลักหนาแน่นมาก</h4>
            <p>แต่ยังมีพื้นที่สีเขียวทางเลือกอีกหลายแห่งกระจายอยู่ทั่วกรุงเทพฯ ที่ประชาชนยังเข้าไม่ถึงหรือยังไม่รู้จัก</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="story-card yellow">
            <h4>🎯 2) การใช้สวนของคนเมืองขับเคลื่อนด้วย 3 ปัจจัยหลัก:</h4>
            <p style="margin-bottom: 4px; font-weight: 800;">• Amenities (สิ่งอำนวยความสะดวก)</p>
            <p style="margin-bottom: 4px; font-weight: 800;">• Connectivity (ความสะดวกในการเชื่อมต่อ BTS/MRT)</p>
            <p style="font-weight: 800;">• Health Safety (ความปลอดภัยจากฝุ่น PM2.5)</p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # 4. OBJECTIVE
    # ============================================================
    st.markdown('<div class="section-title">Objective</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-card">
        <p style="font-size: 16px; line-height: 1.8; color: #17342A; font-weight: 650; margin: 0;">
        วัตถุประสงค์ของโปรเจกต์ จึงเป็นการสร้างระบบค้นหาและคัดกรองสวนสาธารณะในกรุงเทพฯ หรือ <b>Interactive Park Finder</b> ขึ้นมา 
        เพื่อเป็นเครื่องมือให้ผู้ใช้งานสามารถ 'เลือกและคัดกรองสวน' ตามเงื่อนไขความสะดวกของตัวเอง 
        ไม่ว่าจะเป็นสิ่งอำนวยความสะดวก ระยะห่างจากรถไฟฟ้า ควบคู่ไปกับการเช็กค่าฝุ่น PM2.5 ล่าสุด ณ สวนแห่งนั้นได้ทันทีในหน้าจอเดียว เพื่อช่วยในการตัดสินใจ 
        และส่งเสริมให้คนกรุงออกไปใช้พื้นที่สีเขียวได้อย่างมั่นใจและปลอดภัยที่สุด
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # 5. SOLUTION (METHODOLOGY) - PRESENTATION MODE EFFECT
    # ============================================================
    st.markdown('<div class="section-title">Solution (Methodology)</div>', unsafe_allow_html=True)
    
    # คำแนะนำสำหรับพรีเซนต์
    st.markdown('<div class="pres-guide">💡 คลิกเลือกหัวข้อด้านล่างเพื่อแสดงสไลด์เจาะลึกทีละข้อระหว่างพรีเซนต์:</div>', unsafe_allow_html=True)
    
    # สร้างเมนูสลับเนื้อหาด้วย Segmented Control (สวย ทันสมัย และสลับ Flow ง่ายมาก)
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

    # --- แสดงเนื้อหาตามสเตปที่เลือกเพื่อไม่ให้ข้อมูลเป็นพรืด ---
    if current_step == "🗄️ 1) Database Architecture":
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">🗄️ Part 1: Database Architecture</div>
            <p style="font-size: 16px; color: #17342A; font-weight: 700; margin-bottom: 20px;">
            สถาปัตยกรรมข้อมูลเบื้องหลังเป็นระบบแบบ <b>Hybrid Database</b> เพื่อดึงจุดเด่นของฐานข้อมูลแต่ละแบบออกมาใช้เก็บข้อมูลแยกกันเป็น 2 ส่วนหลัก:
            </p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                <div style="background: rgba(0,73,44,.04); padding: 24px; border-radius: 20px; border: 1px solid rgba(0,73,44,.08);">
                    <span class="inline-tag">❄️ Structured OLAP Warehouse</span>
                    <p style="margin: 12px 0 0 0; font-weight: 650; color: #17342A; font-size: 15px; line-height: 1.7;">
                        <b style="color: #00492C; font-size: 16px;">• Snowflake:</b><br>
                        ใช้รับหน้าที่ดูแลและจัดเก็บ <b>ข้อมูลที่มีโครงสร้างคงที่ชัดเจน (Static Master Data)</b> ทั้งหมด เช่น มิติโครงสร้างของสวนสาธารณะ, รายชื่อและประเภทของสิ่งอำนวยความสะดวกทั้งหมดในแต่ละสวน รวมถึงพิกัดตำแหน่งทางภูมิศาสตร์ของสถานีรถไฟฟ้า BTS และ MRT ทั่วกรุงเทพฯ
                    </p>
                </div>
                <div style="background: rgba(30,67,128,.04); padding: 24px; border-radius: 20px; border: 1px solid rgba(30,67,128,.08);">
                    <span class="inline-tag blue">🍃 Dynamic NoSQL Document</span>
                    <p style="margin: 12px 0 0 0; font-weight: 650; color: #17342A; font-size: 15px; line-height: 1.7;">
                        <b style="color: #1E4380; font-size: 16px;">• MongoDB:</b><br>
                        ใช้รับหน้าที่จัดเก็บ <b>ข้อมูลที่มีความยืดหยุ่นสูงและเปลี่ยนแปลงตลอดเวลา (Dynamic Stream)</b> อย่างค่าฝุ่น PM2.5 จากสถานีตรวจวัดตามเขตต่างๆ ซึ่งถูกส่งต่อมาในรูปแบบ Dynamic JSON โครงสร้างข้อมูลที่ไม่นิ่ง เพื่อรอการนำไปประมวลผลต่ออย่างรวดเร็ว
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif current_step == "⚡ 2) Processing & DuckDB Engine":
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">⚡ Part 2: Processing & DuckDB In-Memory Engine</div>
            <p style="font-size: 15.5px; color: #17342A; font-weight: 700; margin-bottom: 25px;">
            กระบวนการจัดการข้อมูลแบบเรียลไทม์ และการประมวลผลความเร็วสูงด้วย SQL Engine บนหน่วยความจำ:
            </p>
            
            <div style="display: flex; flex-direction: column; gap: 24px;">
                <div style="border-bottom: 1px solid rgba(0,73,44,.06); padding-bottom: 20px;">
                    <div style="margin-bottom: 10px;">
                        <span class="inline-tag">🌐 API Gateway Connection</span>
                        <span class="inline-tag blue">🔄 Real-Time Replace Method</span>
                    </div>
                    <p style="margin: 0; font-weight: 650; color: #17342A; line-height: 1.7; font-size: 15px;">
                        <b style="color: #00492C;">- Dynamic JSON Management:</b> ทันทีที่มีผู้ใช้เปิดหน้าเว็บแอปพลิเคชันขึ้นมา Streamlit จะทำการดึงข้อมูลสดใหม่โดยยิงตรงไปที่ API ของทาง <b>Air4Thai</b> เพื่อเก็บข้อมูล ณ วินาทีนั้นลงมาเป็นรูปแบบ JSON จากนั้นส่งไปอัปเดตทับลงบนฐานข้อมูล MongoDB แบบเรียลไทม์ด้วยฟังก์ชัน <code>replace_one</code> (อัปเดตข้อมูลทับ 90 สถานีหลัก) ทำให้ลดภาระพื้นที่จัดเก็บ และหน้าแอปฯ ได้ข้อมูลปัจจุบันรวดเร็วเสมอ
                    </p>
                </div>
                
                <div style="border-bottom: 1px solid rgba(0,73,44,.06); padding-bottom: 20px;">
                    <div style="margin-bottom: 10px;">
                        <span class="inline-tag">📍 Spatial Distance Matrix</span>
                        <span class="inline-tag yellow">🧮 SciPy cdist Analytics</span>
                    </div>
                    <p style="margin: 0; font-weight: 650; color: #17342A; line-height: 1.7; font-size: 15px;">
                        <b style="color: #00492C;">- Geospatial Matrix:</b> ระบบจะทำการดึงข้อมูลพิกัดละติจูดและลองจิจูดของสวนสาธารณะจาก Snowflake ขึ้นมาเปรียบเทียบกับพิกัดที่ตั้งของสถานีตรวจวัด Air4Thai ใน MongoDB โดยประมวลผลผ่านฟังก์ชัน <code>cdist</code> ของไลบรารี <b>SciPy</b> เพื่อคำนวณหาระยะห่างที่ใกล้ที่สุด ทำให้ระบบสามารถจับคู่ค่าฝุ่นของสถานีที่อยู่ใกล้สวนแห่งนั้นมากที่สุดมาแสดงผลได้อย่างถูกต้องแม่นยำ
                    </p>
                </div>
                
                <div>
                    <div style="margin-bottom: 10px;">
                        <span class="inline-tag">🚀 OLAP In-Memory SQL</span>
                        <span class="inline-tag blue">💎 Performance Boost</span>
                    </div>
                    <p style="margin: 0; font-weight: 650; color: #17342A; line-height: 1.7; font-size: 15px;">
                        <b style="color: #00492C;">- DuckDB In-Memory SQL Engine:</b> ข้อมูลทั้งหมดที่ถูกดึงและคำนวณเสร็จสิ้น จะถูกนำมาขึ้นทะเบียน (Register) เข้าสู่ตารางชั่วคราวใน <b>DuckDB Engine</b> ซึ่งทำงานบน Memory ทั้งหมดเพื่อรองรับการคัดกรองข้อมูลความเร็วสูง การทำงานส่วนนี้เปลี่ยนมาใช้พลังการสืบค้นของ SQL บน DuckDB แทน Pandas ดั้งเดิม ส่งผลให้ประสิทธิภาพการกรองเงื่อนไขของ User มีความสมูทและรวดเร็วกว่าเดิมมหาศาล
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif current_step == "🤖 3) AI Integration":
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">🤖 Part 3: Context-Aware AI Integration</div>
            
            <div style="background: rgba(155,204,208,.12); padding: 18px 24px; border-radius: 18px; border: 1px dashed #9BCCD0; margin-bottom: 25px;">
                <span class="inline-tag blue" style="background:#9BCCD0; color:#00492C;">🧠 LLM Brain</span>
                <span style="font-weight: 700; color: #17342A; font-size: 16px; margin-left: 5px;">
                    <b>Core Engine:</b> Gemini 2.5 Flash API ประมวลผลผ่านไลบรารีอย่างเป็นทางการของกูเกิล
                </span>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div style="background: #FAFBF8; padding: 20px; border-radius: 16px; border-left: 5px solid #1E4380;">
                    <b style="color: #1E4380; font-size: 15.5px;">🎯 1. Context-Aware Prompt Engineering</b>
                    <p style="margin: 8px 0 0 0; font-weight: 650; color: #17342A; line-height: 1.7; font-size: 14.5px;">
                        เพื่อควบคุมให้ระบบปัญญาประดิษฐ์ให้คำตอบที่สอดคล้องกับวัตถุประสงค์โครงการ ระบบจึงได้รับการออกแบบ Prompt คุมทิศทาง (Guardrails) เพื่อบีบให้คำแนะนำของโมเดลโฟกัสเฉพาะเรื่องหัวข้อการออกกำลังกาย สุขภาพ และข้อมูลพื้นที่สีเขียวอย่างตรงประเด็น ไม่หลุดหัวข้อ
                    </p>
                </div>
                
                <div style="background: #FAFBF8; padding: 20px; border-radius: 16px; border-left: 5px solid #00492C;">
                    <b style="color: #00492C; font-size: 15.5px;">⛓️ 2. Rule-based Hybrid Pipeline</b>
                    <p style="margin: 8px 0 0 0; font-weight: 650; color: #17342A; line-height: 1.7; font-size: 14.5px;">
                        เมื่อผู้ใช้ต้องการวิเคราะห์เชิงลึกเกี่ยวกับตัวสวน ระบบหลังบ้านจะวิ่งไปคัดแยกข้อมูลบริบทจริง (Ground Truth Data) จากฐานข้อมูล <b>Snowflake</b> มาประมวลผลผ่าน Logic เงื่อนไขก่อน จากนั้นจึงทำการแนบข้อเท็จจริงดังกล่าวเข้าไปใน Prompt ยิงส่งให้ Gemini วิธีนี้ทำให้คำตอบของ AI มีหลักสัญกรณ์ที่อิงอยู่บนฐานข้อมูลจริง ไม่เกิดการคิดไปเองหรือข้อมูลมโน (Hallucination)
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("DADS 5001 · BKK Urban Green Spaces & Connectivity")

# เรียกใช้งานฟังก์ชัน
render_about_this_project()
