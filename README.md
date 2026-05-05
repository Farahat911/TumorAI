# 🩺 TumorAI: Hybrid Medical Imaging & Growth Analysis System

**TumorAI** هو نظام متكامل يعتمد على تقنيات الذكاء الاصطناعي والرؤية الحاسوبية لتصنيف الأورام الجلدية ومتابعة معدل نموها زمنياً. تم تطوير هذا المشروع كجزء من دراسة **الطرق الرياضية (Mathematical Methods)** لدمج المفاهيم التفاضلية والعددية في أنظمة التشخيص الطبي.

## 🚀 Key Features
*   **AI Classification:** تصنيف دقيق للأورام (حميد/خبيث) باستخدام شبكة **ResNet18** العصبية.
*   **Temporal Tracking:** حساب مساحة الآفة الجلدية أسبوعياً ورسم حدودها بدقة باستخدام مكتبة **OpenCV**.
*   **Growth Rate Analysis:** تطبيق مفاهيم الاشتقاق العددي لحساب معدل التغير للتنبؤ بمدى خطورة الحالة.
*   **Professional Dashboards:** لوحة تحكم إحصائية تفاعلية لعرض الحالات الحرجة والمستقرة باستخدام **React**.
*   **Medical Reports:** توليد تقارير طبية احترافية بصيغة PDF قابلة للطباعة.

## 🛠️ Tech Stack & Tools
لقد تم استخدام مجموعة من الأدوات المتقدمة لبناء وتدريب النظام:
*   **Frontend:** React.js (Vite).
*   **Backend:** FastAPI (Python).
*   **AI Framework:** PyTorch & Torchvision.
*   **Computer Vision:** OpenCV.
*   **Training Environment:** 
    *   **Google Colab:** لاستخدام معالجات الرسوميات (T4 GPU) في تدريب الموديل سحابياً.
    *   **Kaggle API:** لسحب مجموعات البيانات الطبية الضخمة (ISIC Dataset) مباشرة إلى بيئة التدريب.

## 📐 Mathematical Foundations
يرتكز النظام على أسس رياضية متينة تتماشى مع منهج الطرق الرياضية:

### 1. معدل التغير (Numerical Differentiation)
يستخدم النظام الاشتقاق العددي لحساب سرعة نمو الورم عبر الزمن ($t$):
$$Rate = \frac{Area_{current} - Area_{previous}}{Area_{previous}} \times 100$$
حيث يمثل هذا المعدل التقريب الرياضي للاشتقاق الأول للمساحة بالنسبة للزمن $\frac{dA}{dt}$.

### 2. تحسين الأوزان (Gradient-based Optimization)
تعتمد عملية تعلم الذكاء الاصطناعي على **الاشتقاق الجزئي (Partial Derivatives)** لتقليل دالة الخطأ عبر خوارزمية الـ Backpropagation:
$$w_{new} = w_{old} - \eta \frac{\partial L}{\partial w}$$
حيث $\eta$ هو معامل التعلم، و $\frac{\partial L}{\partial w}$ هو منحدر دالة الخطأ بالنسبة للأوزان.

### 3. تحليل الشكل الهندي (Geometric Analysis)
لحساب مدى تعرج حدود الورم (Circularity Index):
$$C = \frac{4\pi \times Area}{Perimeter^2}$$
هذه المعادلة الرياضية تساعد في التمييز بين الأشكال المنتظمة وغير المنتظمة طبياً.

## 👨‍💻 Developer
*   **Mohammed Farahat (Faro)**
*   Engineering Student at **Mansoura National University**, AI Department (2nd Year).
*   **Portfolio:** [mofarahat.pythonanywhere.com](https://mofarahat.pythonanywhere.com/)

---
*هذا المشروع تم تطويره للأغراض التعليمية والبحثية كجزء من متطلبات مادة الطرق الرياضية.*
