import torch
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

from model import DefectCNN
from dataset import DefectDataset, get_train_val_test_transform, ID2LABEL

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def evaluate_model(model_path, test_csv, batch_size=16):
    _, test_transform = get_train_val_test_transform()
    test_dataset = DefectDataset(test_csv, transform=test_transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model = DefectCNN(num_classes=6).to(DEVICE)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.eval()

    all_pred = []
    all_true = []

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(DEVICE)
            outputs = model(imgs)
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            all_pred.extend(preds)
            all_true.extend(labels.numpy())

    acc = accuracy_score(all_true, all_pred)
    cm = confusion_matrix(all_true, all_pred)
    report = classification_report(all_true, all_pred, target_names=list(ID2LABEL.values()), digits=4)

    # 绘制混淆矩阵
    plt.figure(figsize=(8, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=list(ID2LABEL.values()),
                yticklabels=list(ID2LABEL.values()))
    plt.xlabel("预测类别")
    plt.ylabel("真实类别")
    plt.title("NEU‑CLS测试集混淆矩阵")
    plt.tight_layout()
    plt.savefig("../models/confusion_matrix.png", dpi=150)

    result_text = f"""
====模型评估结果====
测试集准确率：{acc:.4f}
{classification_report(all_true, all_pred, target_names=list(ID2LABEL.values()), digits=4)}
"""
    print(result_text)
    with open("../models/evaluation_report.txt", "w", encoding="utf‑8") as f:
        f.write(result_text)
    return acc, cm, report


if __name__ == "__main__":
    evaluate_model(
        model_path="../models/defect_cnn.pth",
        test_csv="../data/processed/test_index.csv",
        batch_size=16
    )
