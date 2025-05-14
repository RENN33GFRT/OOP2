from unittest.mock import patch

import pytest

from src.Classes import Category, LawnGrass, Product, Smartphone


def test_count_category():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )
    assert category1.category_count == 1
    assert category1.product_count == 2
    product3 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product3],
    )
    assert category2.category_count == 2
    assert category2.product_count == 3
    product4 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category1.add_product(product4)
    assert category1.product_count == 4
    with pytest.raises(TypeError):
        category1.add_product({})


def test_init_product(product):
    assert product.name == "Iphone 16"
    assert product.description == "512GB, Gray space"
    assert product.price == 250000.0
    assert product.quantity == 7


def test_init_category(category):
    assert category.name == "Смартфоны"
    assert (
        category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert category.products == [
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n",
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n",
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n",
    ]


def test_product_add_new():
    new_product = Product.new_product(
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
    product.price = -100
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
    mock_input.return_value = "y"
    product.price = 1000
    assert product.price == 1000
    mock_input.return_value = "n"
    product.price = 800
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
    assert captured.out == "Смартфоны, количество продуктов: 22 шт.\n"

    assert product1 + product2 == 2114000.0


def test_subclasses_product():
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")

    assert smartphone1 + smartphone2 == 2580000.0

    with pytest.raises(TypeError):
        assert smartphone1 + grass1

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
    assert grass1.germination_period == "7 дней"
    assert grass1.color == "Зеленый"