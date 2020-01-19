# coding: utf-8
import random
from off.default_constants import categories
from off.default_functions import format_category, is_category_fr
from off.api_scrapper import Api_consult
from off.orm import Session, Product, Category, Store
from off.orm import ProductSave
from off.orm import CategoriesT, StoresT
from sqlalchemy.orm import aliased
from subprocess import PIPE, Popen


class Db_off:

    """ Mother Class for fetching and writing database

    Class variables:
    ---------------
        session     :   initialize a Session to ORM
        product_id  :   integer to reference product id in use
        category_id :   integer to reference catefory_id in use
        store_id    :   integer to reference store id in use

    """

    def __init__(self):
        self.session = Session()
        self.product_id = 0
        self.category_id = 0
        self.store_idstore_id = 0

    def fetch_store_id(self, store=''):
        """ Fetch id for specified store """

        instance = (self.session.query(Store)
                    . filter(Store.store == store)
                    .first()
                    )

        return instance.id

    def fetch_category_id(self, cat=''):
        """ fetch id for specified category """

        instance = (self.session.query(Category)
                    .filter(Category.category == cat)
                    .first()
                    )

        return instance.id

    def reset_database(self):
        """ delete records from every table """

        self.session.query(CategoriesT).delete(synchronize_session=False)
        self.session.query(StoresT).delete(synchronize_session=False)
        self.session.query(ProductSave).delete(synchronize_session=False)
        self.session.query(Store).delete(synchronize_session=False)
        self.session.query(Category).delete(synchronize_session=False)
        self.session.query(Product).delete(synchronize_session=False)
        self.session.commit()
        self.session.close()


class Db_fetch(Db_off):

    """ Class for fetching database """

    def __init__(self):

        Db_off.__init__(self)

    def fetch_categories(self):
        """ Fetch my categories from table category """

        return (self.session.query
                (Category.id, Category.category.label('reference'))
                .filter(Category.my_category == True)
                .order_by(Category.category)
                .all()
                )

    def fetch_products(self, cat_id):
        """ Fetch products for specified category """

        return (self.session.query
                (Product.id, Product.product_name.label('reference'))
                .filter(Product.id == CategoriesT.product_id)
                .filter(CategoriesT.category_id == cat_id)
                .order_by(Product.product_name)
                .all()
                )

    def fetch_product_details(self, prod_id):
        """ Fetch details for specified product id """

        return (self.session.query(Product)
                    .filter(Product.id == prod_id)
                    .first()
                ).__dict__

    def fetch_product_categories(self, prod_id):
        """ Fetch categories for specified product """

        return (self.session.query
                (Category.category.label('reference'))
                .filter(Category.id == CategoriesT.category_id)
                .filter(CategoriesT.product_id == prod_id)
                .order_by('reference')
                .all()
                )

    def fetch_product_stores(self, prod_id):
        """ Fetch stores for specified product """

        return (self.session.query
                (Store.store.label('reference'))
                .filter(Store.id == StoresT.store_id)
                .filter(StoresT.product_id == prod_id)
                .order_by(Store.store)
                .all()
                )

    def fetch_product_replacement(self, prod_id, cat_id,  max_nutriscore):
        """ Fetch random product for replacement
            for a different product
            in same category
            with a minus nutriscore value
            """

        query = (self.session.query
                 (Product.id.label('id'),
                  Product.product_name.label('reference'))
                 .filter(Product.id != prod_id)
                 .filter(Product.id == CategoriesT.product_id)
                 .filter(Product.nutrition_grade_fr < max_nutriscore)
                 .filter(CategoriesT.category_id == cat_id)
                 )

        rowcount = query.count()
        randomrow = query.offset(int(rowcount*random.random())).first()

        if randomrow is None:
            return 0
        else:
            return randomrow.id

    def fetch_replacement_records(self):
        """ Fetch replacement recorded in database """

        Prod_rep = aliased(Product)

        return (self.session.query
                (ProductSave.id.label('id'),
                 Product.product_name.label('product'),
                 Prod_rep.product_name.label('replacement'))
                .filter(ProductSave.product_id == Product.id)
                .filter(ProductSave.product_replace_id == Prod_rep.id)
                .all()
                )


class Db_write(Db_off):

    """ Class for recording in database """

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

            self.add_categories_record(record_categories)
            self.add_stores_record(record_stores)

        self.session.commit()
        self.session.close()

    def add_categories_record(self, record_categories):
        """ add referenced categories in product records """

        for instance in record_categories:

            instance = instance.strip()
            instance = format_category(instance)

            if is_category_fr(instance):

                if instance.lower().strip() not in self.doubled_category:

                    insertion = Category(category=instance, my_category=0)
                    self.session.add(insertion)
                    self.session.flush()
                    self.category_id = insertion.id
                    self.doubled_category.add(instance.lower().strip())

                else:

                    self.category_id = self.fetch_category_id(instance)

                self.add_product_category()

    def add_product_category(self):
        """ add categories linked with product in table CategoriesT """

        insertion = CategoriesT(
            product_id=self.product_id, category_id=self.category_id)
        self.session.add(insertion)

    def add_stores_record(self, record_stores):
        """ add referenced stores in product's records """

        for instance in record_stores:

            instance = instance.strip()

            if instance != '':

                if instance.lower().strip() not in self.doubled_store:

                    insertion = Store(store=str(instance))
                    self.session.add(insertion)
                    self.session.flush()
                    self.store_id = insertion.id
                    self.doubled_store.add(instance.lower().strip())

                else:
                    self.store_id = self.fetch_store_id(instance)

                self.add_product_store()

    def add_product_store(self):
        """ add stores linked with product in table CategoriesT """

        insertion = StoresT(product_id=self.product_id,
                            store_id=self.store_id)
        self.session.add(insertion)

    def add_product_substitution(self, prod_id, rep_id):

        insertion = (ProductSave(
            product_id=prod_id,
            product_replace_id=rep_id)
        )
        self.session.add(insertion)
        self.session.commit()
        self.session.close()
