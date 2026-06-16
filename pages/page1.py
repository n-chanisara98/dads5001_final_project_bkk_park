import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้าง (Wide mode)
st.set_page_config(page_title="Page 1: Park Analytics", layout="wide")

# ----------------------------------------------------------------------
# 1. MOCK DATA (โครงสร้างข้อมูลจำลองเพื่อประมวลผล)
# ----------------------------------------------------------------------
@st.cache_data
def load_data():
    # ข้อมูลรายเขต
    district_data = {
        "District": ["จตุจักร", "ปทุมวัน", "ราชเทวี", "คลองเตย", "บางขุนเทียน", "ลาดกระบัง", "พระนคร", "ห้วยขวาง", "บางแค", "ธนบุรี"],
        "Population": [150000, 50000, 70000, 100000, 180000, 170000, 45000, 80000, 130000, 110000],
        "Total_Park_Area_Sqm": [900000, 600000, 50000, 400000, 1200000, 850000, 30000, 40000, 90000, 35000],
        "Total_Parks": [5, 3, 2, 4, 6, 5, 2, 1, 3, 2],
        "Monthly_Visitors": [120000, 95000, 15000, 80000, 45000, 50000, 35000, 12000, 25000, 22000]
    }
    df_district = pd.DataFrame(district_data)

    # ข้อมูลรายสวน
    park_data = {
        "Park_Name": ["สวนจตุจักร", "สวนลุมพินี", "สวนรถไฟ", "สวนเบญจกิติ", "สวนสราญรมย์", "สวนธนบุรีรมย์", "สวนเสรีไทย", "สวนเฉลิมพระเกียรติ 80 พรรษา", "สวนสันติภาพ", "สวนรมณีย์นาถ"],
        "District": ["จตุจักร", "ปทุมวัน", "จตุจักร", "คลองเตย", "พระนคร", "ธนบุรี", "บึงกุ่ม", "บางแค", "ราชเทวี", "พระนคร"],
        "ที่จอดรถ (Car Park)": ["มี", "ไม่มี", "มี", "มี", "ไม่มี", "มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี"],
        "มิตรกับสัตว์เลี้ยง (Pet Friendly)": ["ไม่มี", "ไม่มี", "มี", "มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี"],
        "อนุญาตให้ขี่จักรยาน (Bicycle Path)": ["ไม่มี", "มี", "มี", "มี", "ไม่มี", "ไม่มี", "มี", "ไม่มี", "ไม่มี", "ไม่มี"]
    }
    df_parks = pd.DataFrame(park_data)
    
    return df_district, df_parks

df_district, df_parks = load_data()


# ----------------------------------------------------------------------
# 2. SIDEBAR FILTERS (เมนูควบคุมซ้ายมือ)
# ----------------------------------------------------------------------
st.sidebar.header("🔍 ตัวกรองข้อมูล (Filters)")

# Filter 1: เลือกเขต
all_districts = ["ทั้งหมด"] + list(df_district["District"].unique())
selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่:", all_districts)

# Filter 2: เลือกกรองตามสิ่งอำนวยความสะดวก
st.sidebar.subheader("เงื่อนไขสิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("เฉพาะสวนที่เป็นมิตรกับสัตว์เลี้ยง (Pet Friendly)")
filter_bike = st.sidebar.checkbox("เฉพาะสวนที่ขี่จักรยานได้")

# ประยุกต์ใช้ Filter กับ Data Dataframe
df_dist_filtered = df_district.copy()
df_park_filtered = df_parks.copy()

if selected_district != "Total" and selected_district != "ทั้งหมด":
    df_dist_filtered = df_dist_filtered[df_dist_filtered["District"] == selected_district]
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]

if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]
if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]


# ----------------------------------------------------------------------
# 3. DATA CALCULATION (คำนวณสถิติหลัก)
# ----------------------------------------------------------------------
total_green_area = df_dist_filtered["Total_Park_Area_Sqm"].sum()
total_parks = df_dist_filtered["Total_Parks"].sum() if filter_pet == False and filter_bike == False else len(df_park_filtered)
total_pop = df_dist_filtered["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0

# คำนวณรายเขตสำหรับทำกราฟเดี่ยว
df_district["Green_per_Capita"] = df_district["Total_Park_Area_Sqm"] / df_district["Population"]
df_district["Visitor_Density_Ratio"] = df_district["Monthly_Visitors"] / df_district["Population"]


# ----------------------------------------------------------------------
# 4. DASHBOARD UI & VISUALIZATION
# ----------------------------------------------------------------------
st.title("🌳 Page 1: Park Analytics")
st.markdown("วิเคราะห์ภาพรวมความทั่วถึง พฤติกรรมความหนาแน่น และข้อจำกัดในการใช้งานสวนสาธารณะในกรุงเทพฯ")
st.markdown("---")

### ส่วนที่ 1: CUSTOM SCORECARDS (ออกแบบกรอบให้สวยงามด้วย CSS)
st.markdown("""
<style>
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2ecc71;
        text-align: center;
    }
    .kpi-label {
        font-size: 14px;
        color: #7f8c8d;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 24px;
        color: #2c3e50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #27ae60;">
        <div class="kpi-label">พื้นที่สีเขียวทั้งหมด</div>
        <div class="kpi-value">{total_green_area:,.2f} ตร.ม.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #2980b9;">
        <div class="kpi-label">จำนวนสวนสาธารณะทั้งหมด</div>
        <div class="kpi-value">{total_parks:,} แห่ง</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #e67e22;">
        <div class="kpi-label">พื้นที่สีเขียวต่อประชากร</div>
        <div class="kpi-value">{bkk_green_per_capita:.2f} ตร.ม./คน</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


### ส่วนที่ 2: ANALYTICS (กราฟแบบเดี่ยว ไม่แบ่งฝั่ง เห็นชัดเต็มตา)

# กราฟที่ 1: พื้นที่สีเขียวเฉลี่ยต่อหัวประชากร
st.subheader("🟢 พื้นที่สีเขียวเฉลี่ยต่อหัวประชากร (Green Space per Capita) รายเขต")
st.markdown("> *เกณฑ์แนะนำสากลโดย WHO คืออย่างน้อย 9 ตร.ม./คนเพื่อสุขภาวะที่ดี*")

df_sorted_green = df_district.sort_values(by="Green_per_Capita", ascending=True)
fig_green = px.bar(
    df_sorted_green,
    x="Green_per_Capita",
    y="District",
    orientation='h',
    text=df_sorted_green["Green_per_Capita"].apply(lambda x: f"{x:.2f} ตร.ม."),
    color="Green_per_Capita",
    color_continuous_scale="YlGn",
    labels={"Green_per_Capita": "พื้นที่สีเขียว (ตร.ม. ต่อคน)", "District": "เขต"}
)
fig_green.update_traces(textposition='outside')
fig_green.update_layout(showlegend=False, height=400, margin=dict(l=100, r=50, t=20, b=20))
st.plotly_chart(fig_green, use_container_width=True)

st.markdown("---")

# กราฟที่ 2: อัตราส่วนความหนาแน่นของผู้ใช้งานต่อเดือน
st.subheader("👥 อัตราส่วนความหนาแน่นของผู้ใช้งานต่อเดือน แยกรายเขต")
st.markdown("> *คำนวณจาก: จำนวนผู้ใช้บริการในสวนต่อเดือน ÷ จำนวนประชากรทั้งหมดในเขตนั้น (ค่าสูงแปลว่ามีการใช้งานหนาแน่น หรือดึงดูดคนจากเขตอื่นเข้ามามาก)*")

df_sorted_density = df_district.sort_values(by="Visitor_Density_Ratio", ascending=True)
fig_density = px.bar(
    df_sorted_density,
    x="Visitor_Density_Ratio",
    y="District",
    orientation='h',
    text=df_sorted_density["Visitor_Density_Ratio"].apply(lambda x: f"{x:.2f} เท่าของปชกร."),
    color="Visitor_Density_Ratio",
    color_continuous_scale="Oranges",
    labels={"Visitor_Density_Ratio": "อัตราส่วนความหนาแน่น (เท่า)", "District": "เขต"}
)
fig_density.update_traces(textposition='outside')
fig_density.update_layout(showlegend=False, height=400, margin=dict(l=100, r=100, t=20, b=20))
st.plotly_chart(fig_density, use_container_width=True)

st.markdown("---")


### ส่วนที่ 3: NEW INTERPRETATION FOR PARK FEATURES (ปรับมุมมองการวิเคราะห์สิ่งอำนวยความสะดวก)
import plotly.graph_objects as go

# 1. คำนวณร้อยละความพร้อมของแต่ละฟีเจอร์ (เช่น สวนที่มีที่จอดรถ คิดเป็นกี่ % ของสวนทั้งหมด)
total_parks_count = len(df_park_filtered) if len(df_park_filtered) > 0 else 1

pct_car = (df_park_filtered["ที่จอดรถ (Car Park)"] == "มี").sum() / total_parks_count * 100
pct_pet = (df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี").sum() / total_parks_count * 100
pct_bike = (df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี").sum() / total_parks_count * 100

# 2. สร้างกราฟเรดาร์
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
      r=[pct_car, pct_pet, pct_bike, pct_car], # ใส่ค่าแรกซ้ำตอนท้ายเพื่อปิดวงกลม
      theta=['มีที่จอดรถ (%)', 'เป็น Pet Friendly (%)', 'ปั่นจักรยานได้ (%)', 'มีที่จอดรถ (%)'],
      fill='toself',
      fillcolor='rgba(46, 204, 113, 0.3)',
      line=dict(color='#2ecc71', width=2)
))

fig_radar.update_layout(
  polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
  showlegend=False,
  height=350
)
st.plotly_chart(fig_radar, use_container_width=True)
