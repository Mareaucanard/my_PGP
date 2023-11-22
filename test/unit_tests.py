import unittest
from utils import *
from xor import apply_xor
from aes import encrypt_aes, decrypt_aes

class TestXor(unittest.TestCase):
    def test_xor(self):
        message = "68656c6c6f20776f726c64"
        key = "7665727920736563726574"
        ciphered_expected = "1e001e154f53120c000910"

        ciphered_actual = apply_xor(flatten(message), flatten(key))
        self.assertEqual(ciphered_expected, ciphered_actual)

        decoded = apply_xor(flatten(ciphered_actual), flatten(key))
        self.assertEqual(decoded, message)

class TestAes(unittest.TestCase):
    def test_aes(self):
        message = "c2486f4796f0657481a655c559b38aaa"
        key = "6b50fd39f06d33cfefe6936430b6c94f"
        ciphered_expected = "0fc668acd39462d17272fe863929973a"

        ciphered_actual = encrypt_aes(flatten(message), flatten(key))
        self.assertEqual(ciphered_expected, show_hex(ciphered_actual))

        decoded = decrypt_aes(ciphered_actual, flatten(key))
        self.assertEqual(show_hex(decoded), message)

        self.assertRaises(ValueError, encrypt_aes, flatten(message), "bad key")
        self.assertRaises(ValueError, decrypt_aes, flatten(message), "bad key")
        self.assertRaises(ValueError, encrypt_aes, "bad message", flatten(key))
        self.assertRaises(ValueError, decrypt_aes, "bad message", flatten(key))

class TestStringTransforms(unittest.TestCase):
    def f(self, a, b):
        return self.assertEqual(a, b)

    def test_show_hex(self):
        l1 = [0, 255, 127]
        r1 = "00ff7f"
        self.f(show_hex(l1), r1)

        l2 = [ord(x) for x in "Hello, world!"]
        r2 = "48656c6c6f2c20776f726c6421"
        self.f(show_hex(l2), r2)

    def test_show_bytearray(self):
        l1 = [0, 255, 127]
        r1 = "0, 255, 127"

        l2 = [48, 12, 64, 1, 2]
        r2 = "48, 12, 64, 1, 2"
        self.f(show_bytearray(l1), r1)
        self.f(show_bytearray(l2), r2)

    def test_pad_string(self):
        n = "Hello"
        self.f(pad_string(n, 1), "Hello")
        self.f(pad_string(n, 5), "Hello")
        self.f(pad_string(n, 10), "Hello00000")

    def test_rev_hex(self):
        l1 = "00ff7f"
        r1 = "7fff00"
        l2 = "12"
        r2 = "12"
        l3 = "0"
        r3 = "00"

        self.f(rev_hex(l1), r1)
        self.f(rev_hex(rev_hex(l1)), l1)
        self.f(rev_hex(l2), r2)
        self.f(rev_hex(l3), r3)


    def test_hex_string_to_string(self):
        l = "486921"
        r = "Hi!"
        self.f(hex_string_to_string(l), r)
        self.f(string_to_hex_string(r), l)

    def test_chunks(self):
        b = lambda x: bytes([ord(v) for v in x])
        l = b("12345")
        r1 = [b("12"), b("34"), b("5")]
        r2 = [b("12"), b("34"), b("5") + bytes(1)]

        self.f(list(chunks(l, 2)), r1)
        self.f(list(chunks_padded(l, 2)), r2)

    def test_flatten(self):
        l = "010203"
        r = bytearray.fromhex(l)
        self.assertEqual(flatten(l), r)

        self.assertRaises(ValueError, flatten, "0")
