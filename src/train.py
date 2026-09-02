"""
工业表面缺陷检测 - 模型训练脚本
对应课程技术方向：工业机器学习与智能分类识别技术
"""
import os
import csv
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

from model import DefectCNN, DEFECT_NAMES


# ==================== 配置参数 ====================
DATA_DIR = "data"
TRAIN_CSV = os.path.join(DATA_DIR, "processed", "train_index.csv")
VAL_CSV = os.path.join(DATA_DIR, "processed", "val_index.csv")
MODEL_SAVE_PATH = "models/defect_cnn.pth"

BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
NUM_CLASSES = 6
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DefectDataset(Dataset):
    """自定义数据集，从CSV索引读取图片和标签"""
    
    def __init__(self, csv_path, transform=None):
        self.samples = []
        self.transform = transform
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSV里的路径是相对data目录的，这里拼上data前缀
                img_path = os.path.join(DATA_DIR, row['image_path'])
                label = int(row['class_id'])
                self.samples.append((img_path, label))
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('L')  # 转灰度图
        if self.transform:
            image = self.transform(image)
        return image, label


def train_one_epoch(model, dataloader, criterion, optimizer, device):
    """训练一个epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    return running_loss / len(dataloader), correct / total


def validate(model, dataloader, criterion, device):
    """验证模型"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    return running_loss / len(dataloader), correct / total


def main():
    print(f"使用设备: {DEVICE}")
    print("=" * 50)
    
    # 数据预处理：转Tensor + 归一化
    transform = transforms.Compose([
        transforms.Resize((200, 200)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ])
    
    # 加载数据集
    train_dataset = DefectDataset(TRAIN_CSV, transform=transform)
    val_dataset = DefectDataset(VAL_CSV, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"训练集: {len(train_dataset)} 张")
    print(f"验证集: {len(val_dataset)} 张")
    
    # 初始化模型、损失函数、优化器
    model = DefectCNN(num_classes=NUM_CLASSES).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # 训练循环
    best_val_acc = 0.0
    for epoch in range(EPOCHS):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, DEVICE)
        val_loss, val_acc = validate(model, val_loader, criterion, DEVICE)
        
        print(f"Epoch [{epoch+1}/{EPOCHS}] "
              f"训练Loss: {train_loss:.4f}, 训练准确率: {train_acc:.4f} | "
              f"验证Loss: {val_loss:.4f}, 验证准确率: {val_acc:.4f}")
        
        # 保存验证准确率最高的模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  -> 保存最佳模型 (验证准确率: {val_acc:.4f})")
    
    print("=" * 50)
    print(f"训练完成！最佳验证准确率: {best_val_acc:.4f}")
    print(f"模型已保存到: {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    main()
