import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้างและโมเดิร์น
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
# 2. SIDEBAR FILTERS (เมนูควบคุมซ้ายมือ ดีไซน์ใหม่ให้คลีนขึ้น)
# ----------------------------------------------------------------------
st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filters)")
st.sidebar.markdown("---")

# Filter 1: เลือกเขต
all_districts = ["ทั้งหมด"] + sorted(list(df_district["District"].unique()))
selected_district = st.sidebar.selectbox("📍 เลือกเขตพื้นที่:", all_districts)

# Filter 2: เลือกกรองตามสิ่งอำนวยความสะดวก
st.sidebar.markdown("<br><b>🚲 เงื่อนไขสิ่งอำนวยความสะดวก</b>", unsafe_allow_html=True)
filter_pet = st.sidebar.checkbox("เฉพาะสวนที่เป็นมิตรกับสัตว์เลี้ยง")
filter_bike = st.sidebar.checkbox("เฉพาะสวนที่ขี่จักรยานได้")

# ประยุกต์ใช้ Filter กับ Data
df_dist_filtered = df_district.copy()
df_park_filtered = df_parks.copy()

if selected_district != "ทั้งหมด":
    df_dist_filtered = df_dist_filtered[df_dist_filtered["District"] == selected_district]
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]

if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]
if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]


# ----------------------------------------------------------------------
# 3. DATA CALCULATION (คำนวณสถิติหลัก)
# ----------------------------------------------------------------------
# ปรับสูตรคำนวณให้ยืดหยุ่นและสัมพันธ์ตามฟิลเตอร์ด้านซ้าย
total_green_area = df_dist_filtered["Total_Park_Area_Sqm"].sum() if not filter_pet and not filter_bike else (len(df_park_filtered) * 150000) # Fallback หยาบๆ กรณีเลือกฟีเจอร์
total_parks = df_dist_filtered["Total_Parks"].sum() if not filter_pet and not filter_bike else len(df_park_filtered)
total_pop = df_dist_filtered["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0

# คำนวณรายเขตสำหรับกราฟแท่งหลัก
df_district["Green_per_Capita"] = df_district["Total_Park_Area_Sqm"] / df_district["Population"]
df_district["Visitor_Density_Ratio"] = df_district["Monthly_Visitors"] / df_district["Population"]


# ----------------------------------------------------------------------
# 4. DASHBOARD UI & VISUALIZATION
# ----------------------------------------------------------------------
st.title("🌳 Page 1: Park Analytics")
st.markdown("<p style='color: #7f8c8d; font-size: 16px;'>วิเคราะห์ภาพรวมความทั่วถึง พฤติกรรมความหนาแน่น และข้อจำกัดในการใช้งานสวนสาธารณะในกรุงเทพฯ</p>", unsafe_allow_html=True)
st.markdown("---")

### ส่วนที่ 1: PREMIUM SCORECARDS (ดีไซน์สไตล์คลีน มินิมอล มีเงาละมุน)
st.markdown("""
<style>
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
    }
    .kpi-card {
        flex: 1;
        background-color: #f8f9fa;
        padding: 22px 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #2ecc7
