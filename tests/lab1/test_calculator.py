import unittest
from cs102.src.lab1.calculator import calculator


class CalculatorTestCase(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(calculator.addition(125, 27), 152)
        self.assertEqual(calculator.addition(-13, 10), -3)
        self.assertEqual(calculator.addition(16, 18.5), 34.5)

    def test_subtraction(self):
        self.assertEqual(calculator.subtraction(125, 23), 102)
        self.assertEqual(calculator.subtraction(-13, 10), -23)
        self.assertEqual(calculator.subtraction(16, 18.5), -2.5)

    def test_multiplication(self):
        self.assertEqual(calculator.multiplication(21, 3), 63)
        self.assertEqual(calculator.multiplication(-5, 2), -10)
        self.assertEqual(calculator.multiplication(2.5, 4), 10.0)

    def test_division(self):
        self.assertEqual(calculator.division(125, 0), 'Error: division by zero')
        self.assertEqual(calculator.division(-10, 2), -5.0)
        self.assertEqual(calculator.division(10, 2.5), 4.0)
