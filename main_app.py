import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def add_item():
    sku = entry_sku.get()
    sn_number = entry_sn.get()
    position = entry_position.get()
    quantity = entry_quantity.get()
    date = entry_date.get()
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (sku, sn_number, position, quantity, date) VALUES (?, ?, ?, ?, ?)", 
                   (sku, sn_number, position, quantity, date))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Item added successfully")
    clear_entries()

def clear_entries():
    entry_sku.delete(0, tk.END)
    entry_sn.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_date.delete(0, tk.END)

def search_items():
    search_sku = search_entry_sku.get()
    search_sn = search_entry_sn.get()
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    query = "SELECT sku, sn_number, position, quantity, date FROM inventory WHERE sku=? OR sn_number=?"
    cursor.execute(query, (search_sku, search_sn))
    rows = cursor.fetchall()
    conn.close()
    
    for i in tree.get_children():
        tree.delete(i)
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def show_all_items():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sku, sn_number, position, quantity, date FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    
    for i in tree.get_children():
        tree.delete(i)
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_item():
    sku = delete_entry_sku.get()
    sn_number = delete_entry_sn.get()
    quantity_to_delete = int(delete_entry_quantity.get())
    
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity FROM inventory WHERE sku=? OR sn_number=?", (sku, sn_number))
    result = cursor.fetchone()
    
    if result:
        current_quantity = result[0]
        if current_quantity < quantity_to_delete:
            messagebox.showerror("Error", "Not enough quantity to delete")
        else:
            new_quantity = current_quantity - quantity_to_delete
            if new_quantity == 0:
                cursor.execute("DELETE FROM inventory WHERE sku=? OR sn_number=?", (sku, sn_number))
            else:
                cursor.execute("UPDATE inventory SET quantity=? WHERE sku=? OR sn_number=?", (new_quantity, sku, sn_number))
            conn.commit()
            messagebox.showinfo("Success", "Item deleted successfully")
    else:
        messagebox.showerror("Error", "Item not found")
    
    conn.close()
    clear_delete_entries()

def clear_delete_entries():
    delete_entry_sku.delete(0, tk.END)
    delete_entry_sn.delete(0, tk.END)
    delete_entry_quantity.delete(0, tk.END)

def create_gui():
    global entry_sku, entry_sn, entry_position, entry_quantity, entry_date
    global search_entry_sku, search_entry_sn, tree
    global delete_entry_sku, delete_entry_sn, delete_entry_quantity
    
    root = tk.Tk()
    root.title("Warehouse Management System")
    
    # Add Item Section
    tk.Label(root, text="SKU").grid(row=0, column=0)
    tk.Label(root, text="SN Number").grid(row=1, column=0)
    tk.Label(root, text="Position").grid(row=2, column=0)
    tk.Label(root, text="Quantity").grid(row=3, column=0)
    tk.Label(root, text="Date").grid(row=4, column=0)
    
    entry_sku = tk.Entry(root)
    entry_sn = tk.Entry(root)
    entry_position = tk.Entry(root)
    entry_quantity = tk.Entry(root)
    entry_date = tk.Entry(root)
    
    entry_sku.grid(row=0, column=1)
    entry_sn.grid(row=1, column=1)
    entry_position.grid(row=2, column=1)
    entry_quantity.grid(row=3, column=1)
    entry_date.grid(row=4, column=1)
    
    tk.Button(root, text="Add Item", command=add_item).grid(row=5, column=0, columnspan=2)
    
    # Search Section
    tk.Label(root, text="Search SKU").grid(row=6, column=0)
    search_entry_sku = tk.Entry(root)
    search_entry_sku.grid(row=6, column=1)
    
    tk.Label(root, text="Search SN Number").grid(row=7, column=0)
    search_entry_sn = tk.Entry(root)
    search_entry_sn.grid(row=7, column=1)
    
    tk.Button(root, text="Search", command=search_items).grid(row=8, column=0, columnspan=2)
    
    # Show All Items Button
    tk.Button(root, text="Show All Items", command=show_all_items).grid(row=9, column=0, columnspan=2)
    
    # Delete Item Section
    tk.Label(root, text="Delete SKU").grid(row=10, column=0)
    delete_entry_sku = tk.Entry(root)
    delete_entry_sku.grid(row=10, column=1)
    
    tk.Label(root, text="Delete SN Number").grid(row=11, column=0)
    delete_entry_sn = tk.Entry(root)
    delete_entry_sn.grid(row=11, column=1)
    
    tk.Label(root, text="Quantity to Delete").grid(row=12, column=0)
    delete_entry_quantity = tk.Entry(root)
    delete_entry_quantity.grid(row=12, column=1)
    
    tk.Button(root, text="Delete Item", command=delete_item).grid(row=13, column=0, columnspan=2)
    
    # Search Result Table
    columns = ('SKU', 'SN Number', 'Position', 'Quantity', 'Date')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=14, column=0, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
