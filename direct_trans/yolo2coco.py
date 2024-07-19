import os
import json
from PIL import Image

def get_image_info(image_id, image_path):
    with Image.open(image_path) as img:
        width, height = img.size

    image_info = {
        "id": image_id,
        "file_name": os.path.basename(image_path),
        "width": width,
        "height": height
    }
    return image_info

def get_category_info(classes):
    categories = []
    for idx, class_name in enumerate(classes):
        categories.append({
            "id": idx,
            "name": class_name,
            "supercategory": "none"
        })
    return categories

def get_annotation_info(annotation_id, image_id, class_id, bbox, width, height):
    x_center, y_center, box_width, box_height = bbox
    x_center *= width
    y_center *= height
    box_width *= width
    box_height *= height

    xmin = x_center - box_width / 2
    ymin = y_center - box_height / 2

    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": class_id,
        "bbox": [xmin, ymin, box_width, box_height],
        "area": box_width * box_height,
        "segmentation": [],
        "iscrowd": 0
    }
    return annotation_info

def convert_yolo_to_coco(yolo_dir, images_dir, output_json_path):
    classes = []
    with open("D:\program\dataset\carclassyolo\obj.names") as f:
        classes = [line.strip() for line in f.readlines()]

    images = []
    annotations = []
    annotation_id = 0

    for image_id, image_file in enumerate(os.listdir(images_dir)):
        if not image_file.endswith(".jpg"):
            continue

        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(yolo_dir, os.path.splitext(image_file)[0] + '.txt')

        if not os.path.exists(label_path):
            print(f"Warning: Label file for {image_file} not found, skipping")
            continue

        image_info = get_image_info(image_id, image_path)
        images.append(image_info)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])
            bbox = list(map(float, parts[1:]))

            annotation_info = get_annotation_info(annotation_id, image_id, class_id, bbox, image_info['width'], image_info['height'])
            annotations.append(annotation_info)
            annotation_id += 1

    categories = get_category_info(classes)

    coco_format = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    with open(output_json_path, 'w') as json_file:
        json.dump(coco_format, json_file, indent=4)

    print(f"COCO dataset saved to {output_json_path}")

# 示例用法
yolo_labels_dir = "D:\program\dataset\carclassyolo/train\labels"
images_dir = "D:\program\dataset\carclassyolo/train\images"
output_json_path = "D:\program\dataset\carclasscoco/coco_annotations.json"
convert_yolo_to_coco(yolo_labels_dir, images_dir, output_json_path)
