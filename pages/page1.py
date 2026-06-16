import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้าง (Wide mode) พร้อมไอคอนบนแท็บเว็บ
st.set_page_config(page_title="Page 1: Park Analytics", page_icon="🌳", layout="wide")

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

    # คำนวณอัตราส่วนล่วงหน้าก่อนทำการ Filter รายเขต
    df_district["Green_per_Capita"] = df_district["Total_Park_Area_Sqm"] / df_district["Population"]
    df_district["Visitor_Density_Ratio"] = df_district["Monthly_Visitors"] / df_district["Population"]

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
st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filters)")

# Filter 1: เลือกเขต
all_districts = ["ทั้งหมด"] + list(df_district["District"].unique())
selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่:", all_districts)

# Filter 2: เลือกกรองตามสิ่งอำนวยความสะดวก
st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚙️ เงื่อนไขสิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้")

# ประยุกต์ใช้ Filter กับ Dataframe
df_dist_filtered = df_district.copy()
df_park_filtered = df_parks.copy()

# กรองตามสิ่งอำนวยความสะดวกในสวนก่อน เพื่อนำไปกระทบรายเขต
if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]
if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]

# กรองตามพื้นที่/เขต
if selected_district != "ทั้งหมด":
    df_dist_filtered = df_dist_filtered[df_dist_filtered["District"] == selected_district]
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]


# ----------------------------------------------------------------------
# 3. DATA CALCULATION (คำนวณสถิติหลัก)
# ----------------------------------------------------------------------
total_green_area = df_dist_filtered["Total_Park_Area_Sqm"].sum()
total_pop = df_dist_filtered["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0

# หากมีการติ๊กเลือกสิ่งอำนวยความสะดวก ให้นับจำนวนสวนที่ผ่านตัวกรองจริง
if filter_pet or filter_bike:
    total_parks = len(df_park_filtered)
else:
    total_parks = df_dist_filtered["Total_Parks"].sum()


# ----------------------------------------------------------------------
# 4. DASHBOARD UI & VISUALIZATION
# ----------------------------------------------------------------------
st.title("🌳 Park Analytics Dashboard")
st.markdown("วิเคราะห์ภาพรวมความทั่วถึง พฤติกรรมความหนาแน่น และข้อจำกัดในการใช้งานสวนสาธารณะในกรุงเทพมหานคร")
st.markdown("---")

### ส่วนที่ 1: CUSTOM SCORECARDS (ปรับปรุง CSS รองรับทั้ง Light/Dark Mode)
st.markdown("""
<style>
    .kpi-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        flex: 1;
        background-color: var(--background-color, #f8f9fa);
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #2ecc71;
        text-align: left;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 13px;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        color: var(--text-color, #2c3e50);
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #2ecc71;">
        <div class="kpi-label">🍃 พื้นที่สีเขียวรวม ทั้งหมด</div>
        <div class="kpi-value">{total_green_area:,.1f} <span style="font-size:16px; font-weight:normal;">ตร.ม.</span></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #3498db;">
        <div class="kpi-label">🏞️ จำนวนสวนสาธารณะ</div>
        <div class="kpi-value">{total_parks:,} <span style="font-size:16px; font-weight:normal;">แห่ง</span></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # เพิ่มการไฮไลท์สีแดงหากต่ำกว่าเกณฑ์ของ WHO (9 ตร.ม./คน)
    status_color = "#e74c3c" if bkk_green_per_capita < 9 else "#2ecc71"
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {status_color};">
        <div class="kpi-label">👤 พื้นที่สีเขียวต่อหัวประชากร</div>
        <div class="kpi-value">{bkk_green_per_capita:.2f} <span style="font-size:16px; font-weight:normal;">ตร.ม./คน</span></div>
    </div>
    """, unsafe_allow_html=True)


### ส่วนที่ 2: ANALYTICS (แบ่งเป็น 2 คอลัมน์ซ้ายขวา เพื่อความประหยัดพื้นที่และเปรียบเทียบง่าย)
st.markdown("### 📊 การวิเคราะห์มิติเชิงพื้นที่และความหนาแน่น")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("##### 🟢 พื้นที่สีเขียวต่อประชากร รายเขต")
    st.caption("เกณฑ์แนะนำสากลโดย WHO คืออย่างน้อย 9 ตร.ม./คน")
    
    df_sorted_green = df_dist_filtered.sort_values(by="Green_per_Capita", ascending=True)
    
    fig_green = px.bar(
        df_sorted_green,
        x="Green_per_Capita",
        y="District",
        orientation='h',
        text=df_sorted_green["Green_per_Capita"].apply(lambda x: f" {x:.2f} ตร.ม."),
        color="Green_per_Capita",
        color_continuous_scale="Greens",
        labels={"Green_per_Capita": "ตร.ม. ต่อคน", "District": "เขต"}
    )
    fig_green.update_traces(textposition='outside')
    fig_green.update_layout(
        showlegend=False, 
        coloraxis_showscale=False, # ปิดแถบสีข้างๆ เพื่อให้กราฟสะอาดตาขึ้น
        height=380, 
        margin=dict(l=50, r=50, t=10, b=10)
    )
    st.plotly_chart(fig_green, use_container_width=True)

with chart_col2:
    st.markdown("##### 👥 อัตราส่วนความหนาแน่นผู้ใช้งานรายเดือน")
    st.caption("สูตร: จำนวนผู้ใช้บริการต่อเดือน ÷ จำนวนประชากรในเขต (ค่าสูง = หนาแน่นมาก)")
    
    df_sorted_density = df_dist_filtered.sort_values(by="Visitor_Density_Ratio", ascending=True)
    
    fig_density = px.bar(
        df_sorted_density,
        x="Visitor_Density_Ratio",
        y="District",
        orientation='h',
        text=df_sorted_density["Visitor_Density_Ratio"].apply(lambda x: f" {x:.2f} เท่า"),
        color="Visitor_Density_Ratio",
        color_continuous_scale="Oranges",
        labels={"Visitor_Density_Ratio": "อัตราส่วน (เท่า)", "District": "เขต"}
    )
    fig_density.update_traces(textposition='outside')
    fig_density.update_layout(
        showlegend=False, 
        coloraxis_showscale=False, # ปิดแถบสีข้างๆ
        height=380, 
        margin=dict(l=50, r=50, t=10, b=10)
    )
    st.plotly_chart(fig_density, use_container_width=True)

st.markdown("---")


### ส่วนที่ 3: NEW INTERPRETATION FOR PARK FEATURES (สัดส่วนความพร้อมรวมของเมือง)
st.markdown("### 🚲 วิเคราะห์ข้อจำกัดและสิ่งอำนวยความสะดวกในการเข้าใช้บริการ")
st.info("💡 **มุมมองเชิงนโยบาย:** กราฟด้านล่างแสดง 'สัดส่วนความพร้อมรวมของเมือง' เพื่อสะท้อนว่าสวนสาธารณะในกรุงเทพฯ รองรับไลฟ์สไตล์ยุคใหม่ (เช่น การพาสัตว์เลี้ยงมาเดิน หรือการปั่นจักรยาน) ได้ครอบคลุมแล้วหรือยัง")

# จัดการแปลงรูปแบบข้อมูลเพื่อสร้างกราฟแท่งแบบสะสม (Stacked Bar Chart เปรียบเทียบสัดส่วน มี VS ไม่มี)
features = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]
melted_records = []

for feat in features:
    # ดึงค่า count โดยใช้ reindex เพื่อป้องกันเออเร่อกรณีไม่มีข้อมูล "มี" หรือ "ไม่มี" เลยใน Filter นั้นๆ
    counts = df_park_filtered[feat].value_counts().reindex(["มี", "ไม่มี"], fill_value=0)
    melted_records.append({"Feature": feat, "Availability": "มีบริการ", "Count": counts["มี"]})
    melted_records.append({"Feature": feat, "Availability": "ไม่มีบริการ", "Count": counts["ไม่มี"]})

df_features_plot = pd.DataFrame(melted_records)

# สร้าง Stacked Bar Chart
fig_features = px.bar(
    df_features_plot,
    x="Count",
    y="Feature",
    color="Availability",
    orientation='h',
    text="Count",
    color_discrete_map={"มีบริการ": "#2ecc71", "ไม่มีบริการ": "#e74c3c"},
    labels={"Count": "จำนวนสวนสาธารณะ (แห่ง)", "Feature": "ประเภทสิ่งอำนวยความสะดวก", "Availability": "สถานะ"}
)
fig_features.update_layout(
    barmode="stack",
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    height=320,
    margin=dict(l=50, r=50, t=20, b=20)
)
st.plotly_chart(fig_features, use_container_width=True)

# ส่วนแสดงข้อมูลแบบตารางดิบ ซ่อน/แสดงได้ตามความต้องการผู้ใช้
with st.expander("🔍 ดูรายชื่อสวนสาธารณะและรายละเอียดฟีเจอร์แบบเจาะลึก (ตามตัวกรองปัจจุบัน)"):
    if not df_park_filtered.empty:
        st.dataframe(
            df_park_filtered[["Park_Name", "District"] + features], 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะที่ตรงกับเงื่อนไขการกรองปัจจุบันของคุณ")
