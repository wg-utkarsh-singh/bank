from collections import deque
from collections.abc import Callable
from getpass import getpass

from account import Account, BankAccount
from exceptions import AccountNotFound, InsufficientBalance, InvalidPassword
from person import Cashier, Customer, Manager, Person, get_id


def get_validated_input(callback: Callable, *args, **kwargs):
    try:
        return callback(*args, **kwargs)
    except AccountNotFound:
        print("Account not found. Retry!")
        return get_validated_input(callback, *args, **kwargs)
    except InsufficientBalance:
        print(f"Minimum balance must be ₹{BankAccount.min_balance}. Retry!")
        return get_validated_input(callback, *args, **kwargs)
    except InvalidPassword:
        print("Invalid password. Retry!")
        return get_validated_input(callback, *args, **kwargs)
    except ValueError:
        print("Invalid input. Retry!")
        return get_validated_input(callback, *args, **kwargs)


class Bank:
    def __init__(self) -> None:
        self._persons = {}
        self._pending_changes = deque()

    def get_person(self, id: int) -> Person:
        if acc := self._persons.get(id, False):
            return acc
        else:
            raise AccountNotFound

    def num_of_pending_changes(self) -> int:
        return len(self._pending_changes)

    def get_pending_change(self) -> tuple[Person, dict]:
        return self._pending_changes.pop()

    def add_pending_change(self, person: Person, change: dict) -> None:
        self._pending_changes.appendleft((person, change))

    def add_person(self, id: int, account: Person) -> None:
        self._persons[id] = account

    def add_manager(self, name: str, age: int, gender: str, password: str) -> int:
        id = get_id()
        acc = Account(id)
        self.add_person(id, Manager(acc, name, age, gender, password))
        return id

    def _authenticate(self) -> Person:
        id = int(input("Enter id: "))
        person = self.get_person(id)
        password = getpass("Password: ")
        person.login(password)
        return person

    def _input_choice(self, low: int, high: int) -> int:
        choice = int(input(f"Enter choice: [{low}-{high}]: "))
        if low <= choice <= high:
            return choice
        return self._input_choice(low, high)

    def _deposit(self, bank_acc: BankAccount) -> None:
        amount = int(input("Enter amount: "))
        bank_acc.deposit(amount)

    def _withdraw(self, bank_acc: BankAccount) -> None:
        amount = int(input("Enter amount: "))
        bank_acc.withdraw(amount)

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
            "1. Edit details\n2. Deposit\n3. Withdraw\n4. Print passbook\n5. Back to login"
        )
        choice = get_validated_input(self._input_choice, 1, 5)

        if choice == 5:
            self.manage()
            return

        if choice == 1:
            change = customer.request_change()
            self.add_pending_change(customer, change)
        elif choice == 2:
            acc = customer.get_bank_account()
            get_validated_input(self._deposit, acc)
        elif choice == 3:
            acc = customer.get_bank_account()
            get_validated_input(self._withdraw, acc)
        elif choice == 4:
            acc = customer.get_bank_account()
            passbook = acc.get_passbook()
            for statements in passbook:
                print(statements)

        if get_validated_input(self._input_continue):
            self._manage_customer(customer)

    def _input_person(self, person: Person) -> tuple[int, Person]:
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        gen = input("Enter gender: ")
        password = getpass("Enter password: ")
        if isinstance(person, Manager):
            return person.add_cashier(name, age, gen, password)
        balance = int(input("Enter balance: "))
        return person.add_customer(name, age, gen, password, balance)

    def _manage_cashier(self, cashier: Cashier) -> None:
        print("1. Add customer\n2. Back to login")
        choice = get_validated_input(self._input_choice, 1, 2)

        if choice == 2:
            self.manage()
            return

        if choice == 1:
            id, customer = get_validated_input(self._input_person, cashier)
            print(f"Customer with id {id} added to database.")
            self.add_person(id, customer)

        if get_validated_input(self._input_continue):
            self._manage_cashier(cashier)

    def _manage_manager(self, manager: Manager) -> None:
        print("1. Add cashier\n2. Process changes\n3. Back to login")
        choice = get_validated_input(self._input_choice, 1, 3)

        if choice == 3:
            self.manage()
            return

        if choice == 1:
            id, cashier = self._input_person(manager)
            print(f"Cashier with id {id} added to database.")
            self.add_person(id, cashier)
        elif choice == 2:
            if self.num_of_pending_changes() == 0:
                print("No pending changes found!")
            else:
                customer, change = self.get_pending_change()
                if not manager.process_change(customer, change):
                    self.add_pending_change(customer, change)

        if get_validated_input(self._input_continue):
            self._manage_manager(manager)

    def manage(self) -> None:
        person = get_validated_input(self._authenticate)
        name = person.get_details()["name"]
        if isinstance(person, Customer):
            acc = person.get_bank_account()
            balance = acc.get_balance()
            print(f"Hello customer {name}, your current balance is: {balance}")
            self._manage_customer(person)
        elif isinstance(person, Cashier):
            print(f"Hello cashier {name}.")
            self._manage_cashier(person)
        elif isinstance(person, Manager):
            num = self.num_of_pending_changes()
            print(f"Hello manager {name}, no. of pending changes are: {num}")
            self._manage_manager(person)
