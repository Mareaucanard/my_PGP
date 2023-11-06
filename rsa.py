#!/bin/python3
import math

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
    for i in range(1, phi) :
        if math.gcd(i, phi) == 1 and is_prime(i):
            e = i
            return e
    return e

def calculate_d(e, n):
    lNCF =  [i for i in range(1, n) if math.gcd(i, n) == 1].__len__()
    return mod_inverse(e, lNCF)

def generatekey(p, q):
    n = p * q
    phi = lcm(p-1, q-1)
    e = calculate_e(phi)
    d = calculate_d(e, n)

    print(f"Public key: {rev_hex(hex(e)[2:])}-{rev_hex(hex(n)[2:])}")
    print(f"Private key: {rev_hex(hex(d)[2:])}-{rev_hex(hex(n)[2:])}")