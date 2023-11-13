from binascii import unhexlify


def flatten(key: str) -> bytearray:
    try:
        return bytearray.fromhex(key)
    except ValueError as e:
        die(f"Error when trying to flatten {key}: {e}")


def die(message):
    raise ValueError(message)


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
    return s.encode('utf-8').hex()

def hex_string_to_string(s):
    return ''.join([chr(x) for x in unhexlify(s)])

def rev_hex(my_hex):
    if len(my_hex) % 2 != 0:
        my_hex = "0" + my_hex
    if len(my_hex) == 2:
        return my_hex
    else:
        return rev_hex(my_hex[2:]) + rev_hex(my_hex[:2])

def pad_string(s, n):
    return s + '0' * (n - len(s))
