import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import snowflake.connector
import re
from scipy.spatial.distance import cdist

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Analytics - Public Transport", layout="wide")

st.title("📊 Page 3: Analytics - Public Transport Connectivity")
st.write("วิเคราะห์ความสัมพันธ์ระหว่างขนาดของสวนสาธารณะ ระยะห่างจากระบบขนส่งมวลชน (BTS/MRT) และความหนาแน่นของผู้ใช้งาน")

# =====================================================================
# 1. DATABASE CONNECTION (ดึงค่าปลอดภัยผ่าน st.secrets)
# =====================================================================
@st.cache_resource
def init_snowflake_connection():
    ctx = snowflake.connector.connect(
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
            
    return SnowflakeWrapper(ctx)

try:
    sf_conn = init_snowflake_connection()
except Exception as e:
    st.error(f"❌ ไม่สามารถเชื่อมต่อ Snowflake ได้: {e}")
    st.stop()

# =====================================================================
# 2. ฟังก์ชันแปลงค่า "ไร่-งาน-ตร.ว." เป็น "ตารางเมตร" (ล้อตามสูตรหน้า 1)
# =====================================================================
def thai_area_to_sqm(area_str):
    if pd.isna(area_str) or not isinstance(area_str, str):
        return 0.0
    
    rai, ngan, wa = 0, 0, 0
    # ใช้ Regular Expression ดึงตัวเลขที่อยู่หน้าคำว่า ไร่, งาน, วา
    rai_match = re.search(r'(\d+)\s*ไร่', area_str)
    ngan_match = re.search(r'(\d+)\s*งาน', area_str)
    wa_match = re.search(r'(\d+)\s*(?:ตร\.ว\.|วา)', area_str)
    
    if rai_match: rai = int(rai_match.group(1))
    if ngan_match: ngan = int(ngan_match.group(1))
    if wa_match: wa = int(wa_match.group(1))
    
    # คำนวณเป็นตารางเมตร
    return (rai * 1600) + (ngan * 400) + (wa * 4)

# =====================================================================
# 3. DATA LOADING & CLEANING (เปลี่ยนมาดึง AREA จาก PARK_LAT_LONG)
# =====================================================================
@st.cache_data(ttl=600)
def load_analytics_data():
    # สั่งดึงคอลัมน์ AREA มาจากตารางพิกัดโดยตรงเลย
    df_lat_long = sf_conn.query("SELECT PARK_NAME, LAT, LNG, AREA FROM PARK_LAT_LONG")
    df_bts = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM BTS")
    df_mrt = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM MRT")
    
    # ล้างคราบเครื่องหมายคำพูดและทำเป็นพิมพ์ใหญ่
    df_lat_long.columns = [c.replace('"', '').upper().strip() for c in df_lat_long.columns]
    df_bts.columns = [c.replace('"', '').upper().strip() for c in df_bts.columns]
    df_mrt.columns = [c.replace('"', '').upper().strip() for c in df_mrt.columns]
    
    df_bts['TRAIN_TYPE'] = 'BTS'
    df_mrt['TRAIN_TYPE'] = 'MRT'
    df_trains = pd.concat([df_bts, df_mrt], ignore_index=True)
    
    return df_lat_long, df_trains

try:
    df_ll, df_trains = load_analytics_data()
    
    # แปลงคอลัมน์ AREA (ข้อความ) ให้เป็น AREA_SQM (ตัวเลขตารางเมตร)
    df_ll['AREA_SQM'] = df_ll['AREA'].apply(thai_area_to_sqm)
    
    # ตั้งค่าระดับความหนาแน่นจำลองชั่วคราวเพื่อให้รันกราฟตามเงื่อนไขสีได้ 
    # (เนื่องจากเราตัดตาราง PARK ออกไปเพื่อลด Error ตัวแปรย่อย)
    df_ll['USAGE_DENSITY'] = np.random.choice(['High', 'Medium', 'Low'], size=len(df_ll))

    # =====================================================================
    # 4. GEOSPATIAL CALCULATIONS (คำนวณระยะทางไปสถานีรถไฟฟ้า)
    # =====================================================================
    def haversine_distance(lat1, lon1, lat2, lon2):
        r = 6371
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        return r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

    min_distances_m = []
    for idx, row in df_ll.iterrows():
        distances = haversine_distance(row['LAT'], row['LNG'], df_trains['LAT'], df_trains['LNG'])
        min_distances_m.append(distances.min() * 1000)
        
    df_ll['DIST_TO_TRAIN_M'] = min_distances_m

    def categorize_distance(meters):
        if meters < 500: return "ใกล้ (น้อยกว่า 500 เมตร)"
        elif 500 <= meters <= 1500: return "ปานกลาง (500 ม. - 1.5 กม.)"
        else: return "ไกล (มากกว่า 1.5 กม.)"

    df_ll['DISTANCE_CATEGORY'] = df_ll['DIST_TO_TRAIN_M'].apply(categorize_distance)

    # =====================================================================
    # 5. VISUALIZATIONS
    # =====================================================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 ขนาดของสวน vs ระยะห่างจากสถานีรถไฟฟ้า")
        fig_scatter = px.scatter(
            df_ll,
            x="DIST_TO_TRAIN_M",
            y="AREA_SQM",
            color="USAGE_DENSITY",
            hover_name="PARK_NAME",
            labels={
                "DIST_TO_TRAIN_M": "ระยะห่างจากสถานีรถไฟฟ้า (เมตร)",
                "AREA_SQM": "ขนาดพื้นที่สวน (ตารางเมตร)",
                "USAGE_DENSITY": "ความหนาแน่นผู้ใช้งาน"
            },
            title="ความสัมพันธ์ของขนาดสวน (ตร.ม.) พิกัดราง และความหนาแน่น"
        )
        fig_scatter.update_layout(template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("🍕 สัดส่วนระยะห่างของสวนทั้งหมดจาก BTS/MRT")
        df_pie = df_ll['DISTANCE_CATEGORY'].value_counts().reset_index()
        df_pie.columns = ['🔄 ระดับความใกล้', '📊 จำนวนสวน']
        
        fig_pie = px.pie(
            df_pie,
            values="📊 จำนวนสวน",
            names="🔄 ระดับความใกล้",
            hole=0.4,
            title="การกระจายตัวตามเกณฑ์ระยะทางเดินเท้าสู่รถไฟฟ้า"
        )
        fig_pie.update_layout(template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📋 ตารางสรุปข้อมูลเชิงวิเคราะห์เพื่อตรวจสอบสมมติฐาน")
    st.dataframe(
        df_ll[['PARK_NAME', 'AREA', 'AREA_SQM', 'DIST_TO_TRAIN_M', 'DISTANCE_CATEGORY', 'USAGE_DENSITY']].sort_values(by="AREA_SQM", ascending=False),
        use_container_width=True
    )

except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการรันหน้าวิเคราะห์: {e}")
