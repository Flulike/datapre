import os
import json
import xml.etree.ElementTree as ET

def get_categories(xml_files):
    categories = set()
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for obj in root.findall('object'):
            categories.add(obj.find('name').text)
    categories = sorted(list(categories))
    category_map = {cat: idx + 1 for idx, cat in enumerate(categories)}
    return category_map

def convert_annotation(xml_file, category_map):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    image_id = int(''.join(filter(str.isdigit, filename)))
    
    size = root.find('size')
    width = int(size.find('width').text.strip('[]'))
    height = int(size.find('height').text.strip('[]'))

    annotations = []
    for obj in root.findall('object'):
        category = obj.find('name').text
        category_id = category_map[category]

        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text) - 1
        ymin = int(bndbox.find('ymin').text) - 1
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        bbox = [xmin, ymin, xmax - xmin, ymax - ymin]

        annotation = {
            'image_id': image_id,
            'category_id': category_id,
            'bbox': bbox,
            'area': bbox[2] * bbox[3],
            'iscrowd': 0
        }
        annotations.append(annotation)

    return image_id, filename, width, height, annotations

def voc_to_coco(images_path, annotations_path, output_path):
    xml_files = [os.path.join(annotations_path, f) for f in os.listdir(annotations_path) if f.endswith('.xml')]
    category_map = get_categories(xml_files)

    coco_data = {
        'images': [],
        'annotations': [],
        'categories': []
    }

    annotation_id = 1
    for xml_file in xml_files:
        image_id, filename, width, height, annotations = convert_annotation(xml_file, category_map)
        image_info = {
            'id': image_id,
            'file_name': filename,
            'width': width,
            'height': height
        }
        coco_data['images'].append(image_info)

        for annotation in annotations:
            annotation['id'] = annotation_id
            coco_data['annotations'].append(annotation)
            annotation_id += 1

    for category, category_id in category_map.items():
        coco_data['categories'].append({'id': category_id, 'name': category})

    with open(output_path, 'w') as f:
        json.dump(coco_data, f, indent=4)

    print(f"COCO annotations saved to {output_path}")
    print(f"Number of categories: {len(category_map)}")
    print(f"Categories and their IDs: {category_map}")

if __name__ == '__main__':
    images_path = 'D:/program/dataset/bitvehiclevoc/train/images'
    annotations_path = 'D:/program/dataset/bitvehiclevoc/train/annotations'
    output_path = 'train.json'
    voc_to_coco(images_path, annotations_path, output_path)
    print(f"COCO annotations saved to {output_path}")
