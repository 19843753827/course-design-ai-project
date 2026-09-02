"""
自动化测试脚本
测试后端API接口是否正常工作
运行方式: python -m pytest tests/ -v
"""
import os
import sys
import json
import pytest

# 把src目录加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, DB_PATH


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPI:
    """API接口测试类"""
    
    def test_stats_api(self, client):
        """测试统计接口是否可访问"""
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 200
        assert 'total_detections' in data['data']
    
    def test_records_api(self, client):
        """测试历史记录接口"""
        response = client.get('/api/records?page=1&page_size=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 200
        assert 'records' in data['data']
        assert 'total' in data['data']
    
    def test_detect_no_file(self, client):
        """测试检测接口：不上传文件时应返回400"""
        response = client.post('/api/detect')
        assert response.status_code == 400
    
    def test_detect_with_image(self, client):
        """测试检测接口：上传一张图片"""
        # 用samples里的一张图片测试
        test_img_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples', 'Cr_1.jpg')
        
        if not os.path.exists(test_img_path):
            pytest.skip("测试图片不存在，跳过")
        
        with open(test_img_path, 'rb') as f:
            response = client.post(
                '/api/detect',
                data={'image': (f, 'Cr_1.jpg')},
                content_type='multipart/form-data'
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 200
        assert 'defect_type' in data['data']
        assert 'confidence' in data['data']
        assert 0 <= data['data']['confidence'] <= 1


class TestModel:
    """模型测试类"""
    
    def test_model_loading(self):
        """测试模型能否正常加载"""
        import torch
        from model import DefectCNN
        
        model = DefectCNN(num_classes=6)
        # 测试前向传播
        dummy_input = torch.randn(1, 1, 200, 200)
        output = model(dummy_input)
        assert output.shape == (1, 6)  # 输出应该是6类
