from collections import deque
from collections.abc import Callable
from functools import wraps
from getpass import getpass

import exceptions
from account import Account, BankAccount
from person import Cashier, Customer, Manager, Person, get_id


def handle_exception(func: Callable) -> Callable:
    @wraps(func)
    def wrapper_validate_input(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.AccountNotFound:
            print("Account not found. Retry!")
            return wrapper_validate_input(*args, **kwargs)
        except exceptions.InsufficientBalance:
            print(f"Minimum balance must be ₹{BankAccount.min_balance}. Retry!")
            return wrapper_validate_input(*args, **kwargs)
        except exceptions.InvalidPassword:
            print("Invalid password. Retry!")
            return wrapper_validate_input(*args, **kwargs)
        except ValueError:
            print("Invalid input. Retry!")
            return wrapper_validate_input(*args, **kwargs)
        except exceptions.BankAccountBlocked:
            print("Back account blocked. Contact manager!")

    return wrapper_validate_input


class Bank:
    def __init__(self) -> None:
        self._persons = {}
        self._pending_changes = deque()
        self._rejected_changes = deque()

    def get_person(self, id: int) -> Person:
        if person := self._persons.get(id, False):
            return person
        else:
            raise exceptions.AccountNotFound

    def num_of_pending_changes(self) -> int:
        return len(self._pending_changes)

    def num_of_rejected_changes(self) -> int:
        return len(self._rejected_changes)

    def get_pending_change(self) -> tuple[Person, dict]:
        return self._pending_changes.pop()

    def get_rejected_change(self) -> tuple[Person, dict, dict]:
        return self._rejected_changes.pop()

    def add_pending_change(self, person: Person, change: dict) -> None:
        self._pending_changes.appendleft((person, change))

    def add_rejected_change(self, person: Person, cur: dict, to: dict) -> None:
        self._rejected_changes.appendleft((person, cur, to))

    def add_person(self, id: int, account: Person) -> None:
        self._persons[id] = account

    def add_manager(self, name: str, age: int, gender: str, password: str) -> int:
        id = get_id()
        acc = Account(id)
        self.add_person(id, Manager(acc, name, age, gender, password))
        return id

    @handle_exception
    def _input_id(self) -> Person:
        id = int(input("Enter id: "))
        return self.get_person(id)

    @handle_exception
    def _authenticate(self) -> Person:
        person = self._input_id()
        password = getpass("Password: ")
        person.login(password)
        return person

    @handle_exception
    def _input_choice(self, low: int, high: int) -> int:
        choice = int(input(f"Enter choice: [{low}-{high}]: "))
        if low <= choice <= high:
            return choice
        return self._input_choice(low, high)

    @handle_exception
    def _input_amount(self):
        return int(input("Enter amount: "))

    @handle_exception
    def _deposit(self, bank_acc: BankAccount) -> None:
        amount = self._input_amount()
        bank_acc.deposit(amount)

    @handle_exception
    def _withdraw(self, bank_acc: BankAccount) -> None:
        amount = self._input_amount()
        bank_acc.withdraw(amount)

    @handle_exception
    def _input_continue(self) -> bool:
        choice = input("Do you want to continue(y/n): ")
        if choice.startswith("y"):
            return True
        elif choice.startswith("n"):
            return False
        else:
            raise ValueError

    def _manage_customer(self, customer: Customer) -> None:
        print(
            "1. Edit details\n2. Deposit\n3. Withdraw\n4. Print passbook\n5. Print comments\n6. Back to login"
        )
        choice = self._input_choice(1, 6)

        if choice == 6:
            self.manage()
            return

        if choice == 1:
            change = customer.request_change()
            self.add_pending_change(customer, change)
        elif choice == 2:
            acc = customer.get_bank_account()
            self._deposit(acc)
        elif choice == 3:
            acc = customer.get_bank_account()
            self._withdraw(acc)
        elif choice == 4:
            acc = customer.get_bank_account()
            passbook = acc.get_passbook()
            for statements in passbook:
                print(statements)
        elif choice == 5:
            comments = customer.get_comments()
            for comment in comments:
                print(comment)

        if self._input_continue():
            self._manage_customer(customer)

    @handle_exception
    def _input_details(self, person: Person) -> tuple[int, Person]:
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        gen = input("Enter gender: ")
        password = getpass("Enter password: ")
        if isinstance(person, Manager):
            return person.add_cashier(name, age, gen, password)
        balance = int(input("Enter balance: "))
        return person.add_customer(name, age, gen, password, balance)

    @handle_exception
    def _input_set_balance(self, cashier: Cashier) -> None:
        customer = self._input_id()
        bank_acc = customer.get_bank_account()
        amount = self._input_amount()
        cashier.set_balance(bank_acc, amount)

    def _manage_cashier(self, cashier: Cashier) -> None:
        print(
            "1. Add customer\n2. Add comment\n3. Set customer's balance\n4. Back to login"
        )
        choice = self._input_choice(1, 4)

        if choice == 4:
            self.manage()
            return

        if choice == 1:
            id, customer = self._input_details(cashier)
            print(f"Customer with id {id} added to database.")
            self.add_person(id, customer)
        elif choice == 2:
            if self.num_of_rejected_changes() == 0:
                print("No rejected changes found!")
            else:
                customer, cur, to = self.get_rejected_change()
                print(f"Rejected change: {cur} -> {to}")
                comment = input("Enter comment: ")
                cashier.add_comment(customer, cur, to, comment)
        elif choice == 3:
            self._input_set_balance(cashier)

        if self._input_continue():
            self._manage_cashier(cashier)

    def _manage_manager(self, manager: Manager) -> None:
        print("1. Add cashier\n2. Process changes\n3. Block account\n4. Back to login")
        choice = self._input_choice(1, 4)

        if choice == 4:
            self.manage()
            return

        if choice == 1:
            id, cashier = self._input_details(manager)
            print(f"Cashier with id {id} added to database.")
            self.add_person(id, cashier)
        elif choice == 2:
            if self.num_of_pending_changes() == 0:
                print("No pending changes found!")
            else:
                customer, change = self.get_pending_change()
                if not manager.process_change(customer, change):
                    cur = customer.get_details()
                    self.add_rejected_change(customer, cur, change)
        elif choice == 3:
            customer = self._input_id()
            bank_acc = customer.get_bank_account()
            if self._input_continue():
                manager.block_account(bank_acc)
                print(f"Bank account for customer with id {bank_acc.get_id()} blocked.")

        if self._input_continue():
            self._manage_manager(manager)

    def manage(self) -> None:
        person = self._authenticate()
        name = person.get_details()["name"]
        if isinstance(person, Customer):
            acc = person.get_bank_account()
            if not acc.get_status():
                print("Your account has been blocked. Contact manager!")
                self.manage()
            else:
                balance = acc.get_balance()
                print(f"Hello customer {name}, your current balance is: {balance}")
                self._manage_customer(person)
        elif isinstance(person, Cashier):
            num = self.num_of_rejected_changes()
            print(f"Hello cashier {name}, no. of rejected changes are: {num}")
            self._manage_cashier(person)
        elif isinstance(person, Manager):
            num = self.num_of_pending_changes()
            print(f"Hello manager {name}, no. of pending changes are: {num}")
            self._manage_manager(person)
