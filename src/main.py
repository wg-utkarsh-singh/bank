# Testing accounts:
# Manager:  id=52046, name="manager",  age=30, gender="M", password="12345"
# Cashier:  id=20493, name="cashier",  age=25, gender="M", password="12345"
# Customer: id=51164, name="customer", age=21, gender="M", password="12345", balance=1000

from pickle import dump, load

from bank import Bank


def demo_bank() -> Bank:
    bank = Bank()
    manager_id = bank.add_manager("manager", 30, "M", "12345")
    manager = bank.get_person(manager_id)
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
    test_filename = "..\\data\\data.pkl"
    dump_bank_data(demo_bank(), test_filename)
    bank = load_bank_data(test_filename)
    print(bank._persons)
    bank.manage()
