import pytest
from src.classes import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура, автоматически сбрасывающая cчётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Смартфон", "Современный смартфон", 50000.0, 10)
    assert product.name == "Смартфон"
    assert product.description == "Современный смартфон"
    assert product.price == 50000.0
    assert product.quantity == 10


def test_category_initialization():
    product1 = Product("Смартфон", "Современный смартфон", 50000.0, 10)
    product2 = Product("Планшет", "Планшет для работы и развлечений", 30000.0, 5)
    category = Category("Электроника", "Цифровые устройства", [product1, product2])

    assert category.name == "Электроника"
    assert category.description == "Цифровые устройства"
    assert category.products == [product1, product2]


def test_category_count():
    p1 = Product("Телевизор", "4K телевизор", 70000.0, 3)
    Category("Бытовая техника", "Техника для дома", [p1])
    assert Category.category_count == 1

    p2 = Product("Ноутбук", "Лёгкий и мощный", 100000.0, 7)
    Category("Компьютеры", "Техника для работы", [p2])
    assert Category.category_count == 2


def test_product_count():
    p1 = Product("Мышь", "Геймерская мышь", 2000.0, 20)
    p2 = Product("Клавиатура", "Механическая клавиатура", 5000.0, 15)
    Category("Периферия", "Компьютерная периферия", [p1, p2])
    assert Category.product_count == 2

    p3 = Product("Монитор", "27 дюймов, 144 Гц", 25000.0, 8)
    Category("Дисплеи", "Мониторы и проекторы", [p3])
    assert Category.product_count == 3