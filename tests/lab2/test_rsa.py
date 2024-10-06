import unittest

from src.lab2.rsa import is_prime
from src.lab2.rsa import gcd
from src.lab2.rsa import multiplicative_inverse

print(is_prime(13))

print(gcd(12, 15))
print(gcd(3, 7))
print(multiplicative_inverse(7, 40))


class TestCase(unittest.TestCase):

    def test_is_prime(self):
        self.assertEqual(is_prime(2), True)
        self.assertEqual(is_prime(11), True)
        self.assertEqual(is_prime(8), False)

    def test_gcd(self):
        self.assertEqual(gcd(12, 15), 3)
        self.assertEqual(gcd(3, 7), 1)

    def test_multiplicative_inverse(self):
        self.assertEqual(multiplicative_inverse(7, 40), 23)
