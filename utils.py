from sys import stderr, argv
from binascii import unhexlify

def flatten(key: str) -> bytearray:
    try:
        return bytearray.fromhex(key)
    except ValueError as e:
        die(f"Error when trying to flatten {key}: {e}")


def die(message):
    print(message, file=stderr)
    exit(84)


def show_hex(v) -> str:
    return ''.join(f'{x:02x}' for x in v)

def show_bytearray(v):
    return ', '.join(f"{x}" for x in v)


def chunks(lst, n):
    """Iterator for processing list chunk by chunk"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def chunks_padded(lst, n):
    for item in chunks(lst, n):
        item = item + bytes([0] * (n - len(item)))
        yield item

def string_to_hex_string(s):
    return ''.join(f"{ord(x):02x}" for x in s)

def hex_string_to_string(s):
    return unhexlify(s).decode('utf-8')

def rev_hex(my_hex):
    if len(my_hex) % 2 != 0:
        my_hex = "0" + my_hex
    if len(my_hex) == 2:
        return my_hex
    else:
        return rev_hex(my_hex[2:]) + rev_hex(my_hex[:2])

def rev_hex_string(x):
    tmp = bytearray.fromhex(x)
    tmp.reverse()
    return show_hex(tmp)
