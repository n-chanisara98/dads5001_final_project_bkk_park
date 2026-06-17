import pandas as pd
import plotly.express as px
import streamlit as st

# เซ็ตติ้งหน้าจอ Dashboard ให้เป็นแบบกว้าง (Wide mode)
st.set_page_config(page_title="Page 1: Park Analytics", page_icon="🌳", layout="wide")

# ----------------------------------------------------------------------
# 🎨 UI/UX ADVANCED ECO-GLASSMORPHISM PREMIUM STYLING
# ----------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Kanit:wght@300;400;500;600&display=swap');

    /* 1. คุมภาพรวมแอปพลิเคชันด้วยรูปวิวธรรมชาติแบบ High-Contrast และล็อกฟอนต์ */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', 'Kanit', sans-serif;
        background: linear-gradient(rgba(241, 245, 249, 0.85), rgba(241, 245, 249, 0.85)), 
                    url('https://images.unsplash.com/photo-1519331379826-f10be5486c6f?q=80&w=1920') no-repeat center center fixed;
        background-size: cover;
        color: #0f172a;
    }
    
    /* 2. กล่องเนื้อหาหลักสไตล์กระจกฝ้าหน้าต่างโปร่งแสงหรูหรา (Glassmorphism Main Container) */
    [data-testid="stMainBlockContainer"] {
        background: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(20px) saturate(170%);
        -webkit-backdrop-filter: blur(20px) saturate(170%);
        border-radius: 28px;
        padding: 45px 50px !important;
        margin-top: 30px;
        margin-bottom: 30px;
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    /* 3. ปรับแต่งแถบควบคุมด้านข้าง (Sidebar) ให้สมูท ทะลุเห็นวิวธรรมชาติ */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: rgba(255, 255, 255, 0.22) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 4. ออกแบบกล่องตัวกรองและกล่องคำสั่ง (Sidebar Widgets) ให้ดูคลีน มินิมอล */
    [data-testid="stSidebar"] .stCheckbox, [data-testid="stSidebar"] .stSelectbox {
        background-color: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(5px);
        padding: 14px 18px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
    }
    
    /* หัวข้อและคำอธิบาย */
    h1 {
        font-weight: 700 !important;
        color: #1e3a8a !important; /* สีกรมท่าเชิงวิชาการ */
        letter-spacing: -0.6px;
    }
    h5 {
        font-weight: 600 !important;
        color: #0f172a !important;
        margin-top: 20px !important;
        margin-bottom: 12px !important;
    }
    
    /* การ์ดสรุปตัวเลขสถิติ (KPI Scorecards) คอนเซปต์โมเดิร์นคลีน */
    .kpi-card {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-top: 6px solid #10b981;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 28px rgba(15, 23, 42, 0.08);
        background-color: rgba(255, 255, 255, 0.98);
    }
    .kpi-label {
        font-size: 13.5px;
        color: #475569;
        font-weight: 500;
        text-transform: uppercase;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
    }
    .kpi-value {
        font-size: 34px;
        color: #0f172a;
        font-weight: 700;
        line-height: 1;
    }
    .kpi-unit {
        font-size: 15px;
        font-weight: 400;
        color: #64748b;
        margin-left: 5px;
    }
    
    /* บล็อกเน้นจุดสำคัญทางสถิติ (Key Insights Card) */
    .insight-card {
        background: linear-gradient(90deg, rgba(240, 253, 244, 0.9) 0%, rgba(220, 252, 231, 0.9) 100%);
        border-left: 6px solid #10b981;
        padding: 20px 26px;
        border-radius: 16px;
        margin-top: 20px;
        margin-bottom: 30px;
        color: #14532d;
        font-size: 15.5px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.04);
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
st.sidebar.markdown("### 🔍 ตัวกรองข้อมูล (Filters)")

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

# ฟังก์ชันปรับแต่งสีสัน ความสะอาด และความคมชัดของชุดกราฟข้อมูลสากล
def apply_premium_layout(fig):
    fig.update_traces(textposition='outside', textfont=dict(size=11, color='#0f172a', family="Kanit"))
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Kanit, sans-serif", size=12, color='#1e293b'),
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=110, r=60, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(15,23,42,0.06)', zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    return fig

# ----------------------------------------------------------------------
# 4. DASHBOARD UI & VISUALIZATION
# ----------------------------------------------------------------------
st.title("🌳 Park Analytics Dashboard")
st.markdown("<p style='font-size: 15px; color:#1e293b; margin-top:-10px;'>วิเคราะห์โครงสร้างพื้นที่สีเขียว มิติการใช้งานสันทนาการ และความสอดคล้องเชิงนโยบายสาธารณะในเขตกรุงเทพมหานคร</p>", unsafe_allow_html=True)
st.markdown("---")

### ส่วนที่ 1: KPI SCORECARDS
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'''
    <div class="kpi-card" style="border-top-color: #10b981;">
        <div class="kpi-label">🍃 พื้นที่สีเขียวรวม (ตามตัวกรอง)</div>
        <div class="kpi-value">{total_green_area:,.1f}<span class="kpi-unit">ตร.ม.</span></div>
    </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
    <div class="kpi-card" style="border-top-color: #3b82f6;">
        <div class="kpi-label">🏞️ จำนวนสวนสาธารณะรวม</div>
        <div class="kpi-value">{total_parks:,}<span class="kpi-unit">แห่ง</span></div>
    </div>
    ''', unsafe_allow_html=True)
with col3:
    status_color = "#ef4444" if bkk_green_per_capita < 9 else "#10b981"
    st.markdown(f'''
    <div class="kpi-card" style="border-top-color: {status_color};">
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

# คำนวณความสูงชาร์ตแบบ Dynamic เพื่อให้อ่านง่ายและสร้าง Scrollbar รอบนอกอัตโนมัติ
num_rows = len(df_chart_data)
dynamic_height = max(360, num_rows * 38)

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
        fig_area = apply_premium_layout(fig_area)
        fig_area.update_layout(height=dynamic_height)
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
    st.markdown(f"##### 📈 อัตราส่วนสัดส่วนการแบกรับผู้ใช้งานเปรียบเทียบฐานประชากร")
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
    st.markdown(f"##### 🍩 สัดส่วนความพร้อมแยกตามประเภทสิ่งอำนวยความสะดวก")
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
            color_discrete_map={"ที่จอดรถ": "#1e3a8a", "ทางจักรยาน": "#3b82f6", "มิตรกับสัตว์เลี้ยง": "#90e0ef"}
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+value', insidetextfont=dict(size=12, weight='bold', color='#ffffff', family="Kanit"))
        fig_donut.update_layout(
            height=360, 
            margin=dict(l=40, r=40, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Kanit, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5)
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
    st.markdown("### 📋 ตารางสถิติและรายละเอียดสิ่งอำนวยความสะดวกของสวนสาธารณะ")

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
