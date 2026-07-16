import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="pharmacy_db"
)
cursor = conn.cursor()

# MAIN WINDOW
root = tk.Tk()
root.title("Pharmacy Management System")
root.geometry("1000x650")
root.configure(bg="#0f172a")
root.resizable(False, False)

# COLORS AND FONTS
BG       = "#0f172a"
CARD     = "#1e293b"
ACCENT   = "#38bdf8"
ACCENT2  = "#0ea5e9"
SUCCESS  = "#22c55e"
DANGER   = "#ef4444"
WARNING  = "#f59e0b"
TEXT     = "#f1f5f9"
SUBTEXT  = "#94a3b8"
ENTRY_BG = "#273549"

FONT_TITLE = ("Courier New", 18, "bold")
FONT_LABEL = ("Courier New", 10, "bold")
FONT_ENTRY = ("Courier New", 10)
FONT_BTN   = ("Courier New", 10, "bold")
FONT_TABLE = ("Courier New", 9)

# HEADER
header = tk.Frame(root, bg=CARD, pady=12)
header.pack(fill="x")
tk.Label(header, text="PHARMACY MANAGEMENT SYSTEM",
         font=FONT_TITLE, bg=CARD, fg=ACCENT).pack()
tk.Label(header, text="Manage medicines | suppliers | customers | sales",
         font=("Courier New", 9), bg=CARD, fg=SUBTEXT).pack()

# STYLE FOR TABS AND TABLE
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=CARD, foreground=SUBTEXT,
                font=FONT_LABEL, padding=[12, 6])
style.map("TNotebook.Tab", background=[("selected", ACCENT2)],
          foreground=[("selected", "#0f172a")])
style.configure("Treeview", background=CARD, foreground=TEXT,
                fieldbackground=CARD, font=FONT_TABLE, rowheight=26)
style.configure("Treeview.Heading", background=ACCENT2,
                foreground="#0f172a", font=FONT_LABEL, relief="flat")
style.map("Treeview", background=[("selected", ACCENT2)],
          foreground=[("selected", "#0f172a")])

# NOTEBOOK WITH 4 TABS
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=12, pady=8)

# HELPER FUNCTION - CREATE LABEL FRAME
def make_card(parent, title):
    return tk.LabelFrame(parent, text=title,
                         font=FONT_LABEL, bg=CARD, fg=ACCENT,
                         bd=1, relief="solid", padx=10, pady=8)

# HELPER FUNCTION - CREATE BUTTON
def make_button(parent, text, color, cmd):
    return tk.Button(parent, text=text, font=FONT_BTN,
                     bg=color, fg="#0f172a", activebackground=color,
                     relief="flat", cursor="hand2", padx=8, pady=5,
                     command=cmd)

# HELPER FUNCTION - CREATE LABEL AND ENTRY
def make_entry(parent, label, row):
    tk.Label(parent, text=label, font=FONT_LABEL,
             bg=CARD, fg=SUBTEXT).grid(row=row, column=0, sticky="w", pady=3)
    e = tk.Entry(parent, font=FONT_ENTRY, bg=ENTRY_BG,
                 fg=TEXT, insertbackground=TEXT, relief="flat", width=22)
    e.grid(row=row, column=1, padx=(8, 0), pady=3)
    return e

# HELPER FUNCTION - CREATE TABLE
def make_table(parent, cols, widths):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True)
    tree = ttk.Treeview(frame, columns=cols, show="headings")
    for col, w in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")
    tree.tag_configure("even", background="#1e293b")
    tree.tag_configure("odd",  background="#172032")
    tree.tag_configure("low",  background="#450a0a", foreground="#fca5a5")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tree
# TAB 1 - MEDICINES

tab1 = tk.Frame(notebook, bg=BG)
notebook.add(tab1, text="Medicines")

left1 = tk.Frame(tab1, bg=BG, width=280)
left1.pack(side="left", fill="y", padx=(8,8), pady=8)
left1.pack_propagate(False)
right1 = tk.Frame(tab1, bg=BG)
right1.pack(side="left", fill="both", expand=True, pady=8)

# ADD MEDICINE FORM
add_card = make_card(left1, "Add Medicine")
add_card.pack(fill="x", pady=(0,8))
e_name    = make_entry(add_card, "Name",        0)
e_company = make_entry(add_card, "Company",     1)
e_price   = make_entry(add_card, "Price",       2)
e_stock   = make_entry(add_card, "Stock",       3)
e_expiry  = make_entry(add_card, "Expiry Date", 4)
e_supid   = make_entry(add_card, "Supplier ID", 5)
tk.Label(add_card, text="(YYYY-MM-DD)", font=("Courier New", 8),
         bg=CARD, fg=SUBTEXT).grid(row=4, column=1, sticky="e")

# ADD MEDICINE FUNCTION - runs INSERT query
def add_medicine():
    try:
        sql = "INSERT INTO medicines (name, company, price, stock, expiry_date, Supplier_Id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (e_name.get(), e_company.get(), float(e_price.get()),
                  int(e_stock.get()), e_expiry.get(),
                  int(e_supid.get()) if e_supid.get() else None)
        cursor.execute(sql, values)
        conn.commit()
        for e in [e_name, e_company, e_price, e_stock, e_expiry, e_supid]:
            e.delete(0, tk.END)
        messagebox.showinfo("Success", "Medicine added successfully!")
        view_medicines()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

make_button(add_card, "ADD MEDICINE", SUCCESS, add_medicine).grid(
    row=6, column=0, columnspan=2, pady=(8,0), sticky="ew")

# UPDATE STOCK FORM
upd_card = make_card(left1, "Update Stock")
upd_card.pack(fill="x", pady=(0,8))
e_uid    = make_entry(upd_card, "Medicine ID", 0)
e_ustock = make_entry(upd_card, "New Stock",   1)

# UPDATE STOCK FUNCTION - runs UPDATE query
def update_stock():
    try:
        sql = "UPDATE medicines SET stock = %s WHERE id = %s"
        cursor.execute(sql, (int(e_ustock.get()), int(e_uid.get())))
        conn.commit()
        e_uid.delete(0, tk.END)
        e_ustock.delete(0, tk.END)
        messagebox.showinfo("Success", "Stock updated successfully!")
        view_medicines()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

make_button(upd_card, "UPDATE STOCK", WARNING, update_stock).grid(
    row=2, column=0, columnspan=2, pady=(8,0), sticky="ew")

# DELETE MEDICINE FORM
del_card = make_card(left1, "Delete Medicine")
del_card.pack(fill="x")
e_did = make_entry(del_card, "Medicine ID", 0)

# DELETE MEDICINE FUNCTION - runs DELETE query
def delete_medicine():
    try:
        mid = int(e_did.get())
        if messagebox.askyesno("Confirm", "Are you sure you want to delete?"):
            cursor.execute("DELETE FROM medicines WHERE id = %s", (mid,))
            conn.commit()
            e_did.delete(0, tk.END)
            messagebox.showinfo("Success", "Medicine deleted successfully!")
            view_medicines()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

make_button(del_card, "DELETE", DANGER, delete_medicine).grid(
    row=1, column=0, columnspan=2, pady=(8,0), sticky="ew")

# MEDICINE TABLE - uses JOIN query to show supplier info
table_card = make_card(right1, "Medicine Inventory with Supplier Details")
table_card.pack(fill="both", expand=True)
cols1 = ("ID", "Medicine Name", "Company", "Price", "Stock", "Expiry Date", "Supplier Name", "Contact No")
widths1 = [40, 120, 100, 70, 60, 100, 110, 100]
tree1 = make_table(table_card, cols1, widths1)

# VIEW MEDICINES FUNCTION - runs SELECT with JOIN query
def view_medicines():
    for row in tree1.get_children():
        tree1.delete(row)
    # JOIN query - combines medicines and supplier tables
    sql = """SELECT m.id, m.name, m.company, m.price, m.stock,
                    m.expiry_date,
                    CONCAT(s.First_Name, ' ', s.Last_Name),
                    s.Contact_No
             FROM medicines m
             LEFT JOIN supplier s ON m.Supplier_Id = s.Supplier_Id"""
    cursor.execute(sql)
    rows = cursor.fetchall()
    for i, row in enumerate(rows):
        tag = "even" if i % 2 == 0 else "odd"
        # Highlight red if stock is less than 10
        if row[4] is not None and row[4] < 10:
            tag = "low"
        tree1.insert("", tk.END, values=row, tags=(tag,))

view_medicines()
# TAB 2 - CUSTOMERS

tab2 = tk.Frame(notebook, bg=BG)
notebook.add(tab2, text="Customers")

left2 = tk.Frame(tab2, bg=BG, width=280)
left2.pack(side="left", fill="y", padx=(8,8), pady=8)
left2.pack_propagate(False)
right2 = tk.Frame(tab2, bg=BG)
right2.pack(side="left", fill="both", expand=True, pady=8)

cust_card = make_card(left2, "Add Customer")
cust_card.pack(fill="x")
e_cfname = make_entry(cust_card, "First Name",  0)
e_cmname = make_entry(cust_card, "Middle Name", 1)
e_clname = make_entry(cust_card, "Last Name",   2)
e_cphone = make_entry(cust_card, "Phone",       3)

# ADD CUSTOMER FUNCTION - runs INSERT query
def add_customer():
    try:
        sql = "INSERT INTO customer (First_Name, Middle_Name, Last_Name, Phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (e_cfname.get(), e_cmname.get(),
                             e_clname.get(), e_cphone.get()))
        conn.commit()
        for e in [e_cfname, e_cmname, e_clname, e_cphone]:
            e.delete(0, tk.END)
        messagebox.showinfo("Success", "Customer added successfully!")
        view_customers()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

make_button(cust_card, "ADD CUSTOMER", SUCCESS, add_customer).grid(
    row=4, column=0, columnspan=2, pady=(8,0), sticky="ew")

cust_table = make_card(right2, "Customer List")
cust_table.pack(fill="both", expand=True)
cols2 = ("ID", "First Name", "Middle Name", "Last Name", "Phone")
widths2 = [50, 130, 130, 130, 120]
tree2 = make_table(cust_table, cols2, widths2)

# VIEW CUSTOMERS FUNCTION - runs SELECT query
def view_customers():
    for row in tree2.get_children():
        tree2.delete(row)
    cursor.execute("SELECT * FROM customer")
    for i, row in enumerate(cursor.fetchall()):
        tag = "even" if i % 2 == 0 else "odd"
        tree2.insert("", tk.END, values=row, tags=(tag,))

view_customers()
# TAB 3 - SUPPLIERS

tab3 = tk.Frame(notebook, bg=BG)
notebook.add(tab3, text="Suppliers")

left3 = tk.Frame(tab3, bg=BG, width=280)
left3.pack(side="left", fill="y", padx=(8,8), pady=8)
left3.pack_propagate(False)
right3 = tk.Frame(tab3, bg=BG)
right3.pack(side="left", fill="both", expand=True, pady=8)

sup_card = make_card(left3, "Add Supplier")
sup_card.pack(fill="x")
e_sfname = make_entry(sup_card, "First Name",  0)
e_smname = make_entry(sup_card, "Middle Name", 1)
e_slname = make_entry(sup_card, "Last Name",   2)
e_sphone = make_entry(sup_card, "Contact No",  3)

# ADD SUPPLIER FUNCTION - runs INSERT query
def add_supplier():
    try:
        sql = "INSERT INTO supplier (First_Name, Middle_Name, Last_Name, Contact_No) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (e_sfname.get(), e_smname.get(),
                             e_slname.get(), e_sphone.get()))
        conn.commit()
        for e in [e_sfname, e_smname, e_slname, e_sphone]:
            e.delete(0, tk.END)
        messagebox.showinfo("Success", "Supplier added successfully!")
        view_suppliers()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

make_button(sup_card, "ADD SUPPLIER", SUCCESS, add_supplier).grid(
    row=4, column=0, columnspan=2, pady=(8,0), sticky="ew")

sup_table = make_card(right3, "Supplier List")
sup_table.pack(fill="both", expand=True)
cols3 = ("ID", "First Name", "Middle Name", "Last Name", "Contact No")
widths3 = [50, 130, 130, 130, 120]
tree3 = make_table(sup_table, cols3, widths3)

# VIEW SUPPLIERS FUNCTION - runs SELECT query
def view_suppliers():
    for row in tree3.get_children():
        tree3.delete(row)
    cursor.execute("SELECT * FROM supplier")
    for i, row in enumerate(cursor.fetchall()):
        tag = "even" if i % 2 == 0 else "odd"
        tree3.insert("", tk.END, values=row, tags=(tag,))

view_suppliers()
# TAB 4 - SALES

tab4 = tk.Frame(notebook, bg=BG)
notebook.add(tab4, text="Sales")

left4 = tk.Frame(tab4, bg=BG, width=280)
left4.pack(side="left", fill="y", padx=(8,8), pady=8)
left4.pack_propagate(False)
right4 = tk.Frame(tab4, bg=BG)
right4.pack(side="left", fill="both", expand=True, pady=8)

sale_card = make_card(left4, "Add Sale")
sale_card.pack(fill="x")
e_scid    = make_entry(sale_card, "Customer ID",  0)
e_sdate   = make_entry(sale_card, "Sale Date",    1)
e_samount = make_entry(sale_card, "Total Amount", 2)
tk.Label(sale_card, text="(YYYY-MM-DD)", font=("Courier New", 8),
         bg=CARD, fg=SUBTEXT).grid(row=1, column=1, sticky="e")

# ADD SALE FUNCTION - runs INSERT query
def add_sale():
    try:
        sql = "INSERT INTO sales (Customer_Id, Sale_Date, Total_Amount) VALUES (%s, %s, %s)"
        cursor.execute(sql, (int(e_scid.get()), e_sdate.get(),
                             float(e_samount.get())))
        conn.commit()
        for e in [e_scid, e_sdate, e_samount]:
            e.delete(0, tk.END)
        messagebox.showinfo("Success", "Sale recorded successfully!")
        view_sales()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

make_button(sale_card, "ADD SALE", SUCCESS, add_sale).grid(
    row=3, column=0, columnspan=2, pady=(8,0), sticky="ew")

sale_table = make_card(right4, "Sales Records")
sale_table.pack(fill="both", expand=True)
cols4 = ("Sale ID", "Customer ID", "Sale Date", "Total Amount")
widths4 = [80, 120, 150, 180]
tree4 = make_table(sale_table, cols4, widths4)

# VIEW SALES FUNCTION - runs SELECT query
def view_sales():
    for row in tree4.get_children():
        tree4.delete(row)
    cursor.execute("SELECT * FROM sales")
    for i, row in enumerate(cursor.fetchall()):
        tag = "even" if i % 2 == 0 else "odd"
        tree4.insert("", tk.END, values=row, tags=(tag,))

view_sales()

# STATUS BAR
tk.Label(root, text="Red highlighted rows = Low Stock (less than 10) | Data stored in MySQL pharmacy_db",
         font=("Courier New", 9), bg=CARD, fg=SUBTEXT,
         anchor="w", padx=12).pack(fill="x", side="bottom")

# RUN THE WINDOW
root.mainloop()