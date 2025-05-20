from src.Classes import Category, LawnGrass, Product, Smartphone, BaseProduct, LoggingMixin
import pytest
from unittest.mock import patch


def test_base_product_abstract():
    """Тест абстрактного класса"""
    with pytest.raises(TypeError):
        BaseProduct("Test", "Test", 100, 1)


@pytest.fixture
def sample_product():
    return Product("Телефон", "Смартфон", 50000, 10)


@pytest.fixture
def sample_category(sample_product):
    return Category("Электроника", "Техника", [sample_product])


def test_product_creation(sample_product):
    """Тест создания продукта"""
    assert sample_product.name == "Телефон"
    assert sample_product.price == 50000
    assert sample_product.quantity == 10


def test_product_str(sample_product):
    """Тест строкового представления"""
    assert str(sample_product) == "Телефон, 50000 руб. Остаток: 10 шт."


def test_product_add(sample_product):
    """Тест сложения продуктов"""
    p2 = Product("Ноутбук", "Игровой", 100000, 2)
    assert sample_product + p2 == 50000 * 10 + 100000 * 2

    with pytest.raises(TypeError):
        sample_product + "не продукт"


def test_category_creation(sample_category):
    """Тест создания категории"""
    assert sample_category.name == "Электроника"
    assert len(sample_category.products.split('\n')) == 1


def test_category_add_product(sample_category, sample_product):
    """Тест добавления продукта"""
    initial_count = len(sample_category.products.split('\n'))
    sample_category.add_product(Product("Планшет", "Графический", 30000, 5))
    assert len(sample_category.products.split('\n')) == initial_count + 1

    with pytest.raises(ValueError):
        sample_category.add_product("не продукт")


def test_smartphone_creation():
    """Тест создания смартфона"""
    phone = Smartphone("iPhone", "Pro", 100000, 5, "A15", "13", 256, "Black")
    assert phone.performance == "A15"
    assert phone.model == "13"


def test_lawn_grass_creation():
    """Тест создания газонной травы"""
    grass = LawnGrass("Трава", "Зеленая", 500, 100, "Россия", 14, "Green")
    assert grass.country == "Россия"
    assert grass.germination_period == 14


def test_category_counters():
    """Тест счетчиков категорий"""
    initial_categories = Category.total_categories
    initial_products = Category.total_unique_products

    p1 = Product("A", "Desc", 100, 1)
    p2 = Product("B", "Desc", 200, 1)
    Category("Test", "Desc", [p1, p2])

    assert Category.total_categories == initial_categories + 1
    assert Category.total_unique_products == initial_products + 2


def test_product_create_from_dict():
    """Тест создания продукта из словаря"""
    data = {
        "name": "Тест",
        "description": "Тест",
        "price": 100,
        "quantity": 1
    }
    product = Product.create_new_product(data)
    assert product.name == "Тест"
    assert product.price == 100