from unittest.mock import patch
import pytest
from src.Classes import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def product():
    return Product("Iphone 16", "512GB, Gray space", 250000.0, 7)


@pytest.fixture
def smartphone():
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый"
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        7,
        "Зеленый"
    )


@pytest.fixture
def category(product, smartphone):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product, smartphone]
    )


def test_product_initialization(product):
    assert product.product_name == "Iphone 16"
    assert product.product_description == "512GB, Gray space"
    assert product.price == 250000.0
    assert product.product_quantity == 7


def test_product_str(product, capsys):
    print(product)
    captured = capsys.readouterr()
    assert captured.out == "Iphone 16, 250000.0 руб. Остаток: 7 шт.\n"


def test_product_add(product):
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert product + product2 == 250000.0 * 7 + 210000.0 * 8


def test_product_add_type_error(product, smartphone):
    with pytest.raises(TypeError, match="Можно складывать только товары одного типа."):
        product + smartphone


def test_product_create_from_dict():
    product = Product.create_from_dict({
        "name": "Test Product",
        "description": "Test Description",
        "price": 1000.0,
        "quantity": 5
    })
    assert product.product_name == "Test Product"
    assert product.product_description == "Test Description"
    assert product.price == 1000.0
    assert product.product_quantity == 5


@patch('builtins.input', return_value='y')
def test_product_price_setter_decrease(mock_input, product):
    product.price = 200000.0
    assert product.price == 200000.0


@patch('builtins.input', return_value='n')
def test_product_price_setter_decrease_cancel(mock_input, product, capsys):
    original_price = product.price
    product.price = 200000.0
    captured = capsys.readouterr()
    assert "Изменение цены отменено." in captured.out
    assert product.price == original_price


def test_product_price_setter_invalid(product, capsys):
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевой или отрицательной." in captured.out


def test_category_initialization(category, product, smartphone):
    assert category.category_name == "Смартфоны"
    assert len(category._Category__products_list) == 2
    assert Category.category_count >= 1
    assert Category.product_count >= 2


def test_category_str(category, capsys):
    print(category)
    captured = capsys.readouterr()
    assert "Смартфоны, количество продуктов: 12 шт." in captured.out


def test_category_products_property(category):
    products = category.products
    assert len(products) == 2
    assert all(isinstance(p, str) for p in products)


def test_category_add_product(category, product):
    initial_count = len(category._Category__products_list)
    category.add_product(product)
    assert len(category._Category__products_list) == initial_count + 1


def test_category_add_invalid_product(category):
    with pytest.raises(TypeError, match="Можно добавлять только объекты типа Product или его наследников."):
        category.add_product("invalid product")


def test_smartphone_initialization(smartphone):
    assert smartphone.product_name == "Samsung Galaxy S23 Ultra"
    assert smartphone.efficiency_rating == 95.5
    assert smartphone.model_number == "S23 Ultra"
    assert smartphone.memory_size == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_initialization(lawn_grass):
    assert lawn_grass.product_name == "Газонная трава"
    assert lawn_grass.country_of_origin == "Россия"
    assert lawn_grass.germination_period_days == 7
    assert lawn_grass.seed_color == "Зеленый"


def test_category_counters():
    initial_category_count = Category.category_count
    initial_product_count = Category.product_count

    product1 = Product("Test1", "Desc1", 100, 1)
    product2 = Product("Test2", "Desc2", 200, 2)

    category = Category("Test Category", "Test Description", [product1, product2])

    assert Category.category_count == initial_category_count + 1
    assert Category.product_count == initial_product_count + 2

    product3 = Product("Test3", "Desc3", 300, 3)
    category.add_product(product3)

    assert Category.product_count == initial_product_count + 3


def test_product_repr(product):
    repr_str = repr(product)
    assert "Product" in repr_str
    assert "Iphone 16" in repr_str
    assert "250000.0" in repr_str


def test_category_repr(category):
    repr_str = repr(category)
    assert "Category" in repr_str
    assert "Смартфоны" in repr_str
    assert str(len(category._Category__products_list)) in repr_str