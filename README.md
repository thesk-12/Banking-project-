# Banking System – Mini Project

A menu-driven Python application simulating real-world banking operations including account creation, secure login, deposits, withdrawals, fund transfers, and transaction tracking.

## Features
- **Account Creation**: Automatically generates unique 8-digit account numbers and securely sets up a 4-digit PIN.
- **Authentication**: Validates users using their Account Number and PIN.
- **Deposit & Withdrawal**: Input validation preventing negative transactions and checking for sufficient funds.
- **Fund Transfers**: Direct balance transfers between accounts.
- **Transaction History**: Timestamped records for all deposits, withdrawals, and transfers using Python's `datetime` module.
- **PIN Management**: Allows updating PIN with verification checks.
- **Data Persistence**: Automatically stores and retrieves account details via `bank_data.json`.

## Technologies & Modules Used
- Python 3
- `random` (for account number generation)
- `datetime` (for timestamping transactions)
- `json` & `os` (for persistent storage)

## How to Run
```bash
python banking_system.py
