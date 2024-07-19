import os
import json
import numpy as np
import pandas as pd
import cv2
from sklearn.model_selection import train_test_split

np.random.seed(41)

classname_to_id = {'car': 1, 'light-cargo': 2, 'bus': 3, 'cargo': 4,
                   'special': 5, 'motorcycle': 6, 'bicycle': 7, 'person': 8}

class Csv2CoCo:
    def __init__(self, image_dir, total_annos):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.image_dir = image_dir
        self.total_annos = total_annos
        self.classname_to_id = classname_to_id

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w'), ensure_ascii=False, indent=2)  # indent=2 更加美观显示

    def to_coco(self, keys):
        self._init_categories()
        for key in keys:
            self.images.append(self._image(key))
            shapes = self.total_annos[key]
            for shape in shapes:
                bboxi = []
                for cor in shape[:-1]:
                    bboxi.append(int(cor))
                label = shape[-1]
                if isinstance(label, str):  # 如果标签是字符串类型
                    if label in self.classname_to_id:
                        label = self.classname_to_id[label]
                    else:
                        print(f"Warning: Label {label} not found in classname_to_id mapping.")
                        continue
                if label in self.classname_to_id.values():
                    annotation = self._annotation(bboxi, label, key)
                    self.annotations.append(annotation)
                    self.ann_id += 1
            self.img_id += 1
        instance = {
            'info': '123321 created',
            'license': ['license'],
            'images': self.images,
            'annotations': self.annotations,
            'categories': self.categories
        }
        return instance

    def _init_categories(self):
        for k, v in self.classname_to_id.items():
            category = {'id': v, 'name': k}
            self.categories.append(category)

    def _image(self, path):
        image = {}
        print(f"Processing image: {path}")
        img = cv2.imread(os.path.join(self.image_dir, path + '.jpg'))
        if img is not None:
            image['height'] = img.shape[0]
            image['width'] = img.shape[1]
            image['id'] = self.img_id
            image['file_name'] = path + '.jpg'
        else:
            print(f"Warning: Image {path} not found or could not be opened.")
        return image

    def _annotation(self, shape, label, path):
        points = shape[:4]
        annotation = {
            'id': self.ann_id,
            'image_id': self.img_id,
            'category_id': label,
            'segmentation': self._get_seg(points),
            'bbox': self._get_box(points),
            'iscrowd': 0,
            'area': self._get_area(points)
        }
        return annotation

    def _get_box(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return [min_x, min_y, max_x - min_x, max_y - min_y]

    def _get_area(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return (max_x - min_x + 1) * (max_y - min_y + 1)

    def _get_seg(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        h = max_y - min_y
        w = max_x - min_x
        return [[min_x, min_y, min_x, min_y + 0.5 * h, min_x, max_y, min_x + 0.5 * w, max_y, max_x, max_y, max_x, max_y - 0.5 * h, max_x, min_y, max_x - 0.5 * w, min_y]]

if __name__ == '__main__':
    csv_file = "valid.csv"
    image_dir = "D:/program/dataset/carclassyolo/valid/images/"
    saved_coco_path = "D:/program/dataset/carclasscoco/valid/"
    
    total_csv_annotations = {}
    annotations = pd.read_csv(csv_file, header=None).values
    for annotation in annotations:
        key = annotation[0].split(os.sep)[-1]
        value = np.array([annotation[1:]])
        if key in total_csv_annotations.keys():
            total_csv_annotations[key] = np.concatenate((total_csv_annotations[key], value), axis=0)
        else:
            total_csv_annotations[key] = value

    total_keys = list(total_csv_annotations.keys())

    l2c_train = Csv2CoCo(image_dir=image_dir, total_annos=total_csv_annotations)
    train_instance = l2c_train.to_coco(total_keys)
    l2c_train.save_coco_json(train_instance, f'{saved_coco_path}valid.json')
