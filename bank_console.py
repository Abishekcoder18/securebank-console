from dataclasses import dataclass


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


accounts: dict[int, Account] = {}
transactions: dict[int, list[Transaction]] = {}
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
    transactions[next_account_id] = []

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

    del accounts[account_id]
    del transactions[account_id]

    print("\nAccount closed successfully.")


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

        try:

            if choice == "1":
                create_account()

            elif choice == "2":
                deposit()

            elif choice == "3":
                withdraw()

            elif choice == "4":
                check_balance()

            elif choice == "5":
                close_account()

            elif choice == "6":
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