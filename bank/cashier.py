from bank.account import Account, BankAccount
from bank.bank import Bank
from bank.constants import ErrorMsg, Menu, SuccessMsg
from bank.customer import Customer
from bank.exceptions import InsufficientBalance
from bank.person import Person
from helper.console import Input


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
        bank_acc = BankAccount(balance)
        return bank_acc.get_id(), Customer(bank_acc, name, age, gender, password)

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

    def _manage_add_customer(self, bank: Bank) -> None:
        name, age, gender = Input.general_details().values()
        password = Input.password()
        balance = Input.amount()
        try:
            id, customer = self.add_customer(name, age, gender, password, balance)
        except InsufficientBalance:
            print(ErrorMsg.INSUFFICIENT_BALANCE)
            self.manage(bank)
        else:
            bank.add_person(id, customer)
            print(SuccessMsg.CUSTOMER_ADDED.format(id))

    def _manage_add_comment(self, bank: Bank) -> None:
        if bank.num_of_rejected_changes() == 0:
            print(ErrorMsg.REJECTED_CHANGES_NOT_FOUND)
        else:
            customer, cur, to = bank.get_rejected_change()
            print(f"Rejected change: {cur} -> {to}")
            comment = Input.comment()
            self.add_comment(customer, cur, to, comment)

    def _manage_set_balance(self, bank: Bank) -> None:
        customer = bank.authenticate()
        if not isinstance(customer, Customer):
            print(ErrorMsg.ACCOUNT_NOT_FOUND)
            self._manage_set_balance(bank)

        bank_acc = customer.get_bank_account()
        if not bank_acc.is_open():
            print(ErrorMsg.ACCOUNT_BLOCKED)
            return

        try:
            amount = Input.amount()
            self.set_balance(bank_acc, amount)
        except InsufficientBalance:
            print(ErrorMsg.INSUFFICIENT_BALANCE)
            self._manage_set_balance(bank)

    def manage(self, bank: Bank) -> None:
        print(Menu.CASHIER)
        choice = Input.choice(1, 4)
        if choice == 1:
            self._manage_add_customer(bank)
        elif choice == 2:
            self._manage_add_comment(bank)
        elif choice == 3:
            self._manage_set_balance(bank)
        else:
            bank.manage()
            return

        if Input.proceed():
            self.manage(bank)
