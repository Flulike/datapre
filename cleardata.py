import os

def clean_orphan_files(images_dir, labels_dir):
    # 获取所有图像和标签文件的基本名称（去除扩展名）
    image_files = set(os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.endswith('.jpg'))
    label_files = set(os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith('.txt'))

    # 找出没有对应标签的图像文件
    orphan_images = image_files - label_files
    # 找出没有对应图像的标签文件
    orphan_labels = label_files - image_files

    # 删除没有对应标签的图像文件
    for image in orphan_images:
        image_path = os.path.join(images_dir, image + '.jpg')
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Deleted orphan image: {image_path}")
            except OSError as e:
                print(f"Error deleting {image_path}: {e}")

    # 删除没有对应图像的标签文件
    for label in orphan_labels:
        label_path = os.path.join(labels_dir, label + '.txt')
        if os.path.exists(label_path):
            try:
                os.remove(label_path)
                print(f"Deleted orphan label: {label_path}")
            except OSError as e:
                print(f"Error deleting {label_path}: {e}")

    # 检查是否清理干净
    remaining_image_files = set(os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.endswith('.jpg'))
    remaining_label_files = set(os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith('.txt'))

    if remaining_image_files == remaining_label_files:
        print("Cleanup successful: All images have corresponding labels and vice versa.")
    else:
        print("Cleanup incomplete: Mismatch still exists.")
        print(f"Remaining unmatched images: {remaining_image_files - remaining_label_files}")
        print(f"Remaining unmatched labels: {remaining_label_files - remaining_image_files}")


images_dir = "D:\program\dataset\carclassyolo/valid\images"
labels_dir = "D:\program\dataset\carclassyolo/valid\labels"
clean_orphan_files(images_dir, labels_dir)
