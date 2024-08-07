import string
from hashlib import md5
import argparse

def generate_passwords(length: int, chars: list[str]):
    if length == 1:
        for char in chars:
            yield char
    else:
        prev_perms = generate_passwords(length - 1, chars)
        for perm in prev_perms:
            for char in chars:
                yield perm + char


def load_passwords(path: str, encoding='latin-1'):
    try:
        with open(path, "rb") as f:
            while line := f.readline():
                yield line.decode(encoding).strip()
    except FileNotFoundError as e:
        raise ValueError(f"Couldn't find file under {path} path") from e


def crack_password(hash: str, passwords_path: str, max_length: int = 4) -> str | None:
    if passwords_path:
        passwords = load_passwords(passwords_path)
    else:
        passwords = generate_passwords(max_length, list(string.ascii_letters) + list(string.digits))
    for pwd in passwords:
        if md5(pwd.encode("utf-8")).hexdigest() == hash:
            return pwd
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Password Cracker',
        description='Simple Password Cracker that allows to crack md5 encrypted passwords'
    )
    parser.add_argument("hash")
    parser.add_argument(
        "-p",
        "--passwords",
        help="Path to the list of common passwords that should be checked",
        default=""
    )
    parser.add_argument(
        "-l",
        "--length",
        help="Max length of password that should be used in brute force approach",
        type=int,
        choices=range(1, 5),
        default=4
    )
    args = parser.parse_args()
    password = crack_password(
        hash=args.hash,
        max_length=int(args.length),
        passwords_path=args.passwords
    )
    if password is None:
        print("Password not found")
    else:
        print(f"Your password is: {password}")
