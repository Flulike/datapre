import os
import shutil
from sklearn.model_selection import train_test_split

# 定义数据集路径
images_path = "D:/program/dataset/BITVehicle_Dataset/images"
annotations_path = "D:/program/dataset/BITVehicle_Dataset/annotations"
train_images_path = 'D:/program/dataset/BITVehicle_Dataset/train/images'
train_annotations_path = 'D:/program/dataset/BITVehicle_Dataset/train/annotations'
valid_images_path = 'D:/program/dataset/BITVehicle_Dataset/valid/images'
valid_annotations_path = 'D:/program/dataset/BITVehicle_Dataset/valid/annotations'

# 创建训练集和验证集文件夹
os.makedirs(train_images_path, exist_ok=True)
os.makedirs(train_annotations_path, exist_ok=True)
os.makedirs(valid_images_path, exist_ok=True)
os.makedirs(valid_annotations_path, exist_ok=True)

# 获取所有图片文件名
image_files = os.listdir(images_path)
annotation_files = [f.replace('.jpg', '.xml') for f in image_files]

# 按照比例划分训练集和验证集
train_images, valid_images, train_annotations, valid_annotations = train_test_split(
    image_files, annotation_files, test_size=0.15, random_state=42
)

# 复制文件到训练集和验证集文件夹
for image in train_images:
    shutil.copy(os.path.join(images_path, image), os.path.join(train_images_path, image))
for annotation in train_annotations:
    shutil.copy(os.path.join(annotations_path, annotation), os.path.join(train_annotations_path, annotation))
for image in valid_images:
    shutil.copy(os.path.join(images_path, image), os.path.join(valid_images_path, image))
for annotation in valid_annotations:
    shutil.copy(os.path.join(annotations_path, annotation), os.path.join(valid_annotations_path, annotation))

print(f"训练集大小: {len(train_images)}")
print(f"验证集大小: {len(valid_images)}")
