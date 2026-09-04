import os
import cv2
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
import torchvision.transforms as T

# NEU‑CLS 类别映射，和README保持一致
LABEL_DICT = {
    "Crazing": 0,
    "Inclusion": 1,
    "Patches": 2,
    "Pitted_Surface": 3,
    "Rolled_in_Scale": 4,
    "Scratches": 5
}
ID2LABEL = {v: k for k, v in LABEL_DICT.items()}


class DefectDataset(Dataset):
    """工业零部件缺陷数据集，适配csv索引文件，兼容windows中文路径"""
    def __init__(self, csv_path, transform=None):
        self.df = pd.read_csv(csv_path, encoding="utf‑8‑sig")
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = row["image_path"]
        label = int(row["label"])

        # 解决OpenCV中文路径读取失败（README调试记录第4条问题）
        img_array = np.fromfile(img_path, dtype=np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

        if image is None:
            raise FileNotFoundError(f"图片读取失败:{img_path}")

        if self.transform is not None:
            image = self.transform(image)

        return image, label


def get_train_val_test_transform():
    """获取训练、验证测试集预处理，和推理保持一致"""
    train_transform = T.Compose([
        T.ToPILImage(),
        T.Resize((200, 200)),
        T.RandomHorizontalFlip(p=0.5),
        T.ToTensor(),
        T.Normalize(mean=[0.5], std=[0.5])
    ])

    val_test_transform = T.Compose([
        T.ToPILImage(),
        T.Resize((200, 200)),
        T.ToTensor(),
        T.Normalize(mean=[0.5], std=[0.5])
    ])
    return train_transform, val_test_transform


if __name__ == "__main__":
    # 本地自测代码
    csv_file = r"../data/processed/train_index.csv"
    train_tf, _ = get_train_val_test_transform()
    ds = DefectDataset(csv_file, transform=train_tf)
    print(f"数据集样本数量：{len(ds)}")
    img, lab = ds[0]
    print(f"单张图片shape:{img.shape}, label:{lab}")
