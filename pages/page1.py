import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard
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
    df_district["Green_per_Capita"] = df_district["Total_Park_Area_Sqm"] / df_district["Population"]
    df_district["Visitor_Density_Ratio"] = df_district["Monthly_Visitors"] / df_district["Population"]

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
# 2. SIDEBAR FILTERS (ปรับปรุงการกรองไม่ให้ข้อมูลตารางตกหล่น)
# ----------------------------------------------------------------------
st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filters)")

all_districts = ["ทั้งหมด"] + list(df_district["District"].unique())
selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่:", all_districts)

st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚙️ เงื่อนไขสิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้")

# คัดลอกข้อมูลเพื่อเตรียมกรอง
df_dist_filtered = df_district.copy()
df_park_filtered = df_parks.copy()

# ลอจิกการกรอง: กรองรายสวนก่อน เพื่อให้ข้อมูลตารางด้านล่างตรงตามเงื่อนไขสิ่งอำนวยความสะดวกเสมอ
if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]
if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]

# จากนั้นค่อยกรองตามเขตพื้นที่ (ถ้าไม่ได้เลือกทั้งหมด)
if selected_district != "ทั้งหมด":
    df_dist_filtered = df_dist_filtered[df_dist_filtered["District"] == selected_district]
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]

# ----------------------------------------------------------------------
# 3. DATA CALCULATION
# ----------------------------------------------------------------------
total_green_area = df_dist_filtered["Total_Park_Area_Sqm"].sum()
total_pop = df_dist_filtered["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0
total_parks = len(df_park_filtered) if (filter_pet or filter_bike) else df_dist_filtered["Total_Parks"].sum()

# ----------------------------------------------------------------------
# 4. DASHBOARD UI
# ----------------------------------------------------------------------
st.title("🌳 Park Analytics Dashboard")
st.markdown("วิเคราะห์ภาพรวมความทั่วถึง พฤติกรรมความหนาแน่น และข้อจำกัดในการใช้งานสวนสาธารณะในกรุงเทพมหานคร")
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
    st.markdown(f'<div class="kpi-card" style="border-left-color: #2ecc71;"><div class="kpi-label">🍃 พื้นที่สีเขียวรวม ทั้งหมด</div><div class="kpi-value">{total_green_area:,.1f} <span style="font-size:16px; font-weight:normal;">ตร.ม.</span></div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card" style="border-left-color: #3498db;"><div class="kpi-label">🏞️ จำนวนสวนสาธารณะ</div><div class="kpi-value">{total_parks:,} <span style="font-size:16px; font-weight:normal;">แห่ง</span></div></div>', unsafe_allow_html=True)
with col3:
    status_color = "#e74c3c" if bkk_green_per_capita < 9 else "#2ecc71"
    st.markdown(f'<div class="kpi-card" style="border-left-color: {status_color};"><div class="kpi-label">👤 พื้นที่สีเขียวต่อหัวประชากร</div><div class="kpi-value">{bkk_green_per_capita:.2f} <span style="font-size:16px; font-weight:normal;">ตร.ม./คน</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

### ส่วนที่ 2: ANALYTICS (2 Columns)
st.markdown("### 📊 การวิเคราะห์มิติเชิงพื้นที่และความหนาแน่น")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("##### 🟢 พื้นที่สีเขียวต่อประชากร รายเขต")
    df_sorted_green = df_dist_filtered.sort_values(by="Green_per_Capita", ascending=True)
    fig_green = px.bar(df_sorted_green, x="Green_per_Capita", y="District", orientation='h', text=df_sorted_green["Green_per_Capita"].apply(lambda x: f" {x:.2f} ตร.ม."), color="Green_per_Capita", color_continuous_scale="Greens")
    fig_green.update_traces(textposition='outside')
    fig_green.update_layout(showlegend=False, coloraxis_showscale=False, height=350, margin=dict(l=50, r=50, t=10, b=10))
    st.plotly_chart(fig_green, use_container_width=True)

with chart_col2:
    st.markdown("##### 👥 อัตราส่วนความหนาแน่นผู้ใช้งานรายเดือน")
    df_sorted_density = df_dist_filtered.sort_values(by="Visitor_Density_Ratio", ascending=True)
    fig_density = px.bar(df_sorted_density, x="Visitor_Density_Ratio", y="District", orientation='h', text=df_sorted_density["Visitor_Density_Ratio"].apply(lambda x: f" {x:.2f} เท่า"), color="Visitor_Density_Ratio", color_continuous_scale="Oranges")
    fig_density.update_traces(textposition='outside')
    fig_density.update_layout(showlegend=False, coloraxis_showscale=False, height=350, margin=dict(l=50, r=50, t=10, b=10))
    st.plotly_chart(fig_density, use_container_width=True)

st.markdown("---")

### ส่วนที่ 3: PARK FEATURES
st.markdown("### 🚲 วิเคราะห์ข้อจำกัดและสิ่งอำนวยความสะดวกในการเข้าใช้บริการ")
features = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]
melted_records = []
for feat in features:
    counts = df_park_filtered[feat].value_counts().reindex(["มี", "ไม่มี"], fill_value=0)
    melted_records.append({"Feature": feat, "Availability": "มีบริการ", "Count": counts["มี"]})
    melted_records.append({"Feature": feat, "Availability": "ไม่มีบริการ", "Count": counts["ไม่มี"]})

df_features_plot = pd.DataFrame(melted_records)
fig_features = px.bar(df_features_plot, x="Count", y="Feature", color="Availability", orientation='h', text="Count", color_discrete_map={"มีบริการ": "#2ecc71", "ไม่มีบริการ": "#e74c3c"})
fig_features.update_layout(barmode="stack", legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1), height=280)
st.plotly_chart(fig_features, use_container_width=True)

st.markdown("---")

### ส่วนที่ 4: (เพิ่มเข้ามาใหม่) การวิเคราะห์มิติเชิงนโยบายเพื่อหาพื้นที่วิกฤต (Priority Gap Analysis)
st.markdown("### 🎯 ส่วนที่ 4: การวิเคราะห์หาพื้นที่วิกฤตเพื่อวางแผนเชิงนโยบาย (Gap Analysis)")
st.info("💡 **คำอธิบาย:** กราฟด้านล่างเปรียบเทียบระหว่าง 'จำนวนประชากร' และ 'พื้นที่สีเขียวที่มีอยู่จริง' เขตที่อยู่ **โซนขวาล่าง** (ประชากรหนาแน่นสูง แต่มีสวนสาธารณะน้อย) คือเขตวิกฤตเร่งด่วนที่เมืองควรเข้าจัดสรรหรือสร้างสวนแห่งใหม่เพิ่มก่อนเป็นอันดับแรก")

# สร้าง Scatter Plot เพื่อหาพื้นที่ที่เป็นช่องว่าง (Gap)
fig_gap = px.scatter(
    df_dist_filtered,
    x="Population",
    y="Total_Park_Area_Sqm",
    text="District",
    size="Monthly_Visitors", # ขนาดของจุดแปรผันตามจำนวนผู้ใช้งานจริง
    color="Green_per_Capita",
    color_continuous_scale="RdYlGn",
    labels={"Population": "จำนวนประชากรในเขต (คน)", "Total_Park_Area_Sqm": "พื้นที่สีเขียวรวม (ตร.ม.)", "Green_per_Capita": "ตร.ม./คน"}
)
fig_gap.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig_gap.update_layout(height=450, margin=dict(l=50, r=50, t=20, b=20))
st.plotly_chart(fig_gap, use_container_width=True)

st.markdown("---")

### ส่วนแสดงตารางข้อมูลรายชื่อสวน (ที่แก้ไขให้ขึ้นครบถ้วนและเปลี่ยนแปลงแบบ Real-time ตามตัวกรอง)
st.markdown("### 📋 ตารางข้อมูลสวนสาธารณะตามเงื่อนไขตัวกรองปัจจุบัน")
if not df_park_filtered.empty:
    st.dataframe(
        df_park_filtered[["Park_Name", "District"] + features], 
        use_container_width=True, 
        hide_index=True
    )
else:
    st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะตามเงื่อนไขตัวกรองที่คุณเลือกในปัจจุบัน กรุณาปรับตัวกรองที่แถบด้านซ้าย")
