
class Product:
    """
    Класс для представления товара.
    """

    def __init__(self, product_name, product_description, product_price, product_quantity):
        """
        Инициализация объекта Product.
        :param product_name: Название товара
        :param product_description: Описание товара
        :param product_price: Цена товара
        :param product_quantity: Количество на складе
        """
        self.product_name = product_name
        self.product_description = product_description
        self.__product_price = product_price  # приватный атрибут для защиты цены
        self.product_quantity = product_quantity

    def __str__(self):
        """
        Возвращает строковое представление товара.
        """
        return f"{self.product_name}, {self.__product_price} руб. Остаток: {self.product_quantity} шт."

    def __add__(self, other):
        """
        Складывает общую стоимость двух товаров одинакового типа.
        :param other: Другой объект Product
        :return: Общая стоимость (цена * количество) обоих товаров
        """

        if type(self) is type(other):
            total_self = self.price * self.product_quantity
            total_other = other.price * other.product_quantity
            return total_self + total_other
        else:
            raise TypeError("Можно складывать только товары одного типа.")

    @classmethod
    def create_from_dict(cls, params: dict):
        """
        Создает объект Product из словаря параметров.
        :param params: словарь с ключами 'name', 'description', 'price', 'quantity'
        :return: экземпляр класса Product
        """

        name = params["name"]
        description = params["description"]
        price = params["price"]
        quantity = params["quantity"]
        return cls(name, description, price, quantity)

    @property
    def price(self):
        """Геттер для цены товара."""
        return self.__product_price

    @price.setter
    def price(self, new_price):
        """Сеттер для изменения цены с подтверждением при снижении."""
        if new_price <= 0:
            print("Цена не должна быть нулевой или отрицательной.")
            return

        if new_price < self.__product_price:
            confirmation = input("Вы ввели цену ниже прошлой. Подтвердите изменение (y/n): ")
            if confirmation.lower() == 'y':
                self.__product_price = new_price
            else:
                print("Изменение цены отменено.")
        else:
            self.__product_price = new_price


class Category:
    """
    Класс для представления категории товаров.
    """

    category_count = 0  # Общее число созданных категорий
    product_count = 0  # Общее число добавленных товаров во все категории

    def __init__(self, category_name, category_description, initial_products=None):
        """
        Инициализация объекта Category.

        :param category_name: Название категории
        :param category_description: Описание категории
        :param initial_products: список товаров для добавления (по желанию)
        """
        self.category_name = category_name
        self.category_description = category_description
        self.__products_list = []

        if initial_products:
            for prod in initial_products:
                self.add_product(prod)

        Category.category_count += 1

    def __str__(self):
        """
        Возвращает строковое описание категории и общего количества товаров.

        Подсчитывает сумму остатков всех товаров в категории.

        :return: Строка с названием и количеством товаров в штуках.

       """
        total_quantity = sum(product.product_quantity for product in self.__products_list)  #
        return f"{self.category_name}, количество продуктов: {total_quantity} шт."


        def add_product(self, product):
            """
            Добавляет товар в категорию.

            :param product: Объект класса Product или его наследников.
            :raises TypeError: Если переданный объект не является товаром.
            """
            if not isinstance(product, Product):
                raise TypeError("Можно добавлять только объекты типа Product или его наследников.")
            self.__products_list.append(product)
            Category.product_count += 1


        @property
        def products(self):
            """
            Возвращает список строк с информацией о каждом товаре в категории.

            :return: Список строк с именем, ценой и остатком товара.
            """
            return [
                f"{prod.product_name}, {prod.price} руб. Остаток: {prod.product_quantity} шт.\n"
                for prod in self.__products_list
            ]


class Smartphone(Product):
    """
    Наследник класса Product для смартфонов.
    """

    def __init__(self, name, description, price, quantity, efficiency_rating, model_number, memory_size, color):
        """
        Инициализация смартфона.

        :param name: Название модели смартфона.
        :param description: Описание.
        :param price: Цена.
        :param quantity: Количество на складе.
        :param efficiency_rating: Оценка эффективности (например).
        :param model_number: Модельный номер.
        :param memory_size: Объем памяти.
        :param color: Цвет устройства.
        """
        super().__init__(name, description, price, quantity)
        self.efficiency_rating = efficiency_rating
        self.model_number = model_number
        self.memory_size = memory_size
        self.color = color


class LawnGrass(Product):
    """
    Наследник класса Product для семян газона.
    """

    def __init__(self, name, description, price, quantity, country_of_origin,
                 germination_period_days, seed_color):
        """
        Инициализация семян газона.

        :param name: Название семян.
        :param description: Описание.
        :param price: Цена.
        :param quantity: Количество на складе.
        :param country_of_origin: Страна происхождения семян.
        :param germination_period_days: Период прорастания (в днях).
        :param seed_color: Цвет семян/семенного материала.
        """
        super().__init__(name, description, price, quantity)
        self.country_of_origin = country_of_origin
        self.germination_period_days = germination_period_days
        self.seed_color = seed_color
