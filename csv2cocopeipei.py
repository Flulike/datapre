import json
import os
import csv

def csv_to_coco(csv_file, images_dir, output_json):
    # 创建COCO格式的字典
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # 读取CSV文件
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        image_id = 0
        annotation_id = 0

        for row in csv_reader:
            # 添加图像信息
            image_info = {
                "id": image_id,
                "file_name": row['image_path'],
                "height": float(row['height']),  # 转换为浮点数类型
                "width": float(row['width'])     # 转换为浮点数类型
            }
            coco_data['images'].append(image_info)

            # 添加标注信息
            annotation_info = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": int(row['class']),
                "bbox": [float(row['x_center']), float(row['y_center']), float(row['width']), float(row['height'])],
                "area": float(row['width']) * float(row['height']),
                "iscrowd": 0
            }
            coco_data['annotations'].append(annotation_info)

            image_id += 1
            annotation_id += 1

    # 写入到JSON文件
    with open(output_json, 'w') as json_file:
        json.dump(coco_data, json_file, indent=4)


# 示例用法
csv_file = "train1.csv"
images_dir = "D:\program\dataset\carclassyolo/train/images/"
output_json = "D:\program\dataset\carclasscoco/train/train1.json"
csv_to_coco(csv_file, images_dir, output_json)
