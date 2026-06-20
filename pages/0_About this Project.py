import streamlit as st

def render_about_page():
    # ============================================================
    # CUSTOM STYLE FOR ABOUT PAGE
    # ============================================================
    st.markdown("""
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 900;
            color: #00492C;
            margin-bottom: 5px;
            text-align: center;
        }
        .main-subtitle {
            font-size: 18px;
            font-weight: 600;
            color: #51635A;
            text-align: center;
            margin-bottom: 35px;
        }
        .grid-card {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0, 73, 44, 0.06);
            border: 1px solid rgba(0, 73, 44, 0.08);
            margin-bottom: 25px;
            min-height: 340px;
        }
        .card-header {
            font-size: 22px;
            font-weight: 900;
            color: #00492C;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .badge-container {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        .tech-badge {
            background: #EAF6EF;
            color: #00492C;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 750;
            border: 1px solid rgba(0, 73, 44, 0.15);
        }
        .db-badge {
            background: #EBF3FC;
            color: #1E4380;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 750;
            border: 1px solid rgba(30, 67, 128, 0.15);
        }
        .ai-badge {
            background: #FFF8E7;
            color: #B8860B;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 750;
            border: 1px solid rgba(184, 134, 11, 0.15);
        }
        ul.clean-list {
            list-style-type: none;
            padding-left: 0;
        }
        ul.clean-list li {
            margin-bottom: 12px;
            font-size: 14.5px;
            color: #3A4740;
            line-height: 1.5;
            position: relative;
            padding-left: 25px;
        }
        ul.clean-list li::before {
            content: "•";
            color: #00492C;
            font-weight: bold;
            font-size: 20px;
            position: absolute;
            left: 5px;
            top: -2px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>🌳 About This Project</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>เบื้องหลังแนวคิด สถาปัตยกรรมข้อมูล และนวัตกรรม AI พัฒนาเพื่อคนเมืองกรุงเทพฯ</div>", unsafe_allow_html=True)

    # ============================================================
    # SECTION 1: ISSUES, MOTIVATION & OBJECTIVE (ROW 1)
    # ============================================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='grid-card'>
            <div class='card-header'>🎯 Issues & Motivation</div>
            <p style='color: #51635A; font-weight: 600; font-size: 14px; margin-bottom: 15px;'>
                แรงบันดาลใจจากการเติบโตของเทรนด์รักสุขภาพ ท่ามกลางข้อจำกัดของคนเมืองกรุง
            </p>
            <ul class='clean-list'>
                <li><b>Hidden Green Spaces:</b> สวนหลักหนาแน่นมาก แต่ยังมีพื้นที่สีเขียวทางเลือกอีกหลายแห่งกระจายอยู่ทั่วกรุงเทพฯ ที่ประชาชนยังเข้าไม่ถึงหรือยังไม่รู้จัก</li>
                <li><b>The 3 Decision Pillars:</b> การเลือกใช้สวนของคนเมืองขับเคลื่อนด้วย 3 ปัจจัยหลัก ได้แก่ <b>Amenities</b> (สิ่งอำนวยความสะดวก), <b>Connectivity</b> (ความสะดวกในการเชื่อมต่อ BTS/MRT), และ <b>Health Safety</b> (ความปลอดภัยจากฝุ่น PM2.5)</li>
                <li><b>Actionable Platform:</b> ต้องการสร้างเครื่องมือที่เปลี่ยนจากแค่การ 'รู้ว่ามีสวน' ไปสู่การ 'สนับสนุนให้คนกล้าออกไปขยับร่างกายอย่างมั่นใจ'</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='grid-card'>
            <div class='card-header'>🚀 Project Objective</div>
            <p style='color: #51635A; font-weight: 600; font-size: 14px; margin-bottom: 15px;'>
                เป้าหมายสูงสุดของระบบ Interactive Park Finder
            </p>
            <ul class='clean-list'>
                <li><b>All-in-One Dashboard:</b> ผสานรวมการค้นหา คัดกรอง และประเมินสภาพแวดล้อมของสวนสาธารณะให้อยู่บนหน้าจอเดียวแบบ Single-pane-of-glass</li>
                <li><b>Dynamic Customization:</b> อนุญาตให้ผู้ใช้คัดกรองสวนตามเงื่อนไขเฉพาะตัว เช่น ต้องมีห้องน้ำ ระยะเดินไปรถไฟฟ้าไม่เกินกำหนด ควบคู่กับการแสดงค่าฝุ่นสดใหม่ทันที</li>
                <li><b>Empowering Citizens:</b> ส่งเสริมให้การออกกำลังกายกลางแจ้ง (Open-air Workout) มีความปลอดภัยสูงสุด ลดความเสี่ยงทางสุขภาพจากการรับมลพิษโดยไม่ตั้งใจ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # SECTION 2: ARCHITECTURE & METHODOLOGY (ROW 2)
    # ============================================================
    st.markdown("<h3 style='color: #00492C; font-weight: 900; margin-top: 20px; margin-bottom: 15px;'>🛠️ System Architecture & Data Engineering</h3>", unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("""
        <div class='grid-card' style='min-height: 400px;'>
            <div class='card-header'>🗄️ Hybrid Database Strategy</div>
            <div class='badge-container'>
                <span class='db-badge'>Snowflake</span>
                <span class='db-badge'>MongoDB Atlas</span>
            </div>
            <ul class='clean-list'>
                <li><b>Structured Storage:</b> จัดเก็บข้อมูลมิติสวนสาธารณะ สิ่งอำนวยความสะดวก และพิกัดโครงข่ายระบบราง (BTS/MRT) ไว้บน Cloud Data Warehouse ของ <b>Snowflake</b> เพื่อความแม่นยำสูง</li>
                <li><b>Dynamic JSON Management:</b> บริหารจัดการข้อมูลค่าฝุ่นรายชั่วโมงที่มีโครงสร้างยืดหยุ่นจาก Air4Thai API ผ่าน <b>MongoDB Atlas</b> (NoSQL Cloud)</li>
                <li><b>Real-time Upsert Pipeline:</b> ทันทีที่มีการเข้าใช้งานแอปพลิเคชัน ระบบจะยิง API ดึงค่าฝุ่นสดใหม่ และสั่งอัปเดตลง MongoDB ด้วยกลยุทธ์ <code>replace_one</code> ทับสถานีเดิม (90 สถานี) ป้องกันฐานข้อมูลบวมและรักษาความเร็ว</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='grid-card' style='min-height: 400px;'>
            <div class='card-header'>⚡ Processing & DuckDB Engine</div>
            <div class='badge-container'>
                <span class='tech-badge'>DuckDB</span>
                <span class='tech-badge'>SciPy (cdist)</span>
                <span class='tech-badge'>Pandas</span>
            </div>
            <ul class='clean-list'>
                <li><b>Geospatial Matrix:</b> ใช้ฟังก์ชัน <code>cdist</code> จากคอมโพเนนต์ SciPy ในการคำนวณระยะทางพิกัดภูมิศาสตร์ เพื่อจับคู่สวนสาธารณะเข้ากับสถานีตรวจวัดฝุ่นที่อยู่ใกล้ที่สุดโดยอัตโนมัติ</li>
                <li><b>In-Memory SQL Engine:</b> จดทะเบียนตารางผลลัพธ์ที่ Merge แล้วเข้าสู่ <b>DuckDB</b> เพื่อทำหน้าที่เป็นสเปซประมวลผลคำสั่งคัดกรองในหน่วยความจำ</li>
                <li><b>Sub-second Filter:</b> เปลี่ยนจากการพึ่งพา Pandas Logic เพียวๆ มาใช้พลังของ SQL บน DuckDB ทำให้เมื่อผู้ใช้ปรับเงื่อนไขตัวกรอง (Filter) บนแอป แผนที่ Interactive จะเรนเดอร์ใหม่ในเสี้ยววินาที</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class='grid-card' style='min-height: 400px;'>
            <div class='card-header'>🤖 AI Wellness Integration</div>
            <div class='badge-container'>
                <span class='ai-badge'>Gemini 2.5 Flash</span>
                <span class='ai-badge'>Prompt Guardrails</span>
            </div>
            <ul class='clean-list'>
                <li><b>Core AI Engine:</b> บูรณาการ <b>Gemini 2.5 Flash API</b> เพื่อขับเคลื่อนฟีเจอร์ AI Urban Wellness Assistant รองรับการประมวลผลและการตอบกลับที่รวดเร็ว</li>
                <li><b>Context-Aware Framework:</b> ระบบจะดึงโครงสร้างข้อมูลพื้นที่ (Area) และระยะทางลู่วิ่งจริงจาก Snowflake มาเข้า Rule-based Logic แยกประเภทสวนก่อนป้อนเข้า Prompt</li>
                <li><b>Strict Prompt Guardrails:</b> ควบคุมพฤติกรรม LLM ไม่ให้หลุดกรอบนอกเรื่องสุขภาพ ออกแบบแผนสอดคล้องกับขนาดสวนจริง (เช่น สวนเล็กเน้น Bodyweight / สวนใหญ่เน้นวิ่ง) พร้อมปฏิเสธเคสทางการแพทย์เฉพาะทางเพื่อความปลอดภัย</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# เรียกใช้งานฟังก์ชันหน้า About (สามารถสลับหน้าโดยใช้ Sidebar Selectbox ได้ปกติเลยครับ)
render_about_page()
