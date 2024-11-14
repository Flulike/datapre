import os

# 指定数据集路径和输出txt文件路径
dataset_dir = '/mnt/vmlqnap02/home/guo/dataset/car_196/images_discovery_all_3'
output_file = 'cars196_database.txt'

# 打开输出文件
with open(output_file, 'w') as file:
    # 遍历数据集文件夹中的每个文件夹（代表类）
    for class_folder in os.listdir(dataset_dir):
        class_folder_path = os.path.join(dataset_dir, class_folder)

        # 检查是否为文件夹
        if os.path.isdir(class_folder_path):
            # 获取类别标签（假设文件夹名的格式为 "195.smart_fortwo_Convertible_2012"）
            class_label = class_folder.split('.')[0]

            # 遍历类文件夹中的每个图片文件
            for img_file in os.listdir(class_folder_path):
                img_file_path = os.path.join(class_folder_path, img_file)

                # 检查是否为文件（非子文件夹）
                if os.path.isfile(img_file_path):
                    # 写入文件路径和类标签
                    file.write(f"{img_file_path} {class_label}\n")

print(f"已成功生成文件：{output_file}")
