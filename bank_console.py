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

    print(f"\nAccount created successfully!")
    print(f"Account ID: {next_account_id}")

    next_account_id += 1


if __name__ == "__main__":
    create_account()

    print("\nCurrent Accounts:")
    print(accounts)