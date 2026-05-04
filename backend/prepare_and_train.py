import os
import urllib.request
import zipfile
import time

def download_and_extract(url, extract_to='.'):
    file_name = "dataset.zip"
    
    print(f"⏳ جاري تحميل البيانات من الرابط...\nالرابط: {url}")
    # تحميل الملف من الرابط
    urllib.request.urlretrieve(url, file_name)
    print("✅ تم التحميل بنجاح!")
    
    print("⏳ جاري فك الضغط وتجهيز الملفات...")
    # فك الضغط
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    # مسح الملف المضغوط عشان نوفر مساحة
    os.remove(file_name)
    print("✅ تم فك الضغط وتجهيز الـ Dataset!")

# ==========================================
# 1. مرحلة تحميل البيانات أوتوماتيكياً
# ==========================================
# ده لينك افتراضي لداتا مصغرة (تقدر تغيره بلينك الـ ISIC لما ترفعه)
DATASET_URL = "https://example.com/your_skin_cancer_dataset.zip" 

# لو فولدر الـ dataset مش موجود، حمله من اللينك
if not os.path.exists('dataset'):
    download_and_extract(DATASET_URL, extract_to='.')
else:
    print("📁 البيانات موجودة بالفعل، سيتم تخطي التحميل.")

# ==========================================
# 2. مرحلة التدريب (هنا بنشغل الكود اللي كتبناه المرة اللي فاتت)
# ==========================================
print("🚀 بدء تشغيل محرك الذكاء الاصطناعي للتدريب...")
time.sleep(2)

# هنا بتستدعي كود الـ train.py اللي جهزناه
# os.system('python train.py') 
print("هنا الموديل بيبدأ يسحب الصور من الفولدر اللي لسه نازل ويدرب نفسه عليها!")