import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.spatial.distance import cdist

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Analytics - Public Transport", layout="wide")

st.title("📊 Page 3: Analytics - Public Transport Connectivity")
st.write("วิเคราะห์ความสัมพันธ์ระหว่างขนาดของสวนสาธารณะ ระยะห่างจากระบบขนส่งมวลชน (BTS/MRT) และความหนาแน่นของผู้ใช้งาน")

# =====================================================================
# 1. DATABASE CONNECTION & DATA LOADING (Snowflake)
# =====================================================================
@st.cache_data(ttl=600)
def load_analytics_data():
    # ดึงข้อมูลจาก Snowflake บังคับฟิลด์ที่ต้องใช้ในการคำนวณ
    df_park = sf_conn.query("SELECT NAME, AREA_RAI, USAGE_DENSITY FROM PARK")
    df_lat_long = sf_conn.query("SELECT PARK_NAME, LAT, LNG FROM PARK_LAT_LONG")
    
    df_bts = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM BTS")
    df_mrt = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM MRT")
    
    # ล้างคราบเครื่องหมายคำพูดคู่และแปลงเป็นพิมพ์ใหญ่ทันทีต้นทาง
    df_park.columns = [c.replace('"', '').upper().strip() for c in df_park.columns]
    df_lat_long.columns = [c.replace('"', '').upper().strip() for c in df_lat_long.columns]
    df_bts.columns = [c.replace('"', '').upper().strip() for c in df_bts.columns]
    df_mrt.columns = [c.replace('"', '').upper().strip() for c in df_mrt.columns]
    
    # รวมตารางรถไฟฟ้า BTS และ MRT
    df_bts['TRAIN_TYPE'] = 'BTS'
    df_mrt['TRAIN_TYPE'] = 'MRT'
    df_trains = pd.concat([df_bts, df_mrt], ignore_index=True)
    
    return df_park, df_lat_long, df_trains

try:
    df_p, df_ll, df_trains = load_analytics_data()
    
    # ป้องกันเรื่องชื่อคอลหักไม่ตรงกัน โดยการอ้างอิงอิงตามตำแหน่ง Index แรก (เหมือนหน้า 2)
    df_analytics = df_p.merge(df_ll, left_on=df_p.columns[0], right_on=df_ll.columns[0], how='inner')
    
    # =====================================================================
    # 2. GEOSPATIAL CALCULATIONS (ใช้ Pandas คำนวณเพียวๆ ไร้ DuckDB)
    # =====================================================================
    def haversine_distance(lat1, lon1, lat2, lon2):
        r = 6371  # รัศมีโลก (กิโลเมตร)
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        return r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

    min_distances_m = []
    for idx, row in df_analytics.iterrows():
        distances = haversine_distance(row['LAT'], row['LNG'], df_trains['LAT'], df_trains['LNG'])
        min_distances_m.append(distances.min() * 1000)  # แปลงกิโลเมตรเป็นเมตร
        
    df_analytics['DIST_TO_TRAIN_M'] = min_distances_m

    # จัดกลุ่มความใกล้-ไกลจากสถานีรถไฟฟ้าตามเกณฑ์
    def categorize_distance(meters):
        if meters < 500: return "ใกล้ (น้อยกว่า 500 เมตร)"
        elif 500 <= meters <= 1500: return "ปานกลาง (500 ม. - 1.5 กม.)"
        else: return "ไกล (มากกว่า 1.5 กม.)"

    df_analytics['DISTANCE_CATEGORY'] = df_analytics['DIST_TO_TRAIN_M'].apply(categorize_distance)

    # =====================================================================
    # 3. VISUALIZATION LAYOUT
    # =====================================================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 ขนาดของสวน vs ระยะห่างจากสถานีรถไฟฟ้า")
        
        # วาด Scatter Plot ตรวจสอบสมมติฐาน
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
            color_discrete_sequence=px.colors.qualitative.Safe,
            title="ความสัมพันธ์ของขนาดสวน พิกัดราง และความหนาแน่น"
        )
        fig_scatter.update_layout(template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("🍕 สัดส่วนระยะห่างของสวนทั้งหมดจาก BTS/MRT")
        st.write("") 
        
        # นับจำนวนสวนเพื่อทำ Pie Chart
        df_pie = df_analytics['DISTANCE_CATEGORY'].value_counts().reset_index()
        df_pie.columns = ['🔄 ระดับความใกล้', '📊 จำนวนสวน']
        
        fig_pie = px.pie(
            df_pie,
            values="📊 จำนวนสวน",
            names="🔄 ระดับความใกล้",
            hole=0.4,  # ทำเป็น Donut Chart ทรงทันสมัย
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="การกระจายตัวตามเกณฑ์ระยะทางเดินเท้าสู่รถไฟฟ้า"
        )
        fig_pie.update_layout(template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)

    # แสดงตารางสรุปข้อมูลด้านล่างเชิงวิเคราะห์
    st.subheader("📋 ตารางสรุปข้อมูลเชิงวิเคราะห์เพื่อตรวจสอบสมมติฐาน")
    st.dataframe(
        df_analytics
