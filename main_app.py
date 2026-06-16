import streamlit as st

st.set_page_config(page_title="ASEAN Urban & Air Quality Dashboard", layout="wide")

st.title("🏙️ ASEAN Urban Growth & Air Quality Project")
st.write("ยินดีต้อนรับเข้าสู่แดชบอร์ดวิเคราะห์ข้อมูลเมือง พิกัดสวนสาธารณะ และค่าฝุ่น PM2.5")

st.info("👈 กรุณาเลือกหน้าต่างที่ต้องการวิเคราะห์จากเมนูด้านซ้ายได้เลยครับ")

# แอบใส่คำแนะนำเชื่อมต่อ Database ทิ้งไว้ให้เพื่อนในกลุ่มดู
st.subheader("🛠️ Database Connection Guides for Team")
st.code("""
# วิธีดึงข้อมูลจาก MongoDB (ค่าฝุ่นรายชั่วโมง)
import pymongo
# client = pymongo.MongoClient(st.secrets["MONGO_URI"])

# วิธีดึงข้อมูลจาก Snowflake (ข้อมูลประชากร เมือง และสวนสาธารณะ)
import snowflake.connector
# conn = snowflake.connector.connect(**st.secrets["snowflake"])
""", language="python")
