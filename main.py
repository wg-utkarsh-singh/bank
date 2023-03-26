# Testing accounts:
# Manager:  id=40649, name="manager",  age=30, gender="M", password="12345"
# Cashier:  id=27331, name="cashier",  age=25, gender="M", password="12345"
# Customer: id=44846, name="customer", age=21, gender="M", password="12345", balance=1000

from pickle import dump, load

from bank.bank import Bank
from bank.account import Account
from bank.manager import Manager


def demo_bank() -> Bank:
    bank = Bank()

    acc = Account()
    manager = Manager(acc, "manager", 30, "M", "12345")
    bank.add_person(acc.get_id(), manager)

    cashier_id, cashier = manager.add_cashier("cashier", 25, "M", "12345")
    bank.add_person(cashier_id, cashier)

    customer_id, customer = cashier.add_customer("customer", 21, "M", "12345", 1000)
    bank.add_person(customer_id, customer)

    return bank


def dump_bank_data(bank: Bank, filename: str) -> None:
    with open(filename, "wb") as f:
        dump(bank, f)


def load_bank_data(filename: str) -> Bank:
    with open(filename, "rb") as f:
        return load(f)


if __name__ == "__main__":
    test_filename = "data/data.pkl"
    bank = load_bank_data(test_filename)
    bank.manage()
