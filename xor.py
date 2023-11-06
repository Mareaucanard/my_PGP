from itertools import cycle


def apply_xor(message: bytearray, key: bytearray):
    return ''.join([f'{(character ^ k):02x}' for character, k in zip(message, cycle(key))])


message = "68656c6c6f20776f726c64"
key = "7665727920736563726574a"
