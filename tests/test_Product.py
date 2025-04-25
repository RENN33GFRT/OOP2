import unittest
from src.Product import Product, Category

class TestProductAndCategory(unittest.TestCase):

    def setUp(self):
        """Создаем экземпляры для тестов."""
        self.product1 = Product("Товар 1", "Описание товара 1", 100.0, 10)
        self.product2 = Product("Товар 2", "Описание товара 2", 200.0, 5)
        self.category = Category("Категория 1", "Описание категории 1")

    def test_product_initialization(self):
        """Проверяем правильность инициализации продукта."""
        self.assertEqual(self.product1.name, "Товар 1")
        self.assertEqual(self.product1.description, "Описание товара 1")
        self.assertEqual(self.product1.price, 100.0)
        self.assertEqual(self.product1.quantity, 10)

    def test_category_initialization(self):
        """Проверяем правильность инициализации категории."""
        self.assertEqual(self.category.name, "Категория 1")
        self.assertEqual(self.category.description, "Описание категории 1")
        self.assertEqual(len(self.category.products), 0)

    def test_add_product_to_category(self):
        """Проверяем добавление продукта в категорию."""
        self.category.add_product(self.product1)

        # Проверяем количество продуктов в категории
        self.assertEqual(len(self.category.products), 1)

        # Проверяем добавленный продукт
        self.assertEqual(self.category.products[0], self.product1)

    def test_total_products_incremented(self):
        """Проверяем увеличение общего количества продуктов при добавлении."""
        initial_total_products = Category.product_count

        # Добавляем продукт в категорию
        self.category.add_product(self.product2)

        # Проверяем общее количество продуктов
        self.assertEqual(Category.product_count, initial_total_products + 1)


if __name__ == '__main__':
    unittest.main()