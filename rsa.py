#!/bin/python3
import math
import random

def lcm(a, b):
    return abs(a*b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return (x % m + m) % m
    
def rev_hex(my_hex):
    if len(my_hex) % 2 != 0:
        my_hex = "0" + my_hex
    if len(my_hex) == 2:
        return my_hex
    else:
        return rev_hex(my_hex[2:]) + rev_hex(my_hex[:2])
    
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def calculate_e(phi):
    e_list = []
    for i in range(1, phi) :
        if math.gcd(i, phi) == 1 and is_prime(i):
            e_list.append(i)
        if len(e_list) == 10000:
            break
    r = random.SystemRandom()
    return e_list[r.randint(0, len(e_list))]

def calculate_d(e, n):
    return mod_inverse(e, n)

def generatekey(p, q):
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
    key = key.split("-")
    e = int(rev_hex(key[0]), 16)
    n = int(rev_hex(key[1]), 16)
    message = int(message, 16)
    rmessage = pow(message, e, n)
    print(f"{rev_hex(hex(rmessage)[2:])}")

def decrypt_rsa(key, message):
    key = key.split("-")
    d = int(rev_hex(key[0]), 16)
    n = int(rev_hex(key[1]), 16)
    message = int(rev_hex(message), 16)
    rmessage = pow(message, d, n)
    print(f"{rev_hex(hex(rmessage)[2:])}")