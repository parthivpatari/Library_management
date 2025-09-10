import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import date, timedelta

# --- Database Connection ---
conn = psycopg2.connect(
    dbname="librarydb",
    user="add your user of postgre",  #add your postgre username
    password="",  # Set your password
    host="localhost"
)
cursor = conn.cursor()


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        # --- Center and resize ---
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        w, h = int(screen_width*0.75), int(screen_height*0.8)
        x, y = (screen_width - w)//2, (screen_height - h)//2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.resizable(True, True)

        tk.Label(root, text="Library Management System", font=("Arial", 28, "bold")).pack(pady=15)

        # --- Tabs ---
        self.tabControl = ttk.Notebook(root)
        self.tab_students = ttk.Frame(self.tabControl)
        self.tab_books = ttk.Frame(self.tabControl)
        self.tab_staff = ttk.Frame(self.tabControl)
        self.tab_transactions = ttk.Frame(self.tabControl)
        self.tab_service = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_students, text='Students')
        self.tabControl.add(self.tab_books, text='Books')
        self.tabControl.add(self.tab_staff, text='Staff')
        self.tabControl.add(self.tab_transactions, text='Transactions')
        self.tabControl.add(self.tab_service, text='Customer Service')
        self.tabControl.pack(expand=1, fill="both")

        self.init_students_tab()
        self.init_books_tab()
        self.init_staff_tab()
        self.init_transactions_tab()
        self.init_service_tab()


    # ---------------- Students Tab ----------------
    def init_students_tab(self):
        frame = self.tab_students
        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.student_name = tk.Entry(frame)
        self.student_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Department").grid(row=1, column=0, padx=5, pady=5)
        self.student_dept = tk.Entry(frame)
        self.student_dept.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Admission Year").grid(row=2, column=0, padx=5, pady=5)
        self.student_year = tk.Entry(frame)
        self.student_year.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Student", command=self.add_student).grid(row=3, column=0, columnspan=2, pady=10)

        self.students_tree = ttk.Treeview(frame, columns=("ID", "Name", "Dept", "Year"), show='headings')
        for col in ("ID", "Name", "Dept", "Year"):
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150)
        self.students_tree.grid(row=4, column=0, columnspan=2, sticky='nsew')
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        self.load_students()

    def add_student(self):
        try:
            name = self.student_name.get()
            dept = self.student_dept.get()
            year = int(self.student_year.get())
            if not name:
                messagebox.showerror("Error", "Name required")
                return
            cursor.execute("INSERT INTO students (name, department, admission_year) VALUES (%s,%s,%s)",
                           (name, dept, year))
            conn.commit()
            self.load_students()
            messagebox.showinfo("Success", "Student added successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to add student: {e}")

    def load_students(self):
        for i in self.students_tree.get_children():
            self.students_tree.delete(i)
        cursor.execute("SELECT * FROM students ORDER BY student_id")
        for row in cursor.fetchall():
            self.students_tree.insert("", tk.END, values=row)


    # ---------------- Books Tab ----------------
    def init_books_tab(self):
        frame = self.tab_books
        tk.Label(frame, text="Title").grid(row=0, column=0, padx=5, pady=5)
        self.book_title = tk.Entry(frame)
        self.book_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Author").grid(row=1, column=0, padx=5, pady=5)
        self.book_author = tk.Entry(frame)
        self.book_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Category").grid(row=2, column=0, padx=5, pady=5)
        self.book_category = tk.Entry(frame)
        self.book_category.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Book", command=self.add_book).grid(row=3, column=0, columnspan=2, pady=10)

        self.books_tree = ttk.Treeview(frame, columns=("ID", "Title", "Author", "Category"), show='headings')
        for col in ("ID", "Title", "Author", "Category"):
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)
        self.books_tree.grid(row=4, column=0, columnspan=2, sticky='nsew')
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        self.load_books()

    def add_book(self):
        try:
            title = self.book_title.get()
            author = self.book_author.get()
            category = self.book_category.get()
            if not title:
                messagebox.showerror("Error", "Title required")
                return
            cursor.execute("INSERT INTO books (title, author, category) VALUES (%s,%s,%s)",
                           (title, author, category))
            conn.commit()
            self.load_books()
            messagebox.showinfo("Success", "Book added successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def load_books(self):
        for i in self.books_tree.get_children():
            self.books_tree.delete(i)
        cursor.execute("SELECT * FROM books ORDER BY book_id")
        for row in cursor.fetchall():
            self.books_tree.insert("", tk.END, values=row)


    # ---------------- Staff Tab ----------------
    def init_staff_tab(self):
        frame = self.tab_staff
        tk.Label(frame, text="Emp ID").grid(row=0, column=0, padx=5, pady=5)
        self.staff_emp = tk.Entry(frame)
        self.staff_emp.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
        self.staff_name = tk.Entry(frame)
        self.staff_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Role").grid(row=2, column=0, padx=5, pady=5)
        allowed_roles = ['Librarian', 'Assistant', 'Clerk', 'Professor', 'Teacher']
        self.staff_role = ttk.Combobox(frame, values=allowed_roles)
        self.staff_role.grid(row=2, column=1, padx=5, pady=5)
        self.staff_role.set(allowed_roles[0])

        tk.Label(frame, text="Department").grid(row=3, column=0, padx=5, pady=5)
        self.staff_dept = tk.Entry(frame)
        self.staff_dept.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Staff", command=self.add_staff).grid(row=4, column=0, columnspan=2, pady=10)

        self.staff_tree = ttk.Treeview(frame, columns=("ID", "Emp ID", "Name", "Role", "Dept"), show='headings')
        for col in ("ID", "Emp ID", "Name", "Role", "Dept"):
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=150)
        self.staff_tree.grid(row=5, column=0, columnspan=2, sticky='nsew')
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        self.load_staff()

    def add_staff(self):
        try:
            emp = self.staff_emp.get()
            name = self.staff_name.get()
            role = self.staff_role.get()
            dept = self.staff_dept.get()
            cursor.execute("INSERT INTO staff (emp_id, name, role, department) VALUES (%s,%s,%s,%s)",
                           (emp, name, role, dept))
            conn.commit()
            self.load_staff()
            messagebox.showinfo("Success", "Staff added successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to add staff: {e}")

    def load_staff(self):
        for i in self.staff_tree.get_children():
            self.staff_tree.delete(i)
        cursor.execute("SELECT * FROM staff ORDER BY staff_id")
        for row in cursor.fetchall():
            self.staff_tree.insert("", tk.END, values=row)


# ---------------- Transactions Tab ----------------
    def init_transactions_tab(self):
        frame = self.tab_transactions

        self.refresh_users_books()

        tk.Label(frame, text="Student").grid(row=0, column=0, padx=5, pady=5)
        self.trans_student = ttk.Combobox(frame, values=self.students_dropdown)
        self.trans_student.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Staff").grid(row=1, column=0, padx=5, pady=5)
        self.trans_staff = ttk.Combobox(frame, values=self.staff_dropdown)
        self.trans_staff.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Book to Issue").grid(row=2, column=0, padx=5, pady=5)
        self.trans_book = ttk.Combobox(frame, values=[])
        self.trans_book.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Book to Return").grid(row=3, column=0, padx=5, pady=5)
        self.return_book_dropdown = ttk.Combobox(frame, values=[])
        self.return_book_dropdown.grid(row=3, column=1, padx=5, pady=5)

        self.trans_student.bind("<<ComboboxSelected>>", self.update_issue_books)
        self.trans_staff.bind("<<ComboboxSelected>>", self.update_issue_books)
        self.trans_student.bind("<<ComboboxSelected>>", self.update_return_books)
        self.trans_staff.bind("<<ComboboxSelected>>", self.update_return_books)

        tk.Button(frame, text="Issue Book", command=self.issue_book).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Return Book", command=self.return_book).grid(row=5, column=0, columnspan=2, pady=5)

        self.trans_tree = ttk.Treeview(frame, columns=("ID", "Book ID", "Student ID", "Staff ID", "Issue Date", "Due Date", "Return Date"), show='headings')
        for col in ("ID", "Book ID", "Student ID", "Staff ID", "Issue Date", "Due Date", "Return Date"):
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=120)
        self.trans_tree.grid(row=6, column=0, columnspan=2, sticky='nsew')
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        self.load_transactions()


    # --- Transactions Functions ---
    def refresh_users_books(self):
        cursor.execute("SELECT student_id, name FROM students ORDER BY student_id")
        self.students_dropdown = [f"{sid} - {name}" for sid, name in cursor.fetchall()]
        cursor.execute("SELECT staff_id, name FROM staff ORDER BY staff_id")
        self.staff_dropdown = [f"{sid} - {name}" for sid, name in cursor.fetchall()]

    def update_issue_books(self, event=None):
        books = []
        selected_student = self.trans_student.get()
        selected_staff = self.trans_staff.get()
        if selected_student or selected_staff:
            cursor.execute("""
                SELECT book_id, title 
                FROM books 
                WHERE book_id NOT IN (SELECT book_id FROM transactions WHERE return_date IS NULL)
            """)
            books = cursor.fetchall()
        self.trans_book['values'] = [f"{bid} - {title}" for bid, title in books]
        self.trans_book.set('')

    def update_return_books(self, event=None):
        books = []
        selected_student = self.trans_student.get()
        selected_staff = self.trans_staff.get()
        if selected_student:
            student_id = int(selected_student.split(" - ")[0])
            cursor.execute("""
                SELECT b.book_id, b.title
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                WHERE t.student_id=%s AND t.return_date IS NULL
            """, (student_id,))
            books = cursor.fetchall()
        elif selected_staff:
            staff_id = int(selected_staff.split(" - ")[0])
            cursor.execute("""
                SELECT b.book_id, b.title
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                WHERE t.staff_id=%s AND t.return_date IS NULL
            """, (staff_id,))
            books = cursor.fetchall()
        self.return_book_dropdown['values'] = [f"{bid} - {title}" for bid, title in books]
        self.return_book_dropdown.set('')

    def issue_book(self):
        try:
            student = int(self.trans_student.get().split(" - ")[0]) if self.trans_student.get() else None
            staff = int(self.trans_staff.get().split(" - ")[0]) if self.trans_staff.get() else None
            book = int(self.trans_book.get().split(" - ")[0]) if self.trans_book.get() else None
            if not book:
                messagebox.showerror("Error", "Select a book to issue")
                return
            if not student and not staff:
                messagebox.showerror("Error", "Select either Student or Staff")
                return
            if student and staff:
                messagebox.showerror("Error", "Select only Student or Staff, not both")
                return
            today = date.today()
            due = today + timedelta(days=15)
            cursor.execute("""
                INSERT INTO transactions (book_id, student_id, staff_id, issue_date, due_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (book, student, staff, today, due))
            conn.commit()
            self.load_transactions()
            self.update_issue_books()
            self.update_return_books()
            messagebox.showinfo("Success", "Book issued successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to issue book: {e}")

    def return_book(self):
        try:
            book = int(self.return_book_dropdown.get().split(" - ")[0]) if self.return_book_dropdown.get() else None
            if not book:
                messagebox.showerror("Error", "Select a book to return")
                return
            today = date.today()
            cursor.execute("""
                UPDATE transactions
                SET return_date=%s
                WHERE book_id=%s AND return_date IS NULL
            """, (today, book))
            conn.commit()
            self.load_transactions()
            self.update_issue_books()
            self.update_return_books()
            messagebox.showinfo("Success", "Book returned successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to return book: {e}")

    def load_transactions(self):
        for i in self.trans_tree.get_children():
            self.trans_tree.delete(i)
        cursor.execute("SELECT * FROM transactions ORDER BY transaction_id")
        for row in cursor.fetchall():
            self.trans_tree.insert("", tk.END, values=row)


# ---------------- Customer Service Tab ----------------
    def init_service_tab(self):
        frame = self.tab_service
        cursor.execute("SELECT student_id, name FROM students ORDER BY student_id")
        students = cursor.fetchall()
        cursor.execute("SELECT staff_id, name FROM staff ORDER BY staff_id")
        staff_list = cursor.fetchall()
        cursor.execute("SELECT book_id, title FROM books ORDER BY book_id")
        books = cursor.fetchall()

        tk.Label(frame, text="Raised By (Student)").grid(row=0, column=0, padx=5, pady=5)
        self.cs_student = ttk.Combobox(frame, values=[f"{sid} - {name}" for sid, name in students])
        self.cs_student.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Raised By (Staff)").grid(row=1, column=0, padx=5, pady=5)
        self.cs_staff = ttk.Combobox(frame, values=[f"{sid} - {name}" for sid, name in staff_list])
        self.cs_staff.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Book").grid(row=2, column=0, padx=5, pady=5)
        self.cs_book = ttk.Combobox(frame, values=[f"{bid} - {title}" for bid, title in books])
        self.cs_book.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Issue Type").grid(row=3, column=0, padx=5, pady=5)
        self.issue_types = ['Damaged', 'Lost', 'Refund']
        self.cs_issue = ttk.Combobox(frame, values=self.issue_types)
        self.cs_issue.grid(row=3, column=1, padx=5, pady=5)
        self.cs_issue.set(self.issue_types[0])

        tk.Label(frame, text="Priority").grid(row=4, column=0, padx=5, pady=5)
        self.priority_options = ['Low', 'Medium', 'High']
        self.cs_priority = ttk.Combobox(frame, values=self.priority_options)
        self.cs_priority.grid(row=4, column=1, padx=5, pady=5)
        self.cs_priority.set(self.priority_options[1])

        tk.Button(frame, text="Raise Ticket", command=self.raise_ticket).grid(row=5, column=0, columnspan=2, pady=10)

        self.cs_tree = ttk.Treeview(frame, columns=("ID","Student","Staff","Book","Issue Type","Status","Priority","Date Raised"), show='headings')
        for col in ("ID","Student","Staff","Book","Issue Type","Status","Priority","Date Raised"):
            self.cs_tree.heading(col, text=col)
            self.cs_tree.column(col, width=120)
        self.cs_tree.grid(row=6, column=0, columnspan=2, sticky='nsew')
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        self.load_tickets()

    def raise_ticket(self):
        try:
            student = int(self.cs_student.get().split(" - ")[0]) if self.cs_student.get() else None
            staff = int(self.cs_staff.get().split(" - ")[0]) if self.cs_staff.get() else None
            book = int(self.cs_book.get().split(" - ")[0]) if self.cs_book.get() else None
            issue = self.cs_issue.get()
            priority = self.cs_priority.get()
            if not student and not staff:
                messagebox.showerror("Error", "Select either Student or Staff")
                return
            if student and staff:
                messagebox.showerror("Error", "Select only Student or Staff, not both")
                return
            today = date.today()
            cursor.execute("""
                INSERT INTO customer_service (student_id, staff_id, book_id, issue_type, status, priority, date_raised)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (student, staff, book, issue, "Open", priority, today))
            conn.commit()
            self.load_tickets()
            messagebox.showinfo("Success", "Ticket raised successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to raise ticket: {e}")

    def load_tickets(self):
        for i in self.cs_tree.get_children():
            self.cs_tree.delete(i)
        cursor.execute("SELECT * FROM customer_service ORDER BY ticket_id")
        for row in cursor.fetchall():
            self.cs_tree.insert("", tk.END, values=row)


# ---------------- Run App ----------------
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
