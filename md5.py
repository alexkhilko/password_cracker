from bitarray import bitarray
import math

WORD_SIZE = 32
INIT_BUFFER = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]


def _get_block_bit_array(input: bytes) -> bitarray:
    msg = bytearray(input)
    msg_len_in_bits = (8 * len(msg)) & 0xFFFFFFFFFFFFFFFF
    msg.append(0x80)

    while len(msg) % 64 != 56:
        msg.append(0)
    msg += msg_len_in_bits.to_bytes(8, byteorder="little")
    a = bitarray(endian="little")
    a.frombytes(bytes(msg))
    return a


def _to_hex(digest):
    raw = digest.to_bytes(16, byteorder="little")
    return "{:032x}".format(int.from_bytes(raw, byteorder="big"))


def rotate_left(x, amount):
    x &= 0xFFFFFFFF
    return (x << amount | x >> (32 - amount)) & 0xFFFFFFFF


def modular_add(x, y):
    return (x + y) & 0xFFFFFFFF


def get_md5_hash(input: str):
    bits = _get_block_bit_array(input.encode("ascii"))
    constants = [int(abs(math.sin(i + 1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]
    rotate_by = [
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
    ]
    init_temp = INIT_BUFFER[:]
    a, b, c, d = init_temp

    for i in range(64):
        if 0 <= i <= 15:
            f = (b & c) | (~b & d)
            g = i
        elif 16 <= i <= 31:
            f = (d & b) | (~d & c)
            g = (5 * i + 1) % 16
        elif 32 <= i <= 47:
            f = b ^ c ^ d
            g = (3 * i + 5) % 16
        else:
            f = c ^ (b | ~d)
            g = (7 * i) % 16

        to_rotate = (
            a
            + f
            + constants[i]
            + int.from_bytes(
                (bits[WORD_SIZE * g : WORD_SIZE * (1 + g)]).tobytes(),
                byteorder="little",
            )
        )
        temp = (b + rotate_left(to_rotate, rotate_by[i])) & 0xFFFFFFFF

        a, b, c, d = d, temp, b, c

    for i, val in enumerate([a, b, c, d]):
        init_temp[i] += val
        init_temp[i] &= 0xFFFFFFFF

    return _to_hex(
        sum(buffer_content << (32 * i) for i, buffer_content in enumerate(init_temp))
    )


if __name__ == "__main__":
    message = input("Please input your pwd")
    print(f"Your hash for input `{message}` is: \n")
    print(get_md5_hash(message))
