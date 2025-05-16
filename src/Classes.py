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
        super().__init__()  # Для миксина LoggingMixin
        self.name = product_name
        self.description = product_description
        self._price = product_price  # Защищённый атрибут вместо приватного
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
        super().__init__(*args, **kwargs)  # Для корректной работы MRO

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Product(BaseProduct, LoggingMixin):
    """
    Класс для представления товара с основными характеристиками.
    """

    def __init__(self, product_name, product_description, product_price, product_quantity):
        """
        Инициализация товара. Атрибуты устанавливаются через super().__init__() в BaseProduct.
        """
        super().__init__(product_name, product_description, product_price, product_quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if isinstance(other, type(self)):
            return (self.price * self.quantity) + (other.price * other.quantity)
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
        return self._price  # Используем защищённый атрибут

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


# Пример использования
if __name__ == "__main__":
    # Проверка миксина и геттера price
    product = Product("Телефон", "Смартфон", 50000, 10)
    print(product)  # Проверка __str__
    print(f"Цена через геттер: {product.price}")  # Проверка геттера
    product.price = 45000  # Проверка сеттера