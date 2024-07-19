import pandas as pd
import sqlite3

def import_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    # Connect to SQLite database
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()

    # Drop the inventory table if it exists
    cursor.execute('DROP TABLE IF EXISTS inventory')
    
    # Create the inventory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        position TEXT,
        data_matrix TEXT,
        barcode TEXT,
        sn_lot_no TEXT,
        reference_name TEXT
    )
    ''')

    # Iterate over the DataFrame and insert data into the database
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO inventory (position, data_matrix, barcode, sn_lot_no, reference_name) VALUES (?, ?, ?, ?, ?)", 
                       (row['POS'], str(row['Data Matrix']), str(row['Barcode']), str(row['SN/Lot no.']), row['Reference Name']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    file_path = 'Inventory.xlsx' 
    import_data_from_excel(file_path)
