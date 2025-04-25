import unittest
from src.Product import Product

class TestProduct(unittest.TestCase):

    def setUp(self):
        """Создаем экземпляр продукта для тестов."""
        self.product = Product("Товар 1", "Описание товара 1", 100.0, 10)

    def test_product_initialization(self):
        """Проверяем правильность инициализации продукта."""
        self.assertEqual(self.product.name, "Товар 1")
        self.assertEqual(self.product.description, "Описание товара 1")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.quantity, 10)

    def test_product_attributes_type(self):
        """Проверяем типы атрибутов продукта."""
        self.assertIsInstance(self.product.name, str)
        self.assertIsInstance(self.product.description, str)
        self.assertIsInstance(self.product.price, float)
        self.assertIsInstance(self.product.quantity, int)

if __name__ == '__main__':
    unittest.main()