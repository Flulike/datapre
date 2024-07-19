import os
import json
import shutil
import random

def read_txt_annotations(txt_folder, img_folder):
    annotations = []
    image_infos = []
    image_id = 0
    
    for txt_file in os.listdir(txt_folder):
        if txt_file.endswith('.txt'):
            img_file = txt_file.replace('.txt', '.jpg')
            img_path = os.path.join(img_folder, img_file)
            
            if not os.path.exists(img_path):
                continue

            with open(os.path.join(txt_folder, txt_file), 'r') as f:
                lines = f.readlines()
                image_info = {
                    "file_name": img_file,
                    "height": 400,  # 根据实际情况调整
                    "width": 400,   # 根据实际情况调整
                    "id": image_id
                }
                image_infos.append(image_info)

                for line in lines:
                    parts = line.strip().split()
                    #voc转到coco，分类数字+1。coco的0默认为背景
                    category_id = int(parts[0]) + 1
                    #由于我用的奇怪的数据集，后面都是一堆小数，不能用int，得用float提取
                    #具体问题具体分析
                    center_x = float(parts[1])
                    center_y = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    xmin = (center_x - width / 2) * image_info["width"]
                    ymin = (center_y - height / 2) * image_info["height"]
                    bbox_width = width * image_info["width"]
                    bbox_height = height * image_info["height"]

                    annotations.append({
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": [xmin, ymin, bbox_width, bbox_height],
                        "area": bbox_width * bbox_height,
                        "segmentation": [],
                        "iscrowd": 0
                    })
                image_id += 1
    return image_infos, annotations

def split_dataset(txt_folder, images_path, output_path, train_ratio=0.8):
    # 读取所有TXT标注文件
    all_image_infos, all_annotations = read_txt_annotations(txt_folder, images_path)
    
    # 获取所有图像的文件名并打乱顺序
    image_files = [img_info['file_name'] for img_info in all_image_infos]
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
        {"id": 1, "name": "auto"},
        {"id": 2, "name": "bus"},
        {"id": 3, "name": "car"},
        {"id": 4, "name": "lcv"},
        {"id": 5, "name": "motorcycle"},
        {"id": 6, "name": "multiaxle"},
        {"id": 7, "name": "tractor"},
        {"id": 8, "name": "truck"},
        # 添加其他类别
    ]
    train_coco['categories'] = categories
    val_coco['categories'] = categories

    # 将图像和注释划分到训练集和验证集
    for img_info in all_image_infos:
        if img_info['file_name'] in train_images:
            train_coco['images'].append(img_info)
        else:
            val_coco['images'].append(img_info)

    for ann in all_annotations:
        if f"{ann['image_id']:06d}.jpg" in train_images:
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
    txt_folder = "D:/program/dataset/kaggle-data/labels"  # 标注txt文件夹路径
    images_path = "D:/program/dataset/kaggle-data/images"  # 图像文件夹路径
    output_path = "D:/program/dataset/kaggle-data/coco"  # 输出目录路径
    split_dataset(txt_folder, images_path, output_path)

