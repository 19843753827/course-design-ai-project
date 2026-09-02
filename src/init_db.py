"""
数据库初始化脚本
对应课程技术方向：工业质量数据管理与追溯技术
创建SQLite数据库和检测记录表
"""
import sqlite3
import os

# 数据库路径（src目录的上一级，即仓库根目录/data/）
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'defect_detection.db')


def init_database():
    """初始化数据库，创建检测记录表"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建检测记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspection_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            defect_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            remark TEXT
        )
    ''')
    
    # 创建索引，提升查询效率
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_defect_type 
        ON inspection_records(defect_type)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_detection_time 
        ON inspection_records(detection_time)
    ''')
    
    conn.commit()
    conn.close()
    print(f"数据库初始化完成: {DB_PATH}")


if __name__ == "__main__":
    init_database()
