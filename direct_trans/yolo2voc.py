import os
import xml.etree.ElementTree as ET

# 类别名称列表
classes = []
with open("obj.names") as f:
    classes = [line.strip() for line in f.readlines()]

def convert_yolo_to_voc(yolo_dir, images_dir, voc_dir):
    if not os.path.exists(voc_dir):
        os.makedirs(voc_dir)

    for yolo_file in os.listdir(yolo_dir):
        if not yolo_file.endswith(".txt"):
            continue

        image_id = os.path.splitext(yolo_file)[0]
        img_path = os.path.join(images_dir, f"{image_id}.jpg")

        with open(os.path.join(yolo_dir, yolo_file), "r") as f:
            lines = f.readlines()

        # Create XML root
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "folder").text = os.path.basename(images_dir)
        ET.SubElement(annotation, "filename").text = f"{image_id}.jpg"

        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text = "Unknown"

        size = ET.SubElement(annotation, "size")
        width, height, depth = get_image_size(img_path)
        ET.SubElement(size, "width").text = str(width)
        ET.SubElement(size, "height").text = str(height)
        ET.SubElement(size, "depth").text = str(depth)

        ET.SubElement(annotation, "segmented").text = "0"

        for line in lines:
            parts = line.strip().split()
            class_id, x_center, y_center, width, height = map(float, parts)
            class_name = classes[int(class_id)]

            x_center *= width
            y_center *= height
            width *= width
            height *= height

            xmin = int(x_center - width / 2)
            xmax = int(x_center + width / 2)
            ymin = int(y_center - height / 2)
            ymax = int(y_center + height / 2)

            obj = ET.SubElement(annotation, "object")
            ET.SubElement(obj, "name").text = class_name
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = "0"
            ET.SubElement(obj, "difficult").text = "0"

            bbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bbox, "xmin").text = str(xmin)
            ET.SubElement(bbox, "ymin").text = str(ymin)
            ET.SubElement(bbox, "xmax").text = str(xmax)
            ET.SubElement(bbox, "ymax").text = str(ymax)

        tree = ET.ElementTree(annotation)
        tree.write(os.path.join(voc_dir, f"{image_id}.xml"))

def get_image_size(img_path):
    from PIL import Image
    with Image.open(img_path) as img:
        return img.size[0], img.size[1], len(img.getbands())


# 示例用法
yolo_labels_dir = "D:\program\dataset\carclassyolo/train\labels"
images_dir = "D:\program\dataset\carclassyolo/train\images"
voc_annotations_dir = "D:\program\dataset\carclassvoc/train"
convert_yolo_to_voc(yolo_labels_dir, images_dir, voc_annotations_dir)
