import os
import json
import shutil
import random

def read_txt_annotations(txt_folder):
    annotations = []
    for txt_file in os.listdir(txt_folder):
        if txt_file.endswith('.txt'):
            with open(os.path.join(txt_folder, txt_file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    category_id, xmin, ymin, width, height = map(int, parts)
                    image_id = int(txt_file.split('.')[0].split('_')[-1])
                    annotations.append({
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": [xmin, ymin, width, height],
                        "area": width * height,
                        "segmentation": [],
                        "iscrowd": 0
                    })
    return annotations

def split_dataset(txt_folder, images_path, output_path, train_ratio=0.8):
    annotations = read_txt_annotations(txt_folder)
    
    # 获取所有图像的文件名
    image_files = [f for f in os.listdir(images_path) if f.endswith('.jpg')]
    random.shuffle(image_files)
    
    # 计算训练集和验证集的划分点
    split_point = int(len(image_files) * train_ratio)
    train_images = set(image_files[:split_point])
    val_images = set(image_files[split_point:])

    # 初始化新的COCO JSON数据
    coco_template = {
        'images': [],
        'annotations': [],
        'categories': [],
        'licenses': [],
        'info': {}
    }

    train_coco = coco_template.copy()
    val_coco = coco_template.copy()

    # 添加类别信息（根据实际情况调整）
    categories = [
        {"id": 1, "name": "category1"},
        {"id": 2, "name": "category2"},
        # 添加其他类别
    ]
    train_coco['categories'] = categories
    val_coco['categories'] = categories

    # 添加图像信息
    for idx, img_file in enumerate(image_files):
        image_info = {
            "id": idx,
            "file_name": img_file,
            "height": 640,  # 根据实际情况调整
            "width": 640,   # 根据实际情况调整
        }
        if img_file in train_images:
            train_coco['images'].append(image_info)
        else:
            val_coco['images'].append(image_info)

    # 添加注释信息
    for ann in annotations:
        image_file = f"image_{ann['image_id']:06d}.jpg"
        if image_file in train_images:
            train_coco['annotations'].append(ann)
        else:
            val_coco['annotations'].append(ann)

    # 创建输出目录
    train_images_path = os.path.join(output_path, 'train_images')
    val_images_path = os.path.join(output_path, 'val_images')
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)

    # 移动图像文件到相应的目录
    for img_file in train_images:
        shutil.copy(os.path.join(images_path, img_file), os.path.join(train_images_path, img_file))
    
    for img_file in val_images:
        shutil.copy(os.path.join(images_path, img_file), os.path.join(val_images_path, img_file))

    # 保存新的COCO JSON文件
    with open(os.path.join(output_path, 'train_annotations.json'), 'w') as f:
        json.dump(train_coco, f, indent=4)

    with open(os.path.join(output_path, 'val_annotations.json'), 'w') as f:
        json.dump(val_coco, f, indent=4)

    print(f"Dataset split completed. {len(train_coco['images'])} training images and {len(val_coco['images'])} validation images.")

if __name__ == '__main__':
    txt_folder = 'path_to_your_txt_annotations'  # 标注txt文件夹路径
    images_path = 'path_to_your_images'  # 图像文件夹路径
    output_path = 'path_to_output_directory'  # 输出目录路径
    split_dataset(txt_folder, images_path, output_path)
