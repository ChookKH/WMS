import pandas as pd
import sqlite3

def import_data_from_excel(Inventory for.xlsx)
    # 读取Excel文件
    df = pd.read_excel(Inventory for.xlsx)
    # 连接到SQLite数据库
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    # 遍历DataFrame并插入数据到数据库
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO inventory (sku, sn_number, position, quantity, date) VALUES (?, ?, ?, ?, ?)", 
                       (row['SKU'], row['SN Number'], row['Position'], row['Quantity'], row['Date']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    file_path = 'Inventory for.xlsx'  # 将此路径替换为您的Excel文件路径
    import_data_from_excel(Inventory for.xlsx)
