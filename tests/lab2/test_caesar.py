import unittest

from src.lab2.caesar import encrypt_caesar
from src.lab2.caesar import decrypt_caesar


class TestCase(unittest.TestCase):

    def test_encrypt_caesar(self):
        self.assertEqual(encrypt_caesar('python'), 'sbwkrq')
        self.assertEqual(encrypt_caesar('PYTHON'), 'SBWKRQ')
        self.assertEqual(encrypt_caesar('Python3.6'), 'Sbwkrq3.6')

    def test_decrypt_caesar(self):
        self.assertEqual(decrypt_caesar('sbwkrq'), 'python')
        self.assertEqual(decrypt_caesar('SBWKRQ'), 'PYTHON')
        self.assertEqual(decrypt_caesar('Sbwkrq3.6'), 'Python3.6')
