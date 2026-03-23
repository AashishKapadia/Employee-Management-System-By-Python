from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector as mysql

conn = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="employee_db",
    port=3306
)

cursor = conn.cursor()


# Center Display

def center_window(win, width, height):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


# Login display

def login():

    login_win = Toplevel()
    login_win.title("🔐 Login")
    login_win.resizable(False, False)
    center_window(login_win, 320, 230)

    Label(login_win, text="Username", font=("Arial", 12)).pack(pady=5)
    username_entry = Entry(login_win, font=("Arial", 11), width=25)
    username_entry.pack()

    Label(login_win, text="Password", font=("Arial", 12)).pack(pady=5)
    password_entry = Entry(login_win, show="*", font=("Arial", 11), width=25)
    password_entry.pack()

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        cursor.execute(
            "SELECT * FROM employees WHERE usrename=%s AND password=%s",
            (username, password)
        )
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login Successful")
            login_win.destroy()
            main_menu()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    Button(login_win, text="Login", bg="blue", fg="white",
           font=("Arial", 11), width=15, command=submit_login).pack(pady=15)


# Register display

def register():

    win = Toplevel()
    win.title("📝 Register Employee")
    win.resizable(False, False)
    center_window(win, 520, 640)

    fields = [
        ("Employee ID", 0), ("Username", 1), ("Name", 2), ("Age", 3),
        ("Date of Birth (YYYY-MM-DD)", 5), ("Address", 6), ("Blood Type", 7),
        ("Phone Number", 8), ("Salary", 9), ("Emergency Contact", 10),
        ("Bank Account", 11), ("Aadhar", 12), ("PAN", 13),
        ("Password", 14), ("Confirm Password", 15), ("Date of Joining (YYYY-MM-DD)", 16)
    ]

    entries = {}
    for label_text, row in fields:
        Label(win, text=label_text).grid(row=row, column=0, padx=10, pady=4, sticky="e")
        show = "*" if "Password" in label_text else ""
        e = Entry(win, show=show, width=28)
        e.grid(row=row, column=1, padx=5)
        entries[row] = e

    E0, E1, E2, E3 = entries[0], entries[1], entries[2], entries[3]
    E5, E6, E7, E8 = entries[5], entries[6], entries[7], entries[8]
    E9, E10, E11, E12 = entries[9], entries[10], entries[11], entries[12]
    E13, E14, E15, E16 = entries[13], entries[14], entries[15], entries[16]

    Label(win, text="Gender").grid(row=4, column=0, padx=10, pady=4, sticky="e")
    gender = StringVar(value="Male")
    Radiobutton(win, text="Male", variable=gender, value="Male").grid(row=4, column=1, sticky="w")
    Radiobutton(win, text="Female", variable=gender, value="Female").grid(row=4, column=1)
    Radiobutton(win, text="Other", variable=gender, value="Other").grid(row=4, column=1, sticky="e")

    def submit_register():
        if E14.get() != E15.get():
            messagebox.showerror("Error", "Passwords do not match")
            return

        data = (
            E0.get(), E1.get(), E2.get(), E3.get(), gender.get(),
            E5.get(), E6.get(), E7.get(), E8.get(), E9.get(),
            E10.get(), E11.get(), E12.get(), E13.get(),
            E14.get(), E16.get()
        )

        cursor.execute(
            "INSERT INTO employees(Employee_ID,usrename,Emp_Name,Emp_Age,Emp_Gender,"
            "Emp_DOB,Emp_Address,Emp_Blood,Emp_PhoneNo,Emp_Salary,Emp_EMGNo,"
            "Emp_Account,Emp_AadharCard,Emp_PanCard,password,EMP_DOJ) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            data
        )
        conn.commit()
        messagebox.showinfo("Success", "Employee Registered Successfully!")
        win.destroy()

    Button(win, text="✅ Register", bg="green", fg="white",
           font=("Arial", 11), command=submit_register).grid(row=17, column=0, columnspan=2, pady=20)


# View all employee

def view_employees():
    win = Toplevel()
    win.title("👥 All Employees")
    center_window(win, 900, 420)

    columns = ("ID", "Username", "Name", "Age", "Gender", "Phone", "Salary", "DOJ")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=105, anchor="center")

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)

    cursor.execute(
        "SELECT Employee_ID, usrename, Emp_Name, Emp_Age, Emp_Gender, "
        "Emp_PhoneNo, Emp_Salary, EMP_DOJ FROM employees"
    )
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", END, values=row)

    if not rows:
        Label(win, text="No employees found.", font=("Arial", 13), fg="gray").pack(pady=30)


# Search Employee

def search_employee():
    win = Toplevel()
    win.title("🔍 Search Employee")
    win.resizable(False, False)
    center_window(win, 560, 480)

    Label(win, text="Search by Employee ID or Name:", font=("Arial", 11)).pack(pady=10)
    search_entry = Entry(win, font=("Arial", 11), width=30)
    search_entry.pack()

    result_frame = Frame(win)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Name", "Age", "Gender", "Phone", "Salary")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=85, anchor="center")
    tree.pack(fill="both", expand=True)

    def do_search():
        for row in tree.get_children():
            tree.delete(row)

        term = search_entry.get().strip()
        cursor.execute(
            "SELECT Employee_ID, Emp_Name, Emp_Age, Emp_Gender, Emp_PhoneNo, Emp_Salary "
            "FROM employees WHERE Employee_ID=%s OR Emp_Name LIKE %s",
            (term, f"%{term}%")
        )
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", END, values=row)
        if not rows:
            messagebox.showinfo("Not Found", "No employee found matching your search.")

    Button(win, text="🔍 Search", bg="steelblue", fg="white",
           font=("Arial", 11), command=do_search).pack(pady=8)


# Update Employee

def update_employee():
    win = Toplevel()
    win.title("✏️ Update Employee")
    win.resizable(False, False)
    center_window(win, 460, 480)

    Label(win, text="Enter Employee ID to Update:", font=("Arial", 11)).pack(pady=8)
    id_entry = Entry(win, font=("Arial", 11), width=20)
    id_entry.pack()

    form_frame = Frame(win)
    form_frame.pack(pady=10)

    update_fields = [
        ("Name", "Emp_Name"), ("Age", "Emp_Age"), ("Address", "Emp_Address"),
        ("Phone Number", "Emp_PhoneNo"), ("Salary", "Emp_Salary"),
        ("Emergency Contact", "Emp_EMGNo"), ("Password", "password")
    ]

    entries = {}
    for i, (label, col) in enumerate(update_fields):
        Label(form_frame, text=label, anchor="e", width=18).grid(row=i, column=0, padx=8, pady=4)
        show = "*" if col == "password" else ""
        e = Entry(form_frame, show=show, width=25)
        e.grid(row=i, column=1, padx=5, pady=4)
        entries[col] = e

    def load_employee():
        emp_id = id_entry.get().strip()
        cursor.execute("SELECT * FROM employees WHERE Employee_ID=%s", (emp_id,))
        row = cursor.fetchone()
        if not row:
            messagebox.showerror("Not Found", "Employee ID not found.")
            return
        col_names = [desc[0] for desc in cursor.description]
        data = dict(zip(col_names, row))
        for col, entry in entries.items():
            entry.delete(0, END)
            entry.insert(0, data.get(col, ""))

    def save_update():
        emp_id = id_entry.get().strip()
        for col, entry in entries.items():
            val = entry.get().strip()
            if val:
                cursor.execute(
                    f"UPDATE employees SET {col}=%s WHERE Employee_ID=%s",
                    (val, emp_id)
                )
        conn.commit()
        messagebox.showinfo("Success", "Employee updated successfully!")
        win.destroy()

    Button(win, text="Load Employee", bg="steelblue", fg="white",
           font=("Arial", 10), command=load_employee).pack(pady=4)
    Button(win, text="💾 Save Changes", bg="green", fg="white",
           font=("Arial", 11), command=save_update).pack(pady=8)


# Delete Employee 

def delete_employee():
    win = Toplevel()
    win.title("🗑️ Delete Employee")
    win.resizable(False, False)
    center_window(win, 360, 200)

    Label(win, text="Enter Employee ID to Delete:", font=("Arial", 11)).pack(pady=15)
    id_entry = Entry(win, font=("Arial", 11), width=22)
    id_entry.pack()

    def do_delete():
        emp_id = id_entry.get().strip()
        cursor.execute("SELECT Emp_Name FROM employees WHERE Employee_ID=%s", (emp_id,))
        row = cursor.fetchone()
        if not row:
            messagebox.showerror("Not Found", "Employee ID not found.")
            return
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete employee '{row[0]}'? This cannot be undone."
        )
        if confirm:
            cursor.execute("DELETE FROM employees WHERE Employee_ID=%s", (emp_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Employee deleted successfully.")
            win.destroy()

    Button(win, text="🗑️ Delete", bg="red", fg="white",
           font=("Arial", 11), command=do_delete).pack(pady=15)


# main menu

def main_menu():
    menu = Toplevel()
    menu.title("🏢 Employee Management System")
    menu.resizable(False, False)
    center_window(menu, 420, 380)

    Label(menu, text="Employee Management System",
          font=("Arial", 17, "bold")).pack(pady=20)

    btn_cfg = {"width": 25, "font": ("Arial", 11), "pady": 4}

    Button(menu, text="👥 View All Employees", bg="#2196F3", fg="white",
           command=view_employees, **btn_cfg).pack(pady=6)
    Button(menu, text="🔍 Search Employee", bg="#9C27B0", fg="white",
           command=search_employee, **btn_cfg).pack(pady=6)
    Button(menu, text="✏️ Update Employee", bg="#FF9800", fg="white",
           command=update_employee, **btn_cfg).pack(pady=6)
    Button(menu, text="🗑️ Delete Employee", bg="#F44336", fg="white",
           command=delete_employee, **btn_cfg).pack(pady=6)
    Button(menu, text="❌ Exit", bg="#607D8B", fg="white",
           command=menu.destroy, **btn_cfg).pack(pady=6)

    # Status bar
    status = Label(menu, text="Logged in  |  Employee Management System v2.0",
                   bd=1, relief=SUNKEN, anchor="w", font=("Arial", 8), fg="gray")
    status.pack(side=BOTTOM, fill=X)


# main Display

win = Tk()
win.title("🏢 Employee Management System")
win.resizable(False, False)
center_window(win, 400, 300)

Label(win, text="Employee Management System",
      font=("Arial", 18, "bold")).pack(pady=30)

Button(win, text="🔐 Login", width=20, bg="green", fg="white",
       font=("Arial", 11), command=login).pack(pady=8)
Button(win, text="📝 Register", width=20, bg="orange", fg="white",
       font=("Arial", 11), command=register).pack(pady=8)
Button(win, text="❌ Exit", width=20, bg="red", fg="white",
       font=("Arial", 11), command=win.destroy).pack(pady=8)

# Status bar on main window
Label(win, text="Employee Management System v2.0",
      bd=1, relief=SUNKEN, anchor="w", font=("Arial", 8), fg="gray").pack(side=BOTTOM, fill=X)

win.mainloop()