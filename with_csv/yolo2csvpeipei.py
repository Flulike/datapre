import os
import csv

def yolo_to_csv(yolo_dir, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image_path', 'class', 'x_center', 'y_center', 'width', 'height'])

        for label_file in os.listdir(yolo_dir):
            if label_file.endswith('.txt'):
                image_path = os.path.splitext(label_file)[0] + '.jpg'
                label_path = os.path.join(yolo_dir, label_file)

                with open(label_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    class_id, x_center, y_center, width, height = map(float, line.strip().split())
                    writer.writerow([image_path, int(class_id), x_center, y_center, width, height])

yolo_dir = 'D:/program/dataset/carclassyolo/train/labels/'
csv_file = "train1.csv"
yolo_to_csv(yolo_dir, csv_file)
