import database
from models import Member

def register_member(full_name, phone, email):
    """Registers a new member and initializes a zero-balance savings account."""
    try:
        query = "INSERT INTO members (full_name, phone, email) VALUES (?, ?, ?)"
        member_id = database.execute_query(query, (full_name, phone, email))
        
        if member_id:
            savings_query = "INSERT INTO savings (member_id, balance) VALUES (?, 0.0)"
            database.execute_query(savings_query, (member_id,))
            print(f"\nSuccess: Member '{full_name}' registered with ID: {member_id}")
            return member_id
        return None
    except Exception as e:
        print(f"\nError registering member: {e}")
        return None

def view_members():
    """Retrieves all registered SACCO members."""
    query = "SELECT * FROM members"
    results = database.execute_read_query(query)
    return [Member(*row) for row in results]

def search_member(member_id):
    """Searches for a specific member by ID."""
    query = "SELECT * FROM members WHERE member_id = ?"
    result = database.execute_read_query(query, (member_id,))
    if result:
        return Member(*result[0])
    return None

def deposit_savings(member_id, amount):
    """Records a deposit and updates the savings balance."""
    if amount <= 0:
        print("\nValidation Error: Deposit amount must be positive.")
        return False
    try:
        query = "UPDATE savings SET balance = balance + ?, last_updated = CURRENT_TIMESTAMP WHERE member_id = ?"
        database.execute_query(query, (amount, member_id))
        
        trans_query = "INSERT INTO transactions (member_id, transaction_type, amount) VALUES (?, 'Deposit', ?)"
        database.execute_query(trans_query, (member_id, amount))
        print(f"\nSuccess: Deposited KES {amount} to member ID {member_id}.")
        return True
    except Exception as e:
        print(f"\nError processing deposit: {e}")
        return False

def withdraw_savings(member_id, amount):
    """Processes a withdrawal if sufficient funds exist."""
    if amount <= 0:
        print("\nValidation Error: Withdrawal amount must be positive.")
        return False
    try:
        balance = check_savings_balance(member_id)
        if balance >= amount:
            query = "UPDATE savings SET balance = balance - ?, last_updated = CURRENT_TIMESTAMP WHERE member_id = ?"
            database.execute_query(query, (amount, member_id))
            
            trans_query = "INSERT INTO transactions (member_id, transaction_type, amount) VALUES (?, 'Withdrawal', ?)"
            database.execute_query(trans_query, (member_id, amount))
            print(f"\nSuccess: Withdrew KES {amount} from member ID {member_id}.")
            return True
        else:
            print(f"\nError: Insufficient funds. Current balance is KES {balance}.")
            return False
    except Exception as e:
        print(f"\nError processing withdrawal: {e}")
        return False

def check_savings_balance(member_id):
    """Looks up the current savings balance for a member."""
    query = "SELECT balance FROM savings WHERE member_id = ?"
    result = database.execute_read_query(query, (member_id,))
    if result:
        return result[0][0]
    return 0.0

def apply_for_loan(member_id, amount):
    """Records a new loan application in Pending status."""
    if amount <= 0:
        print("\nValidation Error: Loan amount must be positive.")
        return False
    try:
        query = "INSERT INTO loans (member_id, amount, status, balance) VALUES (?, ?, 'Pending', ?)"
        database.execute_query(query, (member_id, amount, amount))
        print(f"\nSuccess: Loan application for KES {amount} submitted for member ID {member_id}.")
        return True
    except Exception as e:
        print(f"\nError applying for loan: {e}")
        return False

def approve_loan(loan_id):
    """Updates a pending loan's workflow status to Approved."""
    try:
        query = "UPDATE loans SET status = 'Approved' WHERE loan_id = ?"
        database.execute_query(query, (loan_id,))
        print(f"\nSuccess: Loan ID {loan_id} has been approved.")
        return True
    except Exception as e:
        print(f"\nError approving loan: {e}")
        return False

def make_loan_repayment(member_id, amount):
    """Processes a repayment against an active, approved loan."""
    if amount <= 0:
        print("\nValidation Error: Repayment amount must be positive.")
        return False
    try:
        loan_query = "SELECT loan_id, balance FROM loans WHERE member_id = ? AND status = 'Approved' AND balance > 0"
        loan = database.execute_read_query(loan_query, (member_id,))
        
        if loan:
            loan_id, current_balance = loan[0]
            if amount > current_balance:
                amount = current_balance
                
            update_query = "UPDATE loans SET balance = balance - ? WHERE loan_id = ?"
            database.execute_query(update_query, (amount, loan_id))
            
            trans_query = "INSERT INTO transactions (member_id, transaction_type, amount) VALUES (?, 'Loan Repayment', ?)"
            database.execute_query(trans_query, (member_id, amount))
            print(f"\nSuccess: Repayment of KES {amount} applied to loan ID {loan_id}.")
            return True
        else:
            print("\nError: No active approved loans found with an outstanding balance.")
            return False
    except Exception as e:
        print(f"\nError making repayment: {e}")
        return False

def view_loan_balance(member_id):
    """Retrieves loan details for a member."""
    query = "SELECT loan_id, amount, status, balance FROM loans WHERE member_id = ?"
    return database.execute_read_query(query, (member_id,))

def view_transactions(member_id=None):
    """Retrieves transaction logs, globally or filtered by member."""
    if member_id:
        query = "SELECT * FROM transactions WHERE member_id = ?"
        return database.execute_read_query(query, (member_id,))
    else:
        query = "SELECT * FROM transactions"
        return database.execute_read_query(query)

def generate_reports():
    """Compiles global SACCO financial summaries."""
    try:
        total_savings = database.execute_read_query("SELECT SUM(balance) FROM savings")[0][0] or 0.0
        total_loans_issued = database.execute_read_query("SELECT SUM(amount) FROM loans WHERE status = 'Approved'")[0][0] or 0.0
        outstanding_loans = database.execute_read_query("SELECT SUM(balance) FROM loans WHERE status = 'Approved'")[0][0] or 0.0
        
        return {
            "Total SACCO Savings": total_savings,
            "Total Loans Issued": total_loans_issued,
            "Total Outstanding Loans": outstanding_loans
        }
    except Exception as e:
        print(f"\nError generating reports: {e}")
        return None