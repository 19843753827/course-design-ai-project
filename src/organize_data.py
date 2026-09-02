"""
数据整理脚本：把混在一个文件夹里的NEU-CLS图片，按文件名前缀自动分到6个类别文件夹
"""
import os
import shutil

# 配置：源文件夹（图片都堆在这里）和目标文件夹（按类别分好）
SOURCE_DIR = "../data/raw/NEU-CLS"  # 改成你那个大文件夹的实际路径
TARGET_DIR = "../data/raw/images"   # 分类后也放在这里，会自动创建子文件夹

# 文件名前缀 -> 类别文件夹名 的映射
CATEGORY_MAP = {
    "Cr_": "crazing",        # 裂纹
    "In_": "inclusion",      # 夹杂
    "Pa_": "patches",        # 斑块
    "PS_": "pitted_surface", # 麻点
    "RS_": "rolled-in_scale",# 氧化铁皮
    "Sc_": "scratches",      # 划痕
}


def organize_images():
    # 确保源文件夹存在
    if not os.path.exists(SOURCE_DIR):
        print(f"错误：源文件夹不存在 {SOURCE_DIR}")
        print("请把脚本里的SOURCE_DIR改成你图片所在的实际路径")
        return

    # 创建6个类别子文件夹
    for folder in CATEGORY_MAP.values():
        os.makedirs(os.path.join(TARGET_DIR, folder), exist_ok=True)

    # 统计
    counts = {k: 0 for k in CATEGORY_MAP.values()}
    unknown = 0

    # 遍历源文件夹里的所有图片
    for filename in os.listdir(SOURCE_DIR):
        filepath = os.path.join(SOURCE_DIR, filename)
        
        # 跳过子文件夹，只处理图片文件
        if os.path.isdir(filepath):
            continue
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            continue

        # 根据文件名前缀判断类别
        target_folder = None
        for prefix, folder in CATEGORY_MAP.items():
            if filename.startswith(prefix):
                target_folder = folder
                break

        if target_folder:
            # 移动到对应类别文件夹
            dest_path = os.path.join(TARGET_DIR, target_folder, filename)
            shutil.move(filepath, dest_path)
            counts[target_folder] += 1
        else:
            print(f"无法识别类别，跳过: {filename}")
            unknown += 1

    # 打印结果
    print("=" * 40)
    print("分类完成！各类别数量：")
    for folder, count in counts.items():
        print(f"  {folder}: {count} 张")
    if unknown > 0:
        print(f"  未识别: {unknown} 张")
    print("=" * 40)


if __name__ == "__main__":
    organize_images()
