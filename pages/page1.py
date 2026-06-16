import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as stop
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้าง (Wide mode)
st.set_page_config(page_title="Page 1: Park Analytics", layout="wide")

# ----------------------------------------------------------------------
# 1. MOCK DATA (จำลองข้อมูลเพื่อความเข้าใจโครงสร้าง)
# ----------------------------------------------------------------------
# หากมีข้อมูลจริง ให้ใช้ pd.read_csv() หรือ pd.read_excel() แทนส่วนนี้
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

    # ข้อมูลรายสวนสาธารณะ (สำหรับพฤติกรรม/สิ่งอำนวยความสะดวก)
    park_data = {
        "Park_Name": ["สวนจตุจักร", "สวนลุมพินี", "สวนรถไฟ", "สวนเบญจกิติ", "สวนสราญรมย์", "สวนธนบุรีรมย์", "สวนเสรีไทย"],
        "District": ["จตุจักร", "ปทุมวัน", "จตุจักร", "คลองเตย", "พระนคร", "ธนบุรี", "บึงกุ่ม"],
        "Has_Car_Park": ["Yes", "No", "Yes", "Yes", "No", "Yes", "No"],
        "Is_Pet_Friendly": ["No", "No", "Yes", "Yes", "No", "No", "Yes"],
        "Allow_Bicycle": ["No", "Yes", "Yes", "Yes", "No", "No", "Yes"] # ข้อมูลเชื่อมมาจาก Park_Path_Distance
    }
    df_parks = pd.DataFrame(park_data)
    
    return df_district, df_parks

df_district, df_parks = load_data()

# ----------------------------------------------------------------------
# 2. DATA CALCULATION (คำนวณตามโจทย์)
# ----------------------------------------------------------------------
# KPI 1 & 2: พื้นที่รวม และ จำนวนสวนรวม
total_green_area = df_district["Total_Park_Area_Sqm"].sum()
total_parks = df_district["Total_Parks"].sum()

# KPI 3: พื้นที่สีเขียวต่อประชากรกรุงเทพ (ภาพรวม)
total_pop = df_district["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop

# คำนวณรายเขต: พื้นที่สีเขียวเฉลี่ยต่อหัวประชากร (Green Space per Capita)
df_district["Green_per_Capita"] = df_district["Total_Park_Area_Sqm"] / df_district["Population"]

# คำนวณรายเขต: ความหนาแน่นของผู้ใช้งาน (ผู้ใช้บริการต่อเดือน / ประชากรในเขต)
df_district["Visitor_Density_Ratio"] = df_district["Monthly_Visitors"] / df_district["Population"]


# ----------------------------------------------------------------------
# 3. DASHBOARD UI & VISUALIZATION
# ----------------------------------------------------------------------
st.title("🌳 Page 1: Park Analytics Dashboard")
st.subheader("วิเคราะห์ความทั่วถึงและพฤติกรรมการใช้งานสวนสาธารณะของคนกรุงเทพฯ")
st.markdown("---")

### ส่วนที่ 1: SCORECARDS (KPIs ข้างบน)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="พื้นที่สีเขียวทั้งหมดในกรุงเทพฯ", 
        value=f"{total_green_area:,.2f} ตร.ม.",
        help="รวมพื้นที่สวนสาธารณะทุกเขตรวมกัน"
    )

with col2:
    st.metric(
        label="จำนวนสวนสาธารณะทั้งหมด", 
        value=f"{total_parks:,} แห่ง"
    )

with col3:
    st.metric(
        label="พื้นที่สีเขียวต่อประชากรภาพรวม (BKK)", 
        value=f"{bkk_green_per_capita:.2f} ตร.ม./คน",
        help="คำนวณจาก: Sum พื้นที่สวนทั้งหมด ÷ Sum ประชากรทั้งหมดทุกเขต"
    )

st.markdown("---")


### ส่วนที่ 2: ANALYTICS (กราฟวิเคราะห์ความทั่วถึงและความหนาแน่น)
st.header("📊 การเข้าถึงสวนสาธารณะ ความหนาแน่น และพฤติกรรมการใช้งาน")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🟢 พื้นที่สีเขียวต่อหัวประชากร แยกรายเขต (ตร.ม./คน)")
    # จัดอันดับ มากที่สุด VS น้อยที่สุด
    df_sorted_green = df_district.sort_values(by="Green_per_Capita", ascending=True)
    
    fig_green = px.bar(
        df_sorted_green,
        x="Green_per_Capita",
        y="District",
        orientation='h',
        text=df_sorted_green["Green_per_Capita"].apply(lambda x: f"{x:.2f}"),
        color="Green_per_Capita",
        color_continuous_scale="Greens",
        labels={"Green_per_Capita": "ตร.ม. ต่อคน", "District": "เขต"}
    )
    fig_green.update_traces(textposition='inside')
    fig_green.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_green, use_container_width=True)

with col_right:
    st.subheader("👥 อัตราส่วนความหนาแน่นของผู้ใช้งานต่อเดือน")
    # แนะนำเป็น Bar chart เรียงจากหนาแน่นสูงสุด เพื่อดูพฤติกรรมเขตที่คนนิยมไปใช้งานสวนสูงเกินประชากรในพื้นที่
    df_sorted_density = df_district.sort_values(by="Visitor_Density_Ratio", ascending=True)
    
    fig_density = px.bar(
        df_sorted_density,
        x="Visitor_Density_Ratio",
        y="District",
        orientation='h',
        text=df_sorted_density["Visitor_Density_Ratio"].apply(lambda x: f"{x:.2f} เท่า"),
        color="Visitor_Density_Ratio",
        color_continuous_scale="Oranges",
        labels={"Visitor_Density_Ratio": "จำนวนผู้ใช้บริการต่อเดือน / ประชากรในเขต", "District": "เขต"}
    )
    fig_density.update_traces(textposition='inside')
    fig_density.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_density, use_container_width=True)

st.markdown("---")


### ส่วนที่ 3: PARK FEATURES (สิ่งอำนวยความสะดวกและประเภทพฤติกรรมการใช้งาน)
st.subheader("🚲 สิ่งอำนวยความสะดวกและเงื่อนไขการใช้งานสวนสาธารณะ")
col_f1, col_f2, col_f3 = st.columns(3)

# คำนวณสัดส่วน/จำนวนของฟีเจอร์ต่างๆ
car_park_counts = df_parks["Has_Car_Park"].value_counts().reset_index()
pet_friendly_counts = df_parks["Is_Pet_Friendly"].value_counts().reset_index()
bicycle_counts = df_parks["Allow_Bicycle"].value_counts().reset_index()

with col_f1:
    st.write("**🚗 สวนที่มีที่จอดรถ (Car Park)**")
    fig_car = px.bar(
        car_park_counts, x="Has_Car_Park", y="count", 
        color="Has_Car_Park", color_discrete_map={"Yes": "#2ecc71", "No": "#e74c3c"},
        labels={"Has_Car_Park": "มีที่จอดรถ", "count": "จำนวนสวน"}
    )
    fig_car.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig_car, use_container_width=True)

with col_f2:
    st.write("**🐶 สวนที่เป็นมิตรกับสัตว์เลี้ยง (Pet Friendly)**")
    fig_pet = px.bar(
        pet_friendly_counts, x="Is_Pet_Friendly", y="count",
        color="Is_Pet_Friendly", color_discrete_map={"Yes": "#3498db", "No": "#e74c3c"},
        labels={"Is_Pet_Friendly": "เป็นมิตรกับสัตว์เลี้ยง", "count": "จำนวนสวน"}
    )
    fig_pet.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig_pet, use_container_width=True)

with col_f3:
    st.write("**🚲 สวนที่อนุญาตให้ปั่นจักรยาน**")
    fig_bike = px.bar(
        bicycle_counts, x="Allow_Bicycle", y="count",
        color="Allow_Bicycle", color_discrete_map={"Yes": "#9b59b6", "No": "#e74c3c"},
        labels={"Allow_Bicycle": "อนุญาตให้ขี่จักรยาน", "count": "จำนวนสวน"}
    )
    fig_bike.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig_bike, use_container_width=True)

# ตารางข้อมูลดิบด้านล่างสำหรับให้ User ตรวจสอบ
if st.checkbox("ดูตารางข้อมูลสวนสาธารณะทั้งหมด"):
    st.dataframe(df_parks, use_container_width=True)
