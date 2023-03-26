from bank.account import BankAccount


class Menu:
    CUSTOMER = "1. Edit details\n2. Deposit\n3. Withdraw\n4. Print passbook\n5. Print comments\n6. Back to login"
    CASHIER = "1. Add customer\n2. Add comment\n3. Set balance\n4. Back to login"
    MANAGER = "1. Add cashier\n2. Process changes\n3. Block account\n4. Back to login"


class ErrorMsg:
    INVALID_PASS = "Invalid password. Retry!"
    ACCOUNT_NOT_FOUND = "Account not found. Retry!"
    ACCOUNT_BLOCKED = "Account blocked. Contact manager."
    INSUFFICIENT_BALANCE = f"Minimum balance must be ₹{BankAccount.MIN_BALANCE}. Retry!"
    PENDING_CHANGES_NOT_FOUND = "No pending changes found!"
    REJECTED_CHANGES_NOT_FOUND = "No rejected changes found!"


class SuccessMsg:
    CUSTOMER_ADDED = "Customer with id {} added to database."
    CASHIER_ADDED = "Cashier with id {} added to database."
    ACCOUNT_BLOCKED = "Bank account for customer with id {} blocked."
