import pandas as pd
import sqlite3

def import_data_from_excel(df):
    # 读取Excel文件
    df = pd.read_excel('Inventory.xlsx')
    df = df[df['SKU'] != 'Empty']
    # 连接到SQLite数据库
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    # 遍历DataFrame并插入数据到数据库
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO inventory (sku, sn_number, position, quantity, date) VALUES (?, ?, ?, ?, ?)", 
                       (row['SKU'], row['SN'], row['Position'], row['Quantity']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    file_path = 'Inventory for.xlsx'  # 将此路径替换为您的Excel文件路径
    import_data_from_excel('Inventory.xlsx')
