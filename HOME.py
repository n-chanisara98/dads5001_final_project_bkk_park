import streamlit as st

st.set_page_config(page_title="BKK Park Finder - Home", layout="wide")

# --- HEADER: ชัดเจน ทันสมัย ---
st.title("🌲 BKK Urban Green Spaces & Connectivity")
st.markdown("##### ระบบบูรณาการฐานข้อมูลพื้นที่สีเขียว โครงข่ายรถไฟฟ้า และดัชนีคุณภาพอากาศกรุงเทพมหานคร")
st.write("---")

# --- SECTION 1: 3 แกนหลักของข้อมูล (Data Architecture) ---
st.markdown("### 🛠️ Data Architecture")
st.write("โปรเจกต์นี้เกิดจากการเชื่อมโยง 3 แหล่งข้อมูลเพื่อตอบโจทย์คนเมือง")

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.metric(label="🍀 สวนสาธารณะ (Snowflake)", value="30+ สวน", delta="คัดกรองพิกัดจริง")
with m_col2:
    st.metric(label="🚊 โครงข่ายรถไฟฟ้าขนส่งมวลชน (Snowflake)", value="BTS & MRT", delta="คำนวณระยะทางเดินเท้า")
with m_col3:
    st.metric(label="😷 ดัชนีฝุ่น (MongoDB)", value="Real-time", delta="Air4Thai API ล่าสุด")

st.write("---")

# --- SECTION 2: ปัญหาและแนวคิด (สั้นกระชับ ไม่ยืดเยื้อ) ---
col_left, col_right = st.columns([5, 4])

with col_left:
    st.markdown("### ❓ Why This App?")
    st.markdown("""
    > **"จะออกไปวิ่งทั้งที ต้องเดินทางสะดวกและอากาศต้องปลอดภัย"**
    
    กรุงเทพฯ มีพื้นที่สีเขียวจำกัด และมักประสบปัญหาฝุ่น **PM2.5** บ่อยครั้ง แอปพลิเคชันนี้จึงออกแบบมาเพื่อแก้ปัญหานั้นโดยการรวมข้อมูลเชิงพื้นที่และการเดินทางมารวมไว้ในที่เดียว เพื่อให้ทุกคนสามารถค้นหาสถานที่ออกกำลังกายที่ตอบโจทย์ชีวิตประจำวันได้จริง
    """)

with col_right:
    st.markdown("### 🗂️ เทคโนโลยีที่เลือกใช้ในโปรเจกต์")
    st.success("**Snowflake**: จัดเก็บข้อมูลโครงสร้างหลัก (Relational Data) ของสวนและสถานีรถไฟฟ้า")
    st.warning("**MongoDB**: จัดเก็บข้อมูลฝุ่นดิบรูปแบบ JSON ที่ดึงมาจาก API")
    st.info("**Pandas & Scipy**: คำนวณระยะห่างทางภูมิศาสตร์ (Spatial Distance Matrix) ระหว่างจุดต่อจุด")

st.write("---")

# --- SECTION 3: สารบัญฟังก์ชันการใช้งานแบบ 3 หน้า (App Directory) ---
st.markdown("### 🖥️ สารบัญฟังก์ชันการใช้งาน (App Directory)")

page_col1, page_col2, page_col3 = st.columns(3)

with page_col1:
    with st.container(border=True): # หน้า 1
        st.markdown("#### 🏠 Page 1: Overview & Park Analytics")
        st.write("วิเคราะห์ภาพรวมขนาดพื้นที่สีเขียวรวมรายเขต พฤติกรรมการใช้งาน และความพร้อมเชิงสันทนาการ (Amenities)")

with page_col2:
    with st.container(border=True): # หน้า 2 
        st.markdown("#### 🔍 Page 2: Park Finder & Air Quality")
        st.write("ระบบ Map-Based ค้นหาสวน คัดกรองขนาดพื้นที่ และจับคู่สถานีตรวจฝุ่นที่อยู่ใกล้ที่สุดโดยอัตโนมัติ เพื่อเช็กสภาพอากาศก่อนออกจากบ้าน")
        
with page_col3:
    with st.container(border=True): # หน้า 3 
        st.markdown("#### 📊 Page 3: Analytics & Connectivity")
        st.write("หน้าวิเคราะห์ความสัมพันธ์เชิงสถิติ (Scatter Plot) ระหว่างขนาดสวนกับระยะห่างสถานีรถไฟฟ้า พร้อม Pie Chart ดูสัดส่วนการเข้าถึงระบบราง")
        

st.write("---")
st.caption("DADS 5001 - Data Analytics and Data Science Tools and Programming Project | 2026")
