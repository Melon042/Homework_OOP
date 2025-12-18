from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Базовый абстрактный класс для продуктов"""

    name: str
    description: str
    __price: float
    quantity: int

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        """Строковое отображение в формате: <{Название продукта}, {N} руб. Остаток: {N} шт.>"""
        pass

    @abstractmethod
    def __add__(self, other):
        """Возвращает общую стоимость складываемых товаров одного класса с учетом их количества"""
        pass

    @property
    @abstractmethod
    def price(self):
        """Возвращает цену объекта Product"""
        return self.__price

    @price.setter
    @abstractmethod
    def price(self, value):
        """Присваивает новую цену с проверкой корректности значения"""


class MixinInit:
    """При '__init__' печатает в консоль информацию от какого класса и с какими параметрами был создан объект."""

    def __init__(self):
        print(f"Создан объект: {repr(self)}")
        super().__init__()


class Product(MixinInit, BaseProduct):
    """Класс 'Продукт'"""

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = price
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.quantity = quantity

        super().__init__()

    def __repr__(self):
        """Строковое отображение в формате: ClassName('name', 'description', price, quantity)"""
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.__price}, {self.quantity})"

    def __str__(self):
        """Строковое отображение в формате: <{Название продукта}, {N} руб. Остаток: {N} шт.>"""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Возвращает общую стоимость складываемых товаров одного класса с учетом их количества"""
        if type(self) == type(other):
            result = self.__price * self.quantity + other.__price * other.quantity
            return result
        else:
            raise TypeError

    @classmethod
    def new_product(cls, product_data: dict, old_products: list = None):
        """Создаёт новый объект класса Product из словаря"""
        if old_products is None:
            old_products = []

        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        new_product = cls(name, description, price, quantity)

        for product in old_products:
            if product.name == new_product.name:
                new_product.quantity += product.quantity
                if product.price > new_product.price:
                    new_product.price = product.price

        return new_product

    @property
    def price(self):
        """Возвращает цену объекта Product"""
        return self.__price

    @price.setter
    def price(self, value):
        """Присваивает новую цену с проверкой корректности значения"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            if value < self.__price:
                answer = input('Новая цена ниже предыдущей, введите "y" для подтверждения или "n" для отмены.')
                if answer == "y":
                    self.__price = value
            else:
                self.__price = value


class Category:
    """Класс 'Категория'"""

    name: str
    description: str
    __products: list

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        """Строковое отображение в формате: <{Название категории}, количество продуктов: {N} шт.>"""
        total_products_count = 0
        for product in self.__products:
            total_products_count += product.quantity

        return f"{self.name}, количество продуктов: {total_products_count} шт."

    def add_product(self, product):
        """Добавляет объект класса Product в список товаров категории"""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError

    def middle_price(self):
        """Вычисляет среднюю цену всех товаров категории"""
        products = self.__products
        total_price = 0
        for product in products:
            total_price += product.price
        try:
            middle_price = total_price / len(products)
        except ZeroDivisionError:
            return 0
        else:
            return middle_price

    @property
    def products(self):
        """Возвращает список строк товаров объекта Product"""
        products = []
        for product in self.__products:
            products.append(str(product))

        return products


class CategoryIterator:
    """Вспомогательный класс для перебора товаров одной категории"""

    def __init__(self, category_obj):
        self.category_obj = category_obj
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.category_obj.products):
            product = self.category_obj.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration


class Smartphone(Product):
    """Подкласс класса Product 'Смартфон'"""

    efficiency: str
    model: str
    memory: str
    color: str

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Подкласс класса Product 'Трава газонная'"""

    country: str
    germination_period: str
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
