import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Page 1: Park Analytics", page_icon="🌳", layout="wide")

# ----------------------------------------------------------------------
# 1. MOCK DATA
# ----------------------------------------------------------------------
@st.cache_data
def load_data():
    district_data = {
        "District": ["จตุจักร", "ปทุมวัน", "ราชเทวี", "คลองเตย", "บางขุนเทียน", "ลาดกระบัง", "พระนคร", "ห้วยขวาง", "บางแค", "ธนบุรี"],
        "Population": [150000, 50000, 70000, 100000, 180000, 170000, 45000, 80000, 130000, 110000],
        "Total_Park_Area_Sqm": [900000, 600000, 50000, 400000, 1200000, 850000, 30000, 40000, 90000, 35000],
        "Total_Parks": [5, 3, 2, 4, 6, 5, 2, 1, 3, 2],
        "Monthly_Visitors": [120000, 95000, 15000, 80000, 45000, 50000, 35000, 12000, 25000, 22000]
    }
    df_district = pd.DataFrame(district_data)

    park_data = {
        "Park_Name": [
            "สวนจตุจักร", "สวนวชิรเบญจทัศ (สวนรถไฟ)", "สวนสมเด็จพระนางเจ้าสิริกิตติ์ฯ", "สวนประชานิเวศน์", "สวนวิภาวดี",
            "สวนลุมพินี", "สวนปทุมวนานุรักษ์", "สวนอุทยาน 100 ปีจุฬาฯ",
            "สวนสันติภาพ", "สวนรมณีย์ราชเทวี",
            "สวนเบญจกิติ", "สวนเบญจสิริ", "สวนคลองเตยพัฒนา", "สวนสร้างสุขคลองเตย",
            "สวนเทียนทะเลพัฒนาพฤกษาชาติ", "สวนเชิงนิเวศชายทะเล", "สวนสาธารณะบึงบางบอน", "สวนขุนเทียน 1", "สวนขุนเทียน 2", "สวนขุนเทียน 3",
            "สวนพระยาภิรมย์", "สวนหนองจอก-ลาดกระบัง", "สวนลาดกระบัง 1", "สวนลาดกระบัง 2", "สวนลาดกระบัง 3",
            "สวนสราญรมย์", "สวนรมณีย์นาถ",
            "สวนวัฒนธรรมห้วยขวาง",
            "สวนเฉลิมพระเกียรติ 80 พรรษา (บางแค)", "สวนเพชรกระเษม", "สวนบางแคภิรมย์",
            "สวนธนบุรีรมย์", "สวนวงเวียนใหญ่"
        ],
        "District": [
            "จตุจักร", "จตุจักร", "จตุจักร", "จตุจักร", "จตุจักร",
            "ปทุมวัน", "ปทุมวัน", "ปทุมวัน",
            "ราชเทวี", "ราชเทวี",
            "คลองเตย", "คลองเตย", "คลองเตย", "คลองเตย",
            "บางขุนเทียน", "บางขุนเทียน", "บางขุนเทียน", "บางขุนเทียน", "บางขุนเทียน", "บางขุนเทียน",
            "ลาดกระบัง", "ลาดกระบัง", "ลาดกระบัง", "ลาดกระบัง", "ลาดกระบัง",
            "พระนคร", "พระนคร",
            "ห้วยขวาง",
            "บางแค", "บางแค", "บางแค",
            "ธนบุรี", "ธนบุรี"
        ],
        "ที่จอดรถ (Car Park)": [
            "มี", "มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี",
            "มี", "มี", "ไม่มี", "ไม่มี", "มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี",
            "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี"
        ],
        "มิตรกับสัตว์เลี้ยง (Pet Friendly)": [
            "ไม่มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี",
            "มี", "ไม่มี", "ไม่มี", "ไม่มี", "มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี",
            "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี"
        ],
        "อนุญาตให้ขี่จักรยาน (Bicycle Path)": [
            "ไม่มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี",
            "มี", "ไม่มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี",
            "มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี", "ไม่มี"
        ],
        "Park_Area_Sqm": [
            300000, 400000, 150000, 30000, 20000,
            450000, 100000, 50000,
            35000, 15000,
            250000, 80000, 40000, 30000,
            400000, 350000, 200000, 100000, 100000, 50000,
            300000, 250000, 150000, 100000, 50000,
            15000, 15000,
            40000,
            40000, 30000, 20000,
            25000, 10000
        ],
        "Park_Monthly_Visitors": [
            40000, 60000, 15000, 3000, 2000,
            70000, 15000, 10000,
            10000, 5000,
            50000, 20000, 6000, 4000,
            15000, 15000, 8000, 3000, 3000, 1000,
            18000, 15000, 10000, 5000, 2000,
            20000, 15000,
            12000,
            12000, 8000, 5000,
            18000, 4000
        ]
    }
    df_parks = pd.DataFrame(park_data)
    return df_district, df_parks


df_district, df_parks = load_data()

# ----------------------------------------------------------------------
# 2. GLOBAL STYLE
# ----------------------------------------------------------------------
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

    div[data-testid="stSelectbox"] div {
        color: #00492C !important;
    }

    .hero-box {
        background: linear-gradient(120deg, rgba(0,73,44,0.95), rgba(30,67,128,0.82)),
                    url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1800&q=80");
        background-size: cover;
        background-position: center;
        padding: 46px 48px;
        border-radius: 30px;
        color: white;
        box-shadow: 0 18px 45px rgba(0,73,44,0.20);
        margin-bottom: 28px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 900;
        margin-bottom: 8px;
        line-height: 1.15;
    }

    .hero-subtitle {
        font-size: 18px;
        font-weight: 500;
        opacity: 0.95;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #00492C;
        margin-top: 18px;
        margin-bottom: 12px;
    }

    .kpi-card {
        background: rgba(255,255,255,0.88);
        padding: 28px 30px;
        border-radius: 26px;
        box-shadow: 0 12px 30px rgba(0,73,44,0.10);
        border: 1px solid rgba(0,73,44,0.10);
        min-height: 160px;
    }

    .kpi-label {
        font-size: 15px;
        color: #51635A;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .kpi-value {
        font-size: 38px;
        color: #00492C;
        font-weight: 900;
        letter-spacing: -1px;
    }

    .kpi-chip {
        display: inline-block;
        margin-top: 13px;
        padding: 9px 15px;
        background: #B1D8B8;
        color: #00492C;
        border-radius: 999px;
        font-size: 14px;
        font-weight: 800;
    }

    .insight-box {
        background: linear-gradient(90deg, #FBBA16 0%, #B1D8B8 100%);
        padding: 24px 30px;
        border-radius: 26px;
        margin-top: 30px;
        margin-bottom: 34px;
        box-shadow: 0 10px 28px rgba(0,73,44,0.12);
        border: 1px solid rgba(0,73,44,0.12);
        font-size: 22px;
        font-weight: 600;
        color: #00492C;
    }

    .chart-card {
        background: rgba(255,255,255,0.88);
        border-radius: 26px;
        padding: 22px 24px 12px 24px;
        box-shadow: 0 12px 30px rgba(0,73,44,0.08);
        border: 1px solid rgba(0,73,44,0.08);
        margin-bottom: 28px;
    }

    .chart-title {
        font-size: 21px;
        font-weight: 850;
        color: #00492C;
        margin-bottom: 6px;
    }

    .chart-desc {
        font-size: 14px;
        color: #66746B;
        margin-bottom: 10px;
    }

    .download-card {
        background: rgba(255,255,255,0.88);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 10px 24px rgba(0,73,44,0.08);
        border: 1px solid rgba(0,73,44,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 3. SIDEBAR FILTERS
# ----------------------------------------------------------------------
st.sidebar.markdown("## 🔍 ตัวกรองข้อมูล")
st.sidebar.markdown("เลือกเงื่อนไขเพื่อดูข้อมูลสวนสาธารณะตามพื้นที่และสิ่งอำนวยความสะดวก")

def reset_filters():
    st.session_state.sel_dist = "ทั้งหมด"
    st.session_state.chk_pet = False
    st.session_state.chk_bike = False

selected_district = st.sidebar.selectbox(
    "เลือกเขตพื้นที่:",
    ["ทั้งหมด"] + list(df_district["District"].unique()),
    key="sel_dist"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ สิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง", key="chk_pet")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้", key="chk_bike")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🔄 ล้างตัวกรองทั้งหมด", on_click=reset_filters, use_container_width=True):
    st.rerun()

# ----------------------------------------------------------------------
# 4. DATA FILTERING
# ----------------------------------------------------------------------
df_park_filtered = df_parks.copy()

if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]

if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]

if selected_district != "ทั้งหมด":
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]

df_dist_summary = df_park_filtered.groupby("District").agg(
    Total_Park_Area_Sqm=("Park_Area_Sqm", "sum"),
    Monthly_Visitors=("Park_Monthly_Visitors", "sum"),
    Total_Parks=("Park_Name", "count")
).reset_index()

df_dist_summary = df_dist_summary.merge(
    df_district[["District", "Population"]],
    on="District",
    how="left"
)

df_dist_summary["Green_per_Capita"] = df_dist_summary["Total_Park_Area_Sqm"] / df_dist_summary["Population"]
df_dist_summary["Ratio_to_Population"] = df_dist_summary["Monthly_Visitors"] / df_dist_summary["Population"]

if selected_district == "ทั้งหมด":
    y_axis_col = "District"
    y_label_text = "เขตพื้นที่"
    df_chart_data = df_dist_summary.copy()
    df_chart_data["Chart_Area"] = df_chart_data["Total_Park_Area_Sqm"]
    df_chart_data["Chart_Visitors"] = df_chart_data["Monthly_Visitors"]
    df_chart_data["Chart_Ratio"] = df_chart_data["Ratio_to_Population"]
    area_suffix = "ตร.ม."
    visitor_suffix = "คน/เดือน"
    ratio_suffix = "เท่าของปชกร."
else:
    y_axis_col = "Park_Name"
    y_label_text = f"รายชื่อสวนในเขต {selected_district}"
    df_chart_data = df_park_filtered.copy()
    df_chart_data["Chart_Area"] = df_chart_data["Park_Area_Sqm"]
    df_chart_data["Chart_Visitors"] = df_chart_data["Park_Monthly_Visitors"]

    current_pop = df_district[df_district["District"] == selected_district]["Population"].values[0]
    df_chart_data["Chart_Ratio"] = df_chart_data["Chart_Visitors"] / current_pop
    area_suffix = "ตร.ม."
    visitor_suffix = "คน/เดือน"
    ratio_suffix = "เท่าของปชกร.เขต"

total_green_area = df_chart_data["Chart_Area"].sum() if not df_chart_data.empty else 0
total_pop = (
    df_district[df_district["District"] == selected_district]["Population"].sum()
    if selected_district != "ทั้งหมด"
    else df_district["Population"].sum()
)
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0
total_parks = len(df_park_filtered)

# ----------------------------------------------------------------------
# 5. HERO SECTION
# ----------------------------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🌳 Park Analytics Dashboard</div>
    <div class="hero-subtitle">
        วิเคราะห์ภาพรวมพื้นที่สีเขียว พฤติกรรมการเข้าใช้งาน และความพร้อมของสิ่งอำนวยความสะดวกในกรุงเทพมหานคร
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 6. KPI CARDS
# ----------------------------------------------------------------------
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #00492C;">
        <div class="kpi-label">🍃 พื้นที่สีเขียวรวม</div>
        <div class="kpi-value">{total_green_area:,.0f} <span style="font-size:17px;">ตร.ม.</span></div>
        <div class="kpi-chip">ตามตัวกรองปัจจุบัน</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #FBBA16;">
        <div class="kpi-label">🏞️ จำนวนสวนสาธารณะ</div>
        <div class="kpi-value">{total_parks:,} <span style="font-size:17px;">แห่ง</span></div>
        <div class="kpi-chip">รวมสวนที่ผ่านเงื่อนไข</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top:8px solid #E22028;">
        <div class="kpi-label">👤 พื้นที่สีเขียวต่อหัว</div>
        <div class="kpi-value">{bkk_green_per_capita:.2f} <span style="font-size:17px;">ตร.ม./คน</span></div>
        <div class="kpi-chip">ต่ำกว่าคำแนะนำ 9 ตร.ม./คน</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 7. INSIGHT BOX WITH PROPER SPACING
# ----------------------------------------------------------------------
if not df_chart_data.empty:
    max_area_name = df_chart_data.loc[df_chart_data["Chart_Area"].idxmax()][y_axis_col]
    max_visit_name = df_chart_data.loc[df_chart_data["Chart_Visitors"].idxmax()][y_axis_col]
    max_ratio_name = df_chart_data.loc[df_chart_data["Chart_Ratio"].idxmax()][y_axis_col]

    st.markdown(f"""
    <div class="insight-box">
        💡 <b>Insight สำคัญ:</b>
        พื้นที่ใหญ่ที่สุดคือ <b>{max_area_name}</b> ·
        ผู้ใช้งานจริงต่อเดือนสูงสุดคือ <b>{max_visit_name}</b> ·
        พื้นที่ที่มีภาระต่อประชากรสูงสุดคือ <b>{max_ratio_name}</b>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 8. CHARTS ROW 1
# ----------------------------------------------------------------------
st.markdown('<div class="section-title">📊 ภาพรวมพื้นที่และการใช้งาน</div>', unsafe_allow_html=True)

pair1_col1, pair1_col2 = st.columns(2)

with pair1_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="chart-title">🟢 ขนาดพื้นที่สีเขียวรวม</div>'
        f'<div class="chart-desc">เปรียบเทียบขนาดพื้นที่สวน {"รายเขต" if selected_district == "ทั้งหมด" else "รายสวน"}</div>',
        unsafe_allow_html=True
    )

    if not df_chart_data.empty:
        df_sorted_area = df_chart_data.sort_values(by="Chart_Area", ascending=True)
        max_area = df_sorted_area["Chart_Area"].max()

        fig_area = px.bar(
            df_sorted_area,
            x="Chart_Area",
            y=y_axis_col,
            orientation="h",
            text=df_sorted_area["Chart_Area"].apply(lambda x: f"{x:,.0f} {area_suffix}"),
            color="Chart_Area",
            color_continuous_scale="Greens",
            labels={"Chart_Area": "ขนาดพื้นที่ (ตร.ม.)", y_axis_col: y_label_text}
        )

        fig_area.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig_area.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=430,
            margin=dict(l=90, r=180, t=20, b=30),
            plot_bgcolor="rgba(255,255,255,0)",
            paper_bgcolor="rgba(255,255,255,0)",
            xaxis=dict(range=[0, max_area * 1.30]),
            font=dict(size=13, color="#51635A")
        )

        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลพื้นที่")

    st.markdown('</div>', unsafe_allow_html=True)

with pair1_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="chart-title">👥 ผู้เข้าใช้งานจริงต่อเดือน</div>'
        f'<div class="chart-desc">เปรียบเทียบจำนวนผู้ใช้งานสวน {"รายเขต" if selected_district == "ทั้งหมด" else "รายสวน"}</div>',
        unsafe_allow_html=True
    )

    if not df_chart_data.empty:
        df_sorted_visitors = df_chart_data.sort_values(by="Chart_Visitors", ascending=True)
        max_visitors = df_sorted_visitors["Chart_Visitors"].max()

        fig_visitors = px.bar(
            df_sorted_visitors,
            x="Chart_Visitors",
            y=y_axis_col,
            orientation="h",
            text=df_sorted_visitors["Chart_Visitors"].apply(lambda x: f"{x:,.0f} {visitor_suffix}"),
            color="Chart_Visitors",
            color_continuous_scale=["#FBBA16", "#F05A28", "#E22028"],
            labels={"Chart_Visitors": "จำนวนผู้เข้าชม (คน/เดือน)", y_axis_col: y_label_text}
        )

        fig_visitors.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig_visitors.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=430,
            margin=dict(l=90, r=180, t=20, b=30),
            plot_bgcolor="rgba(255,255,255,0)",
            paper_bgcolor="rgba(255,255,255,0)",
            xaxis=dict(range=[0, max_visitors * 1.30]),
            font=dict(size=13, color="#51635A")
        )

        st.plotly_chart(fig_visitors, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลผู้ใช้งาน")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 9. CHARTS ROW 2
# ----------------------------------------------------------------------
st.markdown('<div class="section-title">🧭 ความหนาแน่นและสิ่งอำนวยความสะดวก</div>', unsafe_allow_html=True)

pair2_col1, pair2_col2 = st.columns(2)

with pair2_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-title">📈 อัตราส่วนการใช้งานเทียบประชากร</div>'
        '<div class="chart-desc">แสดงพื้นที่ที่มีภาระการใช้งานสูงเมื่อเทียบกับจำนวนประชากร</div>',
        unsafe_allow_html=True
    )

    if not df_chart_data.empty:
        df_sorted_ratio = df_chart_data.sort_values(by="Chart_Ratio", ascending=True)
        max_ratio = df_sorted_ratio["Chart_Ratio"].max()

        fig_ratio = px.bar(
            df_sorted_ratio,
            x="Chart_Ratio",
            y=y_axis_col,
            orientation="h",
            text=df_sorted_ratio["Chart_Ratio"].apply(lambda x: f"{x:.2f} {ratio_suffix}"),
            color="Chart_Ratio",
            color_continuous_scale=["#E2B2B4", "#1E4380"],
            labels={"Chart_Ratio": "ดัชนีอัตราส่วน (เท่า)", y_axis_col: y_label_text}
        )

        fig_ratio.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig_ratio.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=430,
            margin=dict(l=90, r=180, t=20, b=30),
            plot_bgcolor="rgba(255,255,255,0)",
            paper_bgcolor="rgba(255,255,255,0)",
            xaxis=dict(range=[0, max_ratio * 1.30]),
            font=dict(size=13, color="#51635A")
        )

        st.plotly_chart(fig_ratio, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลดัชนี")

    st.markdown('</div>', unsafe_allow_html=True)

with pair2_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-title">🍩 สัดส่วนสิ่งอำนวยความสะดวก</div>'
        '<div class="chart-desc">เปรียบเทียบจำนวนสวนที่มีบริการแต่ละประเภท</div>',
        unsafe_allow_html=True
    )

    if not df_park_filtered.empty:
        features_map = {
            "ที่จอดรถ (Car Park)": "ที่จอดรถ",
            "มิตรกับสัตว์เลี้ยง (Pet Friendly)": "มิตรกับสัตว์เลี้ยง",
            "อนุญาตให้ขี่จักรยาน (Bicycle Path)": "ทางจักรยาน"
        }

        feature_counts = []
        for eng_col, th_name in features_map.items():
            has_service = df_park_filtered[eng_col].value_counts().get("มี", 0)
            feature_counts.append({
                "สิ่งอำนวยความสะดวก": th_name,
                "จำนวนที่มีบริการ": has_service
            })

        df_feature_pie = pd.DataFrame(feature_counts)

        fig_donut = px.pie(
            df_feature_pie,
            values="จำนวนที่มีบริการ",
            names="สิ่งอำนวยความสะดวก",
            hole=0.55,
            color="สิ่งอำนวยความสะดวก",
            color_discrete_map={
                "ที่จอดรถ": "#00492C",
                "ทางจักรยาน": "#FBBA16",
                "มิตรกับสัตว์เลี้ยง": "#98CCD0"
            }
        )

        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent+value"
        )

        fig_donut.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=20, b=30),
            paper_bgcolor="rgba(255,255,255,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.05,
                xanchor="center",
                x=0.5
            ),
            font=dict(size=13, color="#51635A")
        )

        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลสิ่งอำนวยความสะดวก")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 10. DATA TABLE
# ----------------------------------------------------------------------
st.markdown('<div class="section-title">📋 ตารางรายละเอียดสวนสาธารณะ</div>', unsafe_allow_html=True)

table_col, download_col = st.columns([4, 1])

features_disp = [
    "ที่จอดรถ (Car Park)",
    "มิตรกับสัตว์เลี้ยง (Pet Friendly)",
    "อนุญาตให้ขี่จักรยาน (Bicycle Path)"
]

if not df_park_filtered.empty:
    df_table_show = df_park_filtered[
        ["Park_Name", "District", "Park_Area_Sqm", "Park_Monthly_Visitors"] + features_disp
    ].copy()

    df_table_show.columns = [
        "ชื่อสวนสาธารณะ",
        "เขตพื้นที่",
        "ขนาดพื้นที่ (ตร.ม.)",
        "ผู้ใช้บริการ (คน/เดือน)",
        "ที่จอดรถ",
        "มิตรกับสัตว์เลี้ยง",
        "ทางจักรยาน"
    ]

    with download_col:
        csv_data = df_table_show.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 ดาวน์โหลด CSV",
            data=csv_data,
            file_name="bkk_park_filtered_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(
        df_table_show,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะตรงตามตัวกรองที่คุณเลือกในขณะนี้")
