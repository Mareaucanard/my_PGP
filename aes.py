from itertools import cycle
from utils import die, flatten
from copy import copy, deepcopy


def xor(a: bytearray, b: bytearray):
    return [v1 ^ v2 for (v1, v2) in zip(a, b)]


def rot(v: bytearray):
    head, *tail = v
    return tail + [head]


def rev_rot(v: bytearray):
    *head, tail = v
    return [tail] + head


def sub(v: bytearray):
    return [s_box[byte] for byte in v]


def inv_sub(v: bytearray):
    return [s_box_inverse[byte] for byte in v]


def show_bytearray(v):
    return ', '.join(f"{x}" for x in v)


def shift(state: bytearray):
    newState = [None] * 16
    newState[0], newState[4], newState[8], newState[12] = state[0], state[4], state[8], state[12]
    newState[1], newState[5], newState[9], newState[13] = state[5], state[9], state[13], state[1]
    newState[2], newState[6], newState[10], newState[14] = state[10], state[14], state[2], state[6]
    newState[3], newState[7], newState[11], newState[15] = state[15], state[3], state[7], state[11]
    return newState


def un_shift(state: bytearray):
    newState = [None] * 16
    newState[0], newState[4], newState[8], newState[12] = state[0], state[4], state[8], state[12]
    newState[5], newState[9], newState[13], newState[1] = state[1], state[5], state[9], state[13]
    newState[10], newState[14], newState[2], newState[6] = state[2], state[6], state[10], state[14]
    newState[15], newState[3], newState[7], newState[11] = state[3], state[7], state[11], state[15]
    return newState


def matrix_product(m1, m2):
    result = [0] * 4
    width = 1
    height = 4

    for i in range(width):
        for j in range(height):
            tmp = 0
            for k in range(4):
                tmp ^= m1[k][j] * m2[k]
            result[j] = tmp
    return result


mix_matrix = [[2, 3, 1, 1],
              [1, 2, 3, 1],
              [1, 1, 2, 3],
              [3, 1, 1, 2]]

rev_mix_matrix = [[14, 11, 13, 9],
                  [9, 14, 11, 13],
                  [13, 9, 14, 11],
                  [11, 13, 9, 14]]


def gmul(a, b):
    product = 0
    for i in range(8):
        if (b & 1) == 1:
            product ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set == 0x80:
            a ^= 0x1B
        b >>= 1
    return product


def mix_column(c, mixer):
    d = [None] * 4
    for i in range(4):
        r = mixer[i]
        d[i] = gmul(c[0], r[0]) ^ gmul(c[1], r[1]) ^ gmul(
            c[2], r[2]) ^ gmul(c[3], r[3])
    return d


def mix(state):
    result = deepcopy(state)
    for i in range(4):
        indices = [i * 4 + j for j in range(4)]
        start = [int(state[x]) for x in indices]
        column = mix_column(start, mix_matrix)
        for index, value in zip(indices, column):
            result[index] = value
    return result


def rev_mix(state):
    result = deepcopy(state)
    for i in range(4):
        indices = [i * 4 + j for j in range(4)]
        start = [int(state[x]) for x in indices]
        column = mix_column(start, rev_mix_matrix)
        for index, value in zip(indices, column):
            result[index] = value
    return result


def show_hex(v) -> str:
    res = []
    i = 0
    while i < len(v):
        l = []
        for j in range(4):
            l.append(f"{v[i]:02x}")
            i = i + 1
        res.append(''.join(l))
    return ' '.join(res)

# def __iter__(self):
#     return self.v.__iter__()


s_box = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

s_box_inverse = [s_box.index(x) for x in range(len(s_box))]

rc = [None]
for i in range(1, 256):
    if i == 1:
        rc.append(1)
        continue
    prev = rc[i - 1]
    if (prev < 128):
        v = 2 * prev
    else:
        v = (2 * prev) ^ 283
    rc.append(v)

rcon = [None if x == None else [x, 0, 0, 0] for x in rc]


def group_by_n(l: list[list], n: int) -> list:
    result = []
    tmp = None
    for i, item in enumerate(l):
        if i % n == 0 and i != 0:
            result.append(tmp)
            tmp = None

        if tmp is None:
            tmp = item
        else:
            tmp += item
    result.append(tmp)
    return result


def key_expansion(key: bytearray) -> [bytearray]:
    result = [None] * 44

    for i in range(4):
        result[i] = [key[4 * i], key[4 * i + 1],
                           key[4 * i + 2], key[4 * i + 3]]

    for i in range(4, 44):

        tmp = result[i - 1]
        if (i % 4 == 0):
            tmp = sub(rot(tmp))
            tmp = xor(tmp, rcon[i // 4])
        result[i] = xor(result[i - 4], tmp)
    return group_by_n(result, 4)


def encrypt_aes(message: bytearray, key: bytearray):
    if (len(key) != 16):
        die(f"RSA Invalid key, must be 128 bit but was {len(key) * 8}")
    round_key = key_expansion(key)
    state = xor(message, round_key[0])
    for i in range(1, 10):
        state = sub(state)
        state = shift(state)
        state = mix(state)
        state = xor(state, round_key[i])
    state = sub(state)
    state = shift(state)
    state = xor(state, round_key[10])
    print(show_bytearray(state))
    return state


def decrypt_aes(message: bytearray, key: bytearray):
    if (len(key) != 16):
        die(f"RSA Invalid key, must be 128 bit but was {len(key) * 8}")
    round_key = key_expansion(key)
    round_key.reverse()
    state = xor(message, round_key[0])
    for i in range(1, 10):
        state = un_shift(state)
        state = inv_sub(state)
        state = xor(state, round_key[i])
        state = rev_mix(state)
    state = inv_sub(state)
    state = un_shift(state)
    state = xor(state, round_key[10])
    print(show_bytearray(state))
    return state


message = [0x14, 0x15, 0x16, 0x17, 0x10, 0x11, 0x12,
           0x13, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1F, 0x20]
key = [0x10, 0x50, 0xa9, 0x25, 0x15, 0xd6, 0x55, 0x55,
       0xd4, 0x50, 0xeb, 0x45, 0x68, 0x21, 0xe9, 0x81]
v = bytes(key)
w = bytes(message)


def f():
    print(key)
    r = key_expansion(key)
    for i in [0, 1, 5, 9, 10]:
        print(f"key {i} = {show_bytearray(r[i])}")
