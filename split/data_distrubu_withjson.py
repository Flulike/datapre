import json
import os
import shutil
import random

def split_dataset(coco_json_path, images_path, output_path, train_ratio=0.8):
    # 读取原始的COCO JSON文件
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # 获取所有图像的ID
    image_ids = [img['id'] for img in coco_data['images']]
    random.shuffle(image_ids)

    # 计算训练集和验证集的划分点
    split_point = int(len(image_ids) * train_ratio)
    train_image_ids = set(image_ids[:split_point])
    valid_image_ids = set(image_ids[split_point:])

    # 初始化新的COCO JSON数据
    train_coco = {
        'images': [],
        'annotations': [],
        'categories': coco_data['categories'],
        'licenses': coco_data.get('licenses', []),
        'info': coco_data.get('info', {})
    }

    valid_coco = {
        'images': [],
        'annotations': [],
        'categories': coco_data['categories'],
        'licenses': coco_data.get('licenses', []),
        'info': coco_data.get('info', {})
    }

    # 将图像和注释划分到训练集和验证集
    for img in coco_data['images']:
        if img['id'] in train_image_ids:
            train_coco['images'].append(img)
        else:
            valid_coco['images'].append(img)

    for ann in coco_data['annotations']:
        if ann['image_id'] in train_image_ids:
            train_coco['annotations'].append(ann)
        else:
            valid_coco['annotations'].append(ann)

    # 创建输出目录
    train_images_path = os.path.join(output_path, 'train_images')
    valid_images_path = os.path.join(output_path, 'valid_images')
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(valid_images_path, exist_ok=True)

    # 移动图像文件到相应的目录
    for img in train_coco['images']:
        shutil.copy(os.path.join(images_path, img['file_name']), os.path.join(train_images_path, img['file_name']))
    
    for img in valid_coco['images']:
        shutil.copy(os.path.join(images_path, img['file_name']), os.path.join(valid_images_path, img['file_name']))

    # 保存新的COCO JSON文件
    with open(os.path.join(output_path, 'train_annotations.json'), 'w') as f:
        json.dump(train_coco, f, indent=4)

    with open(os.path.join(output_path, 'valid_annotations.json'), 'w') as f:
        json.dump(valid_coco, f, indent=4)

    print(f"Dataset split completed. {len(train_coco['images'])} training images and {len(valid_coco['images'])} validation images.")

if __name__ == '__main__':
    coco_json_path = "D:/program/dataset/roboflow-data/_annotations.coco.json"  # 原始COCO标注文件路径
    images_path = 'D:/program/dataset/roboflow-data/'  # 原始图像文件夹路径
    output_path = 'D:/program/dataset/roboflow-data/coco'  # 输出目录路径
    split_dataset(coco_json_path, images_path, output_path)
