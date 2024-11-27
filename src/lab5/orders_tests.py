import re


class Order:
    def __init__(self, order_data):
        """
        Инициализация объекта заказа на основе данных заказа
        """
        self.order_number = order_data[0]
        self.products = order_data[1]
        self.name = order_data[2]
        self.address = order_data[3]
        self.phone_number = order_data[4]
        self.priority = order_data[5]

        self.errors = []

    def validator(self):
        """
        Проверка данных заказа на соответствие шаблонам, заполнение списка ошибок
        """
        # проверка корректности адреса
        if not self.address:
            self.errors.append(('1', 'no data'))
        else:
            if len(self.address.strip().split('. ')) != 4:
                self.errors.append(('1', self.address))

        # проверка корректности номера телефона
        if not self.phone_number:
            self.errors.append(('2', 'no data'))
        else:
            pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
            if not re.match(pattern, self.phone_number):
                self.errors.append(('2', self.phone_number))

    def is_valid(self):
        """
        Проверка заказа на корректность
        """
        return len(self.errors) == 0

    def format_products(self):
        """
        Преобразование строки продуктов под нужный формат
        """
        product_list = [product.strip() for product in self.products.split(',')]
        product_counter = {}
        for product in product_list:
            product_counter[product] = product_counter.get(product, 0) + 1

        formatted_products = []
        for product, count in product_counter.items():
            if count > 1:
                formatted_products.append(f'{product} x{count}')
            else:
                formatted_products.append(product)
        return ', '.join(formatted_products)

    def format_address(self):
        """
        Преобразование строки адреса под нужный формат
        """
        address_parts = self.address.split('. ')
        return '. '.join(address_parts[1:]) if len(address_parts) > 1 else self.address

    def get_country(self):
        """
        Получение страны из строки адреса
        """
        address_parts = self.address.split('. ')
        return address_parts[0] if address_parts else ''

    def get_priority(self):
        """
        Преобразование приоритета доставки в число
        """
        priority_values = {'MAX': 1, 'MIDDLE': 2, 'LOW': 3}
        return priority_values[self.priority]


class OrderProcess:
    def __init__(self, input_file):
        """
        Инициализация объекта для обработки заказов
        """
        self.orders = []
        self.errors = []
        self.read_from_file(input_file)

    def read_from_file(self, input_file):
        """
        Чтение данных заказов из входного файла и создание объектов Order
        """
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    order_data = line.strip().split(';')
                    order = Order(order_data)
                    self.orders.append(order)

    def orders_validator(self):
        """
        Проверка данных заказов на корректность и сбор ошибок
        """
        for order in self.orders:
            order.validator()
            if not order.is_valid():
                for error_type, error_value in order.errors:
                    self.errors.append((order.order_number, error_type, error_value))

    def write_non_valid_orders(self, output_file):
        """
        Запись некорректных заказов в файл
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            for error in self.errors:
                file.write(f'{error[0]};{error[1]};{error[2]}\n')

    def get_valid_orders(self):
        """
        Получение списка корректных заказов
        """
        return [order for order in self.orders if order.is_valid()]

    def sort_orders(self, orders):
        """
        Сортировка заказов по странам и приоритета доставки
        """
        return sorted(orders, key=lambda x: (x.get_country(), x.get_priority()))

    def write_valid_orders(self, orders, output_file):
        """
        Запись корректных заказов в файл
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            for order in orders:
                formatted_products = order.format_products()
                formatted_address = order.format_address()
                file.write(f'{order.order_number};{formatted_products};{order.name};{formatted_address};{order.phone_number};{order.priority}\n')

    def process(self, non_valid_orders_file, valid_orders_file):
        """
        Цикл обработки заказов
        """
        self.orders_validator()
        self.write_non_valid_orders(non_valid_orders_file)

        valid_orders = self.get_valid_orders()
        sorted_valid_orders = self.sort_orders(valid_orders)

        self.write_valid_orders(sorted_valid_orders, valid_orders_file)


def main():
    """
    Главная функция
    """
    process = OrderProcess(input_file='txtf/orders')
    process.process(non_valid_orders_file='txtf/non_valid_orders', valid_orders_file='txtf/order_country')


if __name__ == '__main__':
    main()
