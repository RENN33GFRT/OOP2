class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0  # Атрибут класса для хранения общего количества категорий
    product_count = 0     # Атрибут класса для хранения общего количества продуктов

    def __init__(self, name: str, description: str, products=None):
        self.name = name
        self.description = description
        self.products = []  # Список товаров в категории
        if products:
            for product in products:
                self.products.append(product)

        Category.category_count += 1

    def add_product(self, product: Product):
        self.products.append(product)
        Category.product_count += 1

    def get_product_count(self) -> int:
        return len(self.products)