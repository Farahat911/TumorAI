import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os

# 1. إعداد الجهاز (GPU لو متاح، أو CPU)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"جاري التدريب باستخدام: {device}")

# 2. تجهيز البيانات (Data Augmentation & Normalization)
# دي التعديلات اللي بنعملها عالصور عشان الموديل ميحفظش الصورة زي ما هي، ويتعلم "يفهم" الخصائص
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224), # قص عشوائي لتكبير/تصغير أجزاء
        transforms.RandomHorizontalFlip(), # قلب الصورة أفقياً
        transforms.RandomRotation(20),     # تدوير الصورة بزاوية عشوائية
        transforms.ToTensor(),             # تحويل الصورة لمصفوفة
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) # توحيد الألوان
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

data_dir = 'dataset'

# تحميل البيانات من الفولدرات اللي أنت عملتها
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                  for x in ['train', 'val']}

# إنشاء DataLoader (ده اللي بياخد الصور في "شحنات/Batches" ويديها للموديل)
dataloaders = {x: DataLoader(image_datasets[x], batch_size=4, shuffle=True, num_workers=0)
              for x in ['train', 'val']}

dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes # المفروض يطلع ['benign', 'malignant']
print(f"التصنيفات المكتشفة: {class_names}")
print(f"عدد صور التدريب: {dataset_sizes['train']} | عدد صور الاختبار: {dataset_sizes['val']}")

# 3. بناء الموديل (Transfer Learning)
# هنحمل ResNet18 متدرب قبل كده
weights = models.ResNet18_Weights.DEFAULT
model = models.resnet18(weights=weights)

# تعديل آخر طبقة (Fully Connected Layer) عشان تخرج تصنيفين بس بدل 1000
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(class_names))

model = model.to(device)

# 4. إعدادات التدريب (Loss Function & Optimizer)
criterion = nn.CrossEntropyLoss() # دالة حساب نسبة الخطأ
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9) # الخوارزمية اللي بتعدل الأوزان

# 5. حلقة التدريب (Training Loop)
num_epochs = 5 # عدد المرات اللي الموديل هيشوف فيها الداتا كلها (خليه 5 دلوقتي للتجربة)

print("\n🚀 بدء التدريب...")
for epoch in range(num_epochs):
    print(f'Epoch {epoch+1}/{num_epochs}')
    print('-' * 10)

    for phase in ['train', 'val']:
        if phase == 'train':
            model.train()  # وضع التدريب (تحديث الأوزان شغال)
        else:
            model.eval()   # وضع الاختبار (تحديث الأوزان مقفول)

        running_loss = 0.0
        running_corrects = 0

        # التكرار على شحنات الصور (Batches)
        for inputs, labels in dataloaders[phase]:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad() # تصفير الـ Gradients من اللفة اللي فاتت

            # Forward pass (دخول الصور للموديل)
            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1) # اختيار التصنيف صاحب أعلى احتمال
                loss = criterion(outputs, labels) # حساب نسبة الخطأ

                # Backward pass & optimize (فقط في مرحلة التدريب)
                if phase == 'train':
                    loss.backward()  # حساب التفاضل (تحديد الغلط فين)
                    optimizer.step() # تحديث الأوزان (التعلم)

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        # حساب الدقة في نهاية كل مرحلة
        epoch_loss = running_loss / dataset_sizes[phase]
        epoch_acc = running_corrects.double() / dataset_sizes[phase]

        print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

print('\n✅ اكتمل التدريب!')

# 6. حفظ الأوزان (The Brain)
save_path = 'skin_cancer_model.pth'
torch.save(model.state_dict(), save_path)
print(f"تم حفظ أوزان الموديل بنجاح في ملف: {save_path}")