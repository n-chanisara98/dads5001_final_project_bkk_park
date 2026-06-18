import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
from pymongo import MongoClient
from scipy.spatial.distance import cdist
import snowflake.connector

st.set_page_config(
    page_title="Park Finder & Air Quality",
    page_icon="🌳",
    layout="wide"
)

# =====================================================================
# 0. GLOBAL STYLE
# =====================================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FFF8E7 0%, #EAF6EF 45%, #FDE7D6 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00492C 0%, #1E4380 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stMultiSelect div,
    section[data-testid="stSidebar"] .stSelectbox div {
        color: #00492C !important;
    }

    .hero-box {
        background:
            linear-gradient(120deg, rgba(0,73,44,0.93), rgba(30,67,128,0.70)),
            url("https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=1800&q=80");
        background-size: cover;
        background-position: center;
        padding: 46px 50px;
        border-radius: 32px;
        color: white;
        box-shadow: 0 18px 45px rgba(0,73,44,0.18);
        margin-bottom: 28px;
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
        opacity: 0.95;
        max-width: 980px;
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

    .kpi-card {
        background: rgba(255,255,255,0.90);
        padding: 24px 26px;
        border-radius: 26px;
        box-shadow: 0 12px 30px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        min-height: 145px;
    }

    .kpi-label {
        font-size: 14px;
        color: #51635A;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .kpi-value {
        font-size: 34px;
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
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .map-card {
        background: rgba(255,255,255,0.92);
        border-radius: 28px;
        padding: 22px 24px 24px 24px;
        box-shadow: 0 14px 34px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        margin-bottom: 28px;
    }

    .list-card {
        background: rgba(255,255,255,0.92);
        border-radius: 28px;
        padding: 22px 24px;
        box-shadow: 0 14px 34px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        margin-bottom: 28px;
    }

    .small-title {
        font-size: 21px;
        font-weight: 900;
        color: #00492C;
        margin-bottom: 6px;
    }

    .desc-text {
        color: #66746B;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    .insight-box {
        background: linear-gradient(90deg, #FBBA16 0%, #B1D8B8 100%);
        padding: 22px 28px;
        border-radius: 26px;
        margin-top: 28px;
        margin-bottom: 30px;
        box-shadow: 0 10px 26px rgba(0,73,44,0.12);
        color: #00492C;
        font-size: 20px;
        font-weight: 750;
    }

    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.90);
        border-radius: 18px !important;
        border: 1px solid rgba(0,73,44,0.14) !important;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 1. DATABASE CONNECTIONS
# =====================================================================
@st.cache_resource
def init_connections():
    mongo_client = MongoClient(st.secrets["MONGO_URI"])

    ctx = snowflake.connector.connect(
        user=st.secrets["connections"]["snowflake"]["user"],
        password=st.secrets["connections"]["snowflake"]["password"],
        account=st.secrets["connections"]["snowflake"]["account"],
        warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
        database=st.secrets["connections"]["snowflake"]["database"],
        schema=st.secrets["connections"]["snowflake"]["schema"],
        role=st.secrets["connections"]["snowflake"]["role"],
        client_session_keep_alive=True  # สั่งเปิดท่อ connect ค้างไว้ไม่ให้หมดอายุ
    )

    # 🛡️ ชุบชีวิต Wrapper ตัวดั้งเดิมของพวกคุณ ให้ฉลาดดักจับสายหลุดได้เองอัตโนมัติ
    class SnowflakeWrapper:
        def __init__(self, connection):
            self.conn = connection

        def query(self, sql):
            try:
                # ถ้าสายปิด หรือหมดอายุ ให้แอบล้างแคชเก่าแล้วเปิดสายใหม่ทันที
                if self.conn.is_closed():
                    st.cache_resource.clear()
                    # สั่งสร้างการเชื่อมต่อขึ้นมาใหม่แบบไร้รอยต่อ
                    mongo_client_new, sf_wrapper_new = init_connections()
                    self.conn = sf_wrapper_new.conn
                return pd.read_sql(sql, self.conn)
            except Exception:
                # แผนสำรองสุดท้าย: บังคับเปิดท่อใหม่ดื้อๆ ป้องกันหน้าแดง
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

    return mongo_client, SnowflakeWrapper(ctx)


mongo_client, sf_conn = init_connections()
mongo_db = mongo_client["dads5001"]
mongo_col = mongo_db["pm25"]

# =====================================================================
# 2. DATA FETCHING
# =====================================================================
def refresh_and_get_pm25():
    api_url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php?region=1"

    try:
        response = requests.get(api_url, timeout=5, verify=False)
        if response.status_code == 200:
            api_json_data = response.json()
            mongo_col.replace_one({"_id": "bkk_latest_air"}, api_json_data, upsert=True)
            air_data = api_json_data
        else:
            air_data = mongo_col.find_one({"_id": "bkk_latest_air"})
    except Exception:
        air_data = mongo_col.find_one({"_id": "bkk_latest_air"})

    stations_list = []

    if air_data and "stations" in air_data:
        for station in air_data["stations"]:
            try:
                aqi_last = station.get("AQILast", {})
                pm25_dict = aqi_last.get("PM25", {}) if isinstance(aqi_last, dict) else {}
                pm25_val = pm25_dict.get("value") if isinstance(pm25_dict, dict) else None

                # ดึงค่าวันที่และเวลาของสถานีนี้ออกมาก่อน append
                aqi_last = station.get("AQILast", {})
                meas_date = aqi_last.get("date", "ไม่ระบุ")
                meas_time = aqi_last.get("time", "ไม่ระบุ")
                
                stations_list.append({
                    "station_name": station.get("nameTH"),
                    "station_lat": float(station.get("lat")),
                    "station_lon": float(station.get("long")),
                    "pm25": float(pm25_val) if pm25_val is not None and str(pm25_val).strip() != "-1" else np.nan,
                    "updated_time": f"{meas_date} {meas_time}"
                })

            except (ValueError, TypeError, AttributeError):
                continue

    return pd.DataFrame(stations_list)


@st.cache_data(ttl=600)
def load_snowflake_data():
    df_park = sf_conn.query("""
        SELECT NAME, OPEN, CLOSE, TOILET, SPORTS_FIELD, RUNNING_TRACK,
               CAR_PARK, BICYCLE_PATH, PET_FRIENDLY
        FROM PARK
    """)

    df_lat_long = sf_conn.query("SELECT PARK_NAME, LAT, LNG FROM PARK_LAT_LONG")
    df_dist = sf_conn.query("SELECT PARK_NAME, RUN_M FROM PARK_PATH_DISTANCE")

    df_bts = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM BTS")
    df_mrt = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM MRT")

    df_bts["TRAIN_TYPE"] = "BTS"
    df_mrt["TRAIN_TYPE"] = "MRT"
    df_trains = pd.concat([df_bts, df_mrt], ignore_index=True)

    return df_park, df_lat_long, df_dist, df_trains


df_stations_pm25 = refresh_and_get_pm25()
df_p, df_ll, df_d, df_trains = load_snowflake_data()

# =====================================================================
# 3. DUCKDB MERGING
# =====================================================================
df_pandas_merged = df_p.merge(
    df_ll,
    left_on=df_p.columns[0],
    right_on=df_ll.columns[0],
    how="inner"
)

df_pandas_merged = df_pandas_merged.merge(
    df_d,
    left_on=df_pandas_merged.columns[0],
    right_on=df_d.columns[0],
    how="left"
)

if "RUN_M" in df_pandas_merged.columns:
    df_pandas_merged["RUN_M"] = df_pandas_merged["RUN_M"].fillna(0)
else:
    df_pandas_merged["RUN_M"] = 0

duck_conn = duckdb.connect(database=":memory:")
duck_conn.register("pandas_table", df_pandas_merged)

df_parks_merged = duck_conn.execute("SELECT * FROM pandas_table").df()
duck_conn.register("parks", df_parks_merged)

# =====================================================================
# 4. GEOSPATIAL CALCULATIONS
# =====================================================================
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = (
        np.sin(delta_phi / 2) ** 2
        + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    )

    return r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))


if not df_stations_pm25.empty and not df_parks_merged.empty:
    park_coords = df_parks_merged[["LAT", "LNG"]].values
    station_coords = df_stations_pm25[["station_lat", "station_lon"]].values

    dist_matrix_air = cdist(park_coords, station_coords)
    closest_air_indices = dist_matrix_air.argmin(axis=1)

    df_parks_merged["NEAREST_AIR_STATION"] = df_stations_pm25["station_name"].iloc[closest_air_indices].values
    df_parks_merged["LATEST_PM25"] = df_stations_pm25["pm25"].iloc[closest_air_indices].values
    df_parks_merged["AIR_UPDATED_TIME"] = df_stations_pm25["updated_time"].iloc[closest_air_indices].values
else:
    df_parks_merged["NEAREST_AIR_STATION"] = "ไม่มีข้อมูลสถานี"
    df_parks_merged["LATEST_PM25"] = np.nan
    df_parks_merged["AIR_UPDATED_TIME"] = "ไม่มีข้อมูล"


min_train_distances = []
nearest_train_stations = []

for idx, row in df_parks_merged.iterrows():
    distances_to_trains = haversine_distance(
        row["LAT"],
        row["LNG"],
        df_trains["LAT"],
        df_trains["LNG"]
    )

    min_idx = distances_to_trains.idxmin()
    min_train_distances.append(distances_to_trains[min_idx])
    nearest_train_stations.append(
        f"{df_trains.loc[min_idx, 'STATION_NAME']} ({df_trains.loc[min_idx, 'TRAIN_TYPE']})"
    )

df_parks_merged["DIST_TO_TRAIN_KM"] = min_train_distances
df_parks_merged["NEAREST_TRAIN_STATION"] = nearest_train_stations


def categorize_train_distance(km):
    meters = km * 1000

    if meters < 500:
        return "น้อยกว่า 500 เมตร"
    elif 500 <= meters <= 1500:
        return "500 ม. - 1.5 กม."
    else:
        return "มากกว่า 1.5 กม."


df_parks_merged["TRAIN_DIST_CATEGORY"] = df_parks_merged["DIST_TO_TRAIN_KM"].apply(categorize_train_distance)
duck_conn.register("parks", df_parks_merged)

# =====================================================================
# 5. SIDEBAR FILTERS
# =====================================================================
st.sidebar.markdown("## 🔍 คัดกรองสวนสาธารณะ")
st.sidebar.markdown("เลือกสวนตามระยะรถไฟฟ้าและสิ่งอำนวยความสะดวกที่ต้องการ")

train_dist_filter = st.sidebar.multiselect(
    "ระยะทางจากสถานีรถไฟฟ้า (BTS/MRT):",
    options=["น้อยกว่า 500 เมตร", "500 ม. - 1.5 กม.", "มากกว่า 1.5 กม."],
    default=["น้อยกว่า 500 เมตร", "500 ม. - 1.5 กม.", "มากกว่า 1.5 กม."]
)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎯 สิ่งอำนวยความสะดวก")

filter_toilet = 1 if st.sidebar.checkbox("🚽 ห้องน้ำ (Toilet)") else 0
filter_sports = 1 if st.sidebar.checkbox("⚽ ลานกีฬา (Sports field)") else 0
filter_running = 1 if st.sidebar.checkbox("🏃 ลู่วิ่ง (Running track)") else 0
filter_car = 1 if st.sidebar.checkbox("🚗 ที่จอดรถ (Car park)") else 0
filter_bike = 1 if st.sidebar.checkbox("🚴 ทางจักรยาน (Bicycle path)") else 0
filter_pet = 1 if st.sidebar.checkbox("🐶 สวนสัตว์เลี้ยงเข้าได้ (Pet park)") else 0

# =====================================================================
# 6. DUCKDB FILTERING
# =====================================================================
if train_dist_filter:
    selected = "', '".join(train_dist_filter)
    where_clauses = [f"TRAIN_DIST_CATEGORY IN ('{selected}')"]
else:
    where_clauses = ["1=1"]

if filter_toilet:
    where_clauses.append("TOILET = 1")
if filter_sports:
    where_clauses.append("SPORTS_FIELD = 1")
if filter_running:
    where_clauses.append("RUNNING_TRACK = 1")
if filter_car:
    where_clauses.append("CAR_PARK = 1")
if filter_bike:
    where_clauses.append("BICYCLE_PATH = 1")
if filter_pet:
    where_clauses.append("PET_FRIENDLY = 1")

query_string = f"""
SELECT *
FROM parks
WHERE {' AND '.join(where_clauses)}
"""

df_filtered = duck_conn.execute(query_string).df()

# =====================================================================
# 7. HERO
# =====================================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-tag">LIVE PARK FINDER · PM2.5 MONITOR · BTS/MRT ACCESS</div>
    <div class="hero-title">🌳 Park Finder & Air Quality Monitor</div>
    <div class="hero-subtitle">
        ค้นหาสวนสาธารณะที่เหมาะกับคุณ เช็กค่าฝุ่น PM2.5 ล่าสุด
        และดูความสะดวกในการเดินทางด้วย BTS/MRT ก่อนออกไปวิ่งหรือพักผ่อน
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# 8. KPI SUMMARY
# =====================================================================
total_found = len(df_filtered)
avg_pm25 = df_filtered["LATEST_PM25"].mean() if not df_filtered.empty else np.nan
near_train_count = len(df_filtered[df_filtered["DIST_TO_TRAIN_KM"] <= 1.5]) if not df_filtered.empty else 0
running_count = len(df_filtered[df_filtered["RUNNING_TRACK"] == 1]) if not df_filtered.empty else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #00492C;">
        <div class="kpi-label">🌳 สวนที่ค้นพบ</div>
        <div class="kpi-value">{total_found}</div>
        <div class="kpi-chip">ตรงตามตัวกรอง</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    pm25_text = f"{avg_pm25:.1f}" if not pd.isna(avg_pm25) else "N/A"
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #E22028;">
        <div class="kpi-label">😷 PM2.5 เฉลี่ย</div>
        <div class="kpi-value">{pm25_text}</div>
        <div class="kpi-chip">µg/m³ ล่าสุด</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #FBBA16;">
        <div class="kpi-label">🚇 ใกล้รถไฟฟ้า ≤ 1.5 กม.</div>
        <div class="kpi-value">{near_train_count}</div>
        <div class="kpi-chip">เดินทางสะดวก</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #98CCD0;">
        <div class="kpi-label">🏃 มีลู่วิ่ง</div>
        <div class="kpi-value">{running_count}</div>
        <div class="kpi-chip">เหมาะกับสายสุขภาพ</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# 9. INSIGHT
# =====================================================================
if not df_filtered.empty:
    best_access = df_filtered.loc[df_filtered["DIST_TO_TRAIN_KM"].idxmin()]
    clean_air = df_filtered.loc[df_filtered["LATEST_PM25"].idxmin()] if df_filtered["LATEST_PM25"].notna().any() else None

    clean_text = clean_air["NAME"] if clean_air is not None else "ไม่มีข้อมูล PM2.5"

    st.markdown(f"""
    <div class="insight-box">
        💡 <b>Insight สำคัญ:</b>
        สวนที่ใกล้รถไฟฟ้าที่สุดคือ <b>{best_access["NAME"]}</b>
        ({best_access["DIST_TO_TRAIN_KM"]*1000:.0f} เมตร) ·
        สวนที่ค่าฝุ่นต่ำสุดจากตัวกรองคือ <b>{clean_text}</b>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# 10. MAIN DASHBOARD LAYOUT
# =====================================================================
st.markdown('<div class="section-title">🗺️ แผนที่สวนสาธารณะและคุณภาพอากาศ</div>', unsafe_allow_html=True)

col_map, col_list = st.columns([2.1, 1])

with col_map:
    st.markdown('<div class="map-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="small-title">📍 Interactive Map</div>
    <div class="desc-text">
        สีของจุดแสดงระดับ PM2.5 ล่าสุด ยิ่งสีแดงเข้มยิ่งมีค่าฝุ่นสูง กดหรือชี้ที่จุดเพื่อดูรายละเอียดสวนและสิ่งอำนวยความสะดวก
    </div>
    """, unsafe_allow_html=True)

    if not df_filtered.empty:
        df_map_show = df_filtered.copy()

        amenities_cols = [
            "TOILET",
            "SPORTS_FIELD",
            "RUNNING_TRACK",
            "CAR_PARK",
            "BICYCLE_PATH",
            "PET_FRIENDLY"
        ]

        for col in amenities_cols:
            df_map_show[col] = df_map_show[col].map({1: "✅ มี", 0: "❌ ไม่มี"})

        df_map_show["DIST_TO_TRAIN_M"] = df_map_show["DIST_TO_TRAIN_KM"] * 1000

        fig = px.scatter_mapbox(
            df_map_show,
            lat="LAT",
            lon="LNG",
            hover_name="NAME",
            hover_data={
                "LATEST_PM25": ":.1f",
                "AIR_UPDATED_TIME": True,
                "NEAREST_AIR_STATION": True,
                "NEAREST_TRAIN_STATION": True,
                "DIST_TO_TRAIN_M": ":,.0f",
                "RUN_M": ":,.0f",
                "TOILET": True,
                "SPORTS_FIELD": True,
                "RUNNING_TRACK": True,
                "CAR_PARK": True,
                "BICYCLE_PATH": True,
                "PET_FRIENDLY": True,
                "LAT": False,
                "LNG": False
            },
            color="LATEST_PM25",
            color_continuous_scale=["#B1D8B8", "#FBBA16", "#F05A28", "#E22028"],
            size="DIST_TO_TRAIN_KM",
            size_max=18,
            zoom=10.8,
            height=690
        )

        fig.update_layout(
            mapbox_style="carto-positron",
            margin=dict(r=0, t=0, l=0, b=0),
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
            coloraxis_colorbar=dict(
                title="PM2.5",
                thickness=14,
                len=0.75,
                y=0.5,
                bgcolor="rgba(255,255,255,0.65)"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ ไม่พบสวนสาธารณะตามเงื่อนไขที่เลือก")

    st.markdown('</div>', unsafe_allow_html=True)

with col_list:
    st.markdown('<div class="list-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="small-title">📋 รายชื่อสวนที่ค้นพบ</div>
    <div class="desc-text">
        เปิดดูรายละเอียดเวลาเปิด-ปิด ค่าฝุ่น สถานีรถไฟฟ้าใกล้สุด และสิ่งอำนวยความสะดวก
    </div>
    """, unsafe_allow_html=True)

    if not df_filtered.empty:
        for _, park in df_filtered.iterrows():
            pm25_display = f"{park['LATEST_PM25']:.1f} µg/m³" if not pd.isna(park["LATEST_PM25"]) else "N/A"
            train_m = park["DIST_TO_TRAIN_KM"] * 1000

            with st.expander(f"🌳 {park['NAME']}"):

                air_time = park.get('AIR_UPDATED_TIME', 'ไม่ระบุ')
                st.markdown(f"**⏰ เวลาเปิด-ปิด:** {park['OPEN']} - {park['CLOSE']}")
                st.markdown(f"**😷 PM2.5 ล่าสุด:** {pm25_display} ({air_time})")
                st.markdown(f"**🏢 สถานีวัดฝุ่นใกล้สุด:** {park['NEAREST_AIR_STATION']}")
                st.markdown(f"**🚇 สถานีรถไฟฟ้าใกล้สุด:** {park['NEAREST_TRAIN_STATION']} ({train_m:.0f} เมตร)")

                run_m_raw = str(park["RUN_M"]).strip()

                if run_m_raw == "-" or run_m_raw == "0" or run_m_raw.lower() == "nan" or not run_m_raw:
                    st.markdown("**🏃 ระยะทางลู่วิ่ง:** ไม่มีลู่วิ่ง")
                else:
                    try:
                        run_m_val = float(run_m_raw)
                        st.markdown(f"**🏃 ระยะทางลู่วิ่ง:** {run_m_val:,.0f} เมตร")
                    except Exception:
                        st.markdown(f"**🏃 ระยะทางลู่วิ่ง:** {run_m_raw}")

                amenity_list = []

                if park["TOILET"] == 1:
                    amenity_list.append("🚽 ห้องน้ำ")
                if park["SPORTS_FIELD"] == 1:
                    amenity_list.append("⚽ ลานกีฬา")
                if park["RUNNING_TRACK"] == 1:
                    amenity_list.append("🏃 ลู่วิ่ง")
                if park["CAR_PARK"] == 1:
                    amenity_list.append("🚗 ที่จอดรถ")
                if park["BICYCLE_PATH"] == 1:
                    amenity_list.append("🚴 ทางจักรยาน")
                if park["PET_FRIENDLY"] == 1:
                    amenity_list.append("🐶 สัตว์เลี้ยงเข้าได้")

                st.markdown("**🧩 สิ่งอำนวยความสะดวก:**")
                st.caption(" | ".join(amenity_list) if amenity_list else "ไม่มีสิ่งอำนวยความสะดวกพิเศษ")
    else:
        st.info("ยังไม่มีรายการสวนที่ตรงกับเงื่อนไข")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
# 11. DETAIL TABLE
# =====================================================================
st.markdown('<div class="section-title">📑 ตารางข้อมูลสวนที่ผ่านตัวกรอง</div>', unsafe_allow_html=True)

if not df_filtered.empty:
    df_table = df_filtered[[
        "NAME",
        "OPEN",
        "CLOSE",
        "NEAREST_TRAIN_STATION",
        "DIST_TO_TRAIN_KM",
        "NEAREST_AIR_STATION",
        "LATEST_PM25",
        "RUN_M"
    ]].copy()

    df_table["DIST_TO_TRAIN_M"] = df_table["DIST_TO_TRAIN_KM"] * 1000

    df_table = df_table[[
        "NAME",
        "OPEN",
        "CLOSE",
        "NEAREST_TRAIN_STATION",
        "DIST_TO_TRAIN_M",
        "NEAREST_AIR_STATION",
        "LATEST_PM25",
        "RUN_M"
    ]]

    df_table.columns = [
        "ชื่อสวน",
        "เวลาเปิด",
        "เวลาปิด",
        "สถานีรถไฟฟ้าใกล้สุด",
        "ระยะถึงรถไฟฟ้า (เมตร)",
        "สถานีวัดฝุ่นใกล้สุด",
        "PM2.5 ล่าสุด",
        "ระยะลู่วิ่ง (เมตร)"
    ]

    st.dataframe(
        df_table,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("⚠️ ไม่พบข้อมูลสำหรับแสดงในตาราง")
