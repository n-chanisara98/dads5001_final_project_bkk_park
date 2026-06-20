import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Page 1: Park Analytics", page_icon="🌳", layout="wide")

# ----------------------------------------------------------------------
# 1. MOCK DATA  (คงส่วนข้อมูลเดิมไว้)
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
# 2. STYLE: สดใสกว่า Home + ใช้โทนสีจากภาพ Flavour United
# ----------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', 'Noto Sans Thai', sans-serif; }
.stApp {
    background:
        radial-gradient(circle at top left, rgba(251,186,22,.25), transparent 30%),
        radial-gradient(circle at top right, rgba(155,204,208,.42), transparent 32%),
        linear-gradient(135deg, #FFF8E9 0%, #F8FBF1 45%, #EAF7EF 100%);
}
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #00492C 0%, #0B5A3A 55%, #1E4380 100%);
    border-right: 1px solid rgba(255,255,255,.14);
}
[data-testid="stSidebar"] * { color: #FFF8E9 !important; }
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] h5 { font-weight: 900; }
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.13) !important;
    border: 1px solid rgba(255,255,255,.28) !important;
    border-radius: 14px !important;
}
[data-testid="stSidebar"] .stButton button {
    background: #FBBA16 !important;
    color: #00492C !important;
    border: 0 !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
}

.hero-wrap {
    position: relative;
    overflow: hidden;
    border-radius: 34px;
    min-height: 360px;
    padding: 42px 48px;
    background:
        linear-gradient(90deg, rgba(0,73,44,.94) 0%, rgba(0,73,44,.74) 42%, rgba(0,73,44,.12) 100%),
        url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=2200&q=85');
    background-size: cover;
    background-position: center;
    box-shadow: 0 26px 80px rgba(0,73,44,.22);
    border: 1px solid rgba(255,255,255,.40);
}
.hero-kicker {
    display: inline-flex;
    padding: 9px 15px;
    background: #FBBA16;
    color: #00492C;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 900;
    letter-spacing: .04em;
    text-transform: uppercase;
}
.hero-title {
    margin-top: 22px;
    max-width: 850px;
    color: #FFF8E9;
    font-size: clamp(42px, 5.1vw, 76px);
    line-height: .96;
    font-weight: 950;
    letter-spacing: -2.5px;
}
.hero-subtitle {
    max-width: 760px;
    margin-top: 18px;
    color: rgba(255,248,233,.92);
    font-size: 18px;
    line-height: 1.7;
    font-weight: 650;
}
.hero-pills { display:flex; flex-wrap:wrap; gap:12px; margin-top: 26px; }
.hero-pill {
    padding: 11px 16px;
    border-radius: 999px;
    color: #00492C;
    font-weight: 900;
    background: rgba(255,248,233,.94);
    box-shadow: 0 8px 26px rgba(0,0,0,.14);
}
.section-title { margin: 30px 0 8px 0; color: #00492C; font-size: 28px; font-weight: 950; letter-spacing: -.4px; }
.section-note { margin-bottom: 18px; color: rgba(23,52,42,.72); font-weight: 650; }
.kpi-card {
    min-height: 142px;
    background: rgba(255,255,255,.80);
    border-radius: 28px;
    padding: 24px 26px;
    border: 1px solid rgba(0,73,44,.12);
    box-shadow: 0 18px 54px rgba(0,73,44,.10);
    position: relative;
    overflow: hidden;
}
.kpi-card:before { content:""; position:absolute; inset:0 0 auto 0; height:8px; background: var(--accent); }
.kpi-label { color: rgba(23,52,42,.72); font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: .04em; }
.kpi-value { color: #00492C; font-size: 36px; font-weight: 950; line-height: 1.05; margin-top: 12px; letter-spacing: -1px; }
.kpi-unit { font-size: 15px; font-weight: 800; color: rgba(23,52,42,.70); }
.kpi-chip { display:inline-block; margin-top: 12px; padding: 7px 11px; border-radius: 999px; background: rgba(177,216,184,.55); color:#00492C; font-weight:900; font-size:12px; }
.insight-box {
    background: linear-gradient(135deg, rgba(251,186,22,.38), rgba(177,216,184,.60));
    border: 1px solid rgba(0,73,44,.16);
    border-radius: 26px;
    padding: 20px 24px;
    box-shadow: 0 18px 54px rgba(0,73,44,.08);
    color: #17342A;
    font-size: 16px;
    line-height: 1.8;
}
.insight-box b { color: #00492C; }
.chart-card {
    background: rgba(255,255,255,.94);
    border: 1px solid rgba(0,73,44,.10);
    border-radius: 28px;
    padding: 20px 20px 10px 20px;
    box-shadow: 0 18px 54px rgba(0,73,44,.09);
    margin-bottom: 18px;
}
.chart-title { color:#00492C; font-size: 19px; font-weight: 950; margin: 2px 0 4px 0; }
.chart-caption { color: rgba(23,52,42,.62); font-size: 13px; font-weight: 650; margin-bottom: 8px; }
.story-card { border-radius: 26px; padding: 22px; background: #00492C; color: #FFF8E9; min-height: 176px; box-shadow: 0 18px 54px rgba(0,73,44,.14); }
.story-card.yellow { background:#FBBA16; color:#00492C; }
.story-card.aqua { background:#9BCCD0; color:#00492C; }
.story-card.red { background:#E22028; color:#FFF8E9; }
.story-card h4 { margin: 0 0 8px 0; font-size: 20px; font-weight: 950; }
.story-card p { margin: 0; line-height: 1.7; font-weight: 650; }
hr { margin: 2rem 0; border: none; height: 1px; background: rgba(0,73,44,.14); }

/* ===== Plotly Chart Dark Mode Readability Fix ===== */
.chart-card,
.chart-card *,
.js-plotly-plot,
.js-plotly-plot * {
    color: #17342A !important;
}

.chart-card {
    background: rgba(255,255,255,.94) !important;
}

.modebar,
.modebar * {
    color: #00492C !important;
}

/* ให้ Tooltip อ่านง่ายทั้ง Light/Dark */
.hoverlayer .hovertext,
.hoverlayer .hovertext * {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 3. SIDEBAR FILTERS (คง logic เดิม)
# ----------------------------------------------------------------------
st.sidebar.markdown("### 🌿 Park Filters")
st.sidebar.caption("คัดกรองข้อมูลสวนตามเขตและสิ่งอำนวยความสะดวก")

def reset_filters():
    st.session_state.sel_dist = "ทั้งหมด"
    st.session_state.chk_pet = False
    st.session_state.chk_bike = False

selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่", ["ทั้งหมด"] + list(df_district["District"].unique()), key="sel_dist")
st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚙️ เงื่อนไขสิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง", key="chk_pet")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้", key="chk_bike")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🔄 ล้างตัวกรองทั้งหมด", on_click=reset_filters, use_container_width=True):
    st.rerun()

# ----------------------------------------------------------------------
# 4. DYNAMIC DATA FILTERING PROCESS (คง logic เดิม)
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

df_dist_summary = df_dist_summary.merge(df_district[["District", "Population"]], on="District", how="left")
df_dist_summary["Green_per_Capita"] = df_dist_summary["Total_Park_Area_Sqm"] / df_dist_summary["Population"]
df_dist_summary["Ratio_to_Population"] = df_dist_summary["Monthly_Visitors"] / df_dist_summary["Population"]

if selected_district == "ทั้งหมด":
    y_axis_col = "District"
    y_label_text = "เขตพื้นที่"
    df_chart_data = df_dist_summary.copy()
    df_chart_data["Chart_Area"] = df_chart_data["Total_Park_Area_Sqm"]
    df_chart_data["Chart_Visitors"] = df_chart_data["Monthly_Visitors"]
    df_chart_data["Chart_Ratio"] = df_chart_data["Ratio_to_Population"]
    area_suffix, visitor_suffix, ratio_suffix = "ตร.ม.", "คน/เดือน", "เท่าของปชกร."
else:
    y_axis_col = "Park_Name"
    y_label_text = f"รายชื่อสวนในเขต {selected_district}"
    df_chart_data = df_park_filtered.copy()
    df_chart_data["Chart_Area"] = df_chart_data["Park_Area_Sqm"]
    df_chart_data["Chart_Visitors"] = df_chart_data["Park_Monthly_Visitors"]
    current_pop = df_district[df_district["District"] == selected_district]["Population"].values[0]
    df_chart_data["Chart_Ratio"] = df_chart_data["Chart_Visitors"] / current_pop
    area_suffix, visitor_suffix, ratio_suffix = "ตร.ม.", "คน/เดือน", "เท่าของปชกร.เขต"

total_green_area = df_chart_data["Chart_Area"].sum() if not df_chart_data.empty else 0
total_pop = df_district[df_district["District"] == selected_district]["Population"].sum() if selected_district != "ทั้งหมด" else df_district["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0
total_parks = len(df_park_filtered)
current_scope = "ทุกเขตในชุดข้อมูล" if selected_district == "ทั้งหมด" else f"เขต{selected_district}"

# ----------------------------------------------------------------------
# 5. DASHBOARD UI
# ----------------------------------------------------------------------
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-kicker">🌳 Bangkok Green Space Intelligence</div>
    <div class="hero-title">Park Analytics Dashboard</div>
    <div class="hero-subtitle">
        วิเคราะห์พื้นที่สีเขียว พฤติกรรมผู้ใช้งาน และความพร้อมของสิ่งอำนวยความสะดวก
    </div>
    <div class="hero-pills">
        <span class="hero-pill">📍 Scope: {current_scope}</span>
        <span class="hero-pill">🏞️ {total_parks:,} Parks</span>
        <span class="hero-pill">🍃 {total_green_area:,.0f} sq.m.</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">สรุปตัวเลขหลักจากตัวกรองปัจจุบัน เพื่อให้เห็นภาพรวมก่อนดูรายละเอียดกราฟ</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'''
    <div class="kpi-card" style="--accent:#00492C;">
        <div class="kpi-label">🍃 พื้นที่สีเขียวรวม</div>
        <div class="kpi-value">{total_green_area:,.0f} <span class="kpi-unit">ตร.ม.</span></div>
        <div class="kpi-chip">ตามตัวกรองปัจจุบัน</div>
    </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
    <div class="kpi-card" style="--accent:#FBBA16;">
        <div class="kpi-label">🏞️ จำนวนสวนสาธารณะ</div>
        <div class="kpi-value">{total_parks:,} <span class="kpi-unit">แห่ง</span></div>
        <div class="kpi-chip">รวมสวนที่ผ่านเงื่อนไข</div>
    </div>
    ''', unsafe_allow_html=True)
with col3:
    status_color = "#E22028" if bkk_green_per_capita < 9 else "#00492C"
    status_text = "ต่ำกว่าเกณฑ์แนะนำ 9 ตร.ม./คน" if bkk_green_per_capita < 9 else "อยู่ในระดับดี"
    st.markdown(f'''
    <div class="kpi-card" style="--accent:{status_color};">
        <div class="kpi-label">👤 พื้นที่สีเขียวต่อหัว</div>
        <div class="kpi-value">{bkk_green_per_capita:.2f} <span class="kpi-unit">ตร.ม./คน</span></div>
        <div class="kpi-chip">{status_text}</div>
    </div>
    ''', unsafe_allow_html=True)

if not df_chart_data.empty:
    max_area_name = df_chart_data.loc[df_chart_data["Chart_Area"].idxmax()][y_axis_col]
    max_visit_name = df_chart_data.loc[df_chart_data["Chart_Visitors"].idxmax()][y_axis_col]
    max_ratio_name = df_chart_data.loc[df_chart_data["Chart_Ratio"].idxmax()][y_axis_col]
    
    st.markdown(f'''
    <div class="insight-box" style="clear: both; margin-top: 30px;">
        💡 <b>Insight สำคัญ:</b>
        พื้นที่ใหญ่ที่สุดคือ <b>{max_area_name}</b> · ผู้ใช้งานจริงต่อเดือนสูงสุดคือ <b>{max_visit_name}</b> ·
        พื้นที่ที่มีภาระต่อประชากรสูงสุดคือ <b>{max_ratio_name}</b>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.warning("⚠️ ไม่พบข้อมูลตามตัวกรองที่เลือก")

st.markdown('<div class="section-title">Green Space & Usage Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">เปรียบเทียบขนาดพื้นที่กับจำนวนผู้ใช้งาน เพื่อดูว่าพื้นที่ใดมีศักยภาพสูงและพื้นที่ใดมีการใช้งานหนาแน่น</div>', unsafe_allow_html=True)

# Plotly layout กลาง: บังคับสีตัวอักษร/พื้นหลังให้อ่านได้ทั้ง Light Mode และ Dark Mode
plotly_common_layout = dict(
    paper_bgcolor="rgba(255,255,255,0.96)",
    plot_bgcolor="rgba(255,255,255,0.98)",
    font=dict(
        family="Inter, Noto Sans Thai, sans-serif",
        color="#17342A",
        size=13
    ),
    margin=dict(l=125, r=130, t=20, b=55),
    height=420,
    hoverlabel=dict(
        bgcolor="#17342A",
        font_size=13,
        font_color="#FFFFFF",
        bordercolor="#00492C"
    )
)

pair1_col1, pair1_col2 = st.columns(2)

with pair1_col1:
    st.markdown('<div class="chart-card"><div class="chart-title">🟢 ขนาดพื้นที่สีเขียว</div><div class="chart-caption">เรียงจากน้อยไปมาก เพื่อดูอันดับพื้นที่รวมชัดเจน</div>', unsafe_allow_html=True)
    if not df_chart_data.empty:
        df_sorted_area = df_chart_data.sort_values(by="Chart_Area", ascending=True)
        fig_area = px.bar(
            df_sorted_area, x="Chart_Area", y=y_axis_col, orientation="h",
            text=df_sorted_area["Chart_Area"].apply(lambda x: f" {x:,.0f} {area_suffix}"),
            color="Chart_Area",
            color_continuous_scale=[[0, "#B1D8B8"], [0.55, "#2E8B57"], [1, "#00492C"]],
            labels={"Chart_Area": "ขนาดพื้นที่ (ตร.ม.)", y_axis_col: y_label_text}
        )
        fig_area.update_traces(
            textposition="outside",
            textfont=dict(color="#17342A", size=13),
            marker_line_width=0,
            cliponaxis=False
        )
        fig_area.update_layout(**plotly_common_layout, showlegend=False, coloraxis_showscale=False)
        fig_area.update_xaxes(
            gridcolor="rgba(0,73,44,.12)",
            zeroline=False,
            tickfont=dict(color="#17342A", size=13),
            title_font=dict(color="#17342A", size=14)
        )
        fig_area.update_yaxes(
            title=None,
            tickfont=dict(color="#17342A", size=13)
        )
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลพื้นที่")
    st.markdown('</div>', unsafe_allow_html=True)

with pair1_col2:
    st.markdown('<div class="chart-card"><div class="chart-title">👥 ผู้เข้าใช้งานต่อเดือน</div><div class="chart-caption">สะท้อนความนิยมและภาระการรองรับของสวน</div>', unsafe_allow_html=True)
    if not df_chart_data.empty:
        df_sorted_visitors = df_chart_data.sort_values(by="Chart_Visitors", ascending=True)
        fig_visitors = px.bar(
            df_sorted_visitors, x="Chart_Visitors", y=y_axis_col, orientation="h",
            text=df_sorted_visitors["Chart_Visitors"].apply(lambda x: f" {x:,.0f} {visitor_suffix}"),
            color="Chart_Visitors",
            color_continuous_scale=[[0, "#FBBA16"], [0.55, "#E94B2B"], [1, "#E22028"]],
            labels={"Chart_Visitors": "จำนวนผู้เข้าชม (คน/เดือน)", y_axis_col: y_label_text}
        )
        fig_visitors.update_traces(
            textposition="outside",
            textfont=dict(color="#17342A", size=13),
            marker_line_width=0,
            cliponaxis=False
        )
        fig_visitors.update_layout(**plotly_common_layout, showlegend=False, coloraxis_showscale=False)
        fig_visitors.update_xaxes(
            gridcolor="rgba(0,73,44,.12)",
            zeroline=False,
            tickfont=dict(color="#17342A", size=13),
            title_font=dict(color="#17342A", size=14)
        )
        fig_visitors.update_yaxes(
            title=None,
            tickfont=dict(color="#17342A", size=13)
        )
        st.plotly_chart(fig_visitors, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลผู้ใช้งาน")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Accessibility & Facilities</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">วิเคราะห์ความหนาแน่นของการใช้งานเทียบประชากร และสัดส่วนบริการสำคัญ เช่น ที่จอดรถ สัตว์เลี้ยง และทางจักรยาน</div>', unsafe_allow_html=True)

pair2_col1, pair2_col2 = st.columns(2)

with pair2_col1:
    st.markdown('<div class="chart-card"><div class="chart-title">📈 ดัชนีผู้ใช้งานเทียบประชากร</div><div class="chart-caption">ค่าที่สูงบ่งชี้ว่าพื้นที่นั้นมีการใช้งานหนาแน่นเมื่อเทียบกับประชากร</div>', unsafe_allow_html=True)
    if not df_chart_data.empty:
        df_sorted_ratio = df_chart_data.sort_values(by="Chart_Ratio", ascending=True)
        fig_ratio = px.bar(
            df_sorted_ratio, x="Chart_Ratio", y=y_axis_col, orientation="h",
            text=df_sorted_ratio["Chart_Ratio"].apply(lambda x: f" {x:.2f} {ratio_suffix}"),
            color="Chart_Ratio",
            color_continuous_scale=[[0, "#E2B2B4"], [0.52, "#9BCCD0"], [1, "#1E4380"]],
            labels={"Chart_Ratio": "ดัชนีอัตราส่วน (เท่า)", y_axis_col: y_label_text}
        )
        fig_ratio.update_traces(
            textposition="outside",
            textfont=dict(color="#17342A", size=13),
            marker_line_width=0,
            cliponaxis=False
        )
        fig_ratio.update_layout(**plotly_common_layout, showlegend=False, coloraxis_showscale=False)
        fig_ratio.update_xaxes(
            gridcolor="rgba(0,73,44,.12)",
            zeroline=False,
            tickfont=dict(color="#17342A", size=13),
            title_font=dict(color="#17342A", size=14)
        )
        fig_ratio.update_yaxes(
            title=None,
            tickfont=dict(color="#17342A", size=13)
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลดัชนี")
    st.markdown('</div>', unsafe_allow_html=True)

with pair2_col2:
    st.markdown('<div class="chart-card"><div class="chart-title">🍩 สิ่งอำนวยความสะดวก</div><div class="chart-caption">จำนวนสวนที่มีบริการแต่ละประเภทในชุดข้อมูลที่กรองแล้ว</div>', unsafe_allow_html=True)
    if not df_park_filtered.empty:
        features_map = {
            "ที่จอดรถ (Car Park)": "ที่จอดรถ",
            "มิตรกับสัตว์เลี้ยง (Pet Friendly)": "มิตรกับสัตว์เลี้ยง",
            "อนุญาตให้ขี่จักรยาน (Bicycle Path)": "ทางจักรยาน"
        }
        feature_counts = []
        for eng_col, th_name in features_map.items():
            has_service = df_park_filtered[eng_col].value_counts().get("มี", 0)
            feature_counts.append({"สิ่งอำนวยความสะดวก": th_name, "จำนวนที่มีบริการ": has_service})
        df_feature_pie = pd.DataFrame(feature_counts)

        fig_donut = px.pie(
            df_feature_pie, values="จำนวนที่มีบริการ", names="สิ่งอำนวยความสะดวก", hole=0.58,
            color="สิ่งอำนวยความสะดวก",
            color_discrete_map={"ที่จอดรถ": "#1E4380", "ทางจักรยาน": "#FBBA16", "มิตรกับสัตว์เลี้ยง": "#9BCCD0"}
        )
        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent+value",
            textfont=dict(color="#17342A", size=14),
            marker=dict(line=dict(color="#FFF8E9", width=4))
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(255,255,255,0.96)",
            plot_bgcolor="rgba(255,255,255,0.98)",
            font=dict(
                family="Inter, Noto Sans Thai, sans-serif",
                color="#17342A",
                size=13
            ),
            height=420,
            margin=dict(l=20, r=20, t=20, b=55),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.10,
                xanchor="center",
                x=0.5,
                font=dict(color="#17342A", size=13)
            ),
            hoverlabel=dict(
                bgcolor="#17342A",
                font_size=13,
                font_color="#FFFFFF",
                bordercolor="#00492C"
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลสิ่งอำนวยความสะดวก")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">How to Read This Dashboard</div>', unsafe_allow_html=True)
story1, story2, story3, story4 = st.columns(4)
with story1:
    st.markdown('<div class="story-card"><h4>01 · Green Supply</h4><p>ดูพื้นที่สีเขียวรวม เพื่อหาเขตหรือสวนที่มีศักยภาพด้านพื้นที่มากที่สุด</p></div>', unsafe_allow_html=True)
with story2:
    st.markdown('<div class="story-card yellow"><h4>02 · Real Usage</h4><p>ดูจำนวนผู้ใช้งานจริง เพื่อเข้าใจความนิยมและความต้องการของประชาชน</p></div>', unsafe_allow_html=True)
with story3:
    st.markdown('<div class="story-card aqua"><h4>03 · Pressure</h4><p>ดัชนีเทียบประชากรช่วยชี้พื้นที่ที่อาจมีภาระการใช้งานสูงเกินกำลังรองรับ</p></div>', unsafe_allow_html=True)
with story4:
    st.markdown('<div class="story-card red"><h4>04 · Facilities</h4><p>สัดส่วนสิ่งอำนวยความสะดวกช่วยประเมินความพร้อมสำหรับกิจกรรมในสวน</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------------------------
# 6. TABLE + DOWNLOAD (คงฟังก์ชันดาวน์โหลดเดิม)
# ----------------------------------------------------------------------
table_col, download_col = st.columns([4, 1])
with table_col:
    st.markdown('<div class="section-title">Park Detail Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-note">รายละเอียดสวนที่ผ่านตัวกรอง พร้อมข้อมูลขนาดพื้นที่ ผู้ใช้บริการ และสิ่งอำนวยความสะดวก</div>', unsafe_allow_html=True)

features_disp = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]

if not df_park_filtered.empty:
    df_table_show = df_park_filtered[["Park_Name", "District", "Park_Area_Sqm", "Park_Monthly_Visitors"] + features_disp].copy()
    df_table_show.columns = ["ชื่อสวนสาธารณะ", "เขตพื้นที่", "ขนาดพื้นที่ (ตร.ม.)", "ผู้ใช้บริการ (คน/เดือน)", "ที่จอดรถ", "มิตรกับสัตว์เลี้ยง", "ทางจักรยาน"]

    with download_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        csv_data = df_table_show.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="bkk_park_filtered_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(
        df_table_show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ขนาดพื้นที่ (ตร.ม.)": st.column_config.NumberColumn(format="%d"),
            "ผู้ใช้บริการ (คน/เดือน)": st.column_config.NumberColumn(format="%d"),
        }
    )
else:
    st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะตรงตามตัวกรองที่คุณเลือกในขณะนี้")

st.caption("DADS 5001 · BKK Urban Green Spaces & Connectivity · Park Analytics Dashboard")
