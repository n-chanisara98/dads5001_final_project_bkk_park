import streamlit as st
import pandas as pd
import snowflake.connector
import google.generativeai as genai

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Wellness Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Urban Wellness Assistant")
st.write(
    "AI ผู้ช่วยด้านสุขภาพ การออกกำลังกาย และการใช้สวนสาธารณะในกรุงเทพมหานคร"
)

# ============================================================
# GEMINI
# ============================================================

genai.configure(
    api_key=st.secrets["google"]["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================================
# SNOWFLAKE CONNECTION
# ============================================================

@st.cache_resource
def init_snowflake_connection():

    conn = snowflake.connector.connect(
        user=st.secrets["connections"]["snowflake"]["user"],
        password=st.secrets["connections"]["snowflake"]["password"],
        account=st.secrets["connections"]["snowflake"]["account"],
        warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
        database=st.secrets["connections"]["snowflake"]["database"],
        schema=st.secrets["connections"]["snowflake"]["schema"],
        role=st.secrets["connections"]["snowflake"]["role"]
    )

    class SnowflakeWrapper:
        def __init__(self, connection):
            self.conn = connection

        def query(self, sql):
            return pd.read_sql(sql, self.conn)

    return SnowflakeWrapper(conn)

sf_conn = init_snowflake_connection()

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=600)
def load_park_data():

    query = """
    SELECT
        l.PARK_NAME,
        l.AREA,
        d.RUN_M
    FROM PARK_LAT_LONG l
    LEFT JOIN PARK_PATH_DISTANCE d
        ON l.PARK_NAME = d.PARK_NAME
    """

    df = sf_conn.query(query)

    df.columns = [
        c.replace('"', '').upper().strip()
        for c in df.columns
    ]

    return df

df_parks = load_park_data()

park_list = sorted(
    df_parks["PARK_NAME"]
    .dropna()
    .unique()
)

# ============================================================
# HELPER
# ============================================================

def ask_ai(prompt):

    response = model.generate_content(prompt)

    return response.text

# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs([
    "🏃 Custom Workout Plan",
    "💬 Health Assistant"
])

# ============================================================
# TAB 1
# ============================================================

with tab1:

    st.subheader("🏃 AI Custom Workout Plan")

    selected_park = st.selectbox(
        "เลือกสวนสาธารณะ",
        park_list
    )

    goal = st.selectbox(
        "เป้าหมายการออกกำลังกาย",
        [
            "ลดน้ำหนัก",
            "สุขภาพทั่วไป",
            "เพิ่มความแข็งแรง",
            "เตรียมวิ่งมาราธอน"
        ]
    )

    fitness_level = st.selectbox(
        "ระดับความฟิต",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    workout_time = st.slider(
        "เวลาที่ต้องการออกกำลังกาย (นาที)",
        min_value=15,
        max_value=120,
        value=45,
        step=5
    )

    if st.button(
        "✨ แนะนำ Workout Plan",
        type="primary"
    ):

        park_row = df_parks[
            df_parks["PARK_NAME"] == selected_park
        ].iloc[0]

        area = park_row["AREA"]

        run_m = park_row["RUN_M"]
        run_m_num = pd.to_numeric(run_m, errors="coerce")
        
        # วิเคราะห์ประเภทสวน

        if pd.isna(run_m_num):

            park_type = "ไม่มีข้อมูลลู่วิ่ง"

        elif run_m_num < 1000:

            park_type = "สวนขนาดเล็ก"

        elif run_m_num < 2000:

            park_type = "สวนขนาดกลาง"

        else:

            park_type = "สวนขนาดใหญ่"

        prompt = f"""

คุณคือ Personal Trainer และ Running Coach

ข้อมูลผู้ใช้งาน

สวนสาธารณะ:
{selected_park}

ขนาดพื้นที่:
{area}

ระยะทางวิ่ง:
{run_m}

ประเภทสวน:
{park_type}

เป้าหมาย:
{goal}

ระดับความฟิต:
{fitness_level}

เวลาที่มี:
{workout_time} นาที

กติกาในการออกแบบโปรแกรม

- หากเป็นสวนขนาดใหญ่ ให้เน้น Running Program

- หากเป็นสวนขนาดกลาง ให้ผสม Running และ Bodyweight

- หากเป็นสวนขนาดเล็ก ให้เน้น Circuit Training และ Bodyweight

- หากไม่มีข้อมูลลู่วิ่ง ให้หลีกเลี่ยงการออกแบบโปรแกรมที่ต้องวิ่งระยะไกล และเน้นการออกกำลังกายที่ใช้พื้นที่จำกัด

โปรดสร้างโปรแกรมออกกำลังกายให้เหมาะสมกับ

- เป้าหมาย
- ระดับความฟิต
- เวลาที่มี
- ลักษณะของสวน

จัดรูปแบบคำตอบเป็น

🏃 เหตุผลที่เลือกโปรแกรมนี้

🔥 Warm-up

💪 Main Workout

🧘 Cool Down

⏱ เวลาที่ใช้ในแต่ละช่วง

💡 คำแนะนำเพิ่มเติม

ตอบเป็นภาษาไทย
"""

        with st.spinner("🤖 AI กำลังออกแบบโปรแกรม..."):

            try:

                result = ask_ai(prompt)

                st.markdown(result)

                st.info(
                    """
⚠️ Disclaimer

คำแนะนำนี้สร้างขึ้นโดยระบบ AI เพื่อใช้เป็นข้อมูลเบื้องต้นเท่านั้น

ไม่ใช่คำแนะนำทางการแพทย์
หรือคำแนะนำจากผู้เชี่ยวชาญด้านสุขภาพ

โปรดใช้วิจารณญาณและพิจารณาสภาพร่างกายของตนเองก่อนออกกำลังกาย
"""
                )

            except Exception as e:

                st.error(f"เกิดข้อผิดพลาด: {e}")

# ============================================================
# TAB 2
# ============================================================

with tab2:

    st.subheader("💬 Health Assistant")

    # --------------------------------------------------------
    # FAQ
    # --------------------------------------------------------

    st.markdown("### 📚 FAQ")

    faq_options = [
        "ควรวิ่งกี่ครั้งต่อสัปดาห์",
        "PM2.5 ระดับไหนไม่ควรวิ่ง",
        "เดินเร็วหรือวิ่งเผาผลาญมากกว่า",
        "หลังวิ่งควรกินอะไร",
        "วอร์มอัพก่อนวิ่งอย่างไร",
        "วิ่งตอนเช้าหรือตอนเย็นดีกว่า",
        "มือใหม่ควรเริ่มวิ่งอย่างไร",
        "ออกกำลังกายกี่นาทีต่อวันจึงเพียงพอ"
    ]

    selected_faq = st.selectbox(
        "เลือกคำถาม",
        faq_options
    )

    if st.button("📖 ตอบคำถาม FAQ"):

        prompt = f"""
คุณคือ AI Urban Wellness Assistant

ตอบคำถามต่อไปนี้

{selected_faq}

ตอบเป็นภาษาไทย

- เข้าใจง่าย
- ใช้ภาษาทั่วไป
- ไม่เกิน 300 คำ
- หากมีข้อควรระวังให้ระบุด้วย
"""

        with st.spinner("กำลังค้นหาคำตอบ..."):

            try:

                result = ask_ai(prompt)

                st.markdown(result)

            except Exception as e:

                st.error(f"เกิดข้อผิดพลาด: {e}")

    st.divider()

    # --------------------------------------------------------
    # OPEN QUESTION
    # --------------------------------------------------------

    st.markdown("### ✍️ ถาม AI ได้เอง")

    user_question = st.text_area(
        "พิมพ์คำถามเกี่ยวกับสุขภาพ การออกกำลังกาย หรือการวิ่ง"
    )

    if st.button("🤖 ถาม AI"):

        if user_question.strip() == "":
            st.warning("กรุณากรอกคำถามก่อน")
        else:

            prompt = f"""
คุณคือ AI Urban Wellness Assistant

คุณตอบได้เฉพาะเรื่อง

- สุขภาพ
- การออกกำลังกาย
- การวิ่ง
- โภชนาการเบื้องต้น
- การใช้สวนสาธารณะเพื่อกิจกรรมทางกาย

คำถาม:

{user_question}

ตอบเป็นภาษาไทย

หากเป็นคำถามทางการแพทย์เฉพาะทาง
ให้แนะนำให้ปรึกษาแพทย์หรือผู้เชี่ยวชาญเพิ่มเติม
"""

            with st.spinner("AI กำลังคิดคำตอบ..."):

                try:

                    result = ask_ai(prompt)

                    st.markdown(result)

                except Exception as e:

                    st.error(f"เกิดข้อผิดพลาด: {e}")

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "DADS5001 | Data Analytics and Data Science Tools and Programming"
)
