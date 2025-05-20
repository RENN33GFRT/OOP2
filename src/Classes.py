from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для продуктов.
    Определяет интерфейс и общие свойства для всех продуктов.
    """

    @abstractmethod
    def __init__(self, product_name, product_description, product_price, product_quantity):
        self.name = product_name
        self.description = product_description
        self._price = product_price
        self.quantity = product_quantity

    @classmethod
    @abstractmethod
    def create_new_product(cls, params: dict):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        print(f"\nСоздан объект {self.__class__.__name__} с параметрами:")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}\n")
        super().__init__(*args, **kwargs)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Product(BaseProduct, LoggingMixin):
    """
    Класс для представления товара с основными характеристиками.
    """

    def __init__(self, product_name, product_description, product_price, product_quantity):
        super().__init__(product_name, product_description, product_price, product_quantity)

    def __str__(self):
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if isinstance(other, type(self)):
            return (self._price * self.quantity) + (other._price * other.quantity)
        raise TypeError("Можно складывать только товары одного типа.")

    @classmethod
    def create_new_product(cls, params: dict):
        return cls(
            params["name"],
            params["description"],
            params["price"],
            params["quantity"]
        )

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной.")
            return

        if hasattr(self, '_price') and new_price < self._price:
            user_response = input("Вы ввели цену ниже прошлой. Подтвердите изменение цены (y/n): ")
            if user_response.lower() != "y":
                print("Изменение цены отменено.")
                return

        self._price = new_price


class Category:
    """
    Класс категории товаров. Подсчитывает количество категорий и продуктов внутри них.
    """

    category_count = 0
    product_count = 0

    def __init__(self, category_name, category_description, products=None):
        self.category_name = category_name
        self.category_description = category_description
        self.__products = []

        if products:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.category_name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты типа Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return [f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт." for p in self.__products]


class Smartphone(Product):
    def __init__(self, name, description, price, quantity,
                 efficiency=0, model='', memory=0, color=''):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    @classmethod
    def create_new_product(cls, params: dict):
        return cls(
            name=params.get('name'),
            description=params.get('description'),
            price=params.get('price'),
            quantity=params.get('quantity'),
            efficiency=params.get('efficiency', 0),
            model=params.get('model', ''),
            memory=params.get('memory', 0),
            color=params.get('color', '')
        )


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity,
                 country='', germination_period=0, color=''):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    @classmethod
    def create_new_product(cls, params: dict):
        return cls(
            name=params.get('name'),
            description=params.get('description'),
            price=params.get('price'),
            quantity=params.get('quantity'),
            country=params.get('country', ''),
            germination_period=params.get('germination_period', 0),
            color=params.get('color', '')
        )