import cv2
import numpy as np
import os

def extract_tumor_features(image_path, output_path):
    if not os.path.exists(image_path):
        return 0.0, 1.0, 0.0  # مساحة، دائرية، اختلاف الألوان

    img = cv2.imread(image_path)
    if img is None:
        return 0.0, 1.0, 0.0
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        cv2.imwrite(output_path, img)
        return 0.0, 1.0, 0.0

    largest_contour = max(contours, key=cv2.contourArea)
    area_in_pixels = cv2.contourArea(largest_contour)
    
    # 1. قياس تعرج الحدود (Border Irregularity)
    perimeter = cv2.arcLength(largest_contour, True)
    circularity = 1.0
    if perimeter > 0:
        # معادلة الدائرية: لو قريبة من 1 تبقى وحمة مدورة، لو أقل من 0.6 تبقى متعرجة (خطر)
        circularity = (4 * np.pi * area_in_pixels) / (perimeter * perimeter)

    # 2. قياس اختلاف الألوان (Color Variation)
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.drawContours(mask, [largest_contour], -1, 255, -1)
    mean, stddev = cv2.meanStdDev(img, mask=mask)
    color_variance = float(np.mean(stddev)) # لو الرقم عالي معناه ألوان كتير ملخبطة

    # رسم الحدود
    cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 3)
    cv2.imwrite(output_path, img)

    return area_in_pixels, circularity, color_variance