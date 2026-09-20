import sys
import services

def get_int_input(prompt):
    """Safely gets integer input to prevent crashes."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")

def get_float_input(prompt):
    """Safely gets float input to prevent crashes."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 500 or 500.50).")

def display_menu():
    print("\n" + "="*45)
    print("   SACCO FINANCIAL MANAGEMENT SYSTEM   ")
    print("="*45)
    print("1. Register Member")
    print("2. View Members")
    print("3. Search Member")
    print("4. Deposit Savings")
    print("5. Withdraw Savings")
    print("6. Check Savings Balance")
    print("7. Apply for Loan")
    print("8. Approve Loan")
    print("9. Make Loan Repayment")
    print("10. View Loan Balance")
    print("11. View Transactions")
    print("12. Generate Reports")
    print("13. Exit")
    print("="*45)

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-13): ")

        if choice == '1':
            name = input("Enter Full Name: ").strip()
            phone = input("Enter Phone Number: ").strip()
            email = input("Enter Email Address: ").strip()
            services.register_member(name, phone, email)

        elif choice == '2':
            members = services.view_members()
            if not members:
                print("\nNo members registered yet.")
            else:
                print("\n--- Registered Members ---")
                for m in members:
                    print(f"ID: {m.member_id} | Name: {m.full_name} | Phone: {m.phone}")

        elif choice == '3':
            m_id = get_int_input("Enter Member ID: ")
            member = services.search_member(m_id)
            if member:
                print(f"\nMember Found: ID: {member.member_id}, Name: {member.full_name}, Email: {member.email}, Date Registered: {member.date_registered}")
            else:
                print("\nMember not found.")

        elif choice == '4':
            m_id = get_int_input("Enter Member ID: ")
            amount = get_float_input("Enter deposit amount: ")
            services.deposit_savings(m_id, amount)

        elif choice == '5':
            m_id = get_int_input("Enter Member ID: ")
            amount = get_float_input("Enter withdrawal amount: ")
            services.withdraw_savings(m_id, amount)

        elif choice == '6':
            m_id = get_int_input("Enter Member ID: ")
            balance = services.check_savings_balance(m_id)
            print(f"\nSavings Balance for Member ID {m_id}: KES {balance}")

        elif choice == '7':
            m_id = get_int_input("Enter Member ID: ")
            amount = get_float_input("Enter loan application amount: ")
            services.apply_for_loan(m_id, amount)

        elif choice == '8':
            l_id = get_int_input("Enter Loan ID to approve: ")
            services.approve_loan(l_id)

        elif choice == '9':
            m_id = get_int_input("Enter Member ID: ")
            amount = get_float_input("Enter repayment amount: ")
            services.make_loan_repayment(m_id, amount)

        elif choice == '10':
            m_id = get_int_input("Enter Member ID: ")
            loans = services.view_loan_balance(m_id)
            if not loans:
                print("\nNo loans found for this member.")
            else:
                print(f"\n--- Loan Details for Member {m_id} ---")
                for l in loans:
                    print(f"Loan ID: {l[0]} | Amount: KES {l[1]} | Status: {l[2]} | Outstanding Balance: KES {l[3]}")

        elif choice == '11':
            print("\n1. View all transactions\n2. View transactions by Member ID")
            sub_choice = input("Select option (1 or 2): ")
            if sub_choice == '1':
                transactions = services.view_transactions()
            elif sub_choice == '2':
                m_id = get_int_input("Enter Member ID: ")
                transactions = services.view_transactions(m_id)
            else:
                print("Invalid choice.")
                continue
            
            if not transactions:
                print("\nNo transactions found.")
            else:
                print("\n--- Transaction Log ---")
                for t in transactions:
                    print(f"ID: {t[0]} | Member ID: {t[1]} | Type: {t[2]} | Amount: KES {t[3]} | Date: {t[4]}")

        elif choice == '12':
            reports = services.generate_reports()
            if reports:
                print("\n--- SACCO Financial Summary ---")
                for key, value in reports.items():
                    print(f"{key}: KES {value:,.2f}")

        elif choice == '13':
            print("\nExiting SACCO System. Goodbye!")
            sys.exit()

        else:
            print("\nInvalid choice. Please select a valid option from 1 to 13.")

if __name__ == "__main__":
    main()