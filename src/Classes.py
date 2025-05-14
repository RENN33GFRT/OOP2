from abc import ABC, abstractmethod


class AbstractProduct(ABC):
    """
    Абстрактный базовый класс для продуктов.
    Определяет интерфейс и общие свойства для всех продуктов.
    """

    @abstractmethod
    def __init__(self, product_name, product_description, product_price, product_quantity):
        """
        Инициализация базовых свойств продукта.
        """
        self.product_name = product_name
        self.product_description = product_description
        self.__product_price = product_price
        self.product_quantity = product_quantity

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


class ProductMixin:
    """
    Миксин для логирования информации о продукте.
    """

    def __repr__(self):
        self.log_product_details()

    def log_product_details(self):
        """
        Выводит в консоль информацию о продукте.
        """
        print(
            f"{self.__class__.__name__}({self.product_name}, {self.product_description}, {self._product_price}, {self.product_quantity})")


class Product(AbstractProduct, ProductMixin):
    """
    Класс для представления товара с основными характеристиками.
    """

    def __init__(self, product_name, product_description, product_price, product_quantity):
        """
        Инициализация товара и вызов метода логирования.
        """
        self.product_name = product_name
        self.product_description = product_description
        self._product_price = product_price
        self.product_quantity = product_quantity
        super().__repr__()

    def __str__(self):
        """
        Возвращает строковое описание товара.
        """
        return f"{self.product_name}, {self._product_price} руб. Остаток: {self.product_quantity} шт."

    def __add__(self, other):
        """
        Складывает стоимости двух товаров одинакового типа.

        :param other: другой объект класса Product
        :return: сумма стоимости обоих товаров
        :raises TypeError: если объекты разных типов
        """
        if isinstance(self, type(other)):
            total_value_self = self._product_price * self.product_quantity
            total_value_other = other._product_price * other.product_quantity
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
        name_, description_, price_, quantity_ = (
            params["name"],
            params["description"],
            params["price"],
            params["quantity"]
        )

        return cls(name_, description_, price_, quantity_)

    @property
    def price(self):
        """Геттер для цены продукта."""
        return self._product_price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены продукта с проверкой."""

        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной.")
            return

            # Предупреждение при снижении цены ниже предыдущей и подтверждение изменения пользователем.

        if new_price < self._product_price:
            user_response = input("Вы ввели цену ниже прошлой. Подтвердите изменение цены (y/n): ")
            if user_response.lower() == "y":
                self._product_price = new_price
        else:
            self._product_price = new_price


class Category:
    """
    Класс для организации группы продуктов в категорию.

    Атрибуты:
      - category_name: название категории
      - category_description: описание категории
      - products_list: список продуктов в категории (приватный)
      - class-level счетчики количества категорий и продуктов
    """

    total_products_count = 0  # Общее число добавленных продуктов во все категории
    total_categories_count = 0  # Общее число созданных категорий

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

        Category.total_categories_count += 1


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
    Category.total_products_count += 1


@property
def products(self):
    """
    Возвращает список строк с информацией о продуктах в категории.
    """
    return [f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт.\n" for prod in self.__products_list]


class Smartphone(Product):
    """
    Класс для смартфонов с дополнительными характеристиками.

    Наследует основные свойства от класса Product и добавляет параметры эффективности,
     модели, памяти и цвета.
     """

    def __init__(self, name, description, price, quantity, efficiency_level, model_code, memory_size, color_variant):
        super().__init__(name, description, price, quantity)
        self.efficiency_level = efficiency_level  # уровень эффективности (например батареи)
        self.model_code = model_code  # модель смартфона
        self.memory_size = memory_size  # объем памяти
        self.color_variant = color_variant  # цвет устройства


class LawnGrass(Product):
    """
    Класс для травы газона с дополнительными характеристиками.

    Наследует основные свойства от класса Product и добавляет параметры страны происхождения,
    периода прорастания и цвета травы.
    """

    def __init__(self, name, description, price, quantity,
                 country_of_origin, germination_duration_days,
                 grass_color):
        super().__init__(name, description, price, quantity)
        self.country_of_origin = country_of_origin  # страна происхождения травы
        self.germination_duration_days = germination_duration_days  # период прорастания (дней)
        self.grass_color = grass_color  # цвет травы