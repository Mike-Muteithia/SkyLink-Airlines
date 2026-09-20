import sqlite3
from sqlite3 import Error

DB_FILE = "sacco.db"

def create_connection():
    """Create and return a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        # Enforce foreign key constraints in SQLite
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_query(query, parameters=()):
    """Execute a single query (INSERT, UPDATE, DELETE, CREATE) with parameterization."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Database Error: {e}")
        finally:
            conn.close()

def execute_read_query(query, parameters=()):
    """Execute a read query (SELECT) and return the fetched results."""
    conn = create_connection()
    result = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            result = cursor.fetchall()
        except Error as e:
            print(f"Database Error: {e}")
        finally:
            conn.close()
    return result

def initialize_database():
    """Create the necessary tables for the SACCO system."""
    
    create_members_table = """
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    create_savings_table = """
    CREATE TABLE IF NOT EXISTS savings (
        savings_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        balance REAL DEFAULT 0.0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE CASCADE
    );
    """

    create_loans_table = """
    CREATE TABLE IF NOT EXISTS loans (
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
        balance REAL NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE CASCADE
    );
    """

    create_transactions_table = """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Deposit', 'Withdrawal', 'Loan Repayment')),
        amount REAL NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE CASCADE
    );
    """

    execute_query(create_members_table)
    execute_query(create_savings_table)
    execute_query(create_loans_table)
    execute_query(create_transactions_table)
    print("Database schema initialized successfully.")

if __name__ == "__main__":
    initialize_database()