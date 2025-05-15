from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для продуктов.
    Определяет интерфейс и общие свойства для всех продуктов.
    """

    @abstractmethod
    def __init__(self, product_name, product_description, product_price, product_quantity):
        """
        Инициализация базовых свойств продукта.
        """
        self.name = product_name
        self.description = product_description
        self.price = product_price
        self.quantity = product_quantity

    @classmethod
    @abstractmethod
    def create_new_product(cls, params: dict):
        """
        Создает новый экземпляр продукта на основе переданных параметров.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Возвращает строковое представление продукта.
        """
        pass

    @abstractmethod
    def __add__(self, other):
        """
        Складывает стоимости двух продуктов одинакового типа.
        """
        pass


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        print(f"Создан объект {self.__class__.__name__} с параметрами:")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        super().__init__(*args)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Product(BaseProduct, LoggingMixin):
    """
    Класс для представления товара с основными характеристиками.
    """

    def __init__(self, product_name, product_description, product_price, product_quantity):
        """
        Инициализация товара и вызов метода логирования.
        """
        super().__init__(product_name, product_description, product_price, product_quantity)

    def __str__(self):
        """
        Возвращает строковое описание товара.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Складывает стоимости двух товаров одинакового типа.

        :param other: Другой объект класса Product
        :return: сумма стоимости обоих товаров
        :raises TypeError: если объекты разных типов
        """
        if isinstance(other, type(self)):
            total_value_self = self.price * self.quantity
            total_value_other = other.price * other.quantity
            return total_value_self + total_value_other
        else:
            raise TypeError("Можно складывать только товары одного типа.")

    @classmethod
    def create_new_product(cls, params: dict):
        """
        Создает новый товар из словаря параметров.

        :param params: словарь с ключами 'name', 'description', 'price', 'quantity'
        :return: экземпляр класса Product
        """
        name_ = params["name"]
        description_ = params["description"]
        price_ = params["price"]
        quantity_ = params["quantity"]

        return cls(name_, description_, price_, quantity_)

    @property
    def price(self):
        """Геттер для цены продукта."""
        return self._price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены продукта с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной.")
            return

        if hasattr(self, '_price') and new_price < self._price:
            user_response = input("Вы ввели цену ниже прошлой. Подтвердите изменение цены (y/n): ")
            if user_response.lower() != "y":
                return

        self._price = new_price


class Category:
    """
    Класс для организации группы продуктов в категорию.
    """
    product_count = 0
    category_count = 0

    def __init__(self, category_name, category_description, products=None):
        self.category_name = category_name
        self.category_description = category_description
        self.__products_list = []

        if products:
            for prod in products:
                self.add_product(prod)

        Category.category_count += 1

    def __str__(self):
        total_items = sum(product.quantity for product in self.__products_list)
        return f"{self.category_name}, количество товаров: {total_items} шт."

    def add_product(self, product_item):
        if not isinstance(product_item, Product):
            raise TypeError("Можно добавлять только объекты типа Product или его подклассы.")

        self.__products_list.append(product_item)
        Category.product_count += 1

    @property
    def products(self):
        return [
            f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт."
            for prod in self.__products_list
        ]


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency_level, model_code, memory_size, color_variant):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency_level
        self.model = model_code
        self.memory = memory_size
        self.color = color_variant

    @classmethod
    def create_new_product(cls, params: dict):
        """Реализация абстрактного метода для Smartphone"""
        base_params = {
            'name': params['name'],
            'description': params['description'],
            'price': params['price'],
            'quantity': params['quantity']
        }
        return cls(**base_params,
                 efficiency_level=params.get('efficiency_level', 0),
                 model_code=params.get('model_code', ''),
                 memory_size=params.get('memory_size', 0),
                 color_variant=params.get('color_variant', ''))


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country_of_origin, germination_duration_days, grass_color):
        super().__init__(name, description, price, quantity)
        self.country = country_of_origin
        self.germination_period = germination_duration_days
        self.color = grass_color

    @classmethod
    def create_new_product(cls, params: dict):
        """Реализация абстрактного метода для LawnGrass"""
        base_params = {
            'name': params['name'],
            'description': params['description'],
            'price': params['price'],
            'quantity': params['quantity']
        }
        return cls(**base_params,
                 country_of_origin=params.get('country_of_origin', ''),
                 germination_duration_days=params.get('germination_duration_days', 0),
                 grass_color=params.get('grass_color', ''))