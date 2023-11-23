#!/bin/python3
import math
import random
from utils import rev_hex

def lcm(a, b):
    """Calculates the least common multiple of a and b
    """
    return abs(a*b)

def extended_gcd(a, b):
    """Calculates the extended greatest common divisor of a and b
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def mod_inverse(a, m):
    """Calculates the modular inverse of a mod m
    """
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return (x % m + m) % m

def is_prime(n, k=8):
    """Uses miller-rabin
    see https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    is probabilistic, but still has more than 99.99999% chance of success
    """
    rand_instance = random.SystemRandom()
    lower_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n < 2:
        return False
    if n in lower_primes:
        return True
    for p in lower_primes:
        if n % p == 0:
            return False

    s, d = 0, n-1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for _ in range(k):
        x = pow(rand_instance.randint(2, n-1), d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(1, s):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n-1:
                break
        else:
            return False
    return True

def calculate_e(phi):
    """Calculates the public key
    """
    r = random.SystemRandom()

    while True:
        i =  r.randint(1, phi)
        if math.gcd(i, phi) == 1 and is_prime(i):
            return i

def calculate_d(e, n):
    """Calculates the private key
    """
    return mod_inverse(e, n)

def generate_prime(key_length: int = 1024):
    """Generates a prime number of key_length bits
    """
    r = random.SystemRandom()

    low = 2 ** (key_length - 1) + 1
    high = 2 ** key_length - 1
    candidate = r.randint(low, high)
    while not is_prime(candidate, 1):
        candidate = r.randint(low, high)
    return candidate

def generatekey(p, q):
    """Generates a RSA keypair from two prime numbers
    """
    if not (is_prime(p) and is_prime(q)):
        print("p and q must be prime numbers")
        exit(84)
    n = p * q
    phi = lcm(p-1, q-1)
    e = calculate_e(phi)
    d = calculate_d(e, phi)

    print(f"Public key: {rev_hex(hex(e)[2:])}-{rev_hex(hex(n)[2:])}")
    print(f"Private key: {rev_hex(hex(d)[2:])}-{rev_hex(hex(n)[2:])}")

def crypt_rsa(key, message):
    """Encrypts a message using RSA
    """
    key = key.split("-")
    e = int(rev_hex(key[0]), 16)
    n = int(rev_hex(key[1]), 16)
    message = int(message, 16)
    if message >= n:
        print("Message is too long")
        exit(84)
    rmessage = pow(message, e, n)
    return rev_hex(f"{rmessage:x}")


def decrypt_rsa(key, message):
    """Decrypts a message using RSA
    """
    key = key.split("-")
    d = int(rev_hex(key[0]), 16)
    n = int(rev_hex(key[1]), 16)
    message = int(rev_hex(message), 16)
    rmessage = pow(message, d, n)
    return f"{rmessage:x}"
