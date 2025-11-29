import pytest
from src.classes import Product, Category
from unittest.mock import patch


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура, автоматически сбрасывающая cчётчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Тест инициализации объекта"""
    product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 70000.0, 5)
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет"
    assert product.price == 70000.0
    assert product.quantity == 5


def test_new_product_from_dict():
    """Тест создания продукта из словаря"""
    data = {
        "name": "Ноутбук",
        "description": "Игровой ноутбук",
        "price": 150000.0,
        "quantity": 10
    }
    product = Product.new_product(data)
    assert product.name == "Ноутбук"
    assert product.description == "Игровой ноутбук"
    assert product.price == 150000.0
    assert product.quantity == 10


def test_category_initialization():
    """Тест инициализации объекта Category"""
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 70000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 200000.0, 8)
    category = Category("Смартфоны", "Новые смартфоны", [product1, product2])

    assert category.name == "Смартфоны"
    assert category.description == "Новые смартфоны"
    assert category.products == ["Samsung Galaxy S23 Ultra, 70000.0 руб. Остаток: 5 шт.",
                                 "Iphone 15, 200000.0 руб. Остаток: 8 шт."]


def test_category_product_count():
    """Тест подсчёта количества категорий и товаров"""
    p1 = Product("Iphone 15", "Смартфон", 200000.0, 3)
    Category("Смартфоны apple", "Новые смартфоны", [p1])

    p2 = Product("Samsung Galaxy S23 Ultra", "Смартфон", 70000.0, 7)
    Category("Смартфоны samsung", "Новые смартфоны", [p2])
    assert Category.category_count == 2
    assert Category.product_count == 2


def test_product_price_setter():
    """Тест установки корректной цены"""
    product = Product("Телефон", "Описание", 10000.0, 5)
    product.price = 12000.0
    assert product.price == 12000.0


def test_product_price_setter_zero_or_negative(capsys):
    """Тест попытки установить нулевую или отрицательную цену"""
    product = Product("Телефон", "Описание", 10000.0, 5)

    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 10000.0

    product.price = -10000.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 10000.0


def test_product_price_setter_lower_price():
    """Тест понижения цены с имитацией ввода"""
    product = Product("Телефон", "Тестовый", 10000.0, 1)

    with patch('builtins.input', return_value='n'):
        product.price = 8000.0
    assert product.price == 10000.0

    with patch('builtins.input', return_value='y'):
        product.price = 8000.0
    assert product.price == 8000.0




def test_new_product_merge_existing():
    """Тест объединения при наличии дубликата по имени"""
    existing = Product("Смартфон", "Старое описание", 20000.0, 3)
    new_data = {
        "name": "Смартфон",
        "description": "Новое описание",
        "price": 18000.0,
        "quantity": 5
    }

    result = Product.new_product(new_data, old_products=[existing])

    assert result.quantity == 8
    assert result.price == 20000.0
    assert result.description == "Новое описание"


def test_new_product_merge_higher_new_price():
    """Тест: если новая цена выше — она должна быть установлена"""
    existing = Product("Часы", "Наручные часы", 6000.0, 2)
    new_data = {
        "name": "Часы",
        "description": "Наручные часы",
        "price": 7000.0,
        "quantity": 4
    }

    result = Product.new_product(new_data, old_products=[existing])
    assert result.price == 7000.0
    assert result.quantity == 6

def test_product_add():
    """Тест магического метода __add__ в классе Product"""
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    result = product1 + product2

    assert result == 2580000.0

def test_product_str():
    """Тест строкового отображения объекта класса Product"""
    product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)

    assert str(product) == 'Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.'

def test_category_str():
    """Тест строкового отображения объекта класса Category"""
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    assert str(category) == 'Смартфоны, количество продуктов: 27 шт.'
