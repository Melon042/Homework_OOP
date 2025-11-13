import pytest
from src.classes import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура, автоматически сбрасывающая cчётчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 70000.0, 5)
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет"
    assert product.price == 70000.0
    assert product.quantity == 5


def test_category_initialization():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 70000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 200000.0, 8)
    category = Category("Смартфоны", "Новые смартфоны", [product1, product2])

    assert category.name == "Смартфоны"
    assert category.description == "Новые смартфоны"
    assert category.products == [product1, product2]


def test_category_product_count():
    p1 = Product("Iphone 15", "Смартфон", 200000.0, 3)
    Category("Смартфоны apple", "Новые смартфоны", [p1])

    p2 = Product("Samsung Galaxy S23 Ultra", "Смартфон", 70000.0, 7)
    Category("Смартфоны samsung", "Новые смартфоны", [p2])
    assert Category.category_count == 2
    assert Category.product_count == 2
