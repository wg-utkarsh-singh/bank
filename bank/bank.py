from collections import deque

from bank.constants import ErrorMsg
from bank.exceptions import AccountNotFound, InvalidPassword
from bank.person import Person
from helper.console import Input


class Bank:
    def __init__(self) -> None:
        self._persons = {}
        self._pending_changes = deque()
        self._rejected_changes = deque()

    def get_person(self, id: int) -> Person:
        if person := self._persons.get(id, False):
            return person
        else:
            raise AccountNotFound

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

    def add_person(self, id: int, person: Person) -> None:
        self._persons[id] = person

    def authenticate(self) -> Person:
        try:
            id = Input.id()
            person = self.get_person(id)
            password = Input.password()
            person.login(password)
        except AccountNotFound:
            print(ErrorMsg.ACCOUNT_NOT_FOUND)
            return self.authenticate()
        except InvalidPassword:
            print(ErrorMsg.INVALID_PASS)
            return self.authenticate()
        else:
            return person

    def manage(self) -> None:
        person = self.authenticate()
        person.manage(self)
        if Input.proceed():
            self.manage()
