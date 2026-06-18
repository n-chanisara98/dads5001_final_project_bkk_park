import streamlit as st
import pandas as pd
import snowflake.connector
import google.generativeai as genai

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Urban Wellness Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FFF8E7 0%, #EAF6EF 42%, #FDE7D6 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00492C 0%, #1E4380 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero-box {
        background:
            linear-gradient(120deg, rgba(0,73,44,0.94), rgba(30,67,128,0.72)),
            url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80");
        background-size: cover;
        background-position: center;
        padding: 48px 52px;
        border-radius: 32px;
        color: white;
        box-shadow: 0 18px 45px rgba(0,73,44,0.18);
        margin-bottom: 28px;
    }

    .hero-tag {
        display: inline-block;
        background: #FBBA16;
        color: #00492C;
        padding: 9px 16px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 14px;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 900;
        line-height: 1.15;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 19px;
        font-weight: 600;
        opacity: 0.96;
        max-width: 1050px;
    }

    .kpi-card {
        background: rgba(255,255,255,0.90);
        padding: 24px 26px;
        border-radius: 26px;
        box-shadow: 0 12px 30px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        min-height: 140px;
    }

    .kpi-label {
        font-size: 14px;
        color: #51635A;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .kpi-value {
        font-size: 31px;
        color: #00492C;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    .kpi-chip {
        display: inline-block;
        margin-top: 12px;
        padding: 8px 14px;
        background: #B1D8B8;
        color: #00492C;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 850;
    }

    .section-title {
        font-size: 25px;
        font-weight: 900;
        color: #00492C;
        margin-top: 28px;
        margin-bottom: 14px;
    }

    .content-card {
        background: rgba(255,255,255,0.92);
        border-radius: 28px;
        padding: 26px 28px;
        box-shadow: 0 14px 34px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        margin-bottom: 28px;
    }

    .small-title {
        font-size: 22px;
        font-weight: 900;
        color: #00492C;
        margin-bottom: 6px;
    }

    .desc-text {
        color: #66746B;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .tips-box {
        background: linear-gradient(90deg, #FBBA16 0%, #B1D8B8 100%);
        padding: 22px 28px;
        border-radius: 26px;
        margin-top: 28px;
        margin-bottom: 30px;
        box-shadow: 0 10px 26px rgba(0,73,44,0.12);
        color: #00492C;
        font-size: 19px;
        font-weight: 750;
    }

    div[data-testid="stTabs"] button {
        font-size: 17px;
        font-weight: 800;
    }

    div[data-testid="stButton"] button {
        border-radius: 999px;
        font-weight: 800;
        padding: 0.65rem 1.2rem;
    }

    .disclaimer-box {
        background: #FFF8E7;
        border-left: 8px solid #E22028;
        padding: 18px 22px;
        border-radius: 18px;
        color: #00492C;
        font-weight: 600;
        margin-top: 18px;
    }

    .ai-answer-box {
        background: rgba(255,255,255,0.94);
        border-radius: 24px;
        padding: 24px 28px;
        border: 1px solid rgba(0,73,44,0.12);
        box-shadow: 0 10px 26px rgba(0,73,44,0.08);
        margin-top: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero-box">
    <div class="hero-tag">AI WELLNESS · PARK WORKOUT · HEALTH ASSISTANT</div>
    <div class="hero-title">🤖 AI Urban Wellness Assistant</div>
    <div class="hero-subtitle">
        ผู้ช่วย AI สำหรับวางแผนออกกำลังกายในสวนสาธารณะกรุงเทพฯ
        แนะนำโปรแกรมให้เหมาะกับเป้าหมาย ระดับความฟิต เวลา และลักษณะของสวน
    </div>
</div>
""", unsafe_allow_html=True)

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
        role=st.secrets["connections"]["snowflake"]["role"],
        client_session_keep_alive=True  # เปิดท่อทิ้งไว้เพื่อลดโอกาสสายหลุด
    )

    # 🛡️ ระบบตรวจจับและ Reconnect คืนชีพ Session อัตโนมัติ
    class SnowflakeWrapper:
        def __init__(self, connection):
            self.conn = connection

        def query(self, sql):
            try:
                if self.conn.is_closed():
                    st.cache_resource.clear()
                    sf_wrapper_new = init_snowflake_connection()
                    self.conn = sf_wrapper_new.conn
                return pd.read_sql(sql, self.conn)
            except Exception:
                st.cache_resource.clear()
                ctx_fallback = snowflake.connector.connect(
                    user=st.secrets["connections"]["snowflake"]["user"],
                    password=st.secrets["connections"]["snowflake"]["password"],
                    account=st.secrets["connections"]["snowflake"]["account"],
                    warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
                    database=st.secrets["connections"]["snowflake"]["database"],
                    schema=st.secrets["connections"]["snowflake"]["schema"],
                    role=st.secrets["connections"]["snowflake"]["role"],
                    client_session_keep_alive=True
                )
                self.conn = ctx_fallback
                return pd.read_sql(sql, self.conn)

    return SnowflakeWrapper(conn)

try:
    sf_conn = init_snowflake_connection()
except Exception as e:
    st.error(f"❌ ไม่สามารถเชื่อมต่อ Snowflake ได้: {e}")
    st.stop()

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

try:
    df_parks = load_park_data()
    park_list = sorted(
        df_parks["PARK_NAME"]
        .dropna()
        .unique()
    )
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการโหลดข้อมูลสวน: {e}")
    st.stop()

# ============================================================
# KPI SUMMARY
# ============================================================

total_parks = len(park_list)
run_available = pd.to_numeric(df_parks["RUN_M"], errors="coerce").notna().sum()
largest_run = pd.to_numeric(df_parks["RUN_M"], errors="coerce").max()
largest_run_text = f"{largest_run:,.0f} m" if pd.notna(largest_run) else "N/A"

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #00492C;">
        <div class="kpi-label">🌳 สวนในระบบ</div>
        <div class="kpi-value">{total_parks}</div>
        <div class="kpi-chip">พร้อมให้ AI วิเคราะห์</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #FBBA16;">
        <div class="kpi-label">🏃 มีข้อมูลลู่วิ่ง</div>
        <div class="kpi-value">{run_available}</div>
        <div class="kpi-chip">เหมาะกับ Running Plan</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #E22028;">
        <div class="kpi-label">📏 ลู่วิ่งยาวที่สุด</div>
        <div class="kpi-value">{largest_run_text}</div>
        <div class="kpi-chip">จากฐานข้อมูลสวน</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="tips-box">
    💡 <b>วิธีใช้งาน:</b>
    เลือกสวน เป้าหมาย ระดับความฟิต และเวลาที่มี จากนั้นให้ AI สร้างแผนออกกำลังกายเฉพาะบุคคล
    หรือใช้ Health Assistant เพื่อถามคำถามสุขภาพและการวิ่งเบื้องต้น
</div>
""", unsafe_allow_html=True)

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
    left_col, right_col = st.columns([1.05, 1])

    with left_col:
        st.markdown("""
        <div class="content-card">
            <div class="small-title">🏃 AI Custom Workout Plan</div>
            <div class="desc-text">
                เลือกข้อมูลพื้นฐานของคุณ แล้วให้ AI ออกแบบโปรแกรมออกกำลังกายที่เหมาะกับสวนและเวลาที่มี
            </div>
        """, unsafe_allow_html=True)

        selected_park = st.selectbox(
            "🌳 เลือกสวนสาธารณะ",
            park_list
        )

        goal = st.selectbox(
            "🎯 เป้าหมายการออกกำลังกาย",
            [
                "ลดน้ำหนัก",
                "สุขภาพทั่วไป",
                "เพิ่มความแข็งแรง",
                "เตรียมวิ่งมาราธอน"
            ]
        )

        fitness_level = st.selectbox(
            "🔥 ระดับความฟิต",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        workout_time = st.slider(
            "⏱ เวลาที่ต้องการออกกำลังกาย (นาที)",
            min_value=15,
            max_value=120,
            value=45,
            step=5
        )

        generate_plan = st.button(
            "✨ แนะนำ Workout Plan",
            type="primary",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        <div class="content-card">
            <div class="small-title">🌿 Park-Based Wellness Logic</div>
            <div class="desc-text">
                ระบบจะดูข้อมูลขนาดพื้นที่และระยะลู่วิ่งของสวน เพื่อเลือกประเภทโปรแกรมให้เหมาะกับบริบทจริง
            </div>
            <p>🏞️ <b>สวนขนาดใหญ่:</b> เน้น Running Program</p>
            <p>🌳 <b>สวนขนาดกลาง:</b> ผสม Running + Bodyweight</p>
            <p>🧘 <b>สวนขนาดเล็ก:</b> เน้น Circuit Training</p>
            <p>📍 <b>ไม่มีข้อมูลลู่วิ่ง:</b> ใช้โปรแกรมพื้นที่จำกัด</p>
        </div>
        """, unsafe_allow_html=True)

    if generate_plan:
        filtered_df = df_parks[df_parks["PARK_NAME"] == selected_park]
        
        if filtered_df.empty:
            st.error("❌ ไม่พบข้อมูลของสวนสาธารณะที่เลือกในระบบ")
        else:
            park_row = filtered_df.iloc[0]
            area = park_row["AREA"]
            run_m = park_row["RUN_M"]
            run_m_num = pd.to_numeric(run_m, errors="coerce")

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

                    st.markdown("""
                    <div class="ai-answer-box">
                        <div class="small-title">✨ โปรแกรมที่ AI แนะนำ</div>
                    """, unsafe_allow_html=True)

                    st.markdown(result)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("""
                        <div class="disclaimer-box">
                        ⚠️ <b>Disclaimer:</b>
                        คำแนะนำนี้สร้างขึ้นโดยระบบ AI เพื่อใช้เป็นข้อมูลเบื้องต้นเท่านั้น
                        ไม่ใช่คำแนะนำทางการแพทย์หรือคำแนะนำจากผู้เชี่ยวชาญด้านสุขภาพ
                        โปรดใช้วิจารณญาณและพิจารณาสภาพร่างกายของตนเองก่อนออกกำลังกาย
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดในการเรียก AI: {e}")

# ============================================================
# TAB 2
# ============================================================

with tab2:
    faq_col, ask_col = st.columns([1, 1])

    with faq_col:
        st.markdown("""
        <div class="content-card">
            <div class="small-title">📚 FAQ สุขภาพและการวิ่ง</div>
            <div class="desc-text">
                เลือกคำถามยอดนิยม แล้วให้ AI อธิบายเป็นภาษาไทยแบบเข้าใจง่าย
            </div>
        """, unsafe_allow_html=True)

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

        faq_button = st.button(
            "📖 ตอบคำถาม FAQ",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with ask_col:
        st.markdown("""
        <div class="content-card">
            <div class="small-title">✍️ ถาม AI ได้เอง</div>
            <div class="desc-text">
                พิมพ์คำถามเกี่ยวกับสุขภาพ การออกกำลังกาย การวิ่ง หรือการใช้สวนสาธารณะ
            </div>
        """, unsafe_allow_html=True)

        user_question = st.text_area(
            "พิมพ์คำถามของคุณ",
            height=140
        )

        ask_button = st.button(
            "🤖 ถาม AI",
            type="primary",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if faq_button:
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

                st.markdown("""
                <div class="ai-answer-box">
                    <div class="small-title">📖 คำตอบจาก AI</div>
                """, unsafe_allow_html=True)

                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

    if ask_button:
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
หากเป็นคำถามทางการแพทย์เฉพาะทาง ให้แนะนำให้ปรึกษาแพทย์หรือผู้เชี่ยวชาญเพิ่มเติม
"""

            with st.spinner("AI กำลังคิดคำตอบ..."):
                try:
                    result = ask_ai(prompt)

                    st.markdown("""
                    <div class="ai-answer-box">
                        <div class="small-title">💬 คำตอบจาก AI</div>
                    """, unsafe_allow_html=True)

                    st.markdown(result)
                    st.markdown
