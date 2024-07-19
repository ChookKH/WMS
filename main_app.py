import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def add_item():
    position = entry_position.get()
    data_matrix = entry_data_matrix.get()
    barcode = entry_barcode.get().rstrip('.0')
    sn_lot_no = entry_sn_lot_no.get().rstrip('.0')
    reference_name = entry_reference_name.get()
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (position, data_matrix, barcode, sn_lot_no, reference_name) VALUES (?, ?, ?, ?, ?)", 
                   (position, data_matrix, barcode, sn_lot_no, reference_name))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Item added successfully")
    clear_entries()

def clear_entries():
    entry_position.delete(0, tk.END)
    entry_data_matrix.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)
    entry_sn_lot_no.delete(0, tk.END)
    entry_reference_name.delete(0, tk.END)

def search_items():
    search_position = search_entry_position.get()
    search_data_matrix = search_entry_data_matrix.get()
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    query = "SELECT position, data_matrix, barcode, sn_lot_no, reference_name FROM inventory WHERE position=? OR data_matrix=?"
    cursor.execute(query, (search_position, search_data_matrix))
    rows = cursor.fetchall()
    conn.close()
    
    for i in tree.get_children():
        tree.delete(i)
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def show_all_items():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT position, data_matrix, barcode, sn_lot_no, reference_name FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    
    for i in tree.get_children():
        tree.delete(i)
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_item():
    position = delete_entry_position.get()
    data_matrix = delete_entry_data_matrix.get()
    quantity_to_delete = int(delete_entry_quantity.get())
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity FROM inventory WHERE position=? OR data_matrix=?", (position, data_matrix))
    result = cursor.fetchone()
    
    if result:
        current_quantity = result[0]
        if current_quantity < quantity_to_delete:
            messagebox.showerror("Error", "Not enough quantity to delete")
        else:
            new_quantity = current_quantity - quantity_to_delete
            if new_quantity == 0:
                cursor.execute("DELETE FROM inventory WHERE position=? OR data_matrix=?", (position, data_matrix))
            else:
                cursor.execute("UPDATE inventory SET quantity=? WHERE position=? OR data_matrix=?", (new_quantity, position, data_matrix))
            conn.commit()
            messagebox.showinfo("Success", "Item deleted successfully")
    else:
        messagebox.showerror("Error", "Item not found")
    
    conn.close()
    clear_delete_entries()

def clear_delete_entries():
    delete_entry_position.delete(0, tk.END)
    delete_entry_data_matrix.delete(0, tk.END)
    delete_entry_quantity.delete(0, tk.END)

def create_gui():
    global entry_position, entry_data_matrix, entry_barcode, entry_sn_lot_no, entry_reference_name
    global search_entry_position, search_entry_data_matrix, tree
    global delete_entry_position, delete_entry_data_matrix, delete_entry_quantity
    
    root = tk.Tk()
    root.title("Warehouse Management System")
    
    # Add Item Section
    tk.Label(root, text="Position").grid(row=0, column=0)
    tk.Label(root, text="Data Matrix").grid(row=1, column=0)
    tk.Label(root, text="Barcode").grid(row=2, column=0)
    tk.Label(root, text="SN/Lot No.").grid(row=3, column=0)
    tk.Label(root, text="Reference Name").grid(row=4, column=0)
    
    entry_position = tk.Entry(root)
    entry_data_matrix = tk.Entry(root)
    entry_barcode = tk.Entry(root)
    entry_sn_lot_no = tk.Entry(root)
    entry_reference_name = tk.Entry(root)
    
    entry_position.grid(row=0, column=1)
    entry_data_matrix.grid(row=1, column=1)
    entry_barcode.grid(row=2, column=1)
    entry_sn_lot_no.grid(row=3, column=1)
    entry_reference_name.grid(row=4, column=1)
    
    tk.Button(root, text="Add Item", command=add_item).grid(row=5, column=0, columnspan=2)
    
    # Search Section
    tk.Label(root, text="Search Position").grid(row=6, column=0)
    search_entry_position = tk.Entry(root)
    search_entry_position.grid(row=6, column=1)
    
    tk.Label(root, text="Search Data Matrix").grid(row=7, column=0)
    search_entry_data_matrix = tk.Entry(root)
    search_entry_data_matrix.grid(row=7, column=1)
    
    tk.Button(root, text="Search", command=search_items).grid(row=8, column=0, columnspan=2)
    
    # Show All Items Button
    tk.Button(root, text="Show All Items", command=show_all_items).grid(row=9, column=0, columnspan=2)
    
    # Delete Item Section
    tk.Label(root, text="Delete Position").grid(row=10, column=0)
    delete_entry_position = tk.Entry(root)
    delete_entry_position.grid(row=10, column=1)
    
    tk.Label(root, text="Delete Data Matrix").grid(row=11, column=0)
    delete_entry_data_matrix = tk.Entry(root)
    delete_entry_data_matrix.grid(row=11, column=1)
    
    tk.Label(root, text="Quantity to Delete").grid(row=12, column=0)
    delete_entry_quantity = tk.Entry(root)
    delete_entry_quantity.grid(row=12, column=1)
    
    tk.Button(root, text="Delete Item", command=delete_item).grid(row=13, column=0, columnspan=2)
    
    # Search Result Table
    columns = ('Position', 'Data Matrix', 'Barcode', 'SN/Lot No.', 'Reference Name')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=14, column=0, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
