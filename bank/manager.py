from bank.account import Account, BankAccount
from bank.bank import Bank
from bank.cashier import Cashier
from bank.constants import ErrorMsg, Menu, SuccessMsg
from bank.customer import Customer
from bank.person import Person
from helper.console import Input


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

    def add_cashier(
        self, name: str, age: int, gender: str, password: str
    ) -> tuple[int, Cashier]:
        acc = Account()
        id = acc.get_id()
        return id, Cashier(acc, name, age, gender, password)

    def process_change(self, customer: Customer, change: dict) -> bool:
        rslt = Input.general_details_change(customer.get_details(), change)
        if not rslt:
            return False
        else:
            self.set_customer_details(customer, **change)
            return True

    def block_account(self, bank_acc: BankAccount) -> None:
        bank_acc._is_open = False

    def _manage_add_cashier(self, bank: Bank) -> None:
        name, age, gender = Input.general_details().values()
        password = Input.password()
        id, person = self.add_cashier(name, age, gender, password)
        bank.add_person(id, person)
        print(SuccessMsg.CASHIER_ADDED.format(id))

    def _manage_process_changes(self, bank: Bank) -> None:
        if bank.num_of_pending_changes() == 0:
            print(ErrorMsg.PENDING_CHANGES_NOT_FOUND)
        else:
            customer, change = bank.get_pending_change()
            if not self.process_change(customer, change):
                cur = customer.get_details()
                bank.add_rejected_change(customer, cur, change)

    def _manage_block_account(self, bank: Bank) -> None:
        customer = bank.authenticate()
        bank_acc = customer.get_bank_account()
        if Input.proceed():
            self.block_account(bank_acc)
            print(SuccessMsg.ACCOUNT_BLOCKED.format(bank_acc.get_id()))

    def manage(self, bank: Bank) -> None:
        print(Menu.MANAGER)
        choice = Input.choice(1, 4)
        if choice == 1:
            self._manage_add_cashier(bank)
        elif choice == 2:
            self._manage_process_changes(bank)
        elif choice == 3:
            self._manage_block_account(bank)
        else:
            bank.manage()
            return

        if Input.proceed():
            self.manage(bank)
