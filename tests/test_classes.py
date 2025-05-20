from unittest.mock import patch
import pytest
from src.Classes import Category, LawnGrass, Product, Smartphone

from unittest.mock import patch
import pytest
from Classes import Category, LawnGrass, Product, Smartphone


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
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый"
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        country="Россия",
        germination_period=7,
        color="Зеленый"
    )


@pytest.fixture
def category(product, smartphone):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product, smartphone]
    )


def test_count_category(category):
    # Сбросим счетчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product.create_new_product({
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
    })
    product2 = Product.create_new_product({
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8
    })
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )
    assert Category.category_count == 1
    assert Category.product_count == 2

    product3 = Product.create_new_product({
        "name": '55" QLED 4K',
        "description": "Фоновая подсветка",
        "price": 123000.0,
        "quantity": 7
    })
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product3],
    )
    assert Category.category_count == 2
    assert Category.product_count == 3

    product4 = Product.create_new_product({
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14
    })
    category1.add_product(product4)
    assert Category.product_count == 4
    with pytest.raises(TypeError):
        category1.add_product({})


def test_init_product(product):
    assert product.name == "Iphone 16"
    assert product.description == "512GB, Gray space"
    assert product.price == 250000.0
    assert product.quantity == 7


def test_init_category(category):
    assert category.category_name == "Смартфоны"
    assert len(category.products) == 2


def test_product_add_new():
    new_product = Product.create_new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    assert new_product.name == "Samsung Galaxy S23 Ultra"
    assert new_product.price == 180000.0


@patch("builtins.input")
def test_product_price_set(mock_input, capsys):
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert product.price == 210000.0

    # Test invalid price
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевой или отрицательной." in captured.out
    assert product.price == 210000.0

    # Test price decrease with confirmation
    mock_input.return_value = "y"
    product.price = 1000
    assert product.price == 1000

    # Test price decrease without confirmation
    mock_input.return_value = "n"
    product.price = 800
    captured = capsys.readouterr()
    assert "Изменение цены отменено." in captured.out
    assert product.price == 1000


def test_classes_methods(capsys):
    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )

    print(str(product1))
    captured = capsys.readouterr()
    assert captured.out == "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"

    print(str(product2))
    captured = capsys.readouterr()
    assert captured.out == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"

    print(str(category))
    captured = capsys.readouterr()
    assert "Смартфоны, количество продуктов: 22 шт." in captured.out

    assert product1 + product2 == 210000.0 * 8 + 31000.0 * 14


def test_subclasses_product():
    smartphone1 = Smartphone.create_new_product({
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
        "efficiency": 95.5,
        "model": "S23 Ultra",
        "memory": 256,
        "color": "Серый"
    })
    smartphone2 = Smartphone.create_new_product({
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8,
        "efficiency": 98.2,
        "model": "15",
        "memory": 512,
        "color": "Gray space"
    })
    grass1 = LawnGrass.create_new_product({
        "name": "Газонная трава",
        "description": "Элитная трава для газона",
        "price": 500.0,
        "quantity": 20,
        "country": "Россия",
        "germination_period": 7,
        "color": "Зеленый"
    })

    assert smartphone1 + smartphone2 == 180000.0 * 5 + 210000.0 * 8

    with pytest.raises(TypeError):
        smartphone1 + grass1

    assert smartphone1.name == "Samsung Galaxy S23 Ultra"
    assert smartphone1.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone1.price == 180000.0
    assert smartphone1.quantity == 5
    assert smartphone1.efficiency == 95.5
    assert smartphone1.model == "S23 Ultra"
    assert smartphone1.memory == 256
    assert smartphone1.color == "Серый"

    assert grass1.name == "Газонная трава"
    assert grass1.description == "Элитная трава для газона"
    assert grass1.price == 500.0
    assert grass1.quantity == 20
    assert grass1.country == "Россия"
    assert grass1.germination_period == 7
    assert grass1.color == "Зеленый"


def test_create_with_missing_params():
    # Тест создания Smartphone с неполными параметрами
    smartphone = Smartphone.create_new_product({
        "name": "Test Phone",
        "description": "Test",
        "price": 1000,
        "quantity": 1
    })
    assert smartphone.efficiency == 0
    assert smartphone.model == ""

    # Тест создания LawnGrass с неполными параметрами
    grass = LawnGrass.create_new_product({
        "name": "Test Grass",
        "description": "Test",
        "price": 100,
        "quantity": 1
    })
    assert grass.country == ""
    assert grass.germination_period == 0
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
        efficiency_level=95.5,
        model_code="S23 Ultra",
        memory_size=256,
        color_variant="Серый"
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        country_of_origin="Россия",
        germination_duration_days=7,
        grass_color="Зеленый"
    )


@pytest.fixture
def category(product, smartphone):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product, smartphone]
    )


def test_count_category():
    # Сбросим счетчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product.create_new_product({
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
    })
    product2 = Product.create_new_product({
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8
    })
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )
    assert Category.category_count == 1
    assert Category.product_count == 2

    product3 = Product.create_new_product({
        "name": '55" QLED 4K',
        "description": "Фоновая подсветка",
        "price": 123000.0,
        "quantity": 7
    })
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product3],
    )
    assert Category.category_count == 2
    assert Category.product_count == 3

    product4 = Product.create_new_product({
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14
    })
    category1.add_product(product4)
    assert Category.product_count == 4
    with pytest.raises(TypeError):
        category1.add_product({})


def test_init_product(product):
    assert product.name == "Iphone 16"
    assert product.description == "512GB, Gray space"
    assert product.price == 250000.0
    assert product.quantity == 7


def test_init_category(category):
    assert category.category_name == "Смартфоны"
    assert len(category.products) == 2


def test_product_add_new():
    new_product = Product.create_new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    assert new_product.name == "Samsung Galaxy S23 Ultra"
    assert new_product.price == 180000.0


@patch("builtins.input")
def test_product_price_set(mock_input, capsys):
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert product.price == 210000.0

    # Test invalid price
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевой или отрицательной." in captured.out
    assert product.price == 210000.0

    # Test price decrease with confirmation
    mock_input.return_value = "y"
    product.price = 1000
    assert product.price == 1000

    # Test price decrease without confirmation
    mock_input.return_value = "n"
    product.price = 800
    captured = capsys.readouterr()
    assert "Изменение цены отменено." in captured.out
    assert product.price == 1000


def test_classes_methods(capsys):
    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )

    print(str(product1))
    captured = capsys.readouterr()
    assert captured.out == "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"

    print(str(product2))
    captured = capsys.readouterr()
    assert captured.out == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"

    print(str(category))
    captured = capsys.readouterr()
    assert "Смартфоны, количество товаров: 22 шт." in captured.out

    assert product1 + product2 == 210000.0 * 8 + 31000.0 * 14


def test_subclasses_product():
    smartphone1 = Smartphone.create_new_product({
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
        "efficiency_level": 95.5,
        "model_code": "S23 Ultra",
        "memory_size": 256,
        "color_variant": "Серый"
    })
    smartphone2 = Smartphone.create_new_product({
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8,
        "efficiency_level": 98.2,
        "model_code": "15",
        "memory_size": 512,
        "color_variant": "Gray space"
    })
    grass1 = LawnGrass.create_new_product({
        "name": "Газонная трава",
        "description": "Элитная трава для газона",
        "price": 500.0,
        "quantity": 20,
        "country_of_origin": "Россия",
        "germination_duration_days": 7,
        "grass_color": "Зеленый"
    })

    assert smartphone1 + smartphone2 == 180000.0 * 5 + 210000.0 * 8

    with pytest.raises(TypeError):
        smartphone1 + grass1

    assert smartphone1.name == "Samsung Galaxy S23 Ultra"
    assert smartphone1.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone1.price == 180000.0
    assert smartphone1.quantity == 5
    assert smartphone1.efficiency == 95.5
    assert smartphone1.model == "S23 Ultra"
    assert smartphone1.memory == 256
    assert smartphone1.color == "Серый"

    assert grass1.name == "Газонная трава"
    assert grass1.description == "Элитная трава для газона"
    assert grass1.price == 500.0
    assert grass1.quantity == 20
    assert grass1.country == "Россия"
    assert grass1.germination_period == 7
    assert grass1.color == "Зеленый"


def test_create_with_missing_params():
    # Тест создания Smartphone с неполными параметрами
    smartphone = Smartphone.create_new_product({
        "name": "Test Phone",
        "description": "Test",
        "price": 1000,
        "quantity": 1
    })
    assert smartphone.efficiency == 0
    assert smartphone.model == ""

    # Тест создания LawnGrass с неполными параметрами
    grass = LawnGrass.create_new_product({
        "name": "Test Grass",
        "description": "Test",
        "price": 100,
        "quantity": 1
    })
    assert grass.country == ""
    assert grass.germination_period == 0