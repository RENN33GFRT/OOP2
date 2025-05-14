from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для продуктов.
    Определяет интерфейс и обязательные методы для наследующих классов.
    """

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        """
        Инициализация продукта.
        :param name: Название продукта
        :param description: Описание продукта
        :param price: Цена продукта
        :param quantity: Количество на складе
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @abstractmethod
    def create_new_product(cls, params: dict):
        """
        Создает новый продукт из словаря параметров.
        :param params: Словарь с ключами 'name', 'description', 'price', 'quantity'
        :return: экземпляр продукта
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Строковое представление продукта.
        """
        pass

    @abstractmethod
    def __add__(self, other):
        """
        Операция сложения стоимости двух продуктов.
        :param other: Другой продукт того же типа
        :return: сумма стоимости обоих продуктов
        """
        pass


class ProductMixin:
    """
    Миксин для логирования и отображения информации о продукте.
    """

    def __repr__(self):
        """
        Выводит информацию о продукте при вызове repr().
        """
        self.log_product()

    def log_product(self):
        """
        Выводит в консоль информацию о текущем объекте.
        """
        print(f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})")


class Product(ProductMixin, BaseProduct):
    """
    Класс продукта с основными атрибутами и методами.
    """

    def __init__(self, name, description, price, quantity):
        """
        Инициализация продукта с проверкой количества.
        :param name: Название продукта
        :param description: Описание продукта
        :param price: Цена продукта
        :param quantity: Количество на складе (должно быть > 0)
        """
        self.name = name
        self.description = description
        self.__price = price
        if quantity <= 0:
            raise ValueError("Товар с нулевым или отрицательным количеством не может быть добавлен")
        else:
            self.quantity = quantity
        super().__repr__()

    def __str__(self):
        """
        Возвращает строковое описание продукта.
        """
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Складывает общую стоимость двух продуктов одинакового типа.
        :param other: Другой продукт того же типа
        :return: сумма стоимости обоих продуктов
        """
        if isinstance(self, type(other)):
            total_value_self = self.price * self.quantity
            total_value_other = other.price * other.quantity
            return total_value_self + total_value_other
        else:
            raise TypeError("Можно складывать только продукты одного типа.")

    @classmethod
    def create_new_product(cls, params: dict):
        """
        Создает новый продукт из словаря параметров.
        :param params: словарь с ключами 'name', 'description', 'price', 'quantity'
        :return: экземпляр класса Product
        """
        name_, desc_, price_, qty_ = (
            params["name"],
            params["description"],
            params["price"],
            params["quantity"],
        )
        return cls(name_, desc_, price_, qty_)

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной")
        else:
            if new_price < self.__price:
                answer = input("Вы ввели цену ниже прошлой. Подтвердите изменение (y/n): ")
                if answer.lower() == "y":
                    self.__price = new_price


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
