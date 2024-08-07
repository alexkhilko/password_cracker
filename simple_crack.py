import string
from hashlib import md5


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

print(crack_password("7a95bf926a0333f57705aeac07a362a2", 4))