import csv
import os
import cv2
from tqdm import tqdm

ann_path = 'D:/program/dataset/carclassyolo/valid/labels/'
res_csv = csv.writer(open('valid.csv', 'w', newline=''))

id_to_classname = {0: 'car', 1: 'light-cargo', 2: 'bus', 3: 'cargo',
                   4: 'special', 5: 'motorcycle', 6: 'bicycle', 7: 'person'}

for ann in tqdm(os.listdir(ann_path)):
    if ann.endswith('.txt'):
        print("Processing annotation for:", ann)
        base_name, _ = os.path.splitext(ann)
        img_path = os.path.join(ann_path, base_name + '.jpg')
        ann_txt = open(os.path.join(ann_path, ann)).readlines()

        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            if img is not None:
                h, w, _ = img.shape

                for line in ann_txt:
                    l = line.rstrip('\n').split(' ')
                    x1 = (float(l[1]) * w) - (float(l[3]) * w / 2)
                    y1 = (float(l[2]) * h) - (float(l[4]) * h / 2)
                    x2 = x1 + (float(l[3]) * w)
                    y2 = y1 + (float(l[4]) * h)
                    class_name = id_to_classname[int(l[0])]
                    res_csv.writerow([base_name, x1, y1, x2, y2, class_name])
        else:
            print("Image file not found for annotation:", ann)
