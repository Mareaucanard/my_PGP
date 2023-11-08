from sys import stderr


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
