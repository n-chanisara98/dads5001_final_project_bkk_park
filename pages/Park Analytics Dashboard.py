import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้าง (Wide mode)
st.set_page_config(page_title="Page 1: Park Analytics", page_icon="🌳", layout="wide")

# ----------------------------------------------------------------------
# 🎨 AIRBNB STYLE WITH PARK BACKGROUND & TH AI SARABUN FONT
# ----------------------------------------------------------------------
st.markdown("""
<style>
    /* นำเข้าฟอนต์ TH Sarabun จากคลัง Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');

    /* 1. ตั้งค่าฟอนต์ TH Sarabun และภาพพื้นหลังวิวสวนสาธารณะ */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Sarabun', sans-serif !important;
        background: linear-gradient(rgba(15, 23, 42, 0.25), rgba(15, 23, 42, 0.25)), 
                    url('https://images.unsplash.com/photo-1519331379826-f10be5486c6f?q=80&w=1920') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff !important;
    }

    /* คุมสไตล์ข้อความทั่วไป */
    p, span, label, th, td {
        font-family: 'Sarabun', sans-serif !important;
        font-size: 18px !important;
        color: #ffffff !important;
    }
    
    /* 2. ปรับแต่งคอนเทนต์หลักให้เป็นแผ่นกระจกฝ้าโปร่งเข้มสไตล์ดาร์กหรูหราแบบ Airbnb */
    [data-testid="stMainBlockContainer"] {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(25px) saturate(150%);
        -webkit-backdrop-filter: blur(25px) saturate(150%);
        border-radius: 20px;
        padding: 40px !important;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    /* 3. ปรับแต่งสไตล์ดาร์กเนวี่สเปซฝั่งเมนูด้านข้าง (Sidebar) ตามรูปแบบภาพแป๊ะๆ */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #111827 !important; /* สีกรมท่าเข้มเกือบดำ */
        border-right: 1px solid #1f2937;
    }
    
    /* หัวข้อเมนูฟิลเตอร์ฝั่งแถบข้าง */
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-family: 'Sarabun', sans-serif !important;
    }
    
    /* 4. ปรับแต่งรูปทรงของ Widget ฟิลเตอร์ใน Sidebar */
    [data-testid="stSidebar"] .stSelectbox [data-testid="stWidgetLabel"] {
        margin-bottom: 6px;
    }
    [data-testid="stSidebar"] .stCheckbox, [data-testid="stSidebar"] .stSelectbox {
        background-color: rgba(255, 255, 255, 0.05) !important;
        padding: 6px 12px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 15px;
    }
    
    /* สไตล์หัวข้อหลักบนหน้าจอ */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Sarabun', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    h1 {
        font-size: 40px !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* 5. การ์ดตัวเลข KPI Scorecards ดีไซน์สไตล์ Airbnb (สี่เหลี่ยมขอบมนกระจกโปร่งเทา) */
    .kpi-card {
        background-color: rgba(255, 255, 255, 0.08);
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ff385c; /* สีชมพูแดงเอกลักษณ์แบบ Airbnb */
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        background-color: rgba(255, 255, 255, 0.12);
    }
    .kpi-label {
        font-size: 15px !important;
        color: #cbd5e1 !important;
        font-weight: 400;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 32px !important;
        color: #ffffff !important;
        font-weight: 700;
    }
    .kpi-unit {
        font-size: 16px !important;
        color: #94a3b8 !important;
        margin-left: 5px;
    }
    
    /* กล่องสรุป Insight บรรทัดเดียว */
    .insight-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #ff385c;
        padding: 14px 20px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 25px;
        color: #e2e8f0;
        font-size: 17px !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* จัดสไตล์โครงสร้างตารางข้อมูลสีดาร์ก */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border-radius: 12px;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)

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
st.sidebar.markdown("### 🎯 Filters")

selected_district = st.sidebar.selectbox("เลือกเขตพื้นที่:", ["ทั้งหมด"] + list(df_district["District"].unique()), key="sel_dist")
st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚙️ สิ่งอำนวยความสะดวก")
filter_pet = st.sidebar.checkbox("🐾 เฉพาะมิตรกับสัตว์เลี้ยง", key="chk_pet")
filter_bike = st.sidebar.checkbox("🚲 เฉพาะที่ขี่จักรยานได้", key="chk_bike")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
def reset_filters():
    st.session_state.sel_dist = "ทั้งหมด"
    st.session_state.chk_pet = False
    st.session_state.chk_bike = False

st.sidebar.button("🔄 ล้างตัวกรองทั้งหมด", on_click=reset_filters, use_container_width=True)

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
    df_chart_data["Chart_Visitors"] = df_park_filtered["Park_Monthly_Visitors"]
    
    current_pop = df_district[df_district["District"] == selected_district]["Population"].values[0]
    df_chart_data["Chart_Ratio"] = df_chart_data["Chart_Visitors"] / current_pop
    area_suffix, visitor_suffix, ratio_suffix = "ตร.ม.", "คน/เดือน", "เท่าของปชกร.เขต"

total_green_area = df_chart_data["Chart_Area"].sum()
total_pop = df_district[df_district["District"] == selected_district]["Population"].sum() if selected_district != "ทั้งหมด" else df_district["Population"].sum()
bkk_green_per_capita = total_green_area / total_pop if total_pop > 0 else 0
total_parks = len(df_park_filtered)

# ฟังก์ชันปรับแต่งดีไซน์กราฟแบบ Dark Mode ให้อ่านไทยสระบุรีชัดเจน
def apply_premium_layout(fig):
    fig.update_traces(textposition='outside', textfont=dict(size=14, color='#ffffff', family="Sarabun"))
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,0.04)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Sarabun, sans-serif", size=15, color='#ffffff'),
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=110, r=60, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False, tickfont=dict(color='#cbd5e1')),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#cbd5e1'))
    )
    return fig

# ----------------------------------------------------------------------
# 4. DASHBOARD UI & VISUALIZATION
# ----------------------------------------------------------------------
st.title("🏡 Airbnb BKK Park Market Analytics")
st.markdown("<p style='font-size: 18px; color:#cbd5e1; margin-top:-10px;'>วิเคราะห์โครงสร้างพื้นที่สีเขียว มิติการใช้งานสันทนาการ และปริมาณความหนาแน่นเชิงสถิติทั่วกรุงเทพมหานคร</p>", unsafe_allow_html=True)
st.markdown("---")

### ส่วนที่ 1: KPI SCORECARDS (Airbnb Style)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">🍃 พื้นที่สีเขียวรวม (ตามตัวกรอง)</div>
        <div class="kpi-value">{total_green_area:,.1f}<span class="kpi-unit">ตร.ม.</span></div>
    </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">🏞️ จำนวนสวนสาธารณะรวม</div>
        <div class="kpi-value">{total_parks:,}<span class="kpi-unit">แห่ง</span></div>
    </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">👤 พื้นที่สีเขียวต่อหัวประชากร</div>
        <div class="kpi-value">{bkk_green_per_capita:.2f}<span class="kpi-unit">ตร.ม./คน</span></div>
    </div>
    ''', unsafe_allow_html=True)

# [กล่องสรุปจุดสำคัญที่สุดเพียงหนึ่งเดียว ไว้ด้านบนสุด]
if not df_chart_data.empty:
    max_area_name = df_chart_data.loc[df_chart_data["Chart_Area"].idxmax()][y_axis_col]
    max_visit_name = df_chart_data.loc[df_chart_data["Chart_Visitors"].idxmax()][y_axis_col]
    max_ratio_name = df_chart_data.loc[df_chart_data["Chart_Ratio"].idxmax()][y_axis_col]
    
    st.markdown(f'''
    <div class="insight-card">
        <strong>💡 สรุปจุดสำคัญเชิงสถิติ (Key Insights):</strong> &nbsp;
        พื้นที่ขนาดใหญ่ที่สุด: <u>{max_area_name}</u> &nbsp;|&nbsp; 
        ปริมาณผู้ใช้งานจริงสูงสุด: <u>{max_visit_name}</u> &nbsp;|&nbsp; 
        ดัชนีแบกรับภาระประชากรสูงสุด: <u>{max_ratio_name}</u>
    </div>
    ''', unsafe_allow_html=True)

# คำนวณความสูงชาร์ตแบบ Dynamic
num_rows = len(df_chart_data)
dynamic_height = max(360, num_rows * 38)

# ----------------------------------------------------------------------
# 📊 คู่ที่ 1: ขนาดพื้นที่รวม VS ปริมาณผู้ใช้งานจริง (2 Columns)
# ----------------------------------------------------------------------
pair1_col1, pair1_col2 = st.columns(2)

with pair1_col1:
    st.markdown(f"<h5>🟢 การวิเคราะห์ขนาดพื้นที่รวม ({'รายเขต' if selected_district == 'ทั้งหมด' else f'รายสวนในเขต {selected_district}'})</h5>", unsafe_allow_html=True)
    if not df_chart_data.empty:
        df_sorted_area = df_chart_data.sort_values(by="Chart_Area", ascending=True)
        fig_area = px.bar(
            df_sorted_area, x="Chart_Area", y=y_axis_col, orientation='h',
            text=df_sorted_area["Chart_Area"].apply(lambda x: f" {x:,} {area_suffix}"),
            color="Chart_Area", color_continuous_scale="Greens",
            labels={"Chart_Area": "ขนาดพื้นที่ (ตร.ม.)", y_axis_col: y_label_text}
        )
        fig_area = apply_premium_layout(fig_area)
        fig_area.update_layout(height=dynamic_height)
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลพื้นที่")

with pair1_col2:
    st.markdown(f"<h5>👥 ปริมาณสถิติผู้เข้าใช้งานจริงต่อเดือน ({'รายเขต' if selected_district == 'ทั้งหมด' else f'รายสวนในเขต {selected_district}'})</h5>", unsafe_allow_html=True)
    if not df_chart_data.empty:
        df_sorted_visitors = df_chart_data.sort_values(by="Chart_Visitors", ascending=True)
        fig_visitors = px.bar(
            df_sorted_visitors, x="Chart_Visitors", y=y_axis_col, orientation='h',
            text=df_sorted_visitors["Chart_Visitors"].apply(lambda x: f" {x:,} {visitor_suffix}"),
            color="Chart_Visitors", color_continuous_scale="Oranges",
            labels={"Chart_Visitors": "จำนวนผู้เข้าชม (คน/เดือน)", y_axis_col: y_label_text}
        )
        fig_visitors = apply_premium_layout(fig_visitors)
        fig_visitors.update_layout(height=dynamic_height)
        st.plotly_chart(fig_visitors, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลผู้ใช้งาน")

st.markdown("---")

# ----------------------------------------------------------------------
# 📊 คู่ที่ 2: อัตราส่วนแบกรับประชากร VS สัดส่วนสิ่งอำนวยความสะดวกแยกประเภท (2 Columns)
# ----------------------------------------------------------------------
pair2_col1, pair2_col2 = st.columns(2)

with pair2_col1:
    st.markdown(f"<h5>📈 อัตราส่วนสัดส่วนการแบกรับผู้ใช้งานเปรียบเทียบฐานประชากร</h5>", unsafe_allow_html=True)
    if not df_chart_data.empty:
        df_sorted_ratio = df_chart_data.sort_values(by="Chart_Ratio", ascending=True)
        fig_ratio = px.bar(
            df_sorted_ratio, x="Chart_Ratio", y=y_axis_col, orientation='h',
            text=df_sorted_ratio["Chart_Ratio"].apply(lambda x: f" {x:.2f} {ratio_suffix}"),
            color="Chart_Ratio", color_continuous_scale="Purples",
            labels={"Chart_Ratio": "ดัชนีอัตราส่วน (เท่า)", y_axis_col: y_label_text}
        )
        fig_ratio = apply_premium_layout(fig_ratio)
        fig_ratio.update_layout(height=dynamic_height)
        st.plotly_chart(fig_ratio, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลดัชนี")

with pair2_col2:
    st.markdown(f"<h5>🍩 สัดส่วนความพร้อมแยกตามประเภทสิ่งอำนวยความสะดวก</h5>", unsafe_allow_html=True)
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
            df_feature_pie, values="จำนวนที่มีบริการ", names="สิ่งอำนวยความสะดวก", hole=0.5,
            color="สิ่งอำนวยความสะดวก",
            color_discrete_map={"ที่จอดรถ": "#ff385c", "ทางจักรยาน": "#3b82f6", "มิตรกับสัตว์เลี้ยง": "#06b6d4"}
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+value', insidetextfont=dict(size=14, weight='bold', color='#ffffff', family="Sarabun"))
        fig_donut.update_layout(
            height=360, 
            margin=dict(l=40, r=40, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Sarabun, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5, font=dict(color="#ffffff"))
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลสิ่งอำนวยความสะดวก")

st.markdown("---")

# ----------------------------------------------------------------------
# 📋 ส่วนที่ 5: ตารางสถิติสรุปพร้อมปุ่มดาวน์โหลด (ระนาบเดียวกันแบบ Perfect Grid)
# ----------------------------------------------------------------------
table_header_col, download_btn_col = st.columns([3, 1])

with table_header_col:
    st.markdown(f"<h3>📋 ตารางสถิติและรายละเอียดสิ่งอำนวยความสะดวกของสวนสาธารณะ</h3>", unsafe_allow_html=True)

features_disp = ["ที่จอดรถ (Car Park)", "มิตรกับสัตว์เลี้ยง (Pet Friendly)", "อนุญาตให้ขี่จักรยาน (Bicycle Path)"]

if not df_park_filtered.empty:
    df_table_show = df_park_filtered[["Park_Name", "District", "Park_Area_Sqm", "Park_Monthly_Visitors"] + features_disp].copy()
    df_table_show.columns = ["ชื่อสวนสาธารณะ", "เขตพื้นที่", "ขนาดพื้นที่ (ตร.ม.)", "ผู้ใช้บริการ (คน/เดือน)", "ที่จอดรถ", "มิตรกับสัตว์เลี้ยง", "ทางจักรยาน"]
    
    with download_btn_col:
        csv_data = df_table_show.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดข้อมูลสรุป (CSV)",
            data=csv_data,
            file_name="bkk_park_filtered_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    st.dataframe(df_table_show, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ ไม่พบข้อมูลสวนสาธารณะตรงตามตัวกรองที่คุณเลือกในขณะนี้")
