import os
import json
from PIL import Image 

# VisDrone 数据集路径
visdrone_anno_dir = "D:/program/dataset/VisDrone/VisDrone2019-DET-test/annotations/"
image_dir = "D:/program/dataset/VisDrone/VisDrone2019-DET-test/images/"
output_json = "test.json"

# 类别映射（根据 VisDrone 的类别定义）
categories = [
    {"id": 1, "name": "pedestrian"},
    {"id": 2, "name": "people"},
    {"id": 3, "name": "bicycle"},
    {"id": 4, "name": "car"},
    {"id": 5, "name": "van"},
    {"id": 6, "name": "truck"},
    {"id": 7, "name": "tricycle"},
    {"id": 8, "name": "awning-tricycle"},
    {"id": 9, "name": "bus"},
    {"id": 10, "name": "motor"},
    {"id": 11, "name": "others"}
]

# 初始化 COCO 格式字典
coco_format = {
    "images": [],
    "annotations": [],
    "categories": categories
}

# 遍历 VisDrone 的标注文件
annotation_id = 1
for anno_file in os.listdir(visdrone_anno_dir):
    if not anno_file.endswith(".txt"):
        continue

    # 修改这一行，直接使用文件名（不含扩展名）作为 image_id
    image_name = os.path.splitext(anno_file)[0]  # 获取不含扩展名的文件名
    image_id = hash(image_name) % (10 ** 8)  # 使用哈希值作为数字ID
    image_file = os.path.join(image_dir, f"{image_name}.jpg")  # 使用完整的文件名

    # 使用 PIL 读取图像获取尺寸
    try:
        with Image.open(image_file) as img:
            image_width, image_height = img.size
    except Exception as e:
        print(f"Warning: Could not read image {image_file}: {e}")
        continue

    coco_format["images"].append({
        "id": image_id,
        "file_name": os.path.basename(image_file),
        "width": image_width,
        "height": image_height
    })

    # 读取标注文件
    with open(os.path.join(visdrone_anno_dir, anno_file), "r") as f:
        for line in f:
            parts = line.strip().split(",")
            xmin, ymin, width, height = map(int, parts[:4])
            category_id = int(parts[5])

            # 构造 COCO 格式的 annotation
            annotation = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [xmin, ymin, width, height],
                "area": width * height,
                "iscrowd": 0  # 默认设置为 0
            }
            coco_format["annotations"].append(annotation)
            annotation_id += 1

# 保存为 JSON 文件
with open(output_json, "w") as f:
    json.dump(coco_format, f, indent=4)

print(f"COCO 格式的注释文件已保存为 {output_json}")
