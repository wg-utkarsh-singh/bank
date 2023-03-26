from collections import deque
from random import randint

from bank.exceptions import AccountBlocked, InsufficientBalance


def get_id() -> int:
    low = 10_000
    high = 99_999
    return randint(low, high)


class Account:
    def __init__(self) -> None:
        self._id = get_id()

    def get_id(self) -> int:
        return self._id


class BankAccount(Account):
    MIN_BALANCE = 100

    def __new__(cls, balance: int) -> Account:
        if balance < BankAccount.MIN_BALANCE:
            raise InsufficientBalance
        else:
            return super().__new__(cls)

    def __getnewargs__(self) -> tuple[int]:
        return (self._balance,)

    def __init__(self, balance: int) -> None:
        super().__init__()
        self._balance = balance
        self._passbook = deque()
        self._is_open = True

    def get_balance(self) -> int:
        if not self._is_open:
            raise AccountBlocked
        return self._balance

    def get_passbook(self) -> list[str]:
        if not self._is_open:
            raise AccountBlocked
        return self._passbook

    def is_open(self):
        return self._is_open

    def _add_statement(self, statement: str) -> None:
        self._passbook.appendleft(statement)

    def deposit(self, amount: int) -> None:
        if not self._is_open:
            raise AccountBlocked
        self._balance += amount
        self._add_statement(f"₹{amount} deposited. Balance: ₹{self._balance}")

    def withdraw(self, amount: int) -> None:
        if not self._is_open:
            raise AccountBlocked
        if self._balance - amount < BankAccount.MIN_BALANCE:
            raise InsufficientBalance
        self._balance -= amount
        self._add_statement(f"₹{amount} withdrawn. Balance: ₹{self._balance}")
