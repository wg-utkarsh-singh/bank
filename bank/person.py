from hashlib import sha256

from bank.exceptions import InvalidPassword


def get_hash(password) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


class Person:
    def __init__(self, name: str, age: int, gender: str, password: str) -> None:
        self._name = name
        self._age = age
        self._gender = gender
        self._passhash = get_hash(password)

    def get_details(self) -> dict:
        return {"name": self._name, "age": self._age, "gender": self._gender}

    def login(self, password: str) -> None:
        if self._passhash != get_hash(password):
            raise InvalidPassword
