from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для продуктов.
    Определяет интерфейс и общие свойства для всех продуктов.
    """
    @abstractmethod
    def __init__(self, product_name, product_description, product_price, product_quantity):
        super().__init__(product_name, product_description, product_price, product_quantity)

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
        print(f"Kwargs: {kwargs}\n")  # Для корректной работы MRO

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Product(BaseProduct, LoggingMixin):
    """
    Класс для представления товара с основными характеристиками.
    """

    def __init__(self, product_name, product_description, product_price, product_quantity):
        self.name = product_name
        self.description = product_description
        self.__price = product_price
        self.quantity = product_quantity
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
        return self.__price  # Используем защищённый атрибут

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
    # Проверка миксина и геттера pprice
    product = Product("Телефон", "Смартфон", 50000, 10)
    print(product)  # Проверка __str__
    print(f"Цена через геттер: {product.price}")  # Проверка геттера
    product.price = 45000  # Проверка сеттера

class Category:
    """
    Класс категории товаров. Подсчитывает количество категорий и продуктов внутри них.
    """

    category_counter = 0  # Общее число созданных категорий (статический счетчик)
    product_counter = 0  # Общее число добавленных продуктов (статический счетчик)

    def __init__(self, category_name, category_description, products=None):
        """
        Инициализация категории с названием, описанием и списком продуктов.
        :param category_name: Название категории
        :param category_description: описание категории
        :param products: список объектов Product (по умолчанию None)
        """
        self.category_name = category_name
        self.category_description = category_description
        self._products_list = []
        if products:
            for prod in products:
                self.add_product(prod)
        self.category_counter += 1

    def __str__(self):
        """
        Возвращает строку с названием категории и суммарным количеством товаров.
        """
        total_quantity = sum(prod.quantity for prod in self._products_list)
        return f"{self.category_name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product_obj):
        """
        Добавляет продукт в категорию после проверки типа.
        Увеличивает счетчик общего числа продуктов.
        :param product_obj: Объект класса Product или его наследника
        """
        if not isinstance(product_obj, Product) or not issubclass(type(product_obj), Product):
            raise TypeError("Можно добавлять только объекты типа Product")
        else:
            self._products_list.append(product_obj)
            Category.product_counter += 1

    @property
    def products_info(self):
        """
         Возвращает список строк с информацией о каждом продукте в категории.
         Каждая строка содержит название, цену и остаток по количеству.
         """
        info_list = []
        for item in self._products_list:
            info_list.append(f"{item.name}, {item.price} руб. Остаток: {item.quantity} шт.\n")
        return info_list


def average_price(self):
    """
    Вычисляет среднюю цену всех продуктов в категории.
    Возвращает 0 при отсутствии товаров.
    """
    try:
        count_products = len(self._products_list)
        total_price_sum = sum(prod.price for prod in self._products_list)
        return total_price_sum / count_products if count_products > 0 else 0
    except Exception:
        return 0


class Smartphone(Product):
    """
    Наследник класса Product для смартфонов с дополнительными характеристиками.
    """

    def __init__(self, name, description, price, quantity, efficiency_level, model_name, memory_size, color_variant):
        super().__init__(name, description, price, quantity)
        self.efficiency_level = efficiency_level  # уровень эффективности (например батареи)
        self.model_name = model_name  # модель смартфона
        self.memory_size = memory_size  # объем памяти
        self.color_variant = color_variant  # цвет


class LawnGrass(Product):
    """
    Наследник класса Product для травы/газона с дополнительными характеристиками.
    """

    def __init__(self, name, description, price, quantity,
                 country_of_origin,
                 germination_period_days,
                 grass_color):
        super().__init__(name, description, price, quantity)
        self.country_of_origin = country_of_origin  # страна происхождения
        self.germination_period_days = germination_period_days  # период прорастания (дней)
        self.grass_color = grass_color  # цвет травы/газона