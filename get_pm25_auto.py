import os
import requests
from pymongo import MongoClient
from datetime import datetime, UTC

# 1. เอาลิงก์ MongoDB ของคุณมาวางตรงนี้ (เปลี่ยนตรง 'รหัสผ่านที่คุณตั้ง' ให้เรียบร้อย)
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Error: ไม่พบ MONGO_URI ในระบบ Environmental Variables")

try:
    client = MongoClient(MONGO_URI)
    db = client["dads5001"]
    collection = db["pm25"]
    
    print("เชื่อมต่อ MongoDB สำเร็จ...")

    # 🌟 บรรทัดที่เพิ่มใหม่: ล้างข้อมูลเก่าในถังทิ้งให้หมดก่อนดึงใหม่ ไม่ต้องรันถ้าหากไม่ได้ดึงค่าผิดพลาด
    # collection.delete_many({}) 
    # print("🧹 ล้างข้อมูลเก่าที่ติด Null ออกจากฐานข้อมูลเรียบร้อยแล้ว")

    api_url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php?region=1"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        raw_data = response.json()
        
        # ดึงเวลาอัปเดตจาก API แบบปลอดภัย
        last_update = raw_data.get("LastUpdate", {})
        last_update_date = last_update.get("date", datetime.now().strftime("%Y-%m-%d"))
        last_update_time = last_update.get("time", datetime.now().strftime("%H:%M:%S"))
        
        stations = raw_data.get("stations", [])
        documents_to_insert = []
        
        for station in stations:
            # 1. ดึงพิกัดแบบตรงคีย์เป๊ะ ๆ (lat และ long)
            lat_raw = station.get("lat")
            lon_raw = station.get("long")  # แก้จาก num เป็น long ตาม JSON จริง
            
            # 2. เจาะเข้าชั้น AQILast -> PM25 -> value
            aqi_last = station.get("AQILast", {})
            pm25_value = None
            if isinstance(aqi_last, dict):
                pm25_info = aqi_last.get("PM25", {})
                if isinstance(pm25_info, dict):
                    pm25_value = pm25_info.get("value")  # ดึงค่าเลขทศนิยม เช่น 12.2

            # ฟังก์ชันช่วยแปลงพิกัด (Float)
            def to_float(val):
                try:
                    return float(str(val).strip()) if val is not None else None
                except ValueError:
                    return None

            # ฟังก์ชันช่วยแปลงค่าฝุ่น (แปลงเป็น Float ก่อนแล้วค่อยเก็บทศนิยม หรือปัดเป็น Float ไปเลยเพื่อความละเอียด)
            def to_pm25_float(val):
                try:
                    if val is not None and str(val).strip() != "" and float(str(val)) >= 0:
                        return float(str(val).strip())
                    return None
                except ValueError:
                    return None

            doc = {
                "timestamp_str": f"{last_update_date} {last_update_time}",
                "fetched_at": datetime.now(UTC),
                "stationID": station.get("stationID"),
                "stationName": station.get("nameTH"),
                "areaName": station.get("areaTH"),  # แถมเขต/แขวงให้ด้วย เอาไว้เช็กพิกัดสวนง่ายขึ้น
                "lat": to_float(lat_raw),
                "lon": to_float(lon_raw),
                "pm25": to_pm25_float(pm25_value)
            }
            documents_to_insert.append(doc)
            
        if documents_to_insert:
            result = collection.insert_many(documents_to_insert)
            print(f"🎉 สำเร็จแบบไร้ Null! บันทึกข้อมูลเข้า MongoDB เรียบร้อย ทั้งหมด {len(result.inserted_ids)} สถานี")
        else:
            print("ไม่พบข้อมูลสถานีที่จะบันทึก")
            
    else:
        print("ดึงข้อมูลจาก API ไม่สำเร็จ รหัสเออเร่อ:", response.status_code)

except Exception as e:
    print("เกิดข้อผิดพลาดในการรัน:", e)















