import streamlit as st
import snowflake.connector
import pandas as pd

# 1. ฟังก์ชันเชื่อมต่อ Snowflake โดยดึงค่าจาก Secrets
def init_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

# 2. หัวข้อเว็บ
st.title("📊 BKK Park Analytics")
st.write("Hello Page 1 - หน้านี้ของ [ชื่อเพื่อนคนที่ 1] สำหรับวิเคราะห์ข้อมูล")
st.subheader("Connection Test Result")

try:
    # 3. ยิงคิวรีไปนับจำนวนแถวในตาราง Park
    conn = init_connection()
    query = "SELECT COUNT(*) FROM PARK"
    
    # ดึงข้อมูลมาใส่ Pandas DataFrame
    df = pd.read_sql(query, conn)
    total_parks = df.iloc[0, 0] # ดึงตัวเลขผลลัพธ์ตัวแรกออกมา
    
    # 4. สร้าง Score Card แสดงผลแบบตัวเลขเด่น ๆ
    st.success("เชื่อมต่อกับ Snowflake สำเร็จแล้ว! 🎉")
    st.metric(label="จำนวนสวนสาธารณะทั้งหมดในกรุงเทพฯ", value=f"{total_parks} สวน")

except Exception as e:
    # ถ้าต่อไม่ติดหรือพิมพ์ชื่อตารางผิด มันจะฟ้องส้ม ๆ แดง ๆ ทันที
    st.error("เกิดข้อผิดพลาดในการเชื่อมต่อ Snowflake")
    st.write(e)
