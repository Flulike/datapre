import os
import glob
from PIL import Image

# 类别映射到 YOLO 类索引
CLASS_MAPPING = {
    'car': 0,
    'truck': 1,
    'traffic-sign': 2,
    'people': 3,
    'motor': 4,
    'bicycle': 5,
    'traffic-light': 6,
    'tricycle': 7,
    'bridge': 8,
    'bus': 9,
    'boat': 10,
    'ship': 11
}

# 输入 DOTA 格式标注目录、对应图像目录，以及输出 YOLO 格式标注目录
INPUT_ANN_DIR = 'D:/program/dataset/CODrone/train/annfile'
IMG_DIR = 'D:/program/dataset/CODrone/train/images'
OUTPUT_ANN_DIR = 'D:/program/dataset/CODrone/train/yolo'

os.makedirs(OUTPUT_ANN_DIR, exist_ok=True)

# 支持的图像后缀
IMG_EXTS = ['.png', '.jpg', '.jpeg']

for ann_path in glob.glob(os.path.join(INPUT_ANN_DIR, '*.txt')):
    basename = os.path.splitext(os.path.basename(ann_path))[0]

    # 尝试找到对应的图像文件
    img_path = None
    for ext in IMG_EXTS:
        cand = os.path.join(IMG_DIR, basename + ext)
        if os.path.exists(cand):
            img_path = cand
            break
    if img_path is None:
        print(f"跳过: 未找到图像 {basename} 对应的文件")
        continue

    # 获取图像尺寸
    img = Image.open(img_path)
    img_w, img_h = img.size

    # 输出 YOLO 标签文件路径
    yolo_path = os.path.join(OUTPUT_ANN_DIR, basename + '.txt')

    with open(ann_path, 'r') as fr, open(yolo_path, 'w') as fw:
        for line in fr:
            parts = line.strip().split()
            if len(parts) < 10:
                # 非标准行，忽略
                continue
            # 解析前 8 个值为多边形顶点
            coords = list(map(float, parts[:8]))
            xs = coords[0::2]
            ys = coords[1::2]
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)

            # 计算水平框的中心、宽高
            x_center = (x_min + x_max) / 2.0
            y_center = (y_min + y_max) / 2.0
            box_w = x_max - x_min
            box_h = y_max - y_min

            # 归一化
            x_center /= img_w
            y_center /= img_h
            box_w /= img_w
            box_h /= img_h

            # 类别名称和难度标志
            cls_name = parts[8]
            # difficulty = parts[9]  # 如果需要可用

            # 映射为类别索引
            if cls_name not in CLASS_MAPPING:
                print(f"警告: 未知类别 {cls_name}，已跳过")
                continue
            cls_id = CLASS_MAPPING[cls_name]

            # 写入 YOLO 格式: <cls_id> <x_center> <y_center> <w> <h>
            fw.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}\n")

    print(f"已转换: {basename}" )

print("全部转换完成。")
