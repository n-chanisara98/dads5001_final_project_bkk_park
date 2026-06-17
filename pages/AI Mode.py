import streamlit as st
import pandas as pd
import snowflake.connector
import google.generativeai as genai

st.set_page_config(page_title="AI Healthy Living", layout="wide")

st.title("🤖 AI Urban Health & Wellness Assistant")
st.write("โมเดล AI บนระบบคลาวด์เพื่อการส่งเสริมสุขภาพคนเมือง (The Gemma 4 Good Hackathon)")
st.write("---")

# =====================================================================
# 1. SETUP AI CONFIGURATION (ดึงคีย์ความปลอดภัยจาก Secrets หลังบ้าน)
# =====================================================================
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["google"]["GEMINI_API_KEY"])
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ในระบบ Secrets กรุณาเซ็ตอัพค่าก่อนใช้งาน")
    st.stop()

# เรียกใช้สมองกลเวอร์ชัน Flash ที่ทำงานเร็วที่สุดและเสถียรที่สุดบนคลาวด์
model = genai.GenerativeModel('gemini-1.5-flash')

# =====================================================================
# 2. DATABASE CONNECTION & FETCH DATA
# =====================================================================
@st.cache_resource
def init_snowflake():
    return snowflake.connector.connect(
        user=st.secrets["connections"]["snowflake"]["user"],
        password=st.secrets["connections"]["snowflake"]["password"],
        account=st.secrets["connections"]["snowflake"]["account"],
        warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
        database=st.secrets["connections"]["snowflake"]["database"],
        schema=st.secrets["connections"]["snowflake"]["schema"],
        role=st.secrets["connections"]["snowflake"]["role"]
    )

try:
    ctx = init_snowflake()
    df_parks = pd.read_sql("SELECT PARK_NAME, AREA FROM PARK_LAT_LONG", ctx)
    df_parks.columns = [c.upper().strip() for c in df_parks.columns]
    park_list = df_parks['PARK_NAME'].tolist()
except Exception as e:
    df_parks = pd.DataFrame({'PARK_NAME': ['สวนลุมพินี', 'สวนเบญจกิติ'], 'AREA': ['360 ไร่', '130 ไร่']})
    park_list = ["สวนลุมพินี", "สวนเบญจกิติ", "สวนจตุจักร"]

# =====================================================================
# 3. INTERFACE BLOCK
# =====================================================================
tab_workout, tab_events = st.tabs(["🏋️‍♂️ สวนสวย + แผนวิ่งกินคลีนเฉพาะบุคคล", "📅 7-Day Upcoming BKK Health Events"])

# TAB 1: วิเคราะห์พื้นที่สวนและแนะนำร้านอาหาร
with tab_workout:
    st.subheader("🌲 ค้นหาแผนการออกกำลังกายที่แมตช์กับขนาดพื้นที่และจุดกินคลีน")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        selected_park = st.selectbox("🎯 วันนี้คุณกำลังจะไปสวนสาธารณะแห่งไหน:", park_list, key="park_select")
    with col_in2:
        fitness_goal = st.selectbox(
            "💪 ระดับการฟิตร่างกายของคุณในวันนี้:",
            ["สายเริ่มฝึกเดิน/วิ่งเหยาะเน้นกินลมชมวิว", "สายคาร์ดิโอเน้นเบิร์นไขมัน", "สายเล่นกล้ามเนื้อเวทสตรีทเอาต์"],
            key="goal_select"
        )
    
    if st.button("🚀 รันสมองกลประมวลผลพื้นที่", type="primary"):
        park_info = df_parks[df_parks['PARK_NAME'] == selected_park].iloc[0]
        park_area_text = park_info['AREA']
        
        prompt_input = f"""
        คุณคือ AI ผู้เชี่ยวชาญด้านสุขภาพและผังเมืองกรุงเทพฯ ในโปรเจกต์ส่งเสริมพื้นที่สีเขียว
        ช่วยวิเคราะห์และให้คำแนะนำสำหรับพิกัดนี้: {selected_park} ซึ่งมีขนาดพื้นที่ {park_area_text}
        โดยผู้ใช้งานมีเป้าหมายคือ: {fitness_goal}
        
        โปรดตอบข้อมูลแบ่งเป็น 2 ส่วนหลักให้ชัดเจน:
        1. [Custom Micro-Workout Plan] จงเอาขนาดพื้นที่สวน ({park_area_text}) มาพิจารณาร่วมด้วย หากสวนมีขนาดพื้นที่ใหญ่ ให้จัดโปรแกรมวิ่งระยะยาว คุมโซนหัวใจ แต่ถ้าสวนขนาดเล็ก ให้จัดโปรแกรมแบบ Bodyweight หรือ Street Workout ที่ใช้พื้นที่น้อยแทนให้สอดคล้องกับขนาดพื้นที่จริง
        2. [Healthy Eats Nearby] แนะนำร้านอาหารสุขภาพ อาหารคลีน หรือสลัดบาร์ ที่ตั้งอยู่รอบๆ หรือใกล้เคียงสวน "{selected_park}" มาสัก 2-3 ร้าน พร้อมพิกัดและการเดินทางสั้นๆ
        """
        
        with st.spinner("🧠 AI กำลังคำนวณสัดส่วนพื้นที่และวิเคราะห์เมนูกินคลีนบนระบบคลาวด์..."):
            try:
                response = model.generate_content(prompt_input)
                st.info("🥦 **สรุปแผนออกกำลังกายและพิกัดร้านสุขภาพจาก AI**")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

# TAB 2: ดึงกิจกรรมสุขภาพ Up-coming 7 วันข้างหน้าในกรุงเทพฯ
with tab_events:
    st.subheader("📅 เช็กตารางกิจกรรมวิ่ง งานสุขภาพ และเวิร์กช็อป รอบกรุงฯ 7 วันข้างหน้า")
    
    event_category = st.radio(
        "🎯 เลือกประเภทงานที่คุณสนใจ:",
        ["งานวิ่งมาราธอน/งานปั่นจักรยาน", "คลาสนิทรรศการและโยคะในสวน", "สัมมนาโภชนาการและตลาดนัดอาหาร Organic"],
        horizontal=True
    )
    
    if st.button("🔍 ดึงข้อมูลตารางกิจกรรมล่าสุด", type="secondary"):
        prompt_event = f"""
        โปรดแนะนำรายการกิจกรรมสุขภาพ งานวิ่ง งานโยคะในสวน หรือตลาดนัดสุขภาพ ที่กำลังจะเกิดขึ้นจริงในกรุงเทพมหานคร ภายในกรอบระยะเวลา 7 วันข้างหน้า นับจากเดือนมิถุนายน ปี 2026 ในหมวดหมู่: {event_category}
        ขอรายการอัปเดตที่เป็นประโยชน์สัก 3 งาน ระบุวัน-เวลา สถานที่จัดงาน และคำแนะนำการเตรียมตัวสั้นๆ
        """
        
        with st.spinner("🌐 ดึงฐานข้อมูลกิจกรรมและกรองเทรนด์โดย AI..."):
            try:
                response_ev = model.generate_content(prompt_event)
                st.success("📊 **ตารางกิจกรรมเพื่อสุขภาพรอบกรุงเทพฯ (7 วันข้างหน้า)**")
                st.markdown(response_ev.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

st.write("---")
st.caption("✨ DADS 5001 Project | Google Generative AI Cloud Core Integration")
