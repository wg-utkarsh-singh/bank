from collections import deque
from collections.abc import Iterator

from bank.account import BankAccount
from bank.bank import Bank
from bank.constants import ErrorMsg, Menu
from bank.exceptions import InsufficientBalance
from bank.person import Person
from helper.console import Input


class Customer(Person):
    def __init__(
        self, bank_acc: BankAccount, name: str, age: int, gender: str, password: str
    ) -> None:
        super().__init__(name, age, gender, password)
        self._bank_acc = bank_acc
        self._comment = deque()

    def get_bank_account(self) -> BankAccount:
        return self._bank_acc

    def get_comments(self) -> Iterator[str]:
        return self._comment

    def request_change(self) -> dict:
        return Input.general_details()

    def _manage_edit_details(self, bank: Bank) -> None:
        change = self.request_change()
        bank.add_pending_change(self, change)

    def _manage_deposit(self, bank: Bank) -> None:
        bank_acc = self.get_bank_account()
        amount = Input.amount()
        bank_acc.deposit(amount)

    def _manage_withdraw(self, bank: Bank) -> None:
        bank_acc = self.get_bank_account()
        amount = Input.amount()
        try:
            bank_acc.withdraw(amount)
        except InsufficientBalance:
            print(ErrorMsg.INSUFFICIENT_BALANCE)

    def _manage_print_passbook(self, bank: Bank) -> None:
        bank_acc = self.get_bank_account()
        passbook = bank_acc.get_passbook()
        for statements in passbook:
            print(statements)

    def _manage_print_comments(self, bank: Bank) -> None:
        comments = self.get_comments()
        for comment in comments:
            print(comment)

    def manage(self, bank: Bank) -> None:
        bank_acc = self.get_bank_account()
        if not bank_acc.is_open():
            print(ErrorMsg.ACCOUNT_BLOCKED)
            return

        print(Menu.CUSTOMER)
        choice = Input.choice(1, 6)
        if choice == 1:
            self._manage_edit_details(bank)
        elif choice == 2:
            self._manage_deposit(bank)
        elif choice == 3:
            self._manage_withdraw(bank)
        elif choice == 4:
            self._manage_print_passbook(bank)
        elif choice == 5:
            self._manage_print_comments(bank)
        else:
            bank.manage()
            return

        if Input.proceed():
            self.manage(bank)
