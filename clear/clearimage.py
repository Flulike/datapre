import os

def find_missing_txt(images_dir, labels_dir):
    # 获取图像文件和文本文件的基本名称（去除扩展名）
    image_files = set(os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png'))
    label_files = set(os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith('.txt'))

    # 找出缺少文本文件的图像文件
    missing_txt_images = image_files - label_files

    if missing_txt_images:
        print("Images without corresponding label files:")
        for image in missing_txt_images:
            print(image)
    else:
        print("All images have corresponding label files.")

images_dir = "D:\program\dataset\carclassyolo/valid\labels/"
labels_dir = "D:\program\dataset\carclassyolo/valid\images/"
find_missing_txt(images_dir, labels_dir)
