"""
工业表面缺陷检测系统 - 数据预处理程序
对应课程技术方向：工业数据处理与质量信息化

功能：
1. 扫描原始数据目录，生成数据集索引
2. 分层抽样划分训练集/验证集/测试集（7:1.5:1.5）
3. 数据统计与校验
4. 生成预处理后的索引CSV文件
"""

import os
import csv
import random
import argparse
from collections import Counter
from pathlib import Path

# ==================== 配置参数 ====================
# 6类缺陷定义：类别编号 -> (英文目录名, 中文名称, 文件名前缀)
DEFECT_CLASSES = {
    0: ("crazing", "裂纹", "Cr_"),
    1: ("inclusion", "夹杂", "In_"),
    2: ("patches", "斑块", "Pa_"),
    3: ("pitted_surface", "麻点", "PS_"),
    4: ("rolled-in_scale", "氧化铁皮", "RS_"),
    5: ("scratches", "划痕", "Sc_"),
}

# 数据集划分比例
TRAIN_RATIO = 0.70   # 训练集 70%
VAL_RATIO = 0.15     # 验证集 15%
TEST_RATIO = 0.15    # 测试集 15%

# 随机种子（保证可复现，非常重要！）
RANDOM_SEED = 42


def scan_raw_data(raw_images_dir):
    """
    扫描原始数据目录，生成数据集索引列表
    
    Args:
        raw_images_dir: 原始图片根目录路径
        
    Returns:
        list: 每条记录为 (文件相对路径, 类别编号, 类别中文名)
    """
    index = []
    
    for class_id, (dir_name, class_name, prefix) in DEFECT_CLASSES.items():
        class_dir = os.path.join(raw_images_dir, dir_name)
        
        if not os.path.exists(class_dir):
            print(f"[警告] 类别目录不存在: {class_dir}，跳过该类别")
            continue
        
        # 扫描该类别下所有jpg图片
        image_files = [
            f for f in os.listdir(class_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        
        for img_file in sorted(image_files):
            # 相对路径（相对于data目录），便于跨平台使用
            rel_path = os.path.join("raw", "images", dir_name, img_file)
            index.append((rel_path, class_id, class_name))
        
        print(f"[扫描] {class_name}({dir_name}): {len(image_files)} 张")
    
    return index


def split_dataset(index, train_ratio, val_ratio, test_ratio, seed=42):
    """
    分层抽样划分数据集（保证每个类别的比例在各子集中一致）
    
    Args:
        index: 数据集索引列表
        train_ratio, val_ratio, test_ratio: 划分比例
        seed: 随机种子
        
    Returns:
        tuple: (train_index, val_index, test_index)
    """
    random.seed(seed)
    
    # 按类别分组
    class_groups = {}
    for item in index:
        class_id = item[1]
        if class_id not in class_groups:
            class_groups[class_id] = []
        class_groups[class_id].append(item)
    
    train_index, val_index, test_index = [], [], []
    
    for class_id, items in class_groups.items():
        # 每个类别内部打乱
        shuffled = items.copy()
        random.shuffle(shuffled)
        
        n_total = len(shuffled)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        # 剩余全部归测试集，避免浮点误差导致样本丢失
        
        train_index.extend(shuffled[:n_train])
        val_index.extend(shuffled[n_train:n_train + n_val])
        test_index.extend(shuffled[n_train + n_val:])
    
    # 再次打乱各子集内部顺序（避免按类别排列）
    random.shuffle(train_index)
    random.shuffle(val_index)
    random.shuffle(test_index)
    
    return train_index, val_index, test_index


def save_index_csv(index_list, output_path):
    """
    将数据集索引保存为CSV文件
    
    Args:
        index_list: 索引列表 [(path, class_id, class_name), ...]
        output_path: 输出CSV文件路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "class_id", "class_name"])
        for path, class_id, class_name in index_list:
            writer.writerow([path, class_id, class_name])
    
    print(f"[保存] {output_path} ({len(index_list)} 条记录)")


def print_dataset_stats(index_list, dataset_name):
    """
    打印数据集统计信息
    """
    print(f"\n{'='*50}")
    print(f"【{dataset_name}】统计信息")
    print(f"{'='*50}")
    print(f"总样本数: {len(index_list)}")
    
    class_counter = Counter(item[1] for item in index_list)
    for class_id, (dir_name, class_name, prefix) in DEFECT_CLASSES.items():
        count = class_counter.get(class_id, 0)
        percentage = count / len(index_list) * 100 if index_list else 0
        print(f"  {class_name}({dir_name}): {count} 张 ({percentage:.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="工业表面缺陷数据集预处理")
    parser.add_argument(
        "--raw_dir", 
        type=str, 
        default="data/raw/images",
        help="原始图片根目录路径"
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        default="data",
        help="输出目录路径"
    )
    args = parser.parse_args()
    
    print("=" * 50)
    print("工业表面缺陷检测系统 - 数据预处理")
    print("=" * 50)
    
    # 1. 扫描原始数据
    print("\n[步骤1] 扫描原始数据集...")
    full_index = scan_raw_data(args.raw_dir)
    
    if not full_index:
        print("[错误] 未找到任何图片数据，请检查原始数据目录路径！")
        print(f"       当前路径: {os.path.abspath(args.raw_dir)}")
        return
    
    print(f"\n[扫描完成] 共找到 {len(full_index)} 张图片")
    
    # 2. 保存完整数据集索引
    full_index_path = os.path.join(args.output_dir, "raw", "dataset_index.csv")
    save_index_csv(full_index, full_index_path)
    
    # 3. 分层抽样划分数据集
    print("\n[步骤2] 分层抽样划分数据集（训练70% / 验证15% / 测试15%）...")
    train_index, val_index, test_index = split_dataset(
        full_index, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, seed=RANDOM_SEED
    )
    
    # 4. 保存各子集索引
    print("\n[步骤3] 保存预处理后的索引文件...")
    save_index_csv(train_index, os.path.join(args.output_dir, "processed", "train_index.csv"))
    save_index_csv(val_index, os.path.join(args.output_dir, "processed", "val_index.csv"))
    save_index_csv(test_index, os.path.join(args.output_dir, "processed", "test_index.csv"))
    
    # 5. 打印统计信息
    print_dataset_stats(full_index, "完整数据集")
    print_dataset_stats(train_index, "训练集")
    print_dataset_stats(val_index, "验证集")
    print_dataset_stats(test_index, "测试集")
    
    print("\n" + "=" * 50)
    print("数据预处理完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
