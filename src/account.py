from collections import deque

from exceptions import InsufficientBalance


class Account:
    def __init__(self, id: int) -> None:
        self._id = id

    def get_id(self) -> int:
        return self._id


class BankAccount(Account):
    min_balance = 100

    def __new__(cls, id: int, balance: int) -> Account:
        if balance < BankAccount.min_balance:
            raise InsufficientBalance
        else:
            return super().__new__(cls)

    def __getnewargs__(self) -> tuple[int, int]:
        return self._id, self._balance

    def __init__(self, id: int, balance: int) -> None:
        super().__init__(id)
        self._balance = balance
        self._passbook = deque()

    def get_balance(self) -> int:
        return self._balance

    def get_passbook(self) -> list[str]:
        return self._passbook

    def _add_statement(self, statement: str) -> None:
        self._passbook.appendleft(statement)

    def deposit(self, amount: int) -> None:
        self._balance += amount
        self._add_statement(f"₹{amount} deposited")

    def withdraw(self, amount: int) -> None:
        if self._balance - amount < BankAccount.min_balance:
            raise InsufficientBalance
        self._balance -= amount
        self._add_statement(f"₹{amount} withdrawn")
