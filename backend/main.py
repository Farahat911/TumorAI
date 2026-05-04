from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import shutil
import os
import uuid
import json

# استدعاء الداتابيز
from database import SessionLocal, ReportDB
# استدعاء دالة الرسم وحساب المساحة القديمة
from vision import extract_tumor_features 
# استدعاء العقل المدبر الجديد (Deep Learning)
from ai_engine import predict_skin_lesion_dl

app = FastAPI(title="Skin Cancer AI Analyzer")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

os.makedirs("processed_images", exist_ok=True)
app.mount("/processed", StaticFiles(directory="processed_images"), name="processed")

# ==========================================
# 1. قسم تحليل الصور
# ==========================================
@app.post("/api/analyze-images")
async def analyze_growth_from_images(files: List[UploadFile] = File(...)):
    areas_mm2 = []
    processed_image_urls = []
    
    final_ai_prediction = ""
    final_confidence = 0.0
    
    for file in files:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        
        output_filename = f"{uuid.uuid4().hex}.png"
        output_path = os.path.join("processed_images", output_filename)
        
        # 1. شغل الكلاسيك: استخراج المساحة ورسم الحدود الخضراء
        area_px, _, _ = extract_tumor_features(temp_file_path, output_path)
        areas_mm2.append(round(area_px * 0.015, 2))
        
        # 2. شغل التعلم العميق: إدخال الصورة للموديل الذكي
        pred, conf = predict_skin_lesion_dl(temp_file_path)
        final_ai_prediction = pred
        final_confidence = conf
        
        processed_image_urls.append(f"http://127.0.0.1:8000/processed/{output_filename}")
        os.remove(temp_file_path)

    num_weeks = len(areas_mm2)
    if num_weeks == 0: return {"status": "error", "message": "برجاء رفع الصور."}

    report = {
        "weeks_analyzed": num_weeks,
        "extracted_areas": areas_mm2,
        "processed_images": processed_image_urls,
        # دمج التصنيف مع نسبة الثقة عشان تظهر للدكتور
        "ai_classification": f"{final_ai_prediction} (بنسبة ثقة {final_confidence}%)",
        "initial_warning": None,
        "growth_rates": [],
        "average_growth_rate": 0.0,
        "diagnosis": "",
        "severity_level": 1
    }

    # تحديد الخطورة بناءً على قرار الموديل العميق
    if "خبيث" in final_ai_prediction:
        report["severity_level"] = max(report["severity_level"], 3)

    # حساب معدلات النمو
    if num_weeks > 1:
        for i in range(1, num_weeks):
            prev, curr = areas_mm2[i-1], areas_mm2[i]
            rate = 0.0 if prev == 0 else ((curr - prev) / prev) * 100
            report["growth_rates"].append(round(rate, 2))

        avg_growth = sum(report["growth_rates"]) / len(report["growth_rates"])
        report["average_growth_rate"] = round(avg_growth, 2)

        if avg_growth < -5.0:
            report["diagnosis"] = "حجم الآفة يتقلص، استجابة جيدة."
        elif avg_growth <= 5.0:
            report["diagnosis"] = "حجم الآفة مستقر."
        elif avg_growth < 20.0:
            report["diagnosis"] = "نمو بطيء، يجب المتابعة."
            report["severity_level"] = max(report["severity_level"], 3)
        else:
            report["diagnosis"] = "نمو سريع جداً! مؤشر خطر."
            report["severity_level"] = 4
    else:
        report["diagnosis"] = "فحص مبدئي مقروء بنجاح."

    return report


# ==========================================
# 2. قسم قاعدة البيانات
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ReportCreate(BaseModel):
    id: str
    caseName: str
    date: str
    data: dict

@app.post("/api/reports")
def save_report(report: ReportCreate, db: SessionLocal = Depends(get_db)):
    db_report = ReportDB(
        id=report.id,
        case_name=report.caseName,
        date=report.date,
        data=json.dumps(report.data) 
    )
    db.add(db_report)
    db.commit()
    return {"status": "success"}

@app.get("/api/reports")
def get_reports(db: SessionLocal = Depends(get_db)):
    reports = db.query(ReportDB).order_by(ReportDB.id.desc()).all()
    return [
        {
            "id": r.id,
            "caseName": r.case_name,
            "date": r.date,
            "data": json.loads(r.data)
        }
        for r in reports
    ]

