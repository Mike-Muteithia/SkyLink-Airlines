"""
SACCO Financial Management System
Technology: Python + Tkinter + SQLite

GUI version of the supplied console SACCO system.
Features:
- Member registration, viewing, searching, updating and deleting
- Savings deposits, withdrawals and balances
- Loan applications, approval/rejection, repayments and balances
- Transaction history
- Financial reports
"""

import sqlite3
from datetime import datetime
from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import ttk, messagebox


DB_NAME = "sacco.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS members (
                member_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                registration_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS savings (
                saving_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL CHECK(
                    transaction_type IN ('DEPOSIT', 'WITHDRAWAL')
                ),
                amount REAL NOT NULL CHECK(amount > 0),
                transaction_date TEXT NOT NULL,
                FOREIGN KEY(member_id) REFERENCES members(member_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                application_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING' CHECK(
                    status IN ('PENDING', 'APPROVED', 'REJECTED')
                ),
                FOREIGN KEY(member_id) REFERENCES members(member_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS repayments (
                repayment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                repayment_date TEXT NOT NULL,
                FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
                    ON DELETE CASCADE
            );
        """)


def current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_amount(value):
    try:
        amount = Decimal(value.strip())
        if amount <= 0:
            raise InvalidOperation
        return float(amount.quantize(Decimal("0.01")))
    except (InvalidOperation, ValueError, AttributeError):
        raise ValueError("Enter a valid amount greater than 0.")


def member_exists(member_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT 1 FROM members WHERE member_id = ?", (member_id,)
        ).fetchone() is not None


def get_savings_balance(member_id):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT COALESCE(
                SUM(CASE
                    WHEN transaction_type = 'DEPOSIT' THEN amount
                    ELSE -amount
                END), 0
            ) AS balance
            FROM savings
            WHERE member_id = ?
        """, (member_id,)).fetchone()
        return float(row["balance"])


def get_loan_balance(loan_id):
    with get_connection() as conn:
        loan = conn.execute(
            "SELECT amount FROM loans WHERE loan_id = ?", (loan_id,)
        ).fetchone()

        if loan is None:
            return None

        repayment = conn.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM repayments
            WHERE loan_id = ?
        """, (loan_id,)).fetchone()

        return max(0.0, float(loan["amount"]) - float(repayment["total"]))


# ============================================================
# MAIN APPLICATION
# ============================================================

class SACCOApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("SACCO Financial Management System")
        self.geometry("1250x760")
        self.minsize(1050, 650)

        self.configure(bg="#f2f4f7")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_style()
        initialize_database()
        self.create_header()
        self.create_notebook()
        self.refresh_all()

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    def setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TNotebook",
            background="#f2f4f7",
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            padding=(16, 9),
            font=("Segoe UI", 10, "bold")
        )
        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold")
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 9, "bold"),
            padding=7
        )
        style.configure(
            "TLabel",
            background="#f2f4f7",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Title.TLabel",
            background="#17365d",
            foreground="white",
            font=("Segoe UI", 21, "bold")
        )
        style.configure(
            "Subtitle.TLabel",
            background="#17365d",
            foreground="#dce6f1",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Section.TLabel",
            background="#f2f4f7",
            foreground="#17365d",
            font=("Segoe UI", 14, "bold")
        )
        style.configure(
            "Metric.TLabel",
            background="white",
            foreground="#17365d",
            font=("Segoe UI", 17, "bold")
        )
        style.configure(
            "MetricName.TLabel",
            background="white",
            foreground="#555555",
            font=("Segoe UI", 9)
        )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    def create_header(self):
        header = tk.Frame(self, bg="#17365d", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg="#17365d")
        left.pack(side="left", padx=25, pady=10)

        ttk.Label(
            left,
            text="SACCO FINANCIAL MANAGEMENT SYSTEM",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            left,
            text="Member • Savings • Loans • Repayments • Reports",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(2, 0))

        self.clock_label = tk.Label(
            header,
            bg="#17365d",
            fg="white",
            font=("Segoe UI", 10)
        )
        self.clock_label.pack(side="right", padx=25)
        self.update_clock()

    def update_clock(self):
        self.clock_label.config(
            text=datetime.now().strftime("%d %b %Y  |  %H:%M:%S")
        )
        self.after(1000, self.update_clock)

    # --------------------------------------------------------
    # NOTEBOOK
    # --------------------------------------------------------

    def create_notebook(self):
        container = tk.Frame(self, bg="#f2f4f7")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_tab = tk.Frame(self.notebook, bg="#f2f4f7")
        self.members_tab = tk.Frame(self.notebook, bg="#f2f4f7")
        self.savings_tab = tk.Frame(self.notebook, bg="#f2f4f7")
        self.loans_tab = tk.Frame(self.notebook, bg="#f2f4f7")
        self.transactions_tab = tk.Frame(self.notebook, bg="#f2f4f7")
        self.reports_tab = tk.Frame(self.notebook, bg="#f2f4f7")

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.members_tab, text="Members")
        self.notebook.add(self.savings_tab, text="Savings")
        self.notebook.add(self.loans_tab, text="Loans")
        self.notebook.add(self.transactions_tab, text="Transactions")
        self.notebook.add(self.reports_tab, text="Reports")

        self.create_dashboard()
        self.create_members()
        self.create_savings()
        self.create_loans()
        self.create_transactions()
        self.create_reports()

    # --------------------------------------------------------
    # COMMON HELPERS
    # --------------------------------------------------------

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def labeled_entry(self, parent, label, row, column, width=25):
        ttk.Label(parent, text=label).grid(
            row=row, column=column, sticky="w", padx=6, pady=6
        )
        entry = ttk.Entry(parent, width=width)
        entry.grid(
            row=row, column=column + 1, sticky="ew", padx=6, pady=6
        )
        return entry

    def create_tree(self, parent, columns, headings, widths=None):
        frame = tk.Frame(parent, bg="#f2f4f7")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        for i, column in enumerate(columns):
            tree.heading(column, text=headings[i])
            tree.column(
                column,
                width=(widths[i] if widths else 120),
                anchor="center"
            )

        y_scroll = ttk.Scrollbar(
            frame, orient="vertical", command=tree.yview
        )
        x_scroll = ttk.Scrollbar(
            frame, orient="horizontal", command=tree.xview
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        return tree

    def set_status(self, message):
        self.status_var.set(message)

    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):
        ttk.Label(
            self.dashboard_tab,
            text="Dashboard",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        metrics = tk.Frame(self.dashboard_tab, bg="#f2f4f7")
        metrics.pack(fill="x", padx=15)

        self.metric_vars = {}
        metric_names = [
            ("members", "Total Members"),
            ("savings", "Current Savings"),
            ("loans", "Approved Loans"),
            ("pending", "Pending Loans"),
            ("repayments", "Loan Repayments")
        ]

        for key, name in metric_names:
            card = tk.Frame(
                metrics,
                bg="white",
                bd=1,
                relief="solid"
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=6,
                pady=6
            )

            value = tk.StringVar(value="0")
            self.metric_vars[key] = value

            tk.Label(
                card,
                text=name,
                bg="white",
                fg="#555555",
                font=("Segoe UI", 9)
            ).pack(pady=(15, 4))

            tk.Label(
                card,
                textvariable=value,
                bg="white",
                fg="#17365d",
                font=("Segoe UI", 17, "bold")
            ).pack(pady=(0, 15))

        info = tk.Frame(
            self.dashboard_tab,
            bg="white",
            bd=1,
            relief="solid"
        )
        info.pack(fill="both", expand=True, padx=21, pady=20)

        tk.Label(
            info,
            text="System Overview",
            bg="white",
            fg="#17365d",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 8))

        overview = (
            "Use the tabs above to manage SACCO operations.\n\n"
            "Members: register, search, update and delete members.\n"
            "Savings: record deposits and withdrawals and check balances.\n"
            "Loans: apply, approve/reject, repay and view loan balances.\n"
            "Transactions: review savings transaction history.\n"
            "Reports: view the SACCO's financial summary."
        )

        tk.Label(
            info,
            text=overview,
            justify="left",
            bg="white",
            fg="#444444",
            font=("Segoe UI", 10),
            padx=20,
            pady=10
        ).pack(anchor="w")

        ttk.Button(
            info,
            text="Refresh Dashboard",
            command=self.refresh_all
        ).pack(anchor="w", padx=20, pady=20)

    # ========================================================
    # MEMBERS
    # ========================================================

    def create_members(self):
        ttk.Label(
            self.members_tab,
            text="Member Management",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        form = tk.LabelFrame(
            self.members_tab,
            text="Member Details",
            bg="#f2f4f7",
            fg="#17365d",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=15, pady=8)

        self.member_id_var = tk.StringVar()
        self.member_name_var = tk.StringVar()
        self.member_phone_var = tk.StringVar()
        self.member_email_var = tk.StringVar()

        ttk.Label(form, text="Member ID").grid(
            row=0, column=0, sticky="w", padx=6, pady=6
        )
        ttk.Entry(form, textvariable=self.member_id_var).grid(
            row=0, column=1, sticky="ew", padx=6, pady=6
        )

        ttk.Label(form, text="Full Name").grid(
            row=0, column=2, sticky="w", padx=6, pady=6
        )
        ttk.Entry(form, textvariable=self.member_name_var).grid(
            row=0, column=3, sticky="ew", padx=6, pady=6
        )

        ttk.Label(form, text="Phone Number").grid(
            row=1, column=0, sticky="w", padx=6, pady=6
        )
        ttk.Entry(form, textvariable=self.member_phone_var).grid(
            row=1, column=1, sticky="ew", padx=6, pady=6
        )

        ttk.Label(form, text="Email Address").grid(
            row=1, column=2, sticky="w", padx=6, pady=6
        )
        ttk.Entry(form, textvariable=self.member_email_var).grid(
            row=1, column=3, sticky="ew", padx=6, pady=6
        )

        for col in (1, 3):
            form.columnconfigure(col, weight=1)

        buttons = tk.Frame(form, bg="#f2f4f7")
        buttons.grid(row=2, column=0, columnspan=4, sticky="w", pady=8)

        ttk.Button(
            buttons, text="Register Member",
            command=self.register_member
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Update Member",
            command=self.update_member
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Delete Member",
            command=self.delete_member
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Clear",
            command=self.clear_member_form
        ).pack(side="left", padx=4)

        search_frame = tk.Frame(
            self.members_tab, bg="#f2f4f7"
        )
        search_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(search_frame, text="Search by ID or Name:").pack(
            side="left", padx=(0, 8)
        )

        self.member_search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.member_search_var,
            width=35
        )
        search_entry.pack(side="left", padx=4)
        search_entry.bind("<Return>", lambda event: self.search_members())

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_members
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.refresh_members
        ).pack(side="left", padx=4)

        self.member_tree = self.create_tree(
            self.members_tab,
            ("id", "name", "phone", "email", "date"),
            ("Member ID", "Full Name", "Phone", "Email", "Registration Date"),
            (110, 210, 140, 250, 170)
        )

        self.member_tree.bind(
            "<<TreeviewSelect>>", self.load_selected_member
        )

    def register_member(self):
        member_id = self.member_id_var.get().strip()
        name = self.member_name_var.get().strip()
        phone = self.member_phone_var.get().strip()
        email = self.member_email_var.get().strip()

        if not all([member_id, name, phone, email]):
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all member fields."
            )
            return

        try:
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO members
                    (member_id, full_name, phone, email, registration_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (member_id, name, phone, email, current_date()))

            messagebox.showinfo(
                "Success",
                "Member registered successfully."
            )
            self.clear_member_form()
            self.refresh_all()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate Member",
                "A member with that ID already exists."
            )
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def refresh_members(self, rows=None):
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)

        if rows is None:
            with get_connection() as conn:
                rows = conn.execute("""
                    SELECT member_id, full_name, phone, email,
                           registration_date
                    FROM members
                    ORDER BY full_name
                """).fetchall()

        for row in rows:
            self.member_tree.insert(
                "",
                "end",
                values=(
                    row["member_id"],
                    row["full_name"],
                    row["phone"],
                    row["email"],
                    row["registration_date"]
                )
            )

        self.set_status(f"{len(rows)} member(s) displayed.")

    def search_members(self):
        keyword = self.member_search_var.get().strip()

        if not keyword:
            self.refresh_members()
            return

        with get_connection() as conn:
            rows = conn.execute("""
                SELECT member_id, full_name, phone, email,
                       registration_date
                FROM members
                WHERE member_id LIKE ? OR full_name LIKE ?
                ORDER BY full_name
            """, (f"%{keyword}%", f"%{keyword}%")).fetchall()

        self.refresh_members(rows)

        if not rows:
            messagebox.showinfo(
                "Search",
                "No matching member was found."
            )

    def load_selected_member(self, event=None):
        selection = self.member_tree.selection()
        if not selection:
            return

        values = self.member_tree.item(selection[0], "values")
        self.member_id_var.set(values[0])
        self.member_name_var.set(values[1])
        self.member_phone_var.set(values[2])
        self.member_email_var.set(values[3])

    def update_member(self):
        member_id = self.member_id_var.get().strip()
        phone = self.member_phone_var.get().strip()
        email = self.member_email_var.get().strip()

        if not member_id:
            messagebox.showwarning(
                "Member ID Required",
                "Select or enter a member ID."
            )
            return

        if not member_exists(member_id):
            messagebox.showerror("Not Found", "Member not found.")
            return

        if not phone or not email:
            messagebox.showwarning(
                "Missing Information",
                "Phone number and email are required."
            )
            return

        try:
            with get_connection() as conn:
                conn.execute("""
                    UPDATE members
                    SET phone = ?, email = ?
                    WHERE member_id = ?
                """, (phone, email, member_id))

            messagebox.showinfo(
                "Success",
                "Member information updated successfully."
            )
            self.refresh_all()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def delete_member(self):
        member_id = self.member_id_var.get().strip()

        if not member_id:
            messagebox.showwarning(
                "Member ID Required",
                "Select a member to delete."
            )
            return

        with get_connection() as conn:
            member = conn.execute(
                "SELECT full_name FROM members WHERE member_id = ?",
                (member_id,)
            ).fetchone()

        if member is None:
            messagebox.showerror("Not Found", "Member not found.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete member '{member['full_name']}' and all "
            "associated records?"
        )

        if not confirm:
            return

        try:
            with get_connection() as conn:
                conn.execute(
                    "DELETE FROM members WHERE member_id = ?",
                    (member_id,)
                )

            messagebox.showinfo(
                "Deleted",
                "Member deleted successfully."
            )
            self.clear_member_form()
            self.refresh_all()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def clear_member_form(self):
        self.member_id_var.set("")
        self.member_name_var.set("")
        self.member_phone_var.set("")
        self.member_email_var.set("")
        self.member_tree.selection_remove(
            self.member_tree.selection()
        )

    # ========================================================
    # SAVINGS
    # ========================================================

    def create_savings(self):
        ttk.Label(
            self.savings_tab,
            text="Savings Management",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        form = tk.LabelFrame(
            self.savings_tab,
            text="Savings Transaction",
            bg="#f2f4f7",
            fg="#17365d",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=15, pady=8)

        self.savings_member_var = tk.StringVar()
        self.savings_amount_var = tk.StringVar()
        self.savings_balance_var = tk.StringVar(value="Balance: 0.00")

        ttk.Label(form, text="Member ID").grid(
            row=0, column=0, sticky="w", padx=6, pady=6
        )
        self.savings_member_entry = ttk.Entry(
            form, textvariable=self.savings_member_var
        )
        self.savings_member_entry.grid(
            row=0, column=1, sticky="ew", padx=6, pady=6
        )

        ttk.Label(form, text="Amount").grid(
            row=0, column=2, sticky="w", padx=6, pady=6
        )
        ttk.Entry(
            form, textvariable=self.savings_amount_var
        ).grid(
            row=0, column=3, sticky="ew", padx=6, pady=6
        )

        ttk.Button(
            form,
            text="Check Balance",
            command=self.check_savings_balance
        ).grid(row=0, column=4, padx=6)

        ttk.Button(
            form,
            text="Deposit",
            command=self.deposit_savings
        ).grid(row=1, column=1, sticky="w", padx=6, pady=8)

        ttk.Button(
            form,
            text="Withdraw",
            command=self.withdraw_savings
        ).grid(row=1, column=2, sticky="w", padx=6, pady=8)

        ttk.Button(
            form,
            text="Clear",
            command=self.clear_savings_form
        ).grid(row=1, column=3, sticky="w", padx=6, pady=8)

        tk.Label(
            form,
            textvariable=self.savings_balance_var,
            bg="#f2f4f7",
            fg="#17365d",
            font=("Segoe UI", 12, "bold")
        ).grid(row=2, column=0, columnspan=5, sticky="w", padx=6, pady=8)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        ttk.Label(
            self.savings_tab,
            text="Recent Savings Transactions",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(12, 2))

        self.savings_tree = self.create_tree(
            self.savings_tab,
            ("id", "member", "name", "type", "amount", "date"),
            ("ID", "Member ID", "Member Name", "Type", "Amount", "Date"),
            (70, 110, 200, 120, 130, 180)
        )

    def validate_savings_member(self):
        member_id = self.savings_member_var.get().strip()

        if not member_id:
            messagebox.showwarning(
                "Member ID Required",
                "Enter a member ID."
            )
            return None

        if not member_exists(member_id):
            messagebox.showerror(
                "Not Found",
                "Member not found."
            )
            return None

        return member_id

    def deposit_savings(self):
        member_id = self.validate_savings_member()
        if not member_id:
            return

        try:
            amount = parse_amount(self.savings_amount_var.get())
        except ValueError as error:
            messagebox.showerror("Invalid Amount", str(error))
            return

        try:
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO savings
                    (member_id, transaction_type, amount, transaction_date)
                    VALUES (?, 'DEPOSIT', ?, ?)
                """, (member_id, amount, current_date()))

            balance = get_savings_balance(member_id)

            messagebox.showinfo(
                "Deposit Successful",
                f"Deposit of {amount:,.2f} recorded.\n"
                f"New savings balance: {balance:,.2f}"
            )

            self.savings_balance_var.set(
                f"Balance: {balance:,.2f}"
            )
            self.savings_amount_var.set("")
            self.refresh_all()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def withdraw_savings(self):
        member_id = self.validate_savings_member()
        if not member_id:
            return

        try:
            amount = parse_amount(self.savings_amount_var.get())
        except ValueError as error:
            messagebox.showerror("Invalid Amount", str(error))
            return

        balance = get_savings_balance(member_id)

        if amount > balance:
            messagebox.showerror(
                "Insufficient Savings",
                f"Current balance is {balance:,.2f}."
            )
            return

        try:
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO savings
                    (member_id, transaction_type, amount, transaction_date)
                    VALUES (?, 'WITHDRAWAL', ?, ?)
                """, (member_id, amount, current_date()))

            new_balance = get_savings_balance(member_id)

            messagebox.showinfo(
                "Withdrawal Successful",
                f"Withdrawal of {amount:,.2f} recorded.\n"
                f"New savings balance: {new_balance:,.2f}"
            )

            self.savings_balance_var.set(
                f"Balance: {new_balance:,.2f}"
            )
            self.savings_amount_var.set("")
            self.refresh_all()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def check_savings_balance(self):
        member_id = self.validate_savings_member()
        if not member_id:
            return

        balance = get_savings_balance(member_id)
        self.savings_balance_var.set(
            f"Balance: {balance:,.2f}"
        )

    def clear_savings_form(self):
        self.savings_member_var.set("")
        self.savings_amount_var.set("")
        self.savings_balance_var.set("Balance: 0.00")

    def refresh_savings(self):
        for item in self.savings_tree.get_children():
            self.savings_tree.delete(item)

        with get_connection() as conn:
            rows = conn.execute("""
                SELECT s.saving_id, s.member_id, m.full_name,
                       s.transaction_type, s.amount, s.transaction_date
                FROM savings s
                JOIN members m ON s.member_id = m.member_id
                ORDER BY s.saving_id DESC
            """).fetchall()

        for row in rows:
            self.savings_tree.insert(
                "",
                "end",
                values=(
                    row["saving_id"],
                    row["member_id"],
                    row["full_name"],
                    row["transaction_type"],
                    f"{row['amount']:,.2f}",
                    row["transaction_date"]
                )
            )

    # ========================================================
    # LOANS
    # ========================================================

    def create_loans(self):
        ttk.Label(
            self.loans_tab,
            text="Loan Management",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        form = tk.LabelFrame(
            self.loans_tab,
            text="Loan Operations",
            bg="#f2f4f7",
            fg="#17365d",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=15, pady=8)

        self.loan_member_var = tk.StringVar()
        self.loan_amount_var = tk.StringVar()
        self.loan_id_var = tk.StringVar()
        self.loan_repayment_var = tk.StringVar()
        self.loan_balance_var = tk.StringVar(value="Loan Balance: 0.00")

        ttk.Label(form, text="Member ID").grid(
            row=0, column=0, sticky="w", padx=6, pady=5
        )
        ttk.Entry(
            form, textvariable=self.loan_member_var
        ).grid(
            row=0, column=1, sticky="ew", padx=6, pady=5
        )

        ttk.Label(form, text="Loan Amount").grid(
            row=0, column=2, sticky="w", padx=6, pady=5
        )
        ttk.Entry(
            form, textvariable=self.loan_amount_var
        ).grid(
            row=0, column=3, sticky="ew", padx=6, pady=5
        )

        ttk.Button(
            form,
            text="Apply Loan",
            command=self.apply_loan
        ).grid(row=0, column=4, padx=6)

        ttk.Label(form, text="Loan ID").grid(
            row=1, column=0, sticky="w", padx=6, pady=5
        )
        ttk.Entry(
            form, textvariable=self.loan_id_var
        ).grid(
            row=1, column=1, sticky="ew", padx=6, pady=5
        )

        ttk.Label(form, text="Repayment Amount").grid(
            row=1, column=2, sticky="w", padx=6, pady=5
        )
        ttk.Entry(
            form, textvariable=self.loan_repayment_var
        ).grid(
            row=1, column=3, sticky="ew", padx=6, pady=5
        )

        ttk.Button(
            form,
            text="Approve",
            command=lambda: self.change_loan_status("APPROVED")
        ).grid(row=2, column=1, sticky="w", padx=6, pady=7)

        ttk.Button(
            form,
            text="Reject",
            command=lambda: self.change_loan_status("REJECTED")
        ).grid(row=2, column=2, sticky="w", padx=6, pady=7)

        ttk.Button(
            form,
            text="Repay Loan",
            command=self.repay_loan
        ).grid(row=2, column=3, sticky="w", padx=6, pady=7)

        ttk.Button(
            form,
            text="Check Balance",
            command=self.check_loan_balance
        ).grid(row=2, column=4, padx=6, pady=7)

        ttk.Button(
            form,
            text="Clear",
            command=self.clear_loan_form
        ).grid(row=2, column=5, padx=6, pady=7)

        tk.Label(
            form,
            textvariable=self.loan_balance_var,
            bg="#f2f4f7",
            fg="#17365d",
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=3, column=0, columnspan=6,
            sticky="w", padx=6, pady=6
        )

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        self.loan_tree = self.create_tree(
            self.loans_tab,
            (
                "id", "member", "name", "amount",
                "repaid", "balance", "status", "date"
            ),
            (
                "Loan ID", "Member ID", "Member Name", "Amount",
                "Repaid", "Balance", "Status", "Application Date"
            ),
            (70, 100, 190, 120, 120, 120, 110, 180)
        )

        self.loan_tree.bind(
            "<<TreeviewSelect>>", self.load_selected_loan
        )

    def apply_loan(self):
        member_id = self.loan_member_var.get().strip()

        if not member_id:
            messagebox.showwarning(
                "Member ID Required",
                "Enter a member ID."
            )
            return

        if not member_exists(member_id):
            messagebox.showerror(
                "Not Found",
                "Member not found."
            )
            return

        try:
            amount = parse_amount(self.loan_amount_var.get())
        except ValueError as error:
            messagebox.showerror("Invalid Amount", str(error))
            return

        try:
            with get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO loans
                    (member_id, amount, application_date, status)
                    VALUES (?, ?, ?, 'PENDING')
                """, (member_id, amount, current_date()))

                loan_id = cursor.lastrowid

            messagebox.showinfo(
                "Loan Application",
                f"Loan application #{loan_id} submitted.\n"
                "Status: PENDING"
            )

            self.clear_loan_form()
            self.refresh_all()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def refresh_loans(self):
        for item in self.loan_tree.get_children():
            self.loan_tree.delete(item)

        with get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    l.loan_id,
                    l.member_id,
                    m.full_name,
                    l.amount,
                    l.application_date,
                    l.status,
                    COALESCE(SUM(r.amount), 0) AS repaid
                FROM loans l
                JOIN members m ON l.member_id = m.member_id
                LEFT JOIN repayments r ON l.loan_id = r.loan_id
                GROUP BY l.loan_id
                ORDER BY l.loan_id DESC
            """).fetchall()

        for row in rows:
            balance = max(
                0.0,
                float(row["amount"]) - float(row["repaid"])
            )

            self.loan_tree.insert(
                "",
                "end",
                values=(
                    row["loan_id"],
                    row["member_id"],
                    row["full_name"],
                    f"{row['amount']:,.2f}",
                    f"{row['repaid']:,.2f}",
                    f"{balance:,.2f}",
                    row["status"],
                    row["application_date"]
                )
            )

    def load_selected_loan(self, event=None):
        selection = self.loan_tree.selection()
        if not selection:
            return

        values = self.loan_tree.item(selection[0], "values")

        self.loan_id_var.set(values[0])
        self.loan_member_var.set(values[1])
        self.loan_balance_var.set(
            f"Loan Balance: {values[5]}"
        )

    def get_selected_loan(self):
        loan_id = self.loan_id_var.get().strip()

        if not loan_id:
            selection = self.loan_tree.selection()
            if selection:
                loan_id = self.loan_tree.item(
                    selection[0], "values"
                )[0]

        try:
            loan_id = int(loan_id)
            if loan_id <= 0:
                raise ValueError
            return loan_id
        except ValueError:
            messagebox.showwarning(
                "Loan ID Required",
                "Enter or select a valid loan ID."
            )
            return None

    def change_loan_status(self, status):
        loan_id = self.get_selected_loan()
        if loan_id is None:
            return

        with get_connection() as conn:
            loan = conn.execute("""
                SELECT loan_id, member_id, amount, status
                FROM loans
                WHERE loan_id = ?
            """, (loan_id,)).fetchone()

            if loan is None:
                messagebox.showerror(
                    "Not Found",
                    "Loan not found."
                )
                return

            if loan["status"] != "PENDING":
                messagebox.showwarning(
                    "Cannot Change Status",
                    f"This loan is already {loan['status']}."
                )
                return

            conn.execute(
                "UPDATE loans SET status = ? WHERE loan_id = ?",
                (status, loan_id)
            )

        messagebox.showinfo(
            "Loan Updated",
            f"Loan #{loan_id} has been {status.lower()}."
        )
        self.refresh_all()

    def repay_loan(self):
        loan_id = self.get_selected_loan()
        if loan_id is None:
            return

        try:
            amount = parse_amount(
                self.loan_repayment_var.get()
            )
        except ValueError as error:
            messagebox.showerror("Invalid Amount", str(error))
            return

        with get_connection() as conn:
            loan = conn.execute("""
                SELECT loan_id, member_id, amount, status
                FROM loans
                WHERE loan_id = ?
            """, (loan_id,)).fetchone()

        if loan is None:
            messagebox.showerror(
                "Not Found",
                "Loan not found."
            )
            return

        if loan["status"] != "APPROVED":
            messagebox.showwarning(
                "Invalid Loan Status",
                "Repayment can only be made for an approved loan."
            )
            return

        balance = get_loan_balance(loan_id)

        if balance <= 0:
            messagebox.showinfo(
                "Loan Paid",
                "This loan has already been fully repaid."
            )
            return

        if amount > balance:
            messagebox.showerror(
                "Invalid Repayment",
                f"Repayment cannot exceed the outstanding "
                f"balance of {balance:,.2f}."
            )
            return

        try:
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO repayments
                    (loan_id, amount, repayment_date)
                    VALUES (?, ?, ?)
                """, (loan_id, amount, current_date()))

            new_balance = get_loan_balance(loan_id)

            message = (
                f"Repayment of {amount:,.2f} recorded.\n"
                f"Remaining balance: {new_balance:,.2f}"
            )

            if new_balance == 0:
                message += "\n\nLoan fully repaid."

            messagebox.showinfo(
                "Repayment Successful",
                message
            )

            self.loan_repayment_var.set("")
            self.loan_balance_var.set(
                f"Loan Balance: {new_balance:,.2f}"
            )
            self.refresh_all()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def check_loan_balance(self):
        loan_id = self.get_selected_loan()
        if loan_id is None:
            return

        with get_connection() as conn:
            loan = conn.execute("""
                SELECT l.loan_id, l.amount, l.status, m.full_name
                FROM loans l
                JOIN members m ON l.member_id = m.member_id
                WHERE l.loan_id = ?
            """, (loan_id,)).fetchone()

        if loan is None:
            messagebox.showerror(
                "Not Found",
                "Loan not found."
            )
            return

        balance = get_loan_balance(loan_id)

        self.loan_balance_var.set(
            f"Loan Balance: {balance:,.2f}"
        )

        messagebox.showinfo(
            "Loan Balance",
            f"Member: {loan['full_name']}\n"
            f"Original Loan: {loan['amount']:,.2f}\n"
            f"Status: {loan['status']}\n"
            f"Outstanding Balance: {balance:,.2f}"
        )

    def clear_loan_form(self):
        self.loan_member_var.set("")
        self.loan_amount_var.set("")
        self.loan_id_var.set("")
        self.loan_repayment_var.set("")
        self.loan_balance_var.set("Loan Balance: 0.00")

    # ========================================================
    # TRANSACTIONS
    # ========================================================

    def create_transactions(self):
        ttk.Label(
            self.transactions_tab,
            text="Transaction History",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        controls = tk.Frame(
            self.transactions_tab,
            bg="#f2f4f7"
        )
        controls.pack(fill="x", padx=20, pady=8)

        ttk.Label(
            controls,
            text="Member ID (blank for all):"
        ).pack(side="left", padx=(0, 8))

        self.transaction_member_var = tk.StringVar()

        entry = ttk.Entry(
            controls,
            textvariable=self.transaction_member_var,
            width=25
        )
        entry.pack(side="left", padx=4)

        ttk.Button(
            controls,
            text="Search",
            command=self.refresh_transactions
        ).pack(side="left", padx=4)

        ttk.Button(
            controls,
            text="Show All",
            command=self.show_all_transactions
        ).pack(side="left", padx=4)

        self.transaction_tree = self.create_tree(
            self.transactions_tab,
            ("date", "member", "name", "type", "amount"),
            ("Date", "Member ID", "Member Name", "Type", "Amount"),
            (190, 120, 240, 140, 140)
        )

    def refresh_transactions(self):
        member_id = self.transaction_member_var.get().strip()

        if member_id and not member_exists(member_id):
            messagebox.showerror(
                "Not Found",
                "Member not found."
            )
            return

        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        query = """
            SELECT
                s.transaction_date,
                s.member_id,
                m.full_name,
                s.transaction_type,
                s.amount
            FROM savings s
            JOIN members m ON s.member_id = m.member_id
        """

        params = ()

        if member_id:
            query += " WHERE s.member_id = ? "
            params = (member_id,)

        query += " ORDER BY s.transaction_date DESC"

        with get_connection() as conn:
            rows = conn.execute(query, params).fetchall()

        for row in rows:
            self.transaction_tree.insert(
                "",
                "end",
                values=(
                    row["transaction_date"],
                    row["member_id"],
                    row["full_name"],
                    row["transaction_type"],
                    f"{row['amount']:,.2f}"
                )
            )

        self.set_status(
            f"{len(rows)} transaction(s) displayed."
        )

    def show_all_transactions(self):
        self.transaction_member_var.set("")
        self.refresh_transactions()

    # ========================================================
    # REPORTS
    # ========================================================

    def create_reports(self):
        ttk.Label(
            self.reports_tab,
            text="Financial Report",
            style="Section.TLabel"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        button_frame = tk.Frame(
            self.reports_tab,
            bg="#f2f4f7"
        )
        button_frame.pack(fill="x", padx=20, pady=8)

        ttk.Button(
            button_frame,
            text="Generate / Refresh Report",
            command=self.refresh_report
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Export Report to Text",
            command=self.export_report
        ).pack(side="left", padx=8)

        self.report_text = tk.Text(
            self.reports_tab,
            wrap="word",
            font=("Consolas", 11),
            bg="white",
            fg="#222222",
            padx=20,
            pady=20
        )
        self.report_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    def get_report_data(self):
        with get_connection() as conn:
            members = conn.execute(
                "SELECT COUNT(*) AS total FROM members"
            ).fetchone()["total"]

            deposits = conn.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM savings
                WHERE transaction_type = 'DEPOSIT'
            """).fetchone()["total"]

            withdrawals = conn.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM savings
                WHERE transaction_type = 'WITHDRAWAL'
            """).fetchone()["total"]

            loans_approved = conn.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM loans
                WHERE status = 'APPROVED'
            """).fetchone()["total"]

            loans_pending = conn.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM loans
                WHERE status = 'PENDING'
            """).fetchone()["total"]

            loans_rejected = conn.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM loans
                WHERE status = 'REJECTED'
            """).fetchone()["total"]

            repayments = conn.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM repayments
            """).fetchone()["total"]

            loan_count = conn.execute(
                "SELECT COUNT(*) AS total FROM loans"
            ).fetchone()["total"]

            repayment_count = conn.execute(
                "SELECT COUNT(*) AS total FROM repayments"
            ).fetchone()["total"]

        return {
            "members": int(members),
            "deposits": float(deposits),
            "withdrawals": float(withdrawals),
            "savings_balance": float(deposits) - float(withdrawals),
            "approved": float(loans_approved),
            "pending": float(loans_pending),
            "rejected": float(loans_rejected),
            "repayments": float(repayments),
            "loan_count": int(loan_count),
            "repayment_count": int(repayment_count)
        }

    def format_report(self, data=None):
        if data is None:
            data = self.get_report_data()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            "\n"
            + "=" * 62 + "\n"
            + "              SACCO FINANCIAL REPORT\n"
            + "=" * 62 + "\n"
            + f"Generated:                  {now}\n"
            + "-" * 62 + "\n"
            + f"Total members:              {data['members']}\n"
            + f"Total deposits:             {data['deposits']:,.2f}\n"
            + f"Total withdrawals:          {data['withdrawals']:,.2f}\n"
            + f"Current savings balance:     {data['savings_balance']:,.2f}\n"
            + f"Approved loans:              {data['approved']:,.2f}\n"
            + f"Pending loan applications:   {data['pending']:,.2f}\n"
            + f"Rejected loans:              {data['rejected']:,.2f}\n"
            + f"Total loan repayments:       {data['repayments']:,.2f}\n"
            + f"Number of loans:             {data['loan_count']}\n"
            + f"Number of repayments:        {data['repayment_count']}\n"
            + "=" * 62 + "\n"
        )

    def refresh_report(self):
        report = self.format_report()

        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", report)

    def export_report(self):
        report = self.format_report()
        filename = (
            "sacco_financial_report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(report)

            messagebox.showinfo(
                "Report Exported",
                f"Report saved as:\n{filename}"
            )

        except OSError as error:
            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_dashboard(self):
        data = self.get_report_data()

        self.metric_vars["members"].set(
            str(data["members"])
        )
        self.metric_vars["savings"].set(
            f"{data['savings_balance']:,.2f}"
        )
        self.metric_vars["loans"].set(
            f"{data['approved']:,.2f}"
        )
        self.metric_vars["pending"].set(
            f"{data['pending']:,.2f}"
        )
        self.metric_vars["repayments"].set(
            f"{data['repayments']:,.2f}"
        )

    def refresh_all(self):
        try:
            self.refresh_members()
            self.refresh_savings()
            self.refresh_loans()
            self.refresh_transactions()
            self.refresh_report()
            self.refresh_dashboard()
            self.set_status("System refreshed successfully.")
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ========================================================
    # CLOSE
    # ========================================================

    def on_close(self):
        if messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit the SACCO system?"
        ):
            self.destroy()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    try:
        initialize_database()
        app = SACCOApp()
        app.mainloop()
    except Exception as error:
        messagebox.showerror(
            "Startup Error",
            f"The application could not start:\n{error}"
        )
