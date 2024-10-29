import os
import shutil
import subprocess

def sort_images_by_file_size(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            file_path = os.path.join(directory, filename)
            size = os.path.getsize(file_path)
            images.append((file_path, size))
    # 按照文件大小进行排序
    sorted_images = sorted(images, key=lambda x: x[1], reverse=True)
    return sorted_images


# 导出前7张最大的图片
def copy_largest_images(sorted_images, destination, n=7):
    # 如果目的文件夹不存在，则创建
    if not os.path.exists(destination):
        os.makedirs(destination)
    for i in range(min(n, len(sorted_images))):
        src = sorted_images[i][0]
        dst = os.path.join(destination, os.path.basename(src))
        shutil.copy(src, dst)

def delete_folder(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)


# 鉴黄
def traversal_files(path):
    source_directory = path
    destination_directory = 'temp'
    # 图片排序
    sorted_images = sort_images_by_file_size(source_directory)
    # 取出前七张图片
    copy_largest_images(sorted_images, destination_directory)
    # 鉴别
    porn = 0
    for item in os.scandir(destination_directory):
        if item.is_file():
            img_path = item.path
            # command = rf'python \model\nsfw\nsfw_predict.py {img_path}'
            # 由于图片鉴黄模型不能集成到系统中，因此command改了，如果涉黄模型解决了再改回来
            command = 'echo Hello World!'
            result = subprocess.run(command, shell=True, capture_output=True, text=True).stdout
            try:
                result = eval(result)
                cla = result['class']
                if cla=='porn':
                    porn += 1
            except Exception:
                continue
    delete_folder(destination_directory)
    if porn>0:
        return 1
    else:
        return 0
