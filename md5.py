from bitarray import bitarray
import math
import struct

WORD_SIZE = 32

# Initialization constants (A, B, C, D)
A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476

def _get_block_bit_array(input: bytes) -> bitarray:
    length = len(input) * 8
    bit_array = bitarray(endian="big")
    bit_array.frombytes(input)
    bit_array.append(1)
    while len(bit_array) % 512 != 448:
        bit_array.append(0)
    length_bit_array = bitarray(endian="little")
    length_bit_array.frombytes(struct.pack("<Q", length))
    bit_array.extend(length_bit_array)
    return bit_array

def _split_into_words(bits: bitarray, size: int) -> list[int]:
    words = []
    for i in range(0, len(bits), size):
        words.append(bits[i : i + size])
    return [int.from_bytes(word.tobytes(), byteorder="little") for word in words]

def _get_hash(a, b, c, d):
    
    return f"{a:08x}{b:08x}{c:08x}{d:08x}"

def get_md5_hash(input: bytes):
    block_bits = _get_block_bit_array(input)
    words = _split_into_words(block_bits, WORD_SIZE)
    K = [math.floor(pow(2, 32) * abs(math.sin(i + 1))) for i in range(64)]
    S = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,  # Round 1
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,      # Round 2
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,  # Round 3
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21   # Round 4
    ]
    
    a, b, c, d = A, B, C, D
    modular_add = lambda x, y: (x + y) % pow(2, 32)
    rotate_left = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

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

        temp = modular_add(a, f)
        temp = modular_add(temp, K[i])
        temp = modular_add(temp, words[g])
        temp = rotate_left(temp, S[i])
        temp = modular_add(temp, b)
        
        a, b, c, d = d, temp, b, c
    
    a = modular_add(a, A)
    b = modular_add(b, B)
    c = modular_add(c, C)
    d = modular_add(d, D)
    
    return _get_hash(a, b, c, d)

# Test the implementation
print(get_md5_hash(b"a")) 