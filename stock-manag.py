import sqlite3
import csv
from tkinter import *
from tkinter import ttk, messagebox

DB="pro_stock.db"

# ---------------- DATABASE ----------------
def init_db():
 
    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    qty INTEGER,
    price REAL,
    category TEXT)
    """)

    conn.commit()
    conn.close()


# ---------------- LOGIN WINDOW ----------------
class Login:

    def __init__(self,root):

        self.root=root
        self.root.title("Login - Inventory System")
        self.root.geometry("400x250")

        Label(root,text="Login",font=("Arial",20,"bold")).pack(pady=20)

        self.user=StringVar()
        self.passw=StringVar()

        Label(root,text="Username").pack()
        Entry(root,textvariable=self.user).pack()

        Label(root,text="Password").pack()
        Entry(root,textvariable=self.passw,show="*").pack()

        Button(root,text="Login",command=self.login,width=15,bg="green",fg="white").pack(pady=20)

    def login(self):

        if self.user.get()=="Gurdeep" and self.passw.get()=="1234":

            self.root.destroy()
            main()

        else:

            messagebox.showerror("Error","Invalid Login")


# ---------------- MAIN APP ----------------
class StockSystem:

    def __init__(self,root):

        self.root=root
        self.root.title("Pro Inventory Manager v3.0")
        self.root.geometry("1000x600")

        self.dark=False

        # Variables
        self.name_var=StringVar()
        self.qty_var=IntVar()
        self.price_var=DoubleVar()
        self.cat_var=StringVar()
        self.search_var=StringVar()

        # ---------- MENU ----------
        menu=Menu(root)
        root.config(menu=menu)

        file_menu=Menu(menu,tearoff=0)
        menu.add_cascade(label="File",menu=file_menu)

        file_menu.add_command(label="Export CSV",command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=root.quit)

        view_menu=Menu(menu,tearoff=0)
        menu.add_cascade(label="View",menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode",command=self.toggle_theme)

        # ---------- HEADER ----------
        Label(root,
        text="📦 PROFESSIONAL STOCK MANAGEMENT",
        font=("Arial",22,"bold"),
        bg="#2c3e50",
        fg="white").pack(fill=X)

        # ---------- ENTRY FRAME ----------
        frame=Frame(root,bd=3,relief=RIDGE)
        frame.place(x=20,y=80,width=300,height=420)

        Label(frame,text="Product Name").pack(anchor=W,padx=20)
        Entry(frame,textvariable=self.name_var).pack(fill=X,padx=20,pady=5)

        Label(frame,text="Quantity").pack(anchor=W,padx=20)
        Entry(frame,textvariable=self.qty_var).pack(fill=X,padx=20,pady=5)

        Label(frame,text="Price").pack(anchor=W,padx=20)
        Entry(frame,textvariable=self.price_var).pack(fill=X,padx=20,pady=5)

        Label(frame,text="Category").pack(anchor=W,padx=20)

        cat_box=ttk.Combobox(frame,textvariable=self.cat_var,
        values=["Electronics","Clothing","Food","Other"])
        cat_box.pack(fill=X,padx=20,pady=5)

        # Buttons
        btn=Frame(frame)
        btn.pack(pady=20)

        Button(btn,text="Add",command=self.add_data,bg="green",fg="white").grid(row=0,column=0,padx=5)
        Button(btn,text="Update",command=self.update_data,bg="blue",fg="white").grid(row=0,column=1)
        Button(btn,text="Delete",command=self.delete_data,bg="red",fg="white").grid(row=1,column=0,pady=10)
        Button(btn,text="Clear",command=self.clear_fields).grid(row=1,column=1)

        # ---------- TABLE ----------
        table_frame=Frame(root)
        table_frame.place(x=350,y=80,width=620,height=420)

        Entry(table_frame,textvariable=self.search_var).pack(pady=10)
        Button(table_frame,text="Search",command=self.search_data).pack()

        cols=("id","name","qty","price","cat")

        self.table=ttk.Treeview(table_frame,columns=cols,show="headings")

        for c in cols:
            self.table.heading(c,text=c)

        self.table.pack(fill=BOTH,expand=1)

        self.table.bind("<ButtonRelease-1>",self.select_row)

        self.display()

    # ---------- DATABASE ----------
    def db(self):
        return sqlite3.connect(DB)

    # ---------- ADD ----------
    def add_data(self):

        conn=self.db()
        cur=conn.cursor()

        cur.execute("INSERT INTO inventory(name,qty,price,category) VALUES(?,?,?,?)",
        (self.name_var.get(),
        self.qty_var.get(),
        self.price_var.get(),
        self.cat_var.get()))

        conn.commit()
        conn.close()

        self.display()

    # ---------- DISPLAY ----------
    def display(self):

        for i in self.table.get_children():
            self.table.delete(i)

        conn=self.db()
        cur=conn.cursor()

        cur.execute("SELECT * FROM inventory")

        for row in cur.fetchall():
            self.table.insert("",END,values=row)

        conn.close()

    # ---------- SELECT ----------
    def select_row(self,ev):

        row=self.table.item(self.table.focus())["values"]

        if row:

            self.selected=row[0]

            self.name_var.set(row[1])
            self.qty_var.set(row[2])
            self.price_var.set(row[3])
            self.cat_var.set(row[4])

    # ---------- DELETE ----------
    def delete_data(self):

        conn=self.db()
        cur=conn.cursor()

        cur.execute("DELETE FROM inventory WHERE id=?",(self.selected,))

        conn.commit()
        conn.close()

        self.display()

    # ---------- UPDATE ----------
    def update_data(self):

        conn=self.db()
        cur=conn.cursor()

        cur.execute("""UPDATE inventory SET
        name=?,qty=?,price=?,category=? WHERE id=?""",

        (self.name_var.get(),
        self.qty_var.get(),
        self.price_var.get(),
        self.cat_var.get(),
        self.selected))

        conn.commit()
        conn.close()

        self.display()

    # ---------- SEARCH ----------
    def search_data(self):

        conn=self.db()
        cur=conn.cursor()

        cur.execute("SELECT * FROM inventory WHERE name LIKE ?",
        ('%'+self.search_var.get()+'%',))

        rows=cur.fetchall()

        for i in self.table.get_children():
            self.table.delete(i)

        for r in rows:
            self.table.insert("",END,values=r)

    # ---------- CLEAR ----------
    def clear_fields(self):

        self.name_var.set("")
        self.qty_var.set("")
        self.price_var.set("")
        self.cat_var.set("")

    # ---------- EXPORT ----------
    def export_csv(self):

        conn=self.db()
        cur=conn.cursor()

        cur.execute("SELECT * FROM inventory")

        rows=cur.fetchall()

        with open("inventory_export.csv","w",newline="") as f:

            writer=csv.writer(f)
            writer.writerow(["ID","Name","Qty","Price","Category"])
            writer.writerows(rows)

        messagebox.showinfo("Export","Data exported to CSV")

    # ---------- DARK MODE ----------
    def toggle_theme(self):

        if self.dark:

            self.root.configure(bg="white")
            self.dark=False

        else:

            self.root.configure(bg="#2c2c2c")
            self.dark=True


# ---------------- MAIN ----------------
def main():

    root=Tk()
    app=StockSystem(root)
    root.mainloop()


if __name__=="__main__":

    init_db()

    root=Tk()
    Login(root)
    root.mainloop()