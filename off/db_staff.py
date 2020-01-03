# coding: utf-8
from off.my_constants import categories
from off.my_usual_def import format_category, is_category_fr
from off.api_scrapper import Api_consult
from off.orm import Session, Product, Category, Store
# from off.orm import ProductSave
from off.orm import CategoriesT, StoresT


class Db_off:

    """ Mother Class for consulting and writing in database """

    def __init__(self):
        self.session = Session()
        self.product_id = 0
        self.category_id = 0
        self.store_id = 0


class Db_fetch(Db_off):

    def __init__(self):

        Db_off.__init__(self)

    def fetch_categories(self):
        """ Fetch categories from table category """

        for instance in self.session.query(Category).order_by(Category.id):
            dict0 = {}
            dict0['id'] = instance.id
            dict0['category'] = instance.category
            yield dict0

    def fetch_products(self, category):
        """ Fetch products for specified category """

        for instance in self.session.query(Product).filter(
                Product.category_id == category).order_by(Product.id):
            dict0 = {}
            dict0[str(instance.id)] = instance.product_name
            yield dict0

    def fetch_product_details(self, id):
        """ Fetch details for specified product """

        return self.session.query(Product).filter(
            Product.category_id == id)

    def fetch_store_id(self, store=''):
        """ Fetch id for specified store """
        for instance in self.session.query(Store).filter(
                Store.store == store):
            return instance.id

    def fetch_category_id(self, cat=''):
        """ fetch id for specified category """
        for instance in self.session.query(Category).filter(
                Category.category == cat):
            return instance.id


class Db_write(Db_off):

    def __init__(self):

        self.doubled_category = set()
        self.doubled_store = set()

        Db_off.__init__(self)

    def add_my_categories(self):
        """ Adding categories choosed from constants.categories
            and add them to doubled_category set"""

        for entry in categories:
            insertion = Category(category=entry, my_category=True)
            self.session.add(insertion)
            self.doubled_category.add(entry.lower().strip())

        self.session.commit()

    def add_product_records(self):
        """ save products in database """

        api = Api_consult()

        for record in api.api_scrapp_and_clean():

            record_products = record[0]
            record_categories = record[1]
            record_stores = record[2]
            self.category_id = int(record[3])

            insertion = Product(**record_products)
            self.session.add(insertion)
            self.session.flush()
            self.product_id = insertion.id

            insertion = CategoriesT(
                product_id=self.product_id, category_id=self.category_id)
            self.session.add(insertion)

            self.add_categories_record(record_categories)
            self.add_stores_record(record_stores)

        self.session.commit()
        self.session.close()

    def add_categories_record(self, record_categories):

        for instance in record_categories:

            instance = instance.strip()
            instance = format_category(instance)

            if instance.lower().strip() not in self.doubled_category \
                    and is_category_fr(instance):

                insertion = Category(category=instance, my_category=0)
                self.session.add(insertion)
                self.session.flush()
                self.category_id = insertion.id
                self.doubled_category.add(instance.lower().strip())

                self.add_product_category()

    def add_product_category(self):

        insertion = CategoriesT(
            product_id=self.product_id, category_id=self.category_id)
        self.session.add(insertion)

    def add_stores_record(self, record_stores):

        for instance in record_stores:

            instance = instance.strip()

            if instance.lower().strip() not in self.doubled_store \
                    and instance != '':

                insertion = Store(store=str(instance))
                self.session.add(insertion)
                self.session.flush()
                self.store_id = insertion.id
                self.doubled_store.add(instance.lower().strip())

                self.add_product_store()

    def add_product_store(self):

        insertion = StoresT(product_id=self.product_id, store_id=self.store_id)
        self.session.add(insertion)
