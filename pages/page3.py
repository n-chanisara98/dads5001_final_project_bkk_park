import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import snowflake.connector
from scipy.spatial.distance import cdist

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Analytics - Public Transport", layout="wide")

st.title("📊 Page 3: Analytics - Public Transport Connectivity")
st.write("วิเคราะห์ความสัมพันธ์ระหว่างขนาดของสวนสาธารณะ ระยะห่างจากระบบขนส่งมวลชน (BTS/MRT) และความหนาแน่นของผู้ใช้งาน")

# =====================================================================
# 1. DATABASE CONNECTION (ดึงค่าปลอดภัยผ่าน st.secrets แบบเดียวกับหน้า 2)
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

# เรียกใช้งานการเชื่อมต่อสำหรับหน้า 3
try:
    sf_conn = init_snowflake_connection()
except Exception as e:
    st.error(f"❌ ไม่สามารถเชื่อมต่อ Snowflake ได้: {e}")
    st.stop()

# =====================================================================
# 2. DATA LOADING & CLEANING
# =====================================================================
@st.cache_data(ttl=600)
def load_analytics_data():
    df_park = sf_conn.query("SELECT NAME, AREA_RAI, USAGE_DENSITY FROM PARK")
    df_lat_long = sf_conn.query("SELECT PARK_NAME, LAT, LNG FROM PARK_LAT_LONG")
    df_bts = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM BTS")
    df_mrt = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM MRT")
    
    # ล้างคราบเครื่องหมายคำพูดและทำเป็นพิมพ์ใหญ่
    df_park.columns = [c.replace('"', '').upper().strip() for c in df_park.columns]
    df_lat_long.columns = [c.replace('"', '').upper().strip() for c in df_lat_long.columns]
    df_bts.columns = [c.replace('"', '').upper().strip() for c in df_bts.columns]
    df_mrt.columns = [c.replace('"', '').upper().strip() for c in df_mrt.columns]
    
    df_bts['TRAIN_TYPE'] = 'BTS'
    df_mrt['TRAIN_TYPE'] = 'MRT'
    df_trains = pd.concat([df_bts, df_mrt], ignore_index=True)
    
    return df_park, df_lat_long, df_trains

try:
    df_p, df_ll, df_trains = load_analytics_data()
    
    # รวมร่างตารางสวนกับพิกัด อ้างอิงตามตำแหน่ง Index แรกเพื่อความชัวร์
    df_analytics = df_p.merge(df_ll, left_on=df_p.columns[0], right_on=df_ll.columns[0], how='inner')
    
    # =====================================================================
    # 3. GEOSPATIAL CALCULATIONS (คำนวณระยะทางไปสถานีรถไฟฟ้า)
    # =====================================================================
    def haversine_distance(lat1, lon1, lat2, lon2):
        r = 6371
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        return r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

    min_distances_m = []
    for idx, row in df_analytics.iterrows():
        distances = haversine_distance(row['LAT'], row['LNG'], df_trains['LAT'], df_trains['LNG'])
        min_distances_m.append(distances.min() * 1000)
        
    df_analytics['DIST_TO_TRAIN_M'] = min_distances_m

    def categorize_distance(meters):
        if meters < 500: return "ใกล้ (น้อยกว่า 500 เมตร)"
        elif 500 <= meters <= 1500: return "ปานกลาง (500 ม. - 1.5 กม.)"
        else: return "ไกล (มากกว่า 1.5 กม.)"

    df_analytics['DISTANCE_CATEGORY'] = df_analytics['DIST_TO_TRAIN_M'].apply(categorize_distance)

    # =====================================================================
    # 4. VISUALIZATIONS
    # =====================================================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 ขนาดของสวน vs ระยะห่างจากสถานีรถไฟฟ้า")
        fig_scatter = px.scatter(
            df_analytics,
            x="DIST_TO_TRAIN_M",
            y="AREA_RAI",
            color="USAGE_DENSITY",
            hover_name="NAME",
            labels={
                "DIST_TO_TRAIN_M": "ระยะห่างจากสถานีรถไฟฟ้า (เมตร)",
                "AREA_RAI": "ขนาดพื้นที่สวน (ไร่)",
                "USAGE_DENSITY": "ความหนาแน่นผู้ใช้งาน"
            },
            title="ความสัมพันธ์ของขนาดสวน พิกัดราง และความหนาแน่น"
        )
        fig_scatter.update_layout(template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("🍕 สัดส่วนระยะห่างของสวนทั้งหมดจาก BTS/MRT")
        df_pie = df_analytics['DISTANCE_CATEGORY'].value_counts().reset_index()
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
        df_analytics[['NAME', 'AREA_RAI', 'DIST_TO_TRAIN_M', 'DISTANCE_CATEGORY', 'USAGE_DENSITY']].sort_values(by="AREA_RAI", ascending=False),
        use_container_width=True
    )

except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการรันหน้าวิเคราะห์: {e}")
