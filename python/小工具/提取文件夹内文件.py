import os
import shutil
from concurrent.futures import ThreadPoolExecutor

def move_images(src_dir, dst_dir, image_extensions=None):
    """
    将源文件夹及其子文件夹中的所有图片文件移动到目标文件夹。
    如果要复制则改为copy_images
    参数:
    src_dir (str): 源文件夹路径
    dst_dir (str): 目标文件夹路径
    image_extensions (list): 图片文件扩展名列表（可选）
    """
    
    # 如果没有提供图片扩展名列表，使用默认的图片扩展名
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # 如果目标文件夹不存在，则创建目标文件夹
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    def move_file(src_file, dst_file):
        """
        移动单个文件并处理重名文件情况。
        
        参数:
        src_file (str): 源文件路径
        dst_file (str): 目标文件路径
        """
        if not os.path.exists(dst_file):
            shutil.move(src_file, dst_file)    # 如果是复制用这个shutil.copy2(src_file, dst_file)
        else:
            # 如果目标文件夹中存在同名文件，添加计数器重命名文件
            base, ext = os.path.splitext(dst_file)
            counter = 1
            while os.path.exists(dst_file):
                dst_file = f"{base}_{counter}{ext}"
                counter += 1
            shutil.move(src_file, dst_file)    # 如果是复制用这个shutil.copy2(src_file, dst_file)
        print(f"Moved: {src_file} to {dst_file}")

    files_to_move = []

    # 遍历源文件夹及其所有子文件夹
    for root, _, files in os.walk(src_dir):
        for file in files:
            # 检查文件扩展名是否在图片扩展名列表中
            if any(file.lower().endswith(ext) for ext in image_extensions):
                src_file = os.path.join(root, file)  # 源文件的完整路径
                dst_file = os.path.join(dst_dir, file)  # 目标文件的完整路径
                files_to_move.append((src_file, dst_file))

    # 使用多线程并行处理文件移动
    with ThreadPoolExecutor() as executor:
        executor.map(lambda args: move_file(*args), files_to_move)

# 示例用法
src_directory = '你的源文件夹路径'  # 替换为实际的源文件夹路径
dst_directory = '你的目标文件夹路径'  # 替换为实际的目标文件夹路径
move_images(src_directory, dst_directory)
