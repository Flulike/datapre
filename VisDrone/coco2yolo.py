import os
import json

# COCO JSON 标注文件路径
coco_json_path = "D:/program/dataset/VisDrone/VisDrone2019-DET-val/annotations/val.json"

# YOLO 标签保存目录
output_label_dir = "D:/program/dataset/VisDrone_yolo/val"
os.makedirs(output_label_dir, exist_ok=True)

# 定义 COCO 类别
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

# COCO 类别 ID 转换为 YOLO 类别 ID（从 0 开始）
category_id_map = {cat["id"]: idx for idx, cat in enumerate(categories)}

# 读取 COCO JSON 数据
with open(coco_json_path, "r", encoding="utf-8") as f:
    coco_data = json.load(f)

# 解析 COCO 数据
images = {img["id"]: img["file_name"] for img in coco_data["images"]}
annotations = coco_data["annotations"]

# 遍历标注并转换为 YOLO 格式
yolo_labels = {}
for ann in annotations:
    image_id = ann["image_id"]
    category_id = ann["category_id"]
    bbox = ann["bbox"]  # COCO: [x, y, width, height]

    # 获取图片信息
    img_info = next(img for img in coco_data["images"] if img["id"] == image_id)
    img_width, img_height = img_info["width"], img_info["height"]

    # 计算 YOLO 格式的归一化坐标
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    w /= img_width
    h /= img_height

    # 获取 YOLO 类别 ID
    yolo_category_id = category_id_map.get(category_id, -1)  # 避免错误
    if yolo_category_id == -1:
        continue  # 跳过未定义类别

    # 生成 YOLO 标签
    yolo_line = f"{yolo_category_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"

    # 组织 YOLO 标签文件
    txt_filename = os.path.splitext(images[image_id])[0] + ".txt"
    if txt_filename not in yolo_labels:
        yolo_labels[txt_filename] = []
    yolo_labels[txt_filename].append(yolo_line)

# 保存 YOLO 格式的标注
for txt_file, lines in yolo_labels.items():
    with open(os.path.join(output_label_dir, txt_file), "w") as f:
        f.write("\n".join(lines))

print("转换完成，YOLO 格式的标注已保存在:", output_label_dir)
