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
    """Класс для категорий товаров"""
    total_categories = 0
    total_unique_products = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = products if products else []
        Category.total_categories += 1
        Category.total_unique_products += len(set(p.name for p in self.__products))

    def add_product(self, product):
        if not isinstance(product, Product):
            raise ValueError("Можно добавлять только товары")
        self.__products.append(product)
        if product.name not in [p.name for p in self.__products[:-1]]:
            Category.total_unique_products += 1

    @property
    def products(self):
        return "\n".join(str(p) for p in self.__products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."


class Smartphone(Product):
    """Класс для смартфонов"""
    def __init__(self, name, description, price, quantity, performance, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.performance = performance
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для газонной травы"""
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color