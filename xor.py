from itertools import cycle


def apply_xor(message: bytearray, key: bytearray):
    return ''.join([f'{(character ^ k):02x}' for character, k in zip(message, cycle(key))])
