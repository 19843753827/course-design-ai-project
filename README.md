# 基于轻量化卷积神经网络的工业零部件表面缺陷智能检测系统

> 制造智能技术课程设计项目 | Vibe Coding 开发 | B/S 架构 | 工业质量控制场景

---

## 一、项目简介

本项目面向机械制造、汽车零部件、五金冲压等离散制造场景中的产品表面质量检测环节，开发一套基于机器视觉与轻量化卷积神经网络的智能缺陷检测系统。系统采用 B/S 架构，支持工业工件图片上传、缺陷自动识别分类、检测结果可视化展示与历史数据追溯，旨在辅助人工质检，降低漏检率，提升质检效率与检测标准一致性。

---

## 二、课程技术方向覆盖

本项目运用《制造智能技术》课程至少 3 个核心技术方向：

| 序号 | 技术方向 | 对应课程章节 | 在系统中的实际作用 |
|------|---------|-------------|-------------------|
| 1 | 工业机器视觉与图像处理技术 | 机器视觉与工业图像检测 | 图像灰度化、高斯滤波降噪、边缘检测、缺陷特征提取 |
| 2 | 工业机器学习与智能分类识别技术 | 机器学习与工业智能建模 | 基于 CNN 卷积神经网络的缺陷类型自动识别与分类 |
| 3 | 工业质量数据管理与追溯技术 | 工业数据处理与质量信息化 | 检测数据存储、历史记录查询、质量统计分析与追溯 |

---

## 三、系统架构

本项目采用完整 B/S 架构，自上而下分为四层：

1. **前端 UI 层**：图片上传、检测结果展示、历史记录查询、统计图表展示
2. **后端服务层**：Flask 路由、业务逻辑调度、REST API 接口管理
3. **算法模块层**：图像预处理（灰度化、降噪）、CNN 模型推理分类
4. **数据存储层**：SQLite 数据库，存储检测记录与图片路径

各层之间通过 HTTP/REST API 通信，前后端解耦，算法模块独立封装。

```
┌─────────────────────────────────────────────┐
│           前端 UI 层 (HTML/CSS/JS)           │
│   图片上传 │ 结果展示 │ 历史查询 │ 统计图表    │
└──────────────────┬──────────────────────────┘
                   │ HTTP / REST API
┌──────────────────▼──────────────────────────┐
│          后端服务层 (Python Flask)           │
│   路由管理 │ 业务逻辑 │ 文件处理 │ 接口调度    │
└──────────────────┬──────────────────────────┘
                   │ 函数调用
┌──────────────────▼──────────────────────────┐
│          算法模块层 (OpenCV + PyTorch)       │
│   图像预处理 │ CNN 模型推理 │ 结果后处理      │
└──────────────────┬──────────────────────────┘
                   │ SQL
┌──────────────────▼──────────────────────────┐
│          数据存储层 (SQLite)                 │
│   检测记录表 │ 图片路径 │ 统计数据            │
└─────────────────────────────────────────────┘
```

---

## 四、技术栈

| 层级 | 技术 | 版本/说明 |
|------|------|----------|
| 前端 | HTML5 + CSS3 + JavaScript + Bootstrap | 响应式页面，Chart.js 绘制统计图表 |
| 后端 | Python Flask | Web 框架，RESTful API |
| 算法框架 | OpenCV + PyTorch | 图像处理 + 深度学习推理 |
| 数据库 | SQLite | 轻量级嵌入式数据库，无需额外安装 |
| 开发方式 | Vibe Coding（AI 辅助人机协同开发） | 豆包 AI + 通义灵码 |
| 版本控制 | Git + GitHub | 代码托管与版本管理 |

---

## 五、项目目录结构

```
.
├── README.md                    # 项目说明文档（本文件）
├── 学习笔记.md                  # 第一阶段学习笔记
├── 选题说明.md                  # 第二阶段选题说明
├── 方案设计.md                  # 第二阶段方案设计
│
├── data/                        # 数据目录
│   ├── README.md                # 数据集详细说明与获取方法
│   ├── raw/                     # 原始数据
│   │   ├── images/              # 原始图片（6 个子目录，每类 300 张）
│   │   └── dataset_index.csv    # 完整数据集索引（1800 条）
│   ├── processed/               # 预处理后数据索引
│   │   ├── train_index.csv      # 训练集索引（70%，1260 条）
│   │   ├── val_index.csv        # 验证集索引（15%，270 条）
│   │   └── test_index.csv       # 测试集索引（15%，270 条）
│   └── samples/                 # 样本图片（每类 1 张，共 6 张）
│   └──uploads/
|   └──defect_detection.db       
├── src/                         # 源代码目录
│   ├── preprocess.py            # 数据预处理程序
│   ├── model.py                 # CNN 模型定义（轻量化网络结构）
│   ├── train.py                 # 模型训练脚本
│   ├── init_db.py               # 数据库初始化脚本
│   ├── app.py                   # Flask 后端主程序
│   └── organize_data.py         # 数据集整理程序      
│   └── test_model.py            # 模型测试脚本
├── models/                      # 模型权重目录
│   └── defect_cnn.pth           # 模型权重文件
│
├── web/                         # Web 应用目录
│   ├── index.html               # 主页 HTML 文件
│
├── tests/                       # 测试脚本目录
│   ├── test_api.py              # 后端 API 接口测试
│   ├── __pycache__               # 测试脚本缓存文件
│       ├── test_api.cpython-310-pytest-9.1.1.pyc     # 测试脚本缓存文件
│
├── prompt/                      # AI 提示词追溯日志
│   ├── phase1_vibe_coding_learning.json
│   ├── phase2_topic_planning.json
│   ├── phase3_data_preparation.json
│   
│
└── venv_torch/                    # 虚拟环境目录
|
└── .pytest_cache                  # 测试脚本缓存目录

```
---

## 六、数据集

本项目使用 **NEU-CLS 东北大学热轧钢表面缺陷数据集**，是工业缺陷检测领域的经典公开数据集。

- **数据规模**：6 类缺陷 × 每类 300 张 = 共 1800 张，200×200 像素灰度图
- **缺陷类别**：

| 类别编号 | 英文名称 | 中文名称 | 说明 |
|---------|---------|---------|------|
| 0 | Crazing | 裂纹 | 表面网状细微裂纹 |
| 1 | Inclusion | 夹杂 | 非金属夹杂物 |
| 2 | Patches | 斑块 | 不规则深色斑块 |
| 3 | Pitted Surface | 麻点 | 点状凹坑密集分布 |
| 4 | Rolled-in Scale | 氧化铁皮 | 轧制过程中氧化皮压入 |
| 5 | Scratches | 划痕 | 线性划伤痕迹 |

- **详细说明**：见 `data/README.md`
- **获取链接**：
  - Kaggle（推荐）：https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data
  - 官方发布主页：https://faculty.neu.edu.cn/songkechen/zh_CN/zhym/263269/list/index.htm

---

## 七、数据预处理

运行以下命令完成数据预处理（需先下载数据集并按 `data/README.md` 说明放置到 `data/raw/images/` 目录）：

```bash
python src/preprocess.py --raw_dir data/raw/images
```

**预处理内容：**
- 扫描原始数据集 6 个类别文件夹，生成完整索引 CSV
- 分层抽样划分训练集 (70%) / 验证集 (15%) / 测试集 (15%)，保证各类别比例一致
- 生成各子集索引 CSV 文件（UTF-8-sig 编码，Excel 打开中文不乱码）
- 输出完整数据集及各子集的类别分布统计信息
- 固定随机种子 42，保证划分结果可复现

**输出文件：**
- `data/raw/dataset_index.csv`：完整数据集索引
- `data/processed/train_index.csv`：训练集索引
- `data/processed/val_index.csv`：验证集索引
- `data/processed/test_index.csv`：测试集索引

---

## 八、模型训练与评估

### 8.1 模型结构

系统采用轻量化 CNN 网络，包含以下核心组件：
- 3 个卷积块（Conv + BN + ReLU + MaxPool）
- 2 个全连接层（含 Dropout 防止过拟合）
- 输出层：6 维 Softmax，对应 6 类缺陷

### 8.2 训练命令

```bash
python src/train.py \
  --train_csv data/processed/train_index.csv \
  --val_csv data/processed/val_index.csv \
  --epochs 30 \
  --batch_size 32 \
  --lr 0.001 \
  --save_dir models/
```

### 8.3 训练结果

| 指标 | 数值 |
|------|------|
| 训练集准确率 | 0.9397|
| 验证集准确率 | 0.9481 |
| 最佳 Epoch | 第 10 轮 |
| 损失函数 | CrossEntropyLoss |
| 优化器 | Adam |

---

## 九、系统功能模块

### 9.1 缺陷检测（首页）

- 支持上传 JPG/PNG/BMP 格式图片
- 自动进行图像预处理（灰度化、尺寸归一化、张量转换）
- CNN 模型推理，输出预测类别及置信度
- 页面展示：原图、预处理结果、预测类别、置信度百分比、各类别概率条形图

### 9.2 历史记录

- 自动保存每次检测记录（图片路径、预测结果、置信度、检测时间）
- 支持按时间范围、缺陷类别筛选查询
- 支持分页浏览，点击记录可查看详情


---

## 十、快速开始

### 10.1 环境配置

```bash
# 激活虚拟环境（推荐）
conda activate torch_env

# 安装依赖
pip install flask torch torchvision opencv-python numpy pandas matplotlib scikit-learn
```


### 10.2 初始化数据库

```bash
cd src
python init_db.py
```

该命令会创建 `defect_detection.db` 数据库及检测记录表。

### 10.3 启动系统

```bash
python app.py
```

启动后浏览器访问：**http://127.0.0.1:5000**


---

## 十一、集成调试与测试

### 11.1 单元测试

```bash
# 模型推理测试
python tests/test_model.py

# API 接口测试
python tests/test_api.py
```

### 11.2 端到端集成测试

```bash
python tests/test_system.py
```

测试覆盖：图片上传 → 预处理 → 模型推理 → 结果返回 → 数据库写入 → 历史查询 全流程。

### 11.3 调试记录（Vibe Coding 人机协同证据）

开发过程中遇到并解决的典型问题：

| 序号 | 问题描述 | 原因分析 | 解决方案 |
|------|---------|---------|---------|
| 1 | AI 初版 `app.py` 未限制上传文件大小，大图片导致内存溢出 | 缺少文件大小校验 | 添加上传文件大小限制（如 10MB），超出返回友好提示 |
| 2 | 前端 `fetch` 调用路径与后端路由不匹配 | API 地址拼写错误 | 修正为正确的 `/api/detect` 路径，并统一前后端接口约定 |
| 3 | 模型推理时张量维度不匹配 | 输入图片未按模型要求归一化 | 在 `inference.py` 中统一添加 `transforms.Normalize` |
| 4 | 中文路径在 Windows 下 OpenCV 读取失败 | OpenCV 默认不支持中文路径 | 改用 `np.fromfile` + `cv2.imdecode` 方式读取 |
| 5 | 数据库并发写入报错 | SQLite 默认单写入锁 | 添加线程锁或改为串行写入，Flask 开发环境足够使用 |


---

## 十二、开发进度

| 阶段 | 状态 | 交付物 |
|------|------|--------|
| 第一阶段：工具配置与 Vibe Coding 学习 | ✅ 已完成 | 学习笔记.md、GitHub 仓库、Git 环境配置 |
| 第二阶段：选题与方案设计 | ✅ 已完成 | 选题说明.md、方案设计.md |
| 第三阶段：数据资源整理 | ✅ 已完成 | data/ 目录、preprocess.py、索引 CSV、prompt 日志 |
| 第四阶段：详细开发 | ✅ 已完成 | 模型训练、Flask 后端、前端页面、数据库、测试脚本 |
| 第五阶段：集成调试与报告撰写 | ✅ 已完成 | 完整可运行 Demo、设计报告、测试报告 |
| 第六阶段：答辩 | ⏳ 待开始 | 演示视频、答辩 PPT |

---

## 十三、AI 使用披露

本项目采用 Vibe Coding 方法，全程使用 AI 辅助开发。

- **使用工具**：豆包 AI 助手（选题调研、方案设计、代码解释、文档撰写）、通义灵码 VS Code 插件（代码补全、注释生成、调试辅助）
- **使用环节**：选题调研、架构设计、代码生成、调试辅助、文档梳理
- **审查机制**：所有 AI 生成内容均经过人工审查与运行测试，发现错误及时反馈修正，关键代码段可现场讲解逻辑
- **出错纠正**：AI 初版代码曾出现数据集划分未分层、路径分隔符不兼容、API 路径写错、缺少文件上传大小限制等问题，均已人工指出并修正，详见 prompt 日志

详细 prompt 记录见 `prompt/` 目录。

---

## 十四、参考文献

[1] 张智海等. 制造智能技术基础 [M]. 北京：清华大学出版社，2022.

[2] 杨杰. 人工智能基础 [M]. 北京：机械工业出版社，2025.

[3] Song K, Yan Y. A noise robust method for surface defect detection of steel products [J]. IEEE Transactions on Instrumentation and Measurement, 2013.

[4] NEU 表面缺陷数据集 [EB/OL]. https://faculty.neu.edu.cn/songkechen/zh_CN/zhym/263269/list/index.htm

[5] Flask 官方文档 [EB/OL]. https://flask.palletsprojects.com/, 2024.

[6] PyTorch 官方文档 [EB/OL]. https://pytorch.org/docs/, 2024.

[7] He K, Zhang X, Ren S, et al. Deep Residual Learning for Image Recognition [C]. CVPR, 2016.

---

*文档版本：v1.0 | 最后更新：2026-09-02*
