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
    # ข้อมูลรายเขต
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

    # ข้อมูลรายสวน (มีการใส่ตัวเลขจำลองพื้นที่ Sqm และผู้เข้าใช้ของแต่ละสวนเพื่อใช้ตอน Drill-down)
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
        # ข้อมูลจำลองรายส่วนสำหรับการวาดกราฟเดี่ยวตอนเลือกรายเขต
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
    
    # คำนวณคะแนนความพร้อมรายสวน (มี = 1, ไม่มี = 0)
    features_list = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]
    df_parks["Total_Score"] = df_parks[features_list].apply(lambda x: x == "มี").sum(axis=1)
    
    return df_district, df_parks

df_district, df_parks = load_data()

# ----------------------------------------------------------------------
# 2. SIDEBAR FILTERS
# ----------------------------------------------------------------------
st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filters)")

all_districts = ["ทั้งหมด"] + list(df_district["District"].unique())
selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่:", all_districts)

st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚙️ เงื่อนไขสิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้")

# คัดลอกข้อมูลเพื่อเตรียมกรองตามเงื่อนไข Sidebar
df_dist_filtered = df_district.copy()
df_park_filtered = df_parks.copy()

if filter_pet:
    df_park_filtered = df_park_filtered[df_park_filtered["มิตรกับสัตว์เลี้ยง (Pet Friendly)"] == "มี"]
if filter_bike:
    df_park_filtered = df_park_filtered[df_park_filtered["อนุญาตให้ขี่จักรยาน (Bicycle Path)"] == "มี"]

if selected_district != "ทั้งหมด":
    df_dist_filtered = df_dist_filtered[df_dist_filtered["District"] == selected_district]
    df_park_filtered = df_park_filtered[df_park_filtered["District"] == selected_district]

# ----------------------------------------------------------------------
# 3. DATA CALCULATION (สถิติสำหรับ KPI Cards)
# ----------------------------------------------------------------------
total_green_area = df_park_filtered["Park_Area_Sqm"].sum() if selected_district != "ทั้งหมด" else df_dist_filtered["Total_Park_Area_Sqm"].sum()
total_pop = df_dist_filtered["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0
total_parks = len(df_park_filtered)

# ----------------------------------------------------------------------
# 4. DASHBOARD UI & DYNAMIC VISUALIZATION
# ----------------------------------------------------------------------
st.title("🌳 Park Analytics Dashboard")
st.markdown("วิเคราะห์สถิติความทั่วถึง พฤติกรรมความหนาแน่น และความพร้อมของสิ่งอำนวยความสะดวก")
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
    st.markdown(f'<div class="kpi-card" style="border-left-color: #2ecc71;"><div class="kpi-label">🍃 พื้นที่สีเขียวรวม</div><div class="kpi-value">{total_green_area:,.1f} <span style="font-size:16px; font-weight:normal;">ตร.ม.</span></div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card" style="border-left-color: #3498db;"><div class="kpi-label">🏞️ จำนวนสวนสาธารณะ</div><div class="kpi-value">{total_parks:,} <span style="font-size:16px; font-weight:normal;">แห่ง</span></div></div>', unsafe_allow_html=True)
with col3:
    status_color = "#e74c3c" if bkk_green_per_capita < 9 else "#2ecc71"
    st.markdown(f'<div class="kpi-card" style="border-left-color: {status_color};"><div class="kpi-label">👤 พื้นที่สีเขียวต่อหัวประชากร</div><div class="kpi-value">{bkk_green_per_capita:.2f} <span style="font-size:16px; font-weight:normal;">ตร.ม./คน</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


### ส่วนที่ 2 & 3: LOGIC สลับร่างกราฟ (Drill-down)
chart_col1, chart_col2 = st.columns(2)

if selected_district == "ทั้งหมด":
    # ------------------------------------------------------------------
    # โหมดภาพรวม: แสดงรายเขต (District Mode)
    # ------------------------------------------------------------------
    with chart_col1:
        st.markdown("##### 🟢 พื้นที่สีเขียวต่อประชากร รายเขต")
        df_sorted = df_dist_filtered.sort_values(by="Green_per_Capita", ascending=True)
        fig1 = px.bar(df_sorted, x="Green_per_Capita", y="District", orientation='h', text=df_sorted["Green_per_Capita"].apply(lambda x: f" {x:.2f} ตร.ม."), color="Green_per_Capita", color_continuous_scale="Greens")
        fig1.update_traces(textposition='outside')
        fig1.update_layout(showlegend=False, coloraxis_showscale=False, height=350, margin=dict(l=50, r=50, t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        st.markdown("##### 👥 อัตราส่วนความหนาแน่นผู้ใช้งานรายเดือน รายเขต")
        df_sorted_density = df_dist_filtered.sort_values(by="Visitor_Density_Ratio", ascending=True)
        fig2 = px.bar(df_sorted_density, x="Visitor_Density_Ratio", y="District", orientation='h', text=df_sorted_density["Visitor_Density_Ratio"].apply(lambda x: f" {x:.2f} เท่า"), color="Visitor_Density_Ratio", color_continuous_scale="Oranges")
        fig2.update_traces(textposition='outside')
        fig2.update_layout(showlegend=False, coloraxis_showscale=False, height=350, margin=dict(l=50, r=50, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ส่วนที่ 3: Stack ความพร้อมแบบรายเขต
    st.markdown("### 📊 วิเคราะห์สัดส่วนระดับความพร้อมของสิ่งอำนวยความสะดวก แยกตามรายเขต")
    # หาค่าเฉลี่ยคะแนนความพร้อมของสวนในแต่ละเขตเพื่อเอามาพลอต Stack
    df_district_stack = df_park_filtered.groupby(["District", "Total_Score"]).size().reset_index(name="Count")
    df_district_stack["Total_Score"] = df_district_stack["Total_Score"].map({
        3: "🥇 ครบ 3 ฟีเจอร์ (พรีเมียม)", 2: "🥈 มี 2 ฟีเจอร์", 1: "🥉 มี 1 ฟีเจอร์", 0: "❌ ไม่มีฟีเจอร์สันทนาการเลย"
    })
    
    fig3 = px.bar(df_district_stack, x="Count", y="District", color="Total_Score", orientation='h', text="Count",
                  color_discrete_map={"🥇 ครบ 3 ฟีเจอร์ (พรีเมียม)": "#2ecc71", "🥈 มี 2 ฟีเจอร์": "#f1c40f", "🥉 มี 1 ฟีเจอร์": "#e67e22", "❌ ไม่มีฟีเจอร์สันทนาการเลย": "#e74c3c"},
                  labels={"Count": "จำนวนสวน (แห่ง)", "District": "เขต", "Total_Score": "ระดับความครบครัน"})
    fig3.update_layout(barmode="stack", height=380, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig3, use_container_width=True)

else:
    # ------------------------------------------------------------------
    # โหมดเจาะลึก: สลับร่างเป็นรายสวนในเขตนั้นๆ (Park Mode)
    # ------------------------------------------------------------------
    with chart_col1:
        st.markdown(f"##### 🟢 ขนาดพื้นที่สวนแต่ละแห่ง ในเขต{selected_district}")
        df_park_sorted = df_park_filtered.sort_values(by="Park_Area_Sqm", ascending=True)
        fig1_park = px.bar(df_park_sorted, x="Park_Area_Sqm", y="Park_Name", orientation='h', text=df_park_sorted["Park_Area_Sqm"].apply(lambda x: f" {x:,} ตร.ม."), color="Park_Area_Sqm", color_continuous_scale="Greens")
        fig1_park.update_traces(textposition='outside')
        fig1_park.update_layout(showlegend=False, coloraxis_showscale=False, height=350, margin=dict(l=150, r=50, t=10, b=10))
        st.plotly_chart(fig1_park, use_container_width=True)

    with chart_col2:
        st.markdown(f"##### 👥 จำนวนผู้เข้าใช้งานจริงรายสวน ในเขต{selected_district}")
        df_park_sorted_visit = df_park_filtered.sort_values(by="Park_Monthly_Visitors", ascending=True)
        fig2_park = px.bar(df_park_sorted_visit, x="Park_Monthly_Visitors", y="Park_Name", orientation='h', text=df_park_sorted_visit["Park_Monthly_Visitors"].apply(lambda x: f" {x:,} คน"), color="Park_Monthly_Visitors", color_continuous_scale="Oranges")
        fig2_park.update_traces(textposition='outside')
        fig2_park.update_layout(showlegend=False, coloraxis_showscale=False, height=350, margin=dict(l=150, r=50, t=10, b=10))
        st.plotly_chart(fig2_park, use_container_width=True)

    st.markdown("---")

    # ส่วนที่ 3: Stack ความพร้อมแบบรายสถานที่ (โชว์ฟีเจอร์จริงของสวนแต่ละแห่งในเขตนั้นไปเลย)
    st.markdown(f"### 🗺️ เจาะลึกสิ่งอำนวยความสะดวกรายสวน ในเขต{selected_district}")
    
    # ดึงข้อมูลฟีเจอร์รายสวนมาทำ Stack เพื่อดูว่าสวนแต่ละแห่งได้สีเขียวหรือสีแดงในฟีเจอร์ไหนบ้าง
    features = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]
    melted_records = []
    for _, row in df_park_filtered.iterrows():
        for feat in features:
            melted_records.append({
                "Park_Name": row["Park_Name"],
                "Feature": feat,
                "Status": "มีบริการ" if row[feat] == "มี" else "ไม่มีบริการ"
            })
    df_park_stack = pd.DataFrame(melted_records)
    
    fig3_park = px.bar(df_park_stack, x="Feature", y="Park_Name", color="Status", orientation='h',
                       color_discrete_map={"มีบริการ": "#2ecc71", "ไม่มีบริการ": "#e74c3c"},
                       labels={"Feature": "ประเภทฟีเจอร์", "Park_Name": "ชื่อสวนสาธารณะ", "Status": "สถานะ"})
    fig3_park.update_layout(barmode="stack", height=320, legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1))
    st.plotly_chart(fig3_park, use_container_width=True)


st.markdown("---")

### 📋 ตารางข้อมูลสวนสาธารณะตามเงื่อนไขตัวกรองปัจจุบัน
st.markdown("### 📋 รายชื่อและรายละเอียดสิ่งอำนวยความสะดวกของสวนสาธารณะ")
features_disp = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]
if not df_park_filtered.empty:
    st.dataframe(
        df_park_filtered[["Park_Name", "District"] + features_disp], 
        use_container_width=True, 
        hide_index=True
    )
else:
    st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะตามเงื่อนไขตัวกรองที่คุณเลือกในปัจจุบัน")
