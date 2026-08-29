```
# 基于轻量化卷积神经网络的工业零部件表面缺陷智能检测系统

> 制造智能技术课程设计项目 | Vibe Coding开发 | B/S架构 | 工业质量控制场景

## 项目简介

本项目面向机械制造、汽车零部件、五金冲压等离散制造场景中的产品表面质量检测环节，开发一套基于机器视觉与轻量化卷积神经网络的智能缺陷检测系统。系统采用B/S架构，支持工业工件图片上传、缺陷自动识别分类、检测结果可视化展示与历史数据追溯，旨在辅助人工质检，降低漏检率，提升质检效率与检测标准一致性。

## 课程技术方向覆盖

本项目运用《制造智能技术》课程至少3个核心技术方向：

| 序号 | 技术方向 | 对应课程章节 | 在系统中的实际作用 |
|------|---------|-------------|-------------------|
| 1 | 工业机器视觉与图像处理技术 | 机器视觉与工业图像检测 | 图像灰度化、高斯滤波降噪、边缘检测、缺陷特征提取 |
| 2 | 工业机器学习与智能分类识别技术 | 机器学习与工业智能建模 | 基于CNN卷积神经网络的缺陷类型自动识别与分类 |
| 3 | 工业质量数据管理与追溯技术 | 工业数据处理与质量信息化 | 检测数据存储、历史记录查询、质量统计分析与追溯 |

## 系统架构

本项目采用完整B/S架构，包含四大核心模块：

```

┌─────────────────────────────────────────────┐
│                  前端 UI 层                     │
│  图片上传 | 结果展示 | 历史查询 | 报告预览    │
└──────────────────┬──────────────────────────┘
│ HTTP/REST API
┌──────────────────▼──────────────────────────┐
│                 后端服务层                     │
│  Flask 路由 | 业务逻辑调度 | 接口管理          │
└──────┬───────────────────┬──────────────────┘
│                   │
┌──────▼──────┐     ┌──────▼──────┐
│  算法模块层  │     │  数据存储层  │
│ 图像预处理   │     │  SQLite 数据库│
│ CNN 推理分类  │     │  检测记录存储│
└─────────────┘     └─────────────┘

```

## 技术栈

- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap
- **后端**：Python Flask
- **算法框架**：OpenCV + PyTorch
- **数据库**：SQLite
- **开发方式**：Vibe Coding（AI辅助人机协同开发）
- **版本控制**：Git + GitHub

## 项目目录结构

```

course-design-ai-project/
├── README.md                    # 项目说明文档
├── 学习笔记.md                  # 第一阶段：学习笔记
├── 选题说明.md                  # 第二阶段：选题说明
├── 方案设计.md                  # 第二阶段：方案设计
├── data/                        # 数据目录
│   ├── README.md                # 数据集详细说明与获取方法
│   ├── raw/                     # 原始数据索引
│   │   └── dataset_index.csv    # 完整数据集索引（1800 条）
│   ├── processed/               # 预处理后数据索引
│   │   ├── train_index.csv      # 训练集索引（70%，1260 条）
│   │   ├── val_index.csv        # 验证集索引（15%，270 条）
│   │   └── test_index.csv       # 测试集索引（15%，270 条）
│   └── samples/                 # 样本图片（每类 1 张，共 6 张）
├── src/                         # 源代码目录
│   └── preprocess.py            # 数据预处理程序
├── prompt/                      # AI 提示词追溯日志
│   ├── phase1_vibe_coding_learning.json
│   ├── phase2_topic_planning.json
│   └── phase3_data_preparation.json
└── models/                      # 模型权重目录
└── .gitkeep

```

## 数据集

本项目使用 **NEU-CLS 东北大学热轧钢表面缺陷数据集**，是工业缺陷检测领域的经典公开数据集。

- **数据规模**：6类缺陷 × 每类300张 = 共1800张，200×200像素灰度图
- **缺陷类别**：裂纹(Crazing)、夹杂(Inclusion)、斑块(Patches)、麻点(Pitted Surface)、氧化铁皮(Rolled-in Scale)、划痕(Scratches)
- **详细说明**：见 [data/README.md](data/README.md)
- **获取链接**：
  - 官方发布主页：https://faculty.neu.edu.cn/songkechen/zh_CN/zhym/263269/list/index.htm

## 数据预处理

运行以下命令完成数据预处理（需先下载数据集并按 [data/README.md](data/README.md) 说明放置到 `data/raw/images/` 目录）：

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

## 开发进度

表格

| 阶段 | 状态 | 交付物 |
| --- | --- | --- |
| 第一阶段：工具配置与 Vibe Coding 学习 | ✅ 已完成 | 学习笔记.md、GitHub 仓库、Git 环境配置 |
| 第二阶段：选题与方案设计 | ✅ 已完成 | 选题说明.md、方案设计.md |
| 第三阶段：数据资源整理 | ✅ 已完成 | data / 目录、preprocess.py、索引 CSV、prompt 日志 |
| 第四阶段：详细开发 | 🔄 进行中 | 后端 API、前端页面、CNN 算法模块、数据库 |
| 第五阶段：集成调试与报告撰写 | ⏳ 待开始 | 完整可运行 Demo、设计报告 |
| 第六阶段：答辩 | ⏳ 待开始 | 演示视频、答辩 PPT |

## AI 使用披露

本项目采用 Vibe Coding 方法，全程使用 AI 辅助开发。

- **使用工具**：豆包 AI 助手（选题调研、方案设计、代码解释、文档撰写）、通义灵码 VS Code 插件（代码补全、注释生成、调试辅助）
- **使用环节**：选题调研、架构设计、代码生成、调试辅助、文档梳理
- **审查机制**：所有 AI 生成内容均经过人工审查与运行测试，发现错误及时反馈修正，关键代码段可现场讲解逻辑
- **出错纠正**：AI 初版代码曾出现数据集划分未分层、路径分隔符不兼容等问题，均已人工指出并修正，详见 prompt 日志

详细 prompt 记录见 [prompt/](prompt/) 目录。

## 参考文献

[1] 张智海等。制造智能技术基础 [M]. 北京：清华大学出版社，2022.
[2] 杨杰。人工智能基础 [M]. 北京：机械工业出版社，2025.
[3] Song K, Yan Y. A noise robust method for surface defect detection of steel products [J]. IEEE Transactions on Instrumentation and Measurement, 2013.
[4] NEU 表面缺陷数据集 [EB/OL].[ https://faculty.neu.edu.cn/songkechen/zh_CN/zhym/263269/list/index.htm).
[5] Flask 官方文档 [EB/OL]. [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/), 2024.
[6] PyTorch 官方文档 [EB/OL]. https://pytorch.org/docs/, 2024.