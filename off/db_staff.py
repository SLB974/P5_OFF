# coding: utf-8
from off._constants import categories
from off.orm import Session, Category, Product, ProductSave
from off.orm import t_stores_t, t_categories_t, Store


class Db_off:

    def __init__(self):
        self.session = Session()

    def add_my_categories(self):
        """ Adding categories choosed from constants.categories """

        for entry in categories:
            insertion = Category(categories_fr=entry)
            self.session.add(insertion)

        self.session.commit()

    def fetch_categories(self):
        """ Fetch categories from table category """

        for instance in self.session.query(Category).order_by(Category.id):
            dict0 = {}
            dict0['id'] = instance.id
            dict0['category'] = instance.categories_fr
            yield dict0

    def fetch_products(self, category):

        for instance in self.session.query(Product).filter(
                Product.category_id == category).order_by(Product.id):
            dict0 = {}
            dict0[str(instance.id)] = instance.product_name
            yield dict0

    def fetch_product_details(self, id):

        return self.session.query(Product).filter(
            Product.category_id == id)
