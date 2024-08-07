import string
from hashlib import md5
import argparse

def get_permutations(count: int, chars: list[str]):
    if count == 1:
        for char in chars:
            yield char
    else:
        prev_perms = get_permutations(count - 1, chars)
        for perm in prev_perms:
            for char in chars:
                yield perm + char 


def crack_password(hash: str, max_lenght: int = 4) -> str | None:
    if max_lenght > 5:
        raise ValueError("Maximum length of password is 5")
    permutations = get_permutations(max_lenght, list(string.ascii_letters) + list(string.digits))
    for permutation in permutations:
        if md5(permutation.encode("utf-8")).hexdigest() == hash:
            return permutation
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Password Cracker',
        description='Simple Password Cracker that allows to crack md5 encrypted passwords'
    )
    parser.add_argument("hash")
    args = parser.parse_args()
    print(crack_password(args.hash, 4))