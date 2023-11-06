from sys import stderr


def flatten(key: str) -> bytearray:
    try:
        return bytearray.fromhex(key)
    except ValueError as e:
        die(f"Error when trying to flatten {key}: {e}")

def die(message):
    print(message, file=stderr)
    exit(84)
