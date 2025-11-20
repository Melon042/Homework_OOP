class Product:
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
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, old_products: list = None):
        """Создаёт новый объект класса Product из словаря"""
        if old_products is None:
            old_products = []

        name = product_data['name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']

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
            print('Цена не должна быть нулевая или отрицательная')
        else:
            if value < self.__price:
                answer = input('Новая цена ниже предыдущей, введите "y" для подтверждения или "n" для отмены.')
                if answer == 'y':
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


    def add_product(self, product):
        """Добавляет объект класса Product в список товаров категории"""
        self.__products.append(product)
        Category.product_count += 1


    @property
    def products(self):
        """Возвращает список строк товаров объекта Product"""
        products = []
        for product in self.__products:
            products.append(f'{product.name}, {product.price} руб. Остаток: {product.quantity} шт.')

        return products
