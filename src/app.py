"""
工业表面缺陷检测系统 - Flask后端服务
提供REST API接口，连接前端、算法模块、数据库
"""
import os
import sys
import uuid
import torch
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
from torchvision import transforms

# 确保能导入同目录的model模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model import DefectCNN, DEFECT_NAMES

# ==================== 路径配置（全部基于src目录的上一级，即仓库根目录） ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 仓库根目录
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'uploads')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'defect_cnn.pth')
DB_PATH = os.path.join(BASE_DIR, 'data', 'defect_detection.db')
WEB_FOLDER = os.path.join(BASE_DIR, 'web')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================== Flask应用初始化 ====================
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# ==================== 加载模型（全局只加载一次） ====================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DefectCNN(num_classes=6).to(device)

if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    print(f"模型加载成功: {MODEL_PATH}")
else:
    print(f"警告: 模型文件不存在 {MODEL_PATH}")
    print("请先运行 train.py 训练模型，否则检测结果为随机预测")

# 图像预处理（和训练时保持一致）
transform = transforms.Compose([
    transforms.Resize((200, 200)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5]),
])


# ==================== 工具函数 ====================
def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def predict_defect(image_path):
    """
    调用CNN模型进行缺陷检测推理
    返回: (缺陷类型名称, 置信度)
    """
    image = Image.open(image_path).convert('L')  # 转灰度图
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    defect_type = DEFECT_NAMES[predicted.item()]
    confidence_value = round(confidence.item(), 4)
    return defect_type, confidence_value


def save_record(image_path, defect_type, confidence):
    """保存检测记录到数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inspection_records (image_path, defect_type, confidence) VALUES (?, ?, ?)",
        (image_path, defect_type, confidence)
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


# ==================== API接口 ====================

@app.route('/api/detect', methods=['POST'])
def detect():
    """【接口1】缺陷检测：上传图片，返回检测结果"""
    if 'image' not in request.files:
        return jsonify({"error": "未上传图片文件", "code": 400}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "未选择文件", "code": 400}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "不支持的文件格式，请上传jpg/png/bmp", "code": 400}), 400
    
    # 保存上传的图片（用uuid重命名避免重名）
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    save_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(save_path)
    
    # 调用算法模块检测
    try:
        defect_type, confidence = predict_defect(save_path)
    except Exception as e:
        return jsonify({"error": f"检测失败: {str(e)}", "code": 500}), 500
    
    # 保存记录到数据库
    record_id = save_record(f"/uploads/{unique_name}", defect_type, confidence)
    
    return jsonify({
        "code": 200,
        "message": "检测成功",
        "data": {
            "record_id": record_id,
            "image_path": f"/uploads/{unique_name}",
            "defect_type": defect_type,
            "confidence": confidence,
            "detection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    })


@app.route('/api/records', methods=['GET'])
def get_records():
    """【接口2】获取历史检测记录列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    defect_type = request.args.get('defect_type', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM inspection_records"
    count_query = "SELECT COUNT(*) as total FROM inspection_records"
    params = []
    
    if defect_type:
        query += " WHERE defect_type LIKE ?"
        count_query += " WHERE defect_type LIKE ?"
        params.append(f"%{defect_type}%")
    
    query += " ORDER BY detection_time DESC LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])
    
    cursor.execute(count_query, params[:-2] if defect_type else [])
    total = cursor.fetchone()['total']
    
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        "code": 200,
        "data": {
            "records": records,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """【接口3】获取检测统计数据"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT defect_type, COUNT(*) as count 
        FROM inspection_records 
        GROUP BY defect_type 
        ORDER BY count DESC
    """)
    stats = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) as total FROM inspection_records")
    total = cursor.fetchone()['total']
    conn.close()
    
    return jsonify({
        "code": 200,
        "data": {
            "total_detections": total,
            "defect_distribution": stats
        }
    })


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """提供上传图片的访问路径"""
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/')
def index():
    """首页，返回前端页面"""
    return send_from_directory(WEB_FOLDER, 'index.html')


# ==================== 启动服务 ====================
if __name__ == '__main__':
    print("=" * 50)
    print("工业表面缺陷智能检测系统 - 后端服务启动")
    print(f"设备: {device}")
    print(f"模型: {'已加载' if os.path.exists(MODEL_PATH) else '未加载（随机预测）'}")
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
