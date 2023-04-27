from hashlib import sha256


def hash_password(password):
    return sha256(password.encode("utf-8")).hexdigest()
