import string
from hashlib import md5
import argparse


def _generate_passwords(length: int, chars: list[str]):
    if length == 1:
        for char in chars:
            yield char
    else:
        prev_perms = _generate_passwords(length - 1, chars)
        for perm in prev_perms:
            for char in chars:
                yield perm + char


def _load_passwords(path: str, encoding="latin-1"):
    try:
        with open(path, "rb") as f:
            while line := f.readline():
                yield line.decode(encoding).strip()
    except FileNotFoundError as e:
        raise ValueError(f"Couldn't find file under {path} path") from e


def _generate_rainbow_table(
    filename: str, passwords_path: str, encoding: str = "latin-1"
):
    with open(filename, "w", encoding="latin-1") as file_to_write:
        with open(passwords_path, "r", encoding=encoding) as passwords_file:
            while pwd := passwords_file.readline():
                pwd = pwd.strip()
                hash_ = md5(pwd.encode("utf-8")).hexdigest()
                file_to_write.write(f"{hash_},{pwd},\n")


def _read_rainbow_table(path: str, encoding: "latin-1"):
    try:
        with open(path, "r", encoding=encoding) as f:
            while line := f.readline():
                try:
                    hash, password = line.split(",", 1)
                except Exception:
                    continue
                else:
                    yield hash, password
    except FileNotFoundError as e:
        raise ValueError(f"Couldn't find file under {path} path") from e


def crack_brute_force(hash: str, max_length: int = 4) -> str | None:
    passwords = _generate_passwords(
        max_length, list(string.ascii_letters) + list(string.digits)
    )
    for pwd in passwords:
        if md5(pwd.encode("utf-8")).hexdigest() == hash:
            return pwd
    return None


def crack_via_passwords_file(hash: str, path: str, encoding: str) -> str | None:
    passwords = _load_passwords(path, encoding)
    for pwd in passwords:
        if md5(pwd.encode("utf-8")).hexdigest() == hash:
            return pwd
    return None


def crack_via_rainbow_table(
    hash: str, path: str, encoding: str = "latin-1"
) -> str | None:
    for hash_, pwd in _read_rainbow_table(path, encoding):
        if hash_ == hash:
            return pwd
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Password Cracker",
        description="Simple Hash Cracker that allows to crack md5 encrypted passwords",
    )
    parser.add_argument("hash")
    parser.add_argument(
        "-p",
        "--passwords",
        help="Path to the list of common passwords that should be checked",
        default="",
    )
    parser.add_argument(
        "-l",
        "--length",
        help="Max length of password that should be used in brute force approach",
        type=int,
        choices=range(1, 5),
        default=4,
    )
    parser.add_argument("-r", "--rainbow_table_path", default="")
    parser.add_argument("-e", "--encoding", default="latin-1")
    args = parser.parse_args()
    if args.rainbow_table_path:
        password = crack_via_rainbow_table(
            hash=args.hash, path=args.rainbow_table_path, encoding=args.encoding
        )
    elif args.passwords:
        password = crack_via_passwords_file(
            hash=args.hash, path=args.passwords, encoding=args.encoding
        )
    else:
        password = crack_brute_force(hash=args.hash, max_length=args.length)
    if password is None:
        print("Password not found")
    else:
        print(f"Your password is: {password}")
