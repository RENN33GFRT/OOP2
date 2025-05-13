class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}, {self.__price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        sum1 = self.price * self.quantity
        sum2 = other.price * other.quantity
        return sum1 + sum2

    @classmethod
    def new_product(cls,params:dict):
        new_name,new_description,new_price,new_quantity = params['name'],params['description'],params['price'],params['quantity']
        return cls(new_name,new_description,new_price,new_quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,new_price):
        if new_price <= 0:
            print('Цена не должна быть нулевая или отрицательная')
        else:
            if new_price < self.__price:
                ans = str(input('Вы ввели цену ниже прошлой, подтвердите изменение цены (y/n,да/нет)'))
                if ans.lower() == 'y':
                    self.__price = new_price

class Category:
    name: str
    description: str
    products: list
    product_count = 0
    category_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []
        if products:
            for i in products:
                self.add_product(i)
        Category.category_count += 1

    def __str__(self):
        summ = 0
        for i in self.__products:
            summ += i.quantity
        return f'{self.name}, количество продуктов: {summ} шт.'

    def add_product(self,product):
        if not isinstance(product,Product):
            raise TypeError("Нельзя добавлять объекты не типа Класс")
        else:
            self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        my_list = []
        for i in self.__products:
            my_list.append(f"{i.name}, {i.price} руб. Остаток: {i.quantity} шт.\n")
        return my_list