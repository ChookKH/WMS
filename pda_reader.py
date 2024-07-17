import serial
import sqlite3

def read_from_pda():
    # 打开串行端口
    ser = serial.Serial('COM3', 9600, timeout=1)  # 根据实际端口和波特率设置
    
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            process_pda_input(line)

def process_pda_input(data):
    # 假设PDA发送的数据格式为：SKU,SN,Position,Quantity,Date
    sku, sn, position, quantity, date = data.split(',')
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (sku, sn_number, position, quantity, date) VALUES (?, ?, ?, ?, ?)", 
                   (sku, sn, position, quantity, date))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    read_from_pda()
