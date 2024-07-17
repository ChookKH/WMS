import sqlite3

# 连接到SQLite数据库（如果数据库不存在会自动创建）
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY,
    sku TEXT,
    sn_number TEXT,
    position TEXT,
    quantity INTEGER,
    date TEXT
)
''')

conn.commit()
conn.close()
