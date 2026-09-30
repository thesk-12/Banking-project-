"""
Banking System - Mini Project
Features:
- Account creation with auto-generated unique account numbers
- Authentication via Account Number & PIN
- Balance inquiry, deposit, withdrawal, and fund transfers
- Detailed transaction history with timestamps
- PIN modification and session management
"""

import json
import os
import random
from datetime import datetime

DATA_FILE = "bank_data.json"


def load_data():
    """Load user accounts and data from a JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {}


def save_data(data):
    """Persist user accounts and transaction records to disk."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"\n[!] Error saving data: {e}")


def generate_account_number(existing_accounts):
    """Generate a unique 8-digit account number."""
    while True:
        acc_num = str(random.randint(10000000, 99999999))
        if acc_num not in existing_accounts:
            return acc_num


def record_transaction(account_dict, txn_type, amount, balance_after, note=""):
    """Append a timestamped transaction record to the user's history."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    account_dict["transactions"].append({
        "timestamp": now_str,
        "type": txn_type,
        "amount": amount,
        "balance_after": balance_after,
        "note": note
    })


def create_account(accounts):
    """Handle new account creation."""
    print("\n" + "=" * 40)
    print("        CREATE NEW ACCOUNT")
    print("=" * 40)
    
    name = input("Enter your full name: ").strip()
    if not name:
        print("[!] Name cannot be empty.")
        return

    phone = input("Enter your 10-digit phone number: ").strip()
    if not (phone.isdigit() and len(phone) == 10):
        print("[!] Invalid phone number. Please enter a valid 10-digit number.")
        return

    pin = input("Create a 4-digit PIN: ").strip()
    if not (pin.isdigit() and len(pin) == 4):
        print("[!] Invalid PIN. PIN must be exactly 4 digits.")
        return

    confirm_pin = input("Confirm your 4-digit PIN: ").strip()
    if pin != confirm_pin:
        print("[!] PINs do not match. Account creation aborted.")
        return

    acc_num = generate_account_number(accounts)
    accounts[acc_num] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    record_transaction(accounts[acc_num], "ACCOUNT_OPEN", 0.0, 0.0, "Account initialized")
    save_data(accounts)

    print("\n" + "-" * 40)
    print("[✓] Account created successfully!")
    print(f"    Account Holder : {name}")
    print(f"    Account Number : {acc_num}")
    print("    Initial Balance: $0.00")
    print("    * Please remember your Account Number and PIN.")
    print("-" * 40)


def login(accounts):
    """Authenticate user with Account Number and PIN."""
    print("\n" + "=" * 40)
    print("          USER LOGIN")
    print("=" * 40)
    
    acc_num = input("Enter your 8-digit Account Number: ").strip()
    pin = input("Enter your 4-digit PIN: ").strip()

    user = accounts.get(acc_num)
    if user and user.get("pin") == pin:
        print(f"\n[✓] Welcome back, {user['name']}!")
        account_menu(acc_num, accounts)
    else:
        print("\n[!] Invalid Account Number or PIN. Please try again.")


def check_balance(user):
    """Display the current balance."""
    print("\n" + "-" * 35)
    print(f"Current Balance: ${user['balance']:,.2f}")
    print("-" * 35)


def deposit_money(user, accounts):
    """Process a deposit into the user's account."""
    print("\n" + "-" * 35)
    print("           DEPOSIT MONEY")
    print("-" * 35)
    try:
        amount = float(input("Enter amount to deposit: $"))
        if amount <= 0:
            print("[!] Deposit amount must be greater than zero.")
            return
    except ValueError:
        print("[!] Invalid amount entered.")
        return

    user["balance"] += amount
    record_transaction(user, "DEPOSIT", amount, user["balance"], "Self-deposit")
    save_data(accounts)

    print(f"\n[✓] Successfully deposited ${amount:,.2f}.")
    print(f"    Updated Balance: ${user['balance']:,.2f}")


def withdraw_money(user, accounts):
    """Process a withdrawal from the user's account."""
    print("\n" + "-" * 35)
    print("          WITHDRAW MONEY")
    print("-" * 35)
    try:
        amount = float(input("Enter amount to withdraw: $"))
        if amount <= 0:
            print("[!] Withdrawal amount must be greater than zero.")
            return
    except ValueError:
        print("[!] Invalid amount entered.")
        return

    if amount > user["balance"]:
        print(f"\n[!] Insufficient balance. Available: ${user['balance']:,.2f}")
        return

    user["balance"] -= amount
    record_transaction(user, "WITHDRAW", amount, user["balance"], "Cash withdrawal")
    save_data(accounts)

    print(f"\n[✓] Successfully withdrew ${amount:,.2f}.")
    print(f"    Updated Balance: ${user['balance']:,.2f}")


def transfer_money(sender_acc_num, user, accounts):
    """Transfer funds between two accounts."""
    print("\n" + "-" * 35)
    print("          TRANSFER MONEY")
    print("-" * 35)
    receiver_acc = input("Enter recipient's Account Number: ").strip()

    if receiver_acc == sender_acc_num:
        print("[!] Cannot transfer money to your own account.")
        return

    if receiver_acc not in accounts:
        print("[!] Recipient account not found.")
        return

    try:
        amount = float(input("Enter amount to transfer: $"))
        if amount <= 0:
            print("[!] Transfer amount must be greater than zero.")
            return
    except ValueError:
        print("[!] Invalid amount entered.")
        return

    if amount > user["balance"]:
        print(f"\n[!] Insufficient balance. Available: ${user['balance']:,.2f}")
        return

    recipient = accounts[receiver_acc]
    user["balance"] -= amount
    recipient["balance"] += amount

    record_transaction(
        user,
        "TRANSFER_SENT",
        amount,
        user["balance"],
        f"Transferred to Acc {receiver_acc} ({recipient['name']})"
    )
    record_transaction(
        recipient,
        "TRANSFER_RECEIVED",
        amount,
        recipient["balance"],
        f"Received from Acc {sender_acc_num} ({user['name']})"
    )

    save_data(accounts)

    print(f"\n[✓] Successfully transferred ${amount:,.2f} to {recipient['name']}.")
    print(f"    Updated Balance: ${user['balance']:,.2f}")


def view_transaction_history(user):
    """Display past transaction records."""
    print("\n" + "=" * 70)
    print("                         TRANSACTION HISTORY")
    print("=" * 70)
    transactions = user.get("transactions", [])

    if not transactions:
        print("No transactions found.")
        print("=" * 70)
        return

    print(f"{'Date & Time':<20} | {'Type':<17} | {'Amount':<10} | {'Balance After':<13}")
    print("-" * 70)
    for txn in transactions:
        sign = "+" if txn["type"] in ("DEPOSIT", "TRANSFER_RECEIVED") else "-"
        amt_str = f"{sign}${txn['amount']:,.2f}" if txn["amount"] > 0 else "$0.00"
        bal_str = f"${txn['balance_after']:,.2f}"
        print(f"{txn['timestamp']:<20} | {txn['type']:<17} | {amt_str:<10} | {bal_str:<13}")
        if txn.get("note"):
            print(f"  Note: {txn['note']}")
    print("=" * 70)


def change_pin(user, accounts):
    """Update account PIN."""
    print("\n" + "-" * 35)
    print("            CHANGE PIN")
    print("-" * 35)
    old_pin = input("Enter current PIN: ").strip()
    if old_pin != user["pin"]:
        print("[!] Incorrect current PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("[!] PIN must be exactly 4 digits.")
        return

    if new_pin == old_pin:
        print("[!] New PIN cannot be the same as the old PIN.")
        return

    confirm_new = input("Confirm new 4-digit PIN: ").strip()
    if new_pin != confirm_new:
        print("[!] PIN confirmation does not match.")
        return

    user["pin"] = new_pin
    save_data(accounts)
    print("\n[✓] PIN updated successfully.")


def account_menu(acc_num, accounts):
    """Render the operations menu for an authenticated user."""
    while True:
        user = accounts[acc_num]
        print("\n" + "=" * 35)
        print(f"    ACCOUNT MENU - {user['name'].upper()}")
        print("=" * 35)
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. View Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("=" * 35)

        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            check_balance(user)
        elif choice == "2":
            deposit_money(user, accounts)
        elif choice == "3":
            withdraw_money(user, accounts)
        elif choice == "4":
            transfer_money(acc_num, user, accounts)
        elif choice == "5":
            view_transaction_history(user)
        elif choice == "6":
            change_pin(user, accounts)
        elif choice == "7":
            print("\n[✓] Logged out successfully. Returning to main menu...")
            break
        else:
            print("[!] Invalid option. Please select 1 through 7.")


def main():
    """Main program loop."""
    accounts = load_data()
    while True:
        print("\n" + "=" * 40)
        print("    WELCOME TO THE BANKING SYSTEM")
        print("=" * 40)
        print("1. Create New Account")
        print("2. Login")
        print("3. Exit System")
        print("=" * 40)

        choice = input("Select an option (1-3): ").strip()
        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            login(accounts)
        elif choice == "3":
            print("\nThank you for using the Banking System. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
