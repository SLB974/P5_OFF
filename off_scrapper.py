# coding: utf-8
from sqlalchemy import inspect
from orm import Session, Category, Product
from constants import categories
from API_scripts import Api_consult


class OFF_scrapper:

    def __init__(self):

        self.session = Session()

    def add_choosen_categories(self):
        """ Adding categories choosed from constants.categories """

        for entry in categories:
            insertion = Category(categories_fr=entry)
            self.session.add(insertion)

        self.session.commit()

    def fetch_categories(self):
        """ Fetch categories from table category """

        for instance in self.session.query(Category).order_by(Category.id):
            yield {"category": instance.categories_fr, "id": instance.id}

    def fetch_products(self):
        """ Fetch products from API """

        # Create a mapper that references Product()'s Columns
        mapper = inspect(Product())

        # Create a reference to API_consult
        api = Api_consult()

        # Loop on records in Category()
        for instance in self.fetch_categories():

            # Loop on pages
            for page in range(api.pages):

                # Get API' response
                response = api.api_get_results(instance["category"], page+1)

                # Loop on records
                for record in response["products"]:

                    # Using Dictionnary comprehension for
                    # keeping only interresting datas
                    record = {k: v for (k, v) in record.items()
                              if k in mapper.attrs and k != "id"
                              and v is not None}

                    record["category_id"] = instance["id"]

                    # Using Dictionnary unpacking
                    yield record

    def add_product_records(self):
        """ save products in database """

        for record in self.fetch_products():
            insertion = Product(**record)
            self.session.add(insertion)

        self.session.commit()
