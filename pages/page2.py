import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb # 🦆 เติมพระเอกตัวใหม่ของอาจารย์เข้ามาตรงนี้
from pymongo import MongoClient
from scipy.spatial.distance import cdist

st.set_page_config(layout="wide")
st.title("🌲 Park Finder & Air Quality Monitor (with DuckDB)")
st.subheader("ค้นหาสวนสาธารณะที่เหมาะกับคุณ และเช็กค่าฝุ่น PM2.5 ล่าสุดก่อนออกไปวิ่ง")

# =====================================================================
# 1. DATABASE CONNECTIONS (MongoDB & Snowflake)
# =====================================================================

# แก้ไขเฉพาะช่วงนี้ในโค้ด Page 2 ของคุณนะครับสัด
import snowflake.connector

@st.cache_resource
def init_connections():
    # 1. เชื่อมต่อ MongoDB ตามปกติ
    mongo_client = MongoClient(st.secrets["MONGO_URI"])
    
    # 2. เชื่อมต่อ Snowflake ตรงๆ ผ่าน Connector แบบไม่ต้องง้อ st.connection
    # มันจะวิ่งไปดึงข้อมูลจากโครงสร้างกรุ๊ปที่คุณเขียนไว้ในหน้าเว็บ Secrets ทันที
    ctx = snowflake.connector.connect(
        user=st.secrets["connections"]["snowflake"]["user"],
        password=st.secrets["connections"]["snowflake"]["password"],
        account=st.secrets["connections"]["snowflake"]["account"],
        warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
        database=st.secrets["connections"]["snowflake"]["database"],
        schema=st.secrets["connections"]["snowflake"]["schema"],
        role=st.secrets["connections"]["snowflake"]["role"]
    )
    
    # ห่อคิวรีสคริปต์จำลอง เพื่อให้ฟังก์ชัน .query() ในโค้ดดั้งเดิมด้านล่างรันต่อได้แบบไม่ต้องรื้อโค้ดใหม่
    class SnowflakeWrapper:
        def __init__(self, connection):
            self.conn = connection
        def query(self, sql):
            return pd.read_sql(sql, self.conn)
            
    return mongo_client, SnowflakeWrapper(ctx)

# นำตัวแปรไปใช้งานต่อตามปกติ โค้ดด้านล่างใช้ได้เหมือนเดิมเป๊ะ!
mongo_client, sf_conn = init_connections()

# 🔴 !! อย่าลืมเปลี่ยนชื่อ Database ของคุณตรงนี้ !! 🔴
mongo_db = mongo_client["dads5001"] 
mongo_col = mongo_db["pm25"]

# =====================================================================
# 2. DATA FETCHING (MongoDB & Snowflake)
# =====================================================================

def refresh_and_get_pm25():
    api_url = "http://api.air4thai.com/forweb/getBKK_JSON.php"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            api_json_data = response.json()
            mongo_col.replace_one({"_id": "bkk_latest_air"}, api_json_data, upsert=True)
            air_data = api_json_data
        else:
            air_data = mongo_col.find_one({"_id": "bkk_latest_air"})
    except Exception:
        air_data = mongo_col.find_one({"_id": "bkk_latest_air"})
    
    stations_list = []
    if air_data and 'stations' in air_data:
        for station in air_data['stations']:
            try:
                pm25_val = station.get('aqi', {}).get('pm25', {}).get('value')
                stations_list.append({
                    'station_name': station.get('nameTH'),
                    'station_lat': float(station.get('lat')),
                    'station_lon': float(station.get('lng')),
                    'pm25': float(pm25_val) if pm25_val is not None else np.nan
                })
            except (ValueError, TypeError):
                continue
                
    return pd.DataFrame(stations_list)

@st.cache_data(ttl=600)
def load_snowflake_data():
    # ดึงตารางดิบแยกกันมาจาก Snowflake โดยยังไม่ต้อง Merge ในนี้ (เพราะเราจะไปโชว์พาว Merge ด้วย DuckDB แทน!)
    df_park = sf_conn.query("SELECT NAME, OPEN, CLOSE, TOILET, SPORTS_FIELD, RUNNING_TRACK, CAR_PARK, BICYCLE_PATH, PET_FRIENDLY FROM PARK")
    df_lat_long = sf_conn.query("SELECT PARK_NAME, LAT, LNG FROM PARK_LAT_LONG")
    df_dist = sf_conn.query("SELECT PARK_NAME, RUN_M FROM PARK_PATH_DISTANCE")
    
    df_bts = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM BTS")
    df_mrt = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM MRT")
    
    df_bts['TRAIN_TYPE'] = 'BTS'
    df_mrt['TRAIN_TYPE'] = 'MRT'
    df_trains = pd.concat([df_bts, df_mrt], ignore_index=True)
    
    return df_park, df_lat_long, df_dist, df_trains

# โหลดข้อมูลดิบเข้ามารอไว้ในหน่วยความจำในรูปแบบ DataFrame
df_stations_pm25 = refresh_and_get_pm25()
df_p, df_ll, df_d, df_trains = load_snowflake_data()

df_p.columns = [c.upper().strip() for c in df_p.columns]
df_ll.columns = [c.upper().strip() for c in df_ll.columns]
df_d.columns = [c.upper().strip() for c in df_d.columns]
df_trains.columns = [c.upper().strip() for c in df_trains.columns]




# =====================================================================
# 3. 🔥 DUCKDB INTEGRATION: MERGING DATA WITH SQL (เวอร์ชันเคลียร์พิมพ์ใหญ่)
# =====================================================================

duck_conn = duckdb.connect(database=':memory:')

duck_conn.register("park", df_p)
duck_conn.register("park_ll", df_ll)
duck_conn.register("park_dist", df_d)

df_parks_merged = duck_conn.execute("""
SELECT
    p.NAME,
    p.OPEN,
    p.CLOSE,
    p.TOILET,
    p.SPORTS_FIELD,
    p.RUNNING_TRACK,
    p.CAR_PARK,
    p.BICYCLE_PATH,
    p.PET_FRIENDLY,
    ll.LAT,
    ll.LNG,
    COALESCE(d.RUN_M,0) AS RUN_M
FROM park p
INNER JOIN park_ll ll
    ON p.NAME = ll.PARK_NAME
LEFT JOIN park_dist d
    ON p.NAME = d.PARK_NAME
""").df()

# =====================================================================
# 4. GEOSPATIAL CALCULATIONS (จับคู่พิกัดหา ฝุ่นที่ใกล้สุด & รถไฟฟ้าที่ใกล้สุด)
# =====================================================================

def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
    return r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

# จับคู่สถานีฝุ่นที่ใกล้ที่สุด
if not df_stations_pm25.empty:
    park_coords = df_parks_merged[['LAT', 'LNG']].values
    station_coords = df_stations_pm25[['station_lat', 'station_lon']].values
    dist_matrix_air = cdist(park_coords, station_coords)
    closest_air_indices = dist_matrix_air.argmin(axis=1)
    
    df_parks_merged['NEAREST_AIR_STATION'] = df_stations_pm25['station_name'].iloc[closest_air_indices].values
    df_parks_merged['LATEST_PM25'] = df_stations_pm25['pm25'].iloc[closest_air_indices].values
else:
    df_parks_merged['NEAREST_AIR_STATION'] = "ไม่สามารถดึงข้อมูลได้"
    df_parks_merged['LATEST_PM25'] = np.nan

# คำนวณหาระยะทางจากสวนไปสถานีรถไฟฟ้าที่ใกล้ที่สุด
min_train_distances = []
nearest_train_stations = []

for idx, row in df_parks_merged.iterrows():
    distances_to_trains = haversine_distance(row['LAT'], row['LNG'], df_trains['LAT'], df_trains['LNG'])
    min_idx = distances_to_trains.idxmin()
    min_train_distances.append(distances_to_trains[min_idx])
    nearest_train_stations.append(f"{df_trains.loc[min_idx, 'STATION_NAME']} ({df_trains.loc[min_idx, 'TRAIN_TYPE']})")

df_parks_merged['DIST_TO_TRAIN_KM'] = min_train_distances
df_parks_merged['NEAREST_TRAIN_STATION'] = nearest_train_stations

# แบ่งกลุ่มระยะทางจากรถไฟฟ้าเป็นเมตร
def categorize_train_distance(km):
    meters = km * 1000
    if meters < 500: return "น้อยกว่า 500 เมตร"
    elif 500 <= meters <= 1500: return "500 ม. - 1.5 กม."
    else: return "มากกว่า 1.5 กม."

df_parks_merged['TRAIN_DIST_CATEGORY'] = df_parks_merged['DIST_TO_TRAIN_KM'].apply(categorize_train_distance)

# =====================================================================
# 5. SIDEBAR FILTERS (รับค่าจากหน้าเว็บ)
# =====================================================================

st.sidebar.header("🔍 คัดกรองสวนสาธารณะ")

train_dist_filter = st.sidebar.multiselect(
    "ระยะทางจากสถานีรถไฟฟ้า (BTS/MRT):",
    options=["น้อยกว่า 500 เมตร", "500 ม. - 1.5 กม.", "มากกว่า 1.5 กม."],
    default=["น้อยกว่า 500 เมตร", "500 ม. - 1.5 กม.", "มากกว่า 1.5 กม."]
)

st.sidebar.subheader("🎯 สิ่งอำนวยความสะดวกที่ต้องการ:")
filter_toilet = 1 if st.sidebar.checkbox("ห้องน้ำ (Toilet)") else 0
filter_sports = 1 if st.sidebar.checkbox("ลานกีฬา (Sports field)") else 0
filter_running = 1 if st.sidebar.checkbox("ลู่วิ่ง (Running track)") else 0
filter_car = 1 if st.sidebar.checkbox("ที่จอดรถ (Car park)") else 0
filter_bike = 1 if st.sidebar.checkbox("ทางจักรยาน (Bicycle path)") else 0
filter_pet = 1 if st.sidebar.checkbox("สวนสัตว์เลี้ยงเข้าได้ (Pet park)") else 0

# =====================================================================
# 6. 🔥 DUCKDB INTEGRATION: ADVANCED FILTERING WITH SQL
# =====================================================================
# ใช้ DuckDB ทำการคัดกรองสวนสาธารณะตามเงื่อนไขที่ผู้ใช้เลือกผ่านหน้าเว็บแทนการใช้ Pandas Filter

# เตรียมสร้างคำสั่ง WHERE Clause แบบไดนามิกตามที่ผู้ใช้ติ๊กเลือก
where_clauses = ["TRAIN_DIST_CATEGORY IN (SELECT * FROM UNNEST(?))"]
param_list = [train_dist_filter]

if filter_toilet:  where_clauses.append("TOILET = 1")
if filter_sports:  where_clauses.append("SPORTS_FIELD = 1")
if filter_running: where_clauses.append("RUNNING_TRACK = 1")
if filter_car:     where_clauses.append("CAR_PARK = 1")
if filter_bike:    where_clauses.append("BICYCLE_PATH = 1")
if filter_pet:     where_clauses.append("PET_FRIENDLY = 1")

query_string = f"SELECT * FROM df_parks_merged WHERE " + " AND ".join(where_clauses)

# สั่งคิวรีผลลัพธ์ผ่าน DuckDB ดึงผลลัพธ์สุดท้ายออกมาใช้งาน
df_filtered = duck_conn.execute(query_string, param_list).df()

# =====================================================================
# 7. DASHBOARD LAYOUT & PLOTLY MAP VISUALIZATION
# =====================================================================

col_map, col_list = st.columns([2, 1])

with col_map:
    st.write(f"📊 พบสวนสาธารณะตรงตามเงื่อนไขทั้งหมด **{len(df_filtered)}** แห่ง (ประมวลผลผ่าน DuckDB)")
    
    if not df_filtered.empty:
        df_map_show = df_filtered.copy()
        amenities_cols = ['TOILET', 'SPORTS_FIELD', 'RUNNING_TRACK', 'CAR_PARK', 'BICYCLE_PATH', 'PET_FRIENDLY']
        for col in amenities_cols:
            df_map_show[col] = df_map_show[col].map({1: "✅ มี", 0: "❌ ไม่มี"})
            
        fig = px.scatter_mapbox(
            df_map_show,
            lat="LAT",
            lon="LNG",
            hover_name="NAME",
            hover_data={
                "LATEST_PM25": True,
                "NEAREST_AIR_STATION": True,
                "RUN_M": ":,.0f เมตร",
                "TOILET": True,
                "SPORTS_FIELD": True,
                "RUNNING_TRACK": True,
                "CAR_PARK": True,
                "BICYCLE_PATH": True,
                "PET_FRIENDLY": True,
                "NEAREST_TRAIN_STATION": True,
                "LAT": False,
                "LNG": False
            },
            color="LATEST_PM25",
            color_continuous_scale="Reds",
            size_max=15,
            zoom=11,
            height=650
        )
        
        fig.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ ไม่พบสวนสาธารณะตามเงื่อนไขที่เลือก")

with col_list:
    st.write("📋 **รายชื่อสวนสาธารณะที่ค้นพบ**")
    
    if not df_filtered.empty:
        for _, park in df_filtered.iterrows():
            with st.expander(f"🌳 {park['NAME']}"):
                st.markdown(f"**⏰ เวลาเปิด-ปิด:** {park['OPEN']} - {park['CLOSE']}")
                st.metric(
                    label=f"😷 PM2.5 ล่าสุด ({park['NEAREST_AIR_STATION']})", 
                    value=f"{park['LATEST_PM25']} µg/m³" if not pd.isna(park['LATEST_PM25']) else "N/A"
                )
                st.write(f"🏃 **ระยะทางลู่วิ่ง:** {park['RUN_M']:,} เมตร")
                st.write(f"🚇 **สถานีใกล้สุด:** {park['NEAREST_TRAIN_STATION']} ({park['DIST_TO_TRAIN_KM']*1000:.0f} เมตร)")
                
                amenity_list = []
                if park['TOILET'] == 1: amenity_list.append("🚽 ห้องน้ำ")
                if park['SPORTS_FIELD'] == 1: amenity_list.append("⚽ ลานกีฬา")
                if park['RUNNING_TRACK'] == 1: amenity_list.append("🏃 ลู่วิ่ง")
                if park['CAR_PARK'] == 1: amenity_list.append("🚗 ที่จอดรถ")
                if park['BICYCLE_PATH'] == 1: amenity_list.append("🚴 ทางจักรยาน")
                if park['PET_FRIENDLY'] == 1: amenity_list.append("🐶 สัตว์เลี้ยงเข้าได้")
                
                st.write("**🧩 สิ่งอำนวยความสะดวกที่มี:**")
                st.caption(" | ".join(amenity_list) if amenity_list else "ไม่มีสิ่งอำนวยความสะดวกพิเศษ")
