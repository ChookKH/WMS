import sqlite3

def setup_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    # Create the inventory table with the appropriate schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            position TEXT,
            data_matrix TEXT,
            barcode TEXT,
            sn_lot_no TEXT,
            reference_name TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()