from dataclasses import dataclass


@dataclass
class Account:
    id: int
    customer_name: str
    balance: float


accounts = {}
next_account_id = 1


class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


def create_account():
    global next_account_id

    customer_name = input("Enter customer name: ")

    account = Account(
        id=next_account_id,
        customer_name=customer_name,
        balance=0.0
    )

    accounts[next_account_id] = account

    print("\nAccount created successfully!")
    print(f"Account ID: {next_account_id}")

    next_account_id += 1


def deposit():

    account_id = int(input("Enter Account ID: "))
    amount = float(input("Enter Deposit Amount: "))

    if account_id not in accounts:
        raise AccountNotFoundError("Account not found.")

    if amount <= 0:
        print("Deposit amount must be greater than zero.")
        return

    accounts[account_id].balance += amount

    print("\nDeposit Successful!")
    print(f"Current Balance: ₹{accounts[account_id].balance}")
    
def withdraw():

    account_id = int(input("Enter Account ID: "))
    amount = float(input("Enter Withdrawal Amount: "))

    if account_id not in accounts:
        raise AccountNotFoundError("Account not found.")

    if amount <= 0:
        print("Withdrawal amount must be greater than zero.")
        return

    if amount > accounts[account_id].balance:
        raise InsufficientFundsError("Insufficient balance.")

    accounts[account_id].balance -= amount

    print("\nWithdrawal Successful!")
    print(f"Current Balance: ₹{accounts[account_id].balance}")

if __name__ == "__main__":

    while True:
        print("\n===== SecureBank =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Close Account")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "6":
            print("Thank you for using SecureBank!")
            break
        else:
            print("Feature coming soon...")