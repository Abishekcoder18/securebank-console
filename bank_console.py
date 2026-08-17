"""
SecureBank Console Application

Week 1:
- Account Management
- Deposit and Withdraw
- Balance Inquiry
- Close Account

Week 2:
- Transaction History
- Money Transfer
- Transaction Reversal
- Customer Search using defaultdict
"""

from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Account:
    id: int
    customer_name: str
    balance: float


@dataclass
class Transaction:
    transaction_type: str
    amount: float
    source_account: int
    target_account: int | None = None


# In-memory storage
accounts: dict[int, Account] = {}
transactions: dict[int, list[Transaction]] = {}
customer_index: defaultdict[str, list[int]] = defaultdict(list)
next_account_id = 1


# Custom Exceptions
class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


# Account & Transaction Operations

def create_account():
    global next_account_id

    customer_name = input("Enter customer name: ")

    account = Account(
        id=next_account_id,
        customer_name=customer_name,
        balance=0.0
    )

    accounts[next_account_id] = account
    transactions[next_account_id] = []
    customer_index[customer_name].append(next_account_id)

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

    transactions[account_id].append(
        Transaction(
            transaction_type="Deposit",
            amount=amount,
            source_account=account_id
        )
    )

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

    transactions[account_id].append(
        Transaction(
            transaction_type="Withdraw",
            amount=amount,
            source_account=account_id
        )
    )

    print("\nWithdrawal Successful!")
    print(f"Current Balance: ₹{accounts[account_id].balance}")


def transfer():

    from_account = int(input("From Account ID: "))
    to_account = int(input("To Account ID: "))
    amount = float(input("Transfer Amount: "))

    if from_account not in accounts:
        raise AccountNotFoundError("Source account not found.")

    if to_account not in accounts:
        raise AccountNotFoundError("Destination account not found.")

    if amount <= 0:
        print("Transfer amount must be greater than zero.")
        return

    if amount > accounts[from_account].balance:
        raise InsufficientFundsError("Insufficient balance.")

    # Save original balances for rollback
    original_from_balance = accounts[from_account].balance
    original_to_balance = accounts[to_account].balance

    try:

        accounts[from_account].balance -= amount
        accounts[to_account].balance += amount

        transactions[from_account].append(
            Transaction(
                transaction_type="Transfer Out",
                amount=amount,
                source_account=from_account,
                target_account=to_account
            )
        )

        transactions[to_account].append(
            Transaction(
                transaction_type="Transfer In",
                amount=amount,
                source_account=from_account,
                target_account=to_account
            )
        )

        print("\nTransfer Successful!")

    except Exception:

        accounts[from_account].balance = original_from_balance
        accounts[to_account].balance = original_to_balance

        raise


def find_accounts_by_customer():

    customer_name = input("Enter Customer Name: ")

    if customer_name not in customer_index:
        print("Customer not found.")
        return

    print(f"\nAccounts for {customer_name}:")

    for account_id in customer_index[customer_name]:

        if account_id in accounts:

            print(
                f"Account ID: {account_id}, "
                f"Balance: ₹{accounts[account_id].balance}"
            )


def reverse_last_transaction():

    account_id = int(input("Enter Account ID: "))

    if account_id not in accounts:
        raise AccountNotFoundError("Account not found.")

    if not transactions[account_id]:
        print("No transactions to reverse.")
        return

    last_transaction = transactions[account_id].pop()

    if last_transaction.transaction_type == "Deposit":

        accounts[account_id].balance -= last_transaction.amount

    elif last_transaction.transaction_type == "Withdraw":

        accounts[account_id].balance += last_transaction.amount

    elif last_transaction.transaction_type == "Transfer Out":

        target = last_transaction.target_account

        accounts[account_id].balance += last_transaction.amount
        accounts[target].balance -= last_transaction.amount

        transactions[target].pop()

    elif last_transaction.transaction_type == "Transfer In":

        print("Reverse from the source account only.")

        transactions[account_id].append(last_transaction)

    print("Last transaction reversed successfully.")


def check_balance():

    account_id = int(input("Enter Account ID: "))

    if account_id not in accounts:
        raise AccountNotFoundError("Account not found.")

    print(f"\nCustomer Name : {accounts[account_id].customer_name}")
    print(f"Current Balance : ₹{accounts[account_id].balance}")


def close_account():

    account_id = int(input("Enter Account ID: "))

    if account_id not in accounts:
        raise AccountNotFoundError("Account not found.")

    # Remove account from customer index
    customer_name = accounts[account_id].customer_name
    customer_index[customer_name].remove(account_id)

    # Remove empty customer entry
    if not customer_index[customer_name]:
        del customer_index[customer_name]

    del accounts[account_id]
    del transactions[account_id]

    print("\nAccount closed successfully.")


# CLI Application

if __name__ == "__main__":

    while True:

        print("\n===== SecureBank =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Reverse Last Transaction")
        print("6. Find Customer Accounts")
        print("7. Check Balance")
        print("8. Close Account")
        print("9. Exit")

        choice = input("Enter your choice: ")

        try:

            if choice == "1":
                create_account()

            elif choice == "2":
                deposit()

            elif choice == "3":
                withdraw()

            elif choice == "4":
                transfer()

            elif choice == "5":
                reverse_last_transaction()

            elif choice == "6":
                find_accounts_by_customer()

            elif choice == "7":
                check_balance()

            elif choice == "8":
                close_account()

            elif choice == "9":
                print("\nThank you for using SecureBank!")
                break

            else:
                print("Invalid Choice.")

        except AccountNotFoundError as e:
            print(e)

        except InsufficientFundsError as e:
            print(e)

        except ValueError:
            print("Please enter valid numeric input.")