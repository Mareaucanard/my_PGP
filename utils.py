"""Utils functions for pgp project
Mostly for handling hex string conversion and padding
"""

def flatten(key: str) -> bytearray:
    """Tries to transform an hex string into a bytearray
    On fail raises a ValueError"""
    try:
        return bytearray.fromhex(key)
    except ValueError as e:
        die(f"Error when trying to flatten {key}: {e}")


def die(message):
    """Raises an error with the given message"""
    raise ValueError(message)


def show_hex(v) -> str:
    """Returns a string of 2 byte base16 numbers"""
    return ''.join(f'{x:02x}' for x in v)

def show_bytearray(v):
    """Returns a string of base 10 numbers"""
    return ', '.join(f"{x}" for x in v)


def chunks(lst, n):
    """Generator for processing list chunk by chunk
    Such that you get chunks of length n
    The length of the last chunk may be lower than n
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def chunks_padded(lst, n, identity = bytes([0])):
    """Returns a generator of chunks of size n
    If the final chunk is not long enough to be of size n, pads 0 bytes at the end
    """
    for item in chunks(lst, n):
        item = item + identity * (n - len(item))
        yield item

def string_to_hex_string(s):
    """Takes an utf-8 string and return the hexadecimal representation
    reciprocal of hex_string_to_string
    Stops when an ETX is encountered

    >>> string_to_hex_string("Hello, world!")
    "48656c6c6f2c20776f726c6421"
    """
    return ''.join([f"{ord(c):02x}" for c in s])

def hex_string_to_string(s):
    """Takes an hex representation string and returns a string
    reciprocal of string_to_hex_string

    >>> string_to_hex_string("48656c6c6f2c20776f726c6421")
    "Hello, world!"
    """
    return ''.join([chr(int(x, 16)) for x in chunks(s, 2)])

def rev_hex(my_hex):
    """Inverses endian"""
    if len(my_hex) % 2 != 0:
        my_hex = "0" + my_hex
    if len(my_hex) == 2:
        return my_hex
    else:
        return rev_hex(my_hex[2:]) + rev_hex(my_hex[:2])

def pad_string(s, n, identity = '0'):
    """Adds 0 to the end of the string"""
    return s + identity * (n - len(s))
