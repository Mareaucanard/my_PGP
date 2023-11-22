"""Xor encryption algorithm"""
from itertools import cycle


def apply_xor(message: bytearray, key: bytearray):
    """Applies XOR on every character of the message with the same indexed character of the key
    If the key is longer than the message, loops on the key"""
    return ''.join([f'{(character ^ k):02x}' for character, k in zip(message, cycle(key))])
