import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

# التجهيزات اللي الموديل اتدرب عليها في كولاب
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 1. بناء هيكل الموديل (لازم يكون نفس الهيكل اللي اتدربنا عليه)
model = models.resnet18(weights=None) # مش بنحمل أوزان من النت لأننا هنحط أوزاننا
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2) # عندنا تصنيفين بس: حميد وخبيث

# 2. تحميل الأوزان الذكية (المخ اللي أنت نزلته)
MODEL_PATH = "skin_cancer_model.pth"
if os.path.exists(MODEL_PATH):
    # بنحمله على الـ CPU عشان يشتغل على أي جهاز من غير ما يطلب كارت شاشة
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval() # وضع الاختبار
    print("✅ تم تحميل مخ الذكاء الاصطناعي (Deep Learning) بنجاح!")
else:
    print("⚠️ تحذير: ملف الأوزان غير موجود في فولدر الباك إند!")

# أسماء التصنيفات زي ما كانت في كاجل (benign, malignant)
classes = ['حميد (وحمة عادية)', 'اشتباه في ورم خبيث (Melanoma)']

def predict_skin_lesion_dl(image_path):
    """
    الدالة دي بتاخد الصورة، وتدخلها في الموديل، وترجع التصنيف ونسبة الثقة
    """
    if not os.path.exists(image_path) or not os.path.exists(MODEL_PATH):
        return "الموديل غير متصل", 0.0

    # فتح الصورة وتجهيزها
    img = Image.open(image_path).convert('RGB')
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0) # إضافة بُعد الباتش

    # التنبؤ
    with torch.no_grad():
        output = model(input_batch)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)
        
    # استخراج النتيجة
    prediction = classes[predicted_idx.item()]
    conf_score = round(confidence.item() * 100, 2)
    
    return prediction, conf_score