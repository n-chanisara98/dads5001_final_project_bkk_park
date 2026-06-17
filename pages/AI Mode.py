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
    "AI ผู้ช่วยเลือกสวนสาธารณะ แนะนำกิจกรรมสุขภาพ "
    "และสร้างโปรแกรมออกกำลังกายเฉพาะบุคคล"
)

# ============================================================
# GEMINI CONFIG
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
# HELPER FUNCTION
# ============================================================

def ask_ai(prompt):

    response = model.generate_content(prompt)

    return response.text

# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs([
    "🌳 Park Recommendation",
    "🏃 Custom Workout Plan"
])

# ============================================================
# TAB 1
# ============================================================

with tab1:

    st.subheader(
        "🌳 AI Park Recommendation + Healthy Food"
    )

    selected_park = st.selectbox(
        "เลือกสวนสาธารณะ",
        park_list,
        key="park_rec"
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

    if st.button(
        "✨ วิเคราะห์สวนและแนะนำ",
        type="primary"
    ):

        park_row = df_parks[
            df_parks["PARK_NAME"] == selected_park
        ].iloc[0]

        area = park_row["AREA"]

        run_m = park_row["RUN_M"]

        prompt = f"""
คุณเป็นผู้เชี่ยวชาญด้านสุขภาพ
การออกกำลังกาย
และพื้นที่สีเขียวในกรุงเทพมหานคร

ข้อมูลสวน

ชื่อสวน:
{selected_park}

ขนาดพื้นที่:
{area}

ระยะทางวิ่ง:
{run_m} เมตร

เป้าหมายของผู้ใช้งาน:
{goal}

โปรดตอบเป็นภาษาไทย

1. เหตุผลที่สวนนี้เหมาะกับเป้าหมายดังกล่าว

2. กิจกรรมออกกำลังกายที่เหมาะสม

3. ข้อดีของพื้นที่และระยะทางวิ่ง

4. แนวทางการรับประทานอาหารหลังออกกำลังกาย

5. ตัวอย่างร้านอาหารสุขภาพหรือประเภทอาหารสุขภาพ
ที่ควรมองหาใกล้สวนแห่งนี้
"""

        with st.spinner("🤖 AI กำลังวิเคราะห์..."):

            try:

                result = ask_ai(prompt)

                st.success("วิเคราะห์เสร็จแล้ว")

                st.markdown(result)

            except Exception as e:

                st.error(f"เกิดข้อผิดพลาด: {e}")

# ============================================================
# TAB 2
# ============================================================

with tab2:

    st.subheader(
        "🏃 AI Custom Micro Workout Plan"
    )

    selected_park_workout = st.selectbox(
        "เลือกสวน",
        park_list,
        key="workout_park"
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
        15,
        90,
        30
    )

    if st.button(
        "🔥 สร้าง Workout Plan",
        type="primary"
    ):

        park_row = df_parks[
            df_parks["PARK_NAME"]
            == selected_park_workout
        ].iloc[0]

        area = park_row["AREA"]

        run_m = park_row["RUN_M"]

        prompt = f"""
คุณเป็น Personal Trainer

ข้อมูลสวน

ชื่อสวน:
{selected_park_workout}

พื้นที่:
{area}

ระยะทางวิ่ง:
{run_m} เมตร

ระดับผู้ใช้งาน:
{fitness_level}

เวลาที่มี:
{workout_time} นาที

กติกา

- ถ้าระยะทางวิ่งยาว
ให้เน้น Running Program

- ถ้าระยะทางวิ่งสั้น
ให้เน้น Bodyweight Workout

- ให้เลือกโปรแกรมให้เหมาะกับพื้นที่สวน

โปรดตอบเป็นภาษาไทย

1. Warm-up

2. Main Workout

3. Cool Down

4. เวลาที่ใช้ในแต่ละช่วง

5. Calories ที่คาดว่าจะเผาผลาญ

6. ข้อควรระวัง
"""

        with st.spinner(
            "🏃 AI กำลังออกแบบโปรแกรม..."
        ):

            try:

                result = ask_ai(prompt)

                st.success(
                    "สร้างโปรแกรมสำเร็จ"
                )

                st.markdown(result)

            except Exception as e:

                st.error(
                    f"เกิดข้อผิดพลาด: {e}"
                )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "DADS5001 | Bangkok Public Park Analytics & AI Wellness Assistant"
)
