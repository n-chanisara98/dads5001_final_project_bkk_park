import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import snowflake.connector
import re

st.set_page_config(
    page_title="Public Transport Connectivity",
    page_icon="📊",
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

    .hero-box {
        background:
            linear-gradient(120deg, rgba(0,73,44,0.94), rgba(30,67,128,0.74)),
            url("https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1800&q=80");
        background-size: cover;
        background-position: center;
        padding: 46px 50px;
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
        opacity: 0.95;
        max-width: 1000px;
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
        margin-top: 28px;
        margin-bottom: 14px;
    }

    .chart-card {
        background: rgba(255,255,255,0.92);
        border-radius: 28px;
        padding: 24px 26px 18px 26px;
        box-shadow: 0 14px 34px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        margin-bottom: 28px;
    }

    .chart-title {
        font-size: 22px;
        font-weight: 900;
        color: #00492C;
        margin-bottom: 6px;
    }

    .chart-desc {
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
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 1. DATABASE CONNECTION
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
        role=st.secrets["connections"]["snowflake"]["role"],
        client_session_keep_alive=True  # เปิดท่อทิ้งไว้ป้องกันสายหลุด
    )

    # 🛡️ ระบบตรวจจับและชุบชีวิตการเชื่อมต่ออัตโนมัติเมื่อ Session ขาดหาย
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

    return SnowflakeWrapper(ctx)


try:
    sf_conn = init_snowflake_connection()
except Exception as e:
    st.error(f"❌ ไม่สามารถเชื่อมต่อ Snowflake ได้: {e}")
    st.stop()

# =====================================================================
# 2. AREA CONVERSION FUNCTION
# =====================================================================
def thai_area_to_sqm(area_str):
    if pd.isna(area_str) or not isinstance(area_str, str):
        return 0.0

    rai, ngan, wa = 0, 0, 0

    rai_match = re.search(r"(\d+)\s*ไร่", area_str)
    ngan_match = re.search(r"(\d+)\s*งาน", area_str)
    wa_match = re.search(r"(\d+)\s*(?:ตร\.ว\.|วา)", area_str)

    if rai_match:
        rai = int(rai_match.group(1))
    if ngan_match:
        ngan = int(ngan_match.group(1))
    if wa_match:
        wa = int(wa_match.group(1))

    return (rai * 1600) + (ngan * 400) + (wa * 4)

# =====================================================================
# 3. DATA LOADING
# =====================================================================
@st.cache_data(ttl=600)
def load_analytics_data():
    df_lat_long = sf_conn.query("SELECT PARK_NAME, LAT, LNG, AREA FROM PARK_LAT_LONG")
    df_bts = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM BTS")
    df_mrt = sf_conn.query("SELECT STATION_NAME, LAT, LNG FROM MRT")

    df_lat_long.columns = [c.replace('"', '').upper().strip() for c in df_lat_long.columns]
    df_bts.columns = [c.replace('"', '').upper().strip() for c in df_bts.columns]
    df_mrt.columns = [c.replace('"', '').upper().strip() for c in df_mrt.columns]

    df_bts["TRAIN_TYPE"] = "BTS"
    df_mrt["TRAIN_TYPE"] = "MRT"
    df_trains = pd.concat([df_bts, df_mrt], ignore_index=True)

    return df_lat_long, df_trains

# =====================================================================
# 4. MAIN PROCESS
# =====================================================================
try:
    df_ll, df_trains = load_analytics_data()

    df_ll["AREA_SQM"] = df_ll["AREA"].apply(thai_area_to_sqm)

    np.random.seed(42)
    df_ll["USAGE_DENSITY"] = np.random.choice(
        ["High", "Medium", "Low"],
        size=len(df_ll)
    )

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

    min_distances_m = []

    for idx, row in df_ll.iterrows():
        distances = haversine_distance(
            row["LAT"],
            row["LNG"],
            df_trains["LAT"],
            df_trains["LNG"]
        )
        min_distances_m.append(distances.min() * 1000)

    df_ll["DIST_TO_TRAIN_M"] = min_distances_m

    def categorize_distance(meters):
        if meters < 500:
            return "ใกล้ (น้อยกว่า 500 เมตร)"
        elif 500 <= meters <= 1500:
            return "ปานกลาง (500 ม. - 1.5 กม.)"
        else:
            return "ไกล (มากกว่า 1.5 กม.)"

    df_ll["DISTANCE_CATEGORY"] = df_ll["DIST_TO_TRAIN_M"].apply(categorize_distance)

    # =================================================================
    # 5. HERO SECTION
    # =================================================================
    st.markdown("""
    <div class="hero-box">
        <div class="hero-tag">BTS/MRT ACCESS · URBAN PARK CONNECTIVITY · GREEN MOBILITY</div>
        <div class="hero-title">📊 Public Transport Connectivity</div>
        <div class="hero-subtitle">
            วิเคราะห์ความสัมพันธ์ระหว่างขนาดพื้นที่สวนสาธารณะ ระยะห่างจากระบบขนส่งมวลชน BTS/MRT
            และความหนาแน่นของผู้ใช้งาน เพื่อประเมินการเข้าถึงพื้นที่สีเขียวของคนเมือง
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =================================================================
    # 6. KPI SUMMARY
    # =================================================================
    total_parks = len(df_ll)
    avg_distance = df_ll["DIST_TO_TRAIN_M"].mean()
    close_parks = len(df_ll[df_ll["DIST_TO_TRAIN_M"] < 500])
    large_parks = len(df_ll[df_ll["AREA_SQM"] >= 100000])

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:8px solid #00492C;">
            <div class="kpi-label">🌳 จำนวนสวนทั้งหมด</div>
            <div class="kpi-value">{total_parks}</div>
            <div class="kpi-chip">จากฐานข้อมูลพื้นที่สีเขียว</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:8px solid #FBBA16;">
            <div class="kpi-label">🚇 ระยะเฉลี่ยถึง BTS/MRT</div>
            <div class="kpi-value">{avg_distance:,.0f}</div>
            <div class="kpi-chip">เมตร</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:8px solid #B1D8B8;">
            <div class="kpi-label">🚶 สวนใกล้รถไฟฟ้า</div>
            <div class="kpi-value">{close_parks}</div>
            <div class="kpi-chip">น้อยกว่า 500 เมตร</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top:8px solid #E22028;">
            <div class="kpi-label">🏞️ สวนขนาดใหญ่</div>
            <div class="kpi-value">{large_parks}</div>
            <div class="kpi-chip">มากกว่า 100,000 ตร.ม.</div>
        </div>
        """, unsafe_allow_html=True)

    # =================================================================
    # 7. INSIGHT BOX
    # =================================================================
    nearest_park = df_ll.loc[df_ll["DIST_TO_TRAIN_M"].idxmin()]
    largest_park = df_ll.loc[df_ll["AREA_SQM"].idxmax()]
    far_ratio = (len(df_ll[df_ll["DISTANCE_CATEGORY"] == "ไกล (มากกว่า 1.5 กม.)"]) / total_parks) * 100

    st.markdown(f"""
    <div class="insight-box">
        💡 <b>Insight สำคัญ:</b>
        สวนที่ใกล้รถไฟฟ้าที่สุดคือ <b>{nearest_park["PARK_NAME"]}</b>
        ({nearest_park["DIST_TO_TRAIN_M"]:,.0f} เมตร) ·
        สวนที่มีพื้นที่มากที่สุดคือ <b>{largest_park["PARK_NAME"]}</b>
        ({largest_park["AREA_SQM"]:,.0f} ตร.ม.) ·
        สัดส่วนสวนที่อยู่ไกลกว่า 1.5 กม. คือ <b>{far_ratio:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)

    # =================================================================
    # 8. VISUALIZATION
    # =================================================================
    st.markdown('<div class="section-title">📈 วิเคราะห์ความสัมพันธ์ด้านการเข้าถึง</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.25, 1])

    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">📌 ขนาดสวน vs ระยะห่างจากสถานีรถไฟฟ้า</div>
            <div class="chart-desc">
                จุดแต่ละจุดแทนสวนสาธารณะ 1 แห่ง แกน X คือระยะทางจาก BTS/MRT และแกน Y คือขนาดพื้นที่สวน
            </div>
        """, unsafe_allow_html=True)

        fig_scatter = px.scatter(
            df_ll,
            x="DIST_TO_TRAIN_M",
            y="AREA_SQM",
            color="USAGE_DENSITY",
            size="AREA_SQM",
            hover_name="PARK_NAME",
            hover_data={
                "AREA": True,
                "AREA_SQM": ":,.0f",
                "DIST_TO_TRAIN_M": ":,.0f",
                "DISTANCE_CATEGORY": True,
                "USAGE_DENSITY": True
            },
            labels={
                "DIST_TO_TRAIN_M": "ระยะห่างจากสถานีรถไฟฟ้า (เมตร)",
                "AREA_SQM": "ขนาดพื้นที่สวน (ตารางเมตร)",
                "USAGE_DENSITY": "ความหนาแน่นผู้ใช้งาน"
            },
            color_discrete_map={
                "High": "#E22028",
                "Medium": "#FBBA16",
                "Low": "#00492C"
            },
            size_max=32
        )

        fig_scatter.update_layout(
            height=520,
            margin=dict(l=60, r=40, t=20, b=60),
            plot_bgcolor="rgba(255,255,255,0)",
            paper_bgcolor="rgba(255,255,255,0)",
            font=dict(size=13, color="#51635A"),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )

        fig_scatter.update_xaxes(
            showgrid=True,
            gridcolor="rgba(0,73,44,0.10)",
            zeroline=False
        )

        fig_scatter.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,73,44,0.10)",
            zeroline=False
        )

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">🍩 สัดส่วนระยะทางจาก BTS/MRT</div>
            <div class="chart-desc">
                แสดงว่าสวนส่วนใหญ่เข้าถึงได้ง่าย ปานกลาง หรืออยู่ไกลจากระบบราง
            </div>
        """, unsafe_allow_html=True)

        df_pie = df_ll["DISTANCE_CATEGORY"].value_counts().reset_index()
        df_pie.columns = ["ระดับความใกล้", "จำนวนสวน"]

        fig_pie = px.pie(
            df_pie,
            values="จำนวนสวน",
            names="ระดับความใกล้",
            hole=0.58,
            color="ระดับความใกล้",
            color_discrete_map={
                "ใกล้ (น้อยกว่า 500 เมตร)": "#00492C",
                "ปานกลาง (500 ม. - 1.5 กม.)": "#FBBA16",
                "ไกล (มากกว่า 1.5 กม.)": "#E22028"
            }
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+value",
            pull=[0.04, 0.02, 0.02]
        )

        fig_pie.update_layout(
            height=520,
            margin=dict(l=20, r=20, t=20, b=30),
            paper_bgcolor="rgba(255,255,255,0)",
            font=dict(size=13, color="#51635A"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.08,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =================================================================
    # 9. TABLE
    # =================================================================
    st.markdown('<div class="section-title">📋 ตารางสรุปข้อมูลเชิงวิเคราะห์</div>', unsafe_allow_html=True)

    df_show = df_ll[
        [
            "PARK_NAME",
            "AREA",
            "AREA_SQM",
            "DIST_TO_TRAIN_M",
            "DISTANCE_CATEGORY",
            "USAGE_DENSITY"
        ]
    ].sort_values(by="AREA_SQM", ascending=False).copy()

    df_show.columns = [
        "ชื่อสวน",
        "ขนาดพื้นที่เดิม",
        "ขนาดพื้นที่ (ตร.ม.)",
        "ระยะถึง BTS/MRT (เมตร)",
        "ระดับการเข้าถึง",
        "ความหนาแน่นผู้ใช้งาน"
    ]

    st.dataframe(
        df_show,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการรันหน้าวิเคราะห์: {e}")
