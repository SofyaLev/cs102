from src.lab5.orders_tests import *
import unittest


class TestOrderProcessing(unittest.TestCase):
    def test_order_validation_valid(self):
        """
        Тестирование корректного заказа
        """
        order_data = ['123', 'Product1, Product2', 'Name Surname', 'Country. Region. City. Street', '+1-123-456-78-90', 'MAX']
        order = Order(order_data)
        order.validator()
        self.assertTrue(order.is_valid())
        self.assertEqual(order.errors, [])

    def test_order_validation_invalid_address(self):
        """
        Тестирование заказа, в котором отсутствует адрес
        """
        order_data = ['123', 'Product1, Product2', 'Name Surname', '', '+1-123-456-78-90', 'MAX']
        order = Order(order_data)
        order.validator()
        self.assertFalse(order.is_valid())
        self.assertIn(('1', 'no data'), order.errors)

    def test_order_validation_invalid_phone(self):
        """
        Тестирование заказа, в котором отсутствует номер телефона
        """
        order_data = ['123', 'Product1, Product2', 'Name Surname', '', '', 'MAX']
        order = Order(order_data)
        order.validator()
        self.assertFalse(order.is_valid())
        self.assertIn(('2', 'no data'), order.errors)

    def test_order_validation_invalid_phone_format(self):
        """
        Тестирование заказа с неверным форматом номера телефона
        """
        order_data = ['123', 'Product1, Product2', 'Name Surname', '', '+1-123-456-78-90123', 'MAX']
        order = Order(order_data)
        order.validator()
        self.assertFalse(order.is_valid())
        self.assertIn(('2', '+1-123-456-78-90123'), order.errors)

    def test_order_format_products(self):
        """
        Тестирование форматирования продуктов
        """
        order_data = ['123', 'Product1, Product2, Product2, Product3', 'Name Surname', 'Country. Region. City. Street', '+1-123-456-78-90', 'MAX']
        order = Order(order_data)
        formatted_products = order.format_products()
        expected = 'Product1, Product2 x2, Product3'
        self.assertEqual(formatted_products, expected)

    def test_order_format_address(self):
        """
        Тестирование форматирования адреса
        """
        order_data = ['123', 'Product1, Product2', 'Name Surname', 'Country. Region. City. Street', '+1-123-456-78-90', 'MAX']
        order = Order(order_data)
        formatted_address = order.format_address()
        expected = 'Region. City. Street'
        self.assertEqual(formatted_address, expected)

    def test_order_processor_sorting(self):
        """
        Тестирование сортировки заказов
        """
        processor = OrderProcess('test_valid_orders')
        for order in processor.orders:
            order.validator()
        sorted_orders = processor.sort_orders(processor.orders)
        self.assertEqual(sorted_orders[0].order_number, '1')
        self.assertEqual(sorted_orders[1].order_number, '3')
        self.assertEqual(sorted_orders[2].order_number, '2')


if __name__ == '__main__':
    unittest.main()
