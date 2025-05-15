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
    def new_product(cls, params: dict):
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
        return self.price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены продукта с проверкой."""

        # Проверка на неотрицательную цену

        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной.")
            return

            # Предупреждение при снижении цены ниже предыдущей и подтверждение изменения пользователем.
        if self.price < self.price:
            user_response = input("Вы ввели цену ниже прошлой. Подтвердите изменение цены (y/n): ")
            if user_response.lower() == "y":
                return


class Category:
    """
    Класс для организации группы продуктов в категорию.

    Атрибуты:
      - category_name: название категории
      - category_description: описание категории
      - __products_list: приватный список продуктов в категории
      - class-level счетчики количества категорий и продуктов
    """

    product_count = 0  # Общее число добавленных продуктов во все категории
    category_count = 0  # Общее число созданных категорий

    def __init__(self, category_name, category_description, products=None):
        """
        Инициализация категории и добавление начальных продуктов при наличии.
        """
        self.category_name = category_name
        self.category_description = category_description
        self.__products_list = []

        if products:
            for prod in products:
                self.add_product(prod)

        Category.category_count += 1

    def __str__(self):
        """
        Строковое представление категории с подсчетом общего количества товаров.
        """
        total_items = sum(product.product_quantity for product in self.__products_list)
        return f"{self.category_name}, количество товаров: {total_items} шт."

    def add_product(self, product_item):
        """
        Добавляет продукт в категорию после проверки типа.

        :param product_item: Объект класса Product или его наследника
        :raises TypeError: если объект не является экземпляром класса Product или его подкласса
        """

        if not isinstance(product_item, Product) or not issubclass(type(product_item), Product):
            raise TypeError("Можно добавлять только объекты типа Product или его подклассы.")

        self.__products_list.append(product_item)
        Category.product_count += 1

    @property
    def products(self):
        """
        Возвращает список строк с информацией о продуктах в категории.
        """
        return [
            f"{prod.product_name}, {prod.price} руб. Остаток: {prod.product_quantity} шт."
            for prod in self.__products_list
        ]


class Smartphone(Product):
    """
    Класс для смартфонов с дополнительными характеристиками.

    Наследует основные свойства от класса Product и добавляет параметры эффективности,
     модели, памяти и цвета.
    """

    def __init__(self, name, description, price, quantity, efficiency_level, model_code, memory_size, color_variant):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency_level  # уровень эффективности (например батареи)
        self.model = model_code  # модель смартфона
        self.memory = memory_size  # объем памяти (например ГБ)
        self.color = color_variant  # цвет устройства


class LawnGrass(Product):
    """
    Класс для травы газона с дополнительными характеристиками.

    Наследует основные свойства от класса Product и добавляет параметры страны происхождения,
    периода прорастания и цвета травы.
    """

    def __init__(self, name, description, price, quantity, country_of_origin, germination_duration_days, grass_color):
        super().__init__(name, description, price, quantity)
        self.country = country_of_origin  # страна происхождения травы
        self.germination_period = germination_duration_days  # период прорастания (дней)
        self.color = grass_color  # цвет травы
