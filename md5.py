from bitarray import bitarray
import math
import struct


WORD_SIZE = 32


A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476


def get_block_bit_array(input: bytes) -> bitarray:
    length = len(input) * 8
    length_bit_array = bitarray(endian="little")
    length_bit_array.frombytes(struct.pack("<Q", length))

    bit_array = bitarray(endian="big")
    bit_array.frombytes(input)
    bit_array.append(1)
    while len(bit_array) % 512 != 448:
        bit_array.append(0)
    bit_array = bitarray(bit_array, endian="little")

    bit_array.extend(length_bit_array)
    return bit_array


def split_into_words(bits: bitarray, size: int) -> list[int]:
    words = []
    for i in range(0, len(bits), size):
        words.append(bits[i : i + size])
    return [int.from_bytes(word.tobytes(), byteorder="little") for word in words]


def _get_hash(a, b, c, d):
    # Convert the buffers to little-endian.
    A = struct.unpack("<I", struct.pack(">I", a))[0]
    B = struct.unpack("<I", struct.pack(">I", b))[0]
    C = struct.unpack("<I", struct.pack(">I", c))[0]
    D = struct.unpack("<I", struct.pack(">I", d))[0]
    # Output the buffers in lower-case hexadecimal format.
    return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"


def get_md5_hash(input: bytes):
    block_bits = get_block_bit_array(input)
    words = split_into_words(block_bits, WORD_SIZE)
    K = [math.floor(pow(2, 32) * abs(math.sin(i + 1))) for i in range(64)]
    a, b, c, d = A, B, C, D
    modular_add = lambda a, b: (a + b) % pow(2, 32)
    rotate_left = lambda x, n: (x << n) | (x >> (32 - n))
    # Define the four auxiliary functions that produce one 32-bit word.
    F = lambda x, y, z: (x & y) | (~x & z)
    G = lambda x, y, z: (x & z) | (y & ~z)
    H = lambda x, y, z: x ^ y ^ z
    I = lambda x, y, z: y ^ (x | ~z)
    for i in range(64):
        temp, g = None, None
        if i < 0 <= 15:
            temp = F(B, C, D)
            s = [7, 12, 17, 22]
            g = i
        elif 16 <= i <= 31:
            temp = G(B, C, D)
            s = [5, 9, 14, 20]
            g = (5 * i + 1) % 16
        elif 32 <= i <= 47:
            temp = H(B, C, D)
            s = [4, 11, 16, 23]
            g = (3 * i + 5) % 16
        else:
            temp = I(B, C, D)
            s = [6, 10, 15, 21]
            g = (7 * i) % 16
        temp = modular_add(temp, words[g])
        temp = modular_add(temp, K[i])
        temp = modular_add(temp, A)
        temp = rotate_left(temp, s[i % 4])
        temp = modular_add(temp, B)
        a = d
        d = c
        c = b
        b = temp
    
    a = modular_add(a, A)
    b = modular_add(b, B)
    c = modular_add(c, C)
    d = modular_add(d, D)
    return _get_hash(a, b, c, d)
