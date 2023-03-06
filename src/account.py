from collections import deque

from exceptions import InsufficientBalance, BankAccountBlocked


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
        self._is_open = True

    def get_balance(self) -> int:
        if not self._is_open:
            raise BankAccountBlocked
        return self._balance

    def get_passbook(self) -> list[str]:
        if not self._is_open:
            raise BankAccountBlocked
        return self._passbook

    def get_status(self):
        return self._is_open

    def _add_statement(self, statement: str) -> None:
        self._passbook.appendleft(statement)

    def deposit(self, amount: int) -> None:
        if not self._is_open:
            raise BankAccountBlocked
        self._balance += amount
        self._add_statement(f"₹{amount} deposited. Balance: ₹{self._balance}")

    def withdraw(self, amount: int) -> None:
        if not self._is_open:
            raise BankAccountBlocked
        if self._balance - amount < BankAccount.min_balance:
            raise InsufficientBalance
        self._balance -= amount
        self._add_statement(f"₹{amount} withdrawn. Balance: ₹{self._balance}")
