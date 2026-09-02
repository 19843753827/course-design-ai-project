\# 数据集说明



\## 1. 数据集名称

NEU-CLS 东北大学热轧钢表面缺陷数据集（Northeastern University Surface Defect Database）



\## 2. 数据集简介

本数据集由东北大学宋克臣教授团队发布，是工业表面缺陷检测领域的经典公开数据集，包含热轧钢板表面6类典型缺陷的灰度图像，适用于工业质量控制场景的缺陷分类与检测算法研究。



\## 3. 数据规模

\- 图像总数：1800张

\- 类别数：6类

\- 每类数量：300张

\- 图像尺寸：200×200像素

\- 图像格式：JPG，灰度图



\## 4. 缺陷类别说明

| 类别编号 | 英文名称 | 中文名称 | 文件名前缀 |

|---------|---------|---------|-----------|

| 0 | Crazing | 裂纹 | Cr\_ |

| 1 | Inclusion | 夹杂 | In\_ |

| 2 | Patches | 斑块 | Pa\_ |

| 3 | Pitted Surface | 麻点 | PS\_ |

| 4 | Rolled-in Scale | 氧化铁皮 | RS\_ |

| 5 | Scratches | 划痕 | Sc\_ |



\## 5. 数据集获取链接

以下渠道均可获取本数据集，推荐优先使用Kaggle：



1\. \*\*Kaggle（推荐，最稳定）\*\*：https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data

2\. \*\*官方发布主页\*\*：http://faculty.neu.edu.cn/songkechen/zh\_CN/zlw/list.htm

3\. \*\*GitHub相关项目\*\*：https://github.com/abin24/Mixed-Supervised-Defect-Detection



\## 6. 数据放置方法

由于完整数据集（1800张图片）体积较大，不直接纳入Git仓库。请按以下步骤放置数据：



1\. 从上述链接下载完整数据集并解压

2\. 将6类缺陷图片分别放入 `data/raw/images/` 目录下对应的子文件夹：



