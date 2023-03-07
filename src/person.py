from random import randint
from collections import deque

from account import Account, BankAccount
from exceptions import InvalidPassword


def get_id() -> int:
    lower = 10_000
    high = 99_999
    return randint(lower, high)


class Person:
    def _hash_func(self, key: str) -> int:
        rslt = 17
        mult = 13
        for ch in key:
            rslt += mult * ord(ch)
        return rslt

    def __init__(self, name: str, age: int, gender: str, password: str) -> None:
        self._name = name
        self._age = age
        self._gender = gender
        self._passhash = self._hash_func(password)

    def get_details(self) -> dict:
        return {"name": self._name, "age": self._age, "gender": self._gender}

    def login(self, password: str) -> None:
        if self._passhash != self._hash_func(password):
            raise InvalidPassword


class Customer(Person):
    def __init__(
        self, bank_acc: BankAccount, name: str, age: int, gender: str, password: str
    ) -> None:
        super().__init__(name, age, gender, password)
        self._bank_acc = bank_acc
        self._comment = deque()

    def get_bank_account(self) -> BankAccount:
        return self._bank_acc

    def get_comments(self) -> list:
        return self._comment

    def request_change(self) -> dict:
        try:
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            gender = input("Enter gender: ")
            return {"name": name, "age": age, "gender": gender}
        except ValueError:
            print("Invalid change. Retry!")
            return self.request_change()


class Cashier(Person):
    def __init__(
        self, acc: Account, name: str, age: int, gender: str, password: str
    ) -> None:
        super().__init__(name, age, gender, password)
        self._acc = acc

    def get_account(self) -> Account:
        return self._acc

    def add_customer(
        self, name: str, age: int, gender: str, password: str, balance: int
    ) -> tuple[int, Customer]:
        id = get_id()
        bank_acc = BankAccount(id, balance)
        return id, Customer(bank_acc, name, age, gender, password)

    def add_comment(self, customer: Customer, cur: dict, to: dict, comment) -> None:
        customer._comment.appendleft(f"Change {cur} -> {to} rejected as {comment}.")

    def set_balance(self, bank_acc: BankAccount, amount: int) -> None:
        balance = bank_acc.get_balance()
        if amount == balance:
            return
        elif amount > balance:
            bank_acc.deposit(amount - balance)
        else:
            bank_acc.withdraw(balance - amount)


class Manager(Person):
    def __init__(
        self, acc: Account, name: str, age: int, gender: str, password: str
    ) -> None:
        super().__init__(name, age, gender, password)
        self._acc = acc

    def get_account(self) -> Account:
        return self._acc

    def set_customer_details(
        self, customer: Customer, name: str, age: int, gender: str
    ) -> None:
        customer._name = name
        customer._age = age
        customer._gender = gender

    def process_change(self, customer: Customer, change: dict) -> bool:
        resp = input(f"Changing {customer.get_details()} -> {change}, continue(y/n): ")
        if not resp.startswith("y"):
            return False
        else:
            self.set_customer_details(customer, **change)
            return True

    def add_cashier(
        self, name: str, age: int, gender: str, password: str
    ) -> tuple[int, Cashier]:
        id = get_id()
        acc = Account(id)
        return id, Cashier(acc, name, age, gender, password)

    def block_account(self, bank_acc: BankAccount) -> None:
        bank_acc._is_open = False
