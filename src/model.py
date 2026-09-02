"""
工业表面缺陷检测 - CNN模型定义
对应课程技术方向：工业机器学习与智能分类识别技术
"""
import torch
import torch.nn as nn


class DefectCNN(nn.Module):
    """
    轻量化卷积神经网络，用于6类工业表面缺陷分类
    
    输入：1通道灰度图，尺寸 200x200
    输出：6类缺陷的分类概率
    """
    def __init__(self, num_classes=6):
        super(DefectCNN, self).__init__()
        
        # 特征提取部分：3个卷积块（卷积+ReLU+最大池化）
        self.features = nn.Sequential(
            # 第1个卷积块：1通道 -> 32通道
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 200->100
            
            # 第2个卷积块：32通道 -> 64通道
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 100->50
            
            # 第3个卷积块：64通道 -> 128通道
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 50->25
        )
        
        # 分类器部分：全连接层
        self.classifier = nn.Sequential(
            nn.Linear(128 * 25 * 25, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),  # 防止过拟合
            nn.Linear(256, num_classes),
        )
    
    def forward(self, x):
        """前向传播"""
        x = self.features(x)
        x = x.view(x.size(0), -1)  # 展平
        x = self.classifier(x)
        return x


# 6类缺陷名称映射
DEFECT_NAMES = {
    0: "裂纹(Crazing)",
    1: "夹杂(Inclusion)",
    2: "斑块(Patches)",
    3: "麻点(Pitted Surface)",
    4: "氧化铁皮(Rolled-in Scale)",
    5: "划痕(Scratches)",
}
