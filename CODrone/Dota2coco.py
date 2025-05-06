import os
import glob
import json
from PIL import Image

# 类别映射到 COCO 类别 id
CLASS_MAPPING = {
    'car': 1,
    'truck': 2,
    'traffic-sign': 3,
    'people': 4,
    'motor': 5,
    'bicycle': 6,
    'traffic-light': 7,
    'tricycle': 8,
    'bridge': 9,
    'bus': 10,
    'boat': 11,
    'ship': 12
}

# 文件夹及输出路径配置（请根据实际情况修改）
INPUT_ANN_DIR = 'D:/program/dataset/CODrone/val/annfile'
IMG_DIR = 'D:/program/dataset/CODrone/val/images'
OUTPUT_COCO_JSON = 'D:/program/dataset/CODrone/val/annotations/val.json'

# 支持的图像扩展名
IMG_EXTS = ['.jpg', '.jpeg', '.png']


def polygon_area(xs, ys):
    """
    通过 Shoelace 公式计算多边形面积
    """
    area = 0.0
    n = len(xs)
    for i in range(n):
        j = (i + 1) % n
        area += xs[i] * ys[j] - xs[j] * ys[i]
    return abs(area) / 2


def convert_dota_to_coco(input_dir, img_dir, output_json):
    images = []
    annotations = []
    categories = []

    # 构建 categories
    for name, cid in CLASS_MAPPING.items():
        categories.append({'id': cid, 'name': name, 'supercategory': name})

    ann_id = 1
    img_id = 1

    for ann_file in glob.glob(os.path.join(input_dir, '*.txt')):
        base = os.path.splitext(os.path.basename(ann_file))[0]

        # 匹配图像文件
        img_path = None
        for ext in IMG_EXTS:
            candidate = os.path.join(img_dir, base + ext)
            if os.path.exists(candidate):
                img_path = candidate
                break
        if not img_path:
            print(f"跳过: 未找到图像 {base}")
            continue

        # 读取图像尺寸
        with Image.open(img_path) as img:
            width, height = img.size

        # 添加 image 记录
        images.append({
            'id': img_id,
            'file_name': os.path.basename(img_path),
            'width': width,
            'height': height
        })

        # 读取标注并转换
        with open(ann_file, 'r') as fr:
            for line in fr:
                parts = line.strip().split()
                if len(parts) < 10:
                    continue
                # 解析四点多边形
                coords = list(map(float, parts[:8]))
                xs = coords[0::2]
                ys = coords[1::2]

                # COCO segmentation 需要扁平列表
                segmentation = [coords]

                # 计算 bbox [x, y, w, h]
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)
                bbox = [x_min, y_min, x_max - x_min, y_max - y_min]

                # 计算面积
                area = polygon_area(xs, ys)

                cls_name = parts[8]
                if cls_name not in CLASS_MAPPING:
                    print(f"警告: 未知类别 {cls_name}，跳过")
                    continue
                category_id = CLASS_MAPPING[cls_name]

                # 添加 annotation
                annotations.append({
                    'id': ann_id,
                    'image_id': img_id,
                    'category_id': category_id,
                    'segmentation': segmentation,
                    'area': area,
                    'bbox': bbox,
                    'iscrowd': 0
                })
                ann_id += 1

        print(f"处理完成: 图像 {base} (id={img_id})")
        img_id += 1

    # 组织 COCO 格式
    coco = {
        'info': {},
        'licenses': [],
        'images': images,
        'annotations': annotations,
        'categories': categories
    }

    # 写入 JSON
    with open(output_json, 'w', encoding='utf-8') as fw:
        json.dump(coco, fw, ensure_ascii=False, indent=4)

    print(f"COCO 标注已保存到: {output_json}")


if __name__ == '__main__':
    convert_dota_to_coco(INPUT_ANN_DIR, IMG_DIR, OUTPUT_COCO_JSON)
