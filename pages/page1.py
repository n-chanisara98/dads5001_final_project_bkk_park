import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้าง (Wide mode)
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
# 2. SIDEBAR FILTERS
# ----------------------------------------------------------------------
st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filters)")

if "reset_clicked" not in st.session_state:
    st.session_state.reset_clicked = False

def reset_filters():
    st.session_state.sel_dist = "ทั้งหมด"
    st.session_state.chk_pet = False
    st.session_state.chk_bike = False

selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่:", ["ทั้งหมด"] + list(df_district["District"].unique()), key="sel_dist")
st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚙️ เงื่อนไขสิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง", key="chk_pet")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้", key="chk_bike")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🔄 ล้างตัวกรองทั้งหมด", on_click=reset_filters, use_container_width=True):
    st.rerun()

# ----------------------------------------------------------------------
# 3. DYNAMIC DATA FILTERING PROCESS
# ----------------------------------------------------------------------
df_park_filtered = df_parks.copy()

if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]
if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]

if selected_district != "ทั้งหมด":
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]

# สรุปข้อมูลระดับเขตจากรายสวนที่ผ่านการกรองจริง
df_dist_summary = df_park_filtered.groupby("District").agg(
    Total_Park_Area_Sqm=("Park_Area_Sqm", "sum"),
    Monthly_Visitors=("Park_Monthly_Visitors", "sum"),
    Total_Parks=("Park_Name", "count")
).reset_index()

df_dist_summary = df_dist_summary.merge(df_district[["District", "Population"]], on="District", how="left")
df_dist_summary["Green_per_Capita"] = df_dist_summary["Total_Park_Area_Sqm"] / df_dist_summary["Population"]
df_dist_summary["Ratio_to_Population"] = df_dist_summary["Monthly_Visitors"] / df_dist_summary["Population"]

# คำนวณดัชนีความพร้อมรายสวน (มี = 1 คะแนน, ไม่มี = 0 คะแนน) เต็ม 3 คะแนน
features_list = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]
df_park_filtered["Readiness_Score"] = df_park_filtered[features_list].apply(lambda x: x == "มี").sum(axis=1)

def classify_park(score):
    if score == 3: return "🥇 พรีเมียม (ครบ 3 ฟีเจอร์)"
    elif score >= 1: return "🥈 มาตรฐาน (มี 1-2 ฟีเจอร์)"
    else: return "🥉 พื้นที่พื้นฐาน (เน้นเดิน/วิ่ง)"

df_park_filtered["Readiness_Class"] = df_park_filtered["Readiness_Score"].apply(classify_park)

# จัดเตรียมโครงสร้างป้อนเข้าชาร์ตแบบ Dynamic 
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

total_green_area = df_chart_data["Chart_Area"].sum()
total_pop = df_district[df_district["District"] == selected_district]["Population"].sum() if selected_district != "ทั้งหมด" else df_district["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0
total_parks = len(df_park_filtered)

# ----------------------------------------------------------------------
# 4. DASHBOARD UI & VISUALIZATION (แสดงผลจับคู่ทีละ 2 กราฟ)
# ----------------------------------------------------------------------
st.title("🌳 Park Analytics Dashboard")
st.markdown("วิเคราะห์ภาพรวมขนาดพื้นที่ พฤติกรรมการใช้งาน และความพร้อมสอดคล้องเชิงสันทนาการ")
st.markdown("---")

### ส่วนที่ 1: KPI SCORECARDS
st.markdown("""
<style>
    .kpi-card { background-color: var(--background-color, #f8f9fa); padding: 22px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); border-left: 6px solid #2ecc71; text-align: left; }
    .kpi-label { font-size: 13px; color: #7f8c8d; text-transform: uppercase; margin-bottom: 6px; }
    .kpi-value { font-size: 26px; color: var(--text-color, #2c3e50); font-weight: 700; }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="kpi-card" style="border-left-color: #2ecc71;"><div class="kpi-label">🍃 พื้นที่สีเขียวรวม (ตามตัวกรอง)</div><div class="kpi-value">{total_green_area:,.1f} <span style="font-size:16px; font-weight:normal;">ตร.ม.</span></div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card" style="border-left-color: #3498db;"><div class="kpi-label">🏞️ จำนวนสวนสาธารณะรวม</div><div class="kpi-value">{total_parks:,} <span style="font-size:16px; font-weight:normal;">แห่ง</span></div></div>', unsafe_allow_html=True)
with col3:
    status_color = "#e74c3c" if bkk_green_per_capita < 9 else "#2ecc71"
    st.markdown(f'<div class="kpi-card" style="border-left-color: {status_color};"><div class="kpi-label">👤 พื้นที่สีเขียวต่อหัวประชากร</div><div class="kpi-value">{bkk_green_per_capita:.2f} <span style="font-size:16px; font-weight:normal;">ตร.ม./คน</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 📊 คู่ที่ 1: ขนาดพื้นที่รวม VS ปริมาณผู้ใช้งานจริง (2 Columns)
# ----------------------------------------------------------------------
pair1_col1, pair1_col2 = st.columns(2)

with pair1_col1:
    st.markdown(f"##### 🟢 การวิเคราะห์ขนาดพื้นที่รวม ({'รายเขต' if selected_district == 'ทั้งหมด' else f'รายสวนในเขต {selected_district}'})")
    if not df_chart_data.empty:
        df_sorted_area = df_chart_data.sort_values(by="Chart_Area", ascending=True)
        fig_area = px.bar(
            df_sorted_area, x="Chart_Area", y=y_axis_col, orientation='h',
            text=df_sorted_area["Chart_Area"].apply(lambda x: f" {x:,} {area_suffix}"),
            color="Chart_Area", color_continuous_scale="Greens",
            labels={"Chart_Area": "ขนาดพื้นที่ (ตร.ม.)", y_axis_col: y_label_text}
        )
        fig_area.update_traces(textposition='outside')
        fig_area.update_layout(showlegend=False, coloraxis_showscale=False, height=360, margin=dict(l=100, r=50, t=10, b=10))
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลพื้นที่")

with pair1_col2:
    st.markdown(f"##### 👥 ปริมาณสถิติผู้เข้าใช้งานจริงต่อเดือน ({'รายเขต' if selected_district == 'ทั้งหมด' else f'รายสวนในเขต {selected_district}'})")
    if not df_chart_data.empty:
        df_sorted_visitors = df_chart_data.sort_values(by="Chart_Visitors", ascending=True)
        fig_visitors = px.bar(
            df_sorted_visitors, x="Chart_Visitors", y=y_axis_col, orientation='h',
            text=df_sorted_visitors["Chart_Visitors"].apply(lambda x: f" {x:,} {visitor_suffix}"),
            color="Chart_Visitors", color_continuous_scale="Oranges",
            labels={"Chart_Visitors": "จำนวนผู้เข้าชม (คน/เดือน)", y_axis_col: y_label_text}
        )
        fig_visitors.update_traces(textposition='outside')
        fig_visitors.update_layout(showlegend=False, coloraxis_showscale=False, height=360, margin=dict(l=100, r=50, t=10, b=10))
        st.plotly_chart(fig_visitors, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลผู้ใช้งาน")

st.markdown("---")

# ----------------------------------------------------------------------
# 📊 คู่ที่ 2: อัตราส่วนแบกรับประชากร VS โดนัทสิ่งอำนวยความสะดวก (2 Columns)
# ----------------------------------------------------------------------
pair2_col1, pair2_col2 = st.columns(2)

with pair2_col1:
    st.markdown(f"##### 📈 อัตราส่วนสัดส่วนการแบกรับผู้ใช้งานเปรียบเทียบฐานประชากร")
    if not df_chart_data.empty:
        df_sorted_ratio = df_chart_data.sort_values(by="Chart_Ratio", ascending=True)
        fig_ratio = px.bar(
            df_sorted_ratio, x="Chart_Ratio", y=y_axis_col, orientation='h',
            text=df_sorted_ratio["Chart_Ratio"].apply(lambda x: f" {x:.2f} {ratio_suffix}"),
            color="Chart_Ratio", color_continuous_scale="Purples",
            labels={"Chart_Ratio": "ดัชนีอัตราส่วน (เท่า)", y_axis_col: y_label_text}
        )
        fig_ratio.update_traces(textposition='outside')
        fig_ratio.update_layout(showlegend=False, coloraxis_showscale=False, height=360, margin=dict(l=100, r=50, t=10, b=10))
        st.plotly_chart(fig_ratio, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลดัชนี")

with pair2_col2:
    st.markdown(f"##### 🍩 สัดส่วนระดับความพร้อมของสิ่งอำนวยความสะดวกภายในสวน")
    if not df_park_filtered.empty:
        # คำนวณและนับสัดส่วนระดับสวนในเงื่อนไขปัจจุบันเพื่อทำ Donut Chart
        df_donut_data = df_park_filtered["Readiness_Class"].value_counts().reset_index()
        df_donut_data.columns = ["ระดับความพร้อม", "จำนวนสวน"]
        
        fig_donut = px.pie(
            df_donut_data, values="จำนวนสวน", names="ระดับความพร้อม", hole=0.5,
            color="ระดับความพร้อม",
            color_discrete_map={
                "🥇 พรีเมียม (ครบ 3 ฟีเจอร์)": "#2ecc71",
                "🥈 มาตรฐาน (มี 1-2 ฟีเจอร์)": "#f1c40f",
                "🥉 พื้นที่พื้นฐาน (เน้นเดิน/วิ่ง)": "#e74c3c"
            }
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+value')
        fig_donut.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลสิ่งอำนวยความสะดวก")

st.markdown("---")

# ----------------------------------------------------------------------
# 📋 ส่วนที่ 5: ตารางสถิติสรุปพร้อมปุ่มดาวน์โหลด
# ----------------------------------------------------------------------
table_col, download_col = st.columns([4, 1])
with table_col:
    st.markdown("### 📋 ตารางสถิติและรายละเอียดสิ่งอำนวยความสะดวกของสวนสาธารณะ")
features_disp = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]

if not df_park_filtered.empty:
    df_table_show = df_park_filtered[["Park_Name", "District", "Park_Area_Sqm", "Park_Monthly_Visitors"] + features_disp].copy()
    df_table_show.columns = ["ชื่อสวนสาธารณะ", "เขตพื้นที่", "ขนาดพื้นที่ (ตร.ม.)", "ผู้ใช้บริการ (คน/เดือน)", "ที่จอดรถ", "มิตรกับสัตว์เลี้ยง", "ทางจักรยาน"]
    
    with download_col:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_table_show.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดข้อมูล (CSV)",
            data=csv_data,
            file_name="bkk_park_filtered_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    st.dataframe(df_table_show, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะตรงตามตัวกรองที่คุณเลือกในขณะนี้")
