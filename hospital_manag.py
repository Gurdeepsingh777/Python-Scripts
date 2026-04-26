import sqlite3
from tkinter import *
from tkinter import ttk

db='hospital.db'

def init_creatdb():
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS hsptl(
                id INTEGER,
                name TEXT,
                addr TEXT,
                room INTEGER,
                admit_time DOUBLE,
                discharge_time DOUBLE
                ) ''')
    conn.commit()
    conn.close()

class PetiontManage:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Hospital Management")
        self.root.geometry("1200x600")

        self.name=StringVar()
        self.pid=IntVar()
        self.add=StringVar()
        self.room=IntVar()
        self.admit=DoubleVar()
        self.discharge=DoubleVar()
        self.search=StringVar()
        self.pid.set(1)

        header=Label(root,text="PATIENT MANAGEMENT",font=("Arial",22,'bold'),bg='#2c3e50',fg='white')
        header.pack(fill=X)

        fram1 = Frame(root,bd=3,relief=RIDGE)
        fram1.place(x=20,y=90,width=350,height=500)

        Label(fram1,text="Patient Id").pack(anchor=W,pady=10,fill=X)
        Entry(fram1,textvariable=self.pid).pack(fill=X,padx=30,pady=5)

        Label(fram1,text="Patient Name").pack(anchor=W,pady=10,fill=X)
        Entry(fram1,textvariable=self.name).pack(fill=X,padx=30,pady=5)

        Label(fram1,text="Address").pack(fill=X,pady=10)
        Entry(fram1,textvariable=self.add).pack(fill=X,padx=30)

        Label(fram1,text="Room No").pack(fill=X,pady=10)
        Entry(fram1,textvariable=self.room).pack(fill=X,padx=30)

        Label(fram1,text="Admit-Time").pack(fill=X,pady=10)
        Entry(fram1,textvariable=self.admit).pack(fill=X,padx=30)

        Label(fram1,text="Discharge-Time").pack(fill=X,pady=10)
        Entry(fram1,textvariable=self.discharge).pack(fill=X,padx=30)


        
        btnfrm=Frame(fram1)
        btnfrm.pack(pady=20)

        Button(btnfrm,text="Add",command=self.patientadd,bg="blue",fg="white").grid(row=0,column=0,padx=10,pady=20)
        Button(btnfrm,text="Delete",command=self.patientdel,bg="red",fg="black").grid(row=0,column=1,padx=10,pady=20)
        Button(btnfrm,text="Clear",command=self.clear,bg="lightgreen",fg="black").grid(row=0,column=2,padx=10,pady=20)


      


        fram2 = Frame(root,bd=3,relief=RIDGE)
        fram2.place(x=450,y=90,width=700,height=450)

        btnfrm1=Frame(fram2)
        btnfrm1.pack()

        Entry(btnfrm1,textvariable=self.search).pack(pady=20,padx=10,side=LEFT)
        Button(btnfrm1,text="Search",command=self.namesearch).pack(pady=20,padx=10,side=RIGHT)

        cols = ("id","Patient_Name","Address","Room","Admit_Time","Discharge_Time")

        self.table=ttk.Treeview(fram2,columns=cols,show="headings")
        for i in cols:
            self.table.heading(i,text=i)
        self.table.pack(fill=BOTH,expand=1)

        self.display()


    def patientadd(self):
            conn=sqlite3.connect(db)
            cur=conn.cursor()

            cur.execute("INSERT INTO hsptl(id,name,addr,room,admit_time,discharge_time)VALUES(?,?,?,?,?,?)",
                        (self.pid.get(),
                         self.name.get(),
                         self.add.get(),
                         self.room.get(),
                         self.admit.get(),
                         self.discharge.get()))
            conn.commit()
            conn.close()

            self.display()

    def display(self):
            data=self.table.get_children()
            for x in data:
                  self.table.delete(x)
            conn = sqlite3.connect(db)
            cur=conn.cursor()
            cur.execute("SELECT * FROM hsptl")
            hospitaldb = cur.fetchall()
            for row in hospitaldb:
                  self.table.insert("",END,values=row)
            conn.close()



    def patientdel(self):
            conn=sqlite3.connect(db)
            cur=conn.cursor()
            cur.execute('DELETE FROM hsptl WHERE name=?',(self.name.get(),))

            conn.commit()
            conn.close()
            self.display()
            
            

    def namesearch(self):
            conn=sqlite3.connect(db)
            cur=conn.cursor()
            cur.execute("SELECT * FROM hsptl WHERE name LIKE ?",('%'+self.search.get()+'%',))
            row=cur.fetchall()
            fdata=self.table.get_children()
            for x in fdata:
                  self.table.delete(x)
            for r in row:
                  self.table.insert("",END,values=r)
            conn.close()

    
    def clear(self):
          self.pid.set("")
          self.name.set("")
          self.add.set("")
          self.admit.set("")
          self.room.set("")
          self.discharge.set("")
          


root=Tk()
init_creatdb()
app=PetiontManage(root)



root.mainloop()
