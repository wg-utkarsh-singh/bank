from getpass import getpass


class Input:
    @staticmethod
    def id() -> int:
        try:
            rslt = int(input("Enter id: "))
        except ValueError:
            print("Invalid input. Retry!")
            return Input.id()
        else:
            return rslt

    @staticmethod
    def choice(low: int, high: int) -> int:
        try:
            rslt = int(input(f"Enter choice: [{low}-{high}]: "))
        except ValueError:
            print("Invalid input. Retry!")
            return Input.choice(low, high)
        else:
            if low <= rslt <= high:
                return rslt
            return Input.choice(low, high)

    @staticmethod
    def amount() -> int:
        try:
            rslt = int(input("Enter amount: "))
        except ValueError:
            print("Invalid input. Retry!")
            return Input.amount()
        else:
            return rslt

    @staticmethod
    def proceed() -> bool:
        rslt = input("Do you want to proceed(y/n): ")
        if rslt.startswith("y"):
            return True
        elif rslt.startswith("n"):
            return False
        else:
            print("Response must start with a 'y' or 'n'. Retry!")
            return Input.proceed()

    @staticmethod
    def password() -> str:
        return getpass("Password: ")

    @staticmethod
    def general_details() -> dict:
        try:
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            gender = input("Enter gender: ")
        except ValueError:
            print("Invalid details. Retry!")
            return Input.general_details()
        else:
            return {"name": name, "age": age, "gender": gender}

    @staticmethod
    def comment() -> str:
        rslt = input("Enter comment: ")
        if len(rslt) >= Input.min_comment_length:
            return rslt
        else:
            print("Please write a more descriptive comment.")
            return Input.comment()

    @staticmethod
    def general_details_change(prev: str, to: str) -> bool:
        rslt = input(f"Changing {prev} -> {to}, continue(y/n): ")
        if rslt.startswith("y"):
            return True
        elif rslt.startswith("n"):
            return False
        else:
            print("Response must start with a 'y' or 'n'. Retry!")
            return Input.general_details_change(prev, to)
