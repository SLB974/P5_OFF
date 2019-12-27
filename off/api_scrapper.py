# coding: utf-8
from sqlalchemy import inspect
from off.api_scripts import Api_consult
from off.db_staff import Db_off
from off.orm import Product, Session, t_categories_t


class Off_scrapper:

    def __init__(self):

        self.session = Session()

    def fetch_api_products(self):
        """ Fetch products from API """

        # Create a mapper that references Product()'s Columns
        mapper = inspect(Product())
        db = Db_off()
        api = Api_consult()

        # inject my_categories in database
        db.add_my_categories()

        # Loop on categories
        for instance in db.fetch_categories():

            print("Filling products for Category " +
                  str(instance['category'])+"...")

            response = api.get_results(instance["category"], 15)

            doubled_v = []

            # Loop on records in API's response
            for record in response["products"]:

                if record['product_name'].lower().strip() not in doubled_v and \
                    'nutrition_grade_fr' in record and \
                        record['nutrition_grade_fr'] != '':

                    record = {k: v for (k, v) in record.items()
                              if k in mapper.attrs and k != "id"}

                    record["category_id"] = instance["id"]
                    string = record['product_name'].lower()
                    string = string.strip()
                    doubled_v.append(record['product_name'].lower().strip())

                    yield record

    def add_product_records(self):
        """ save products in database """

        for record in self.fetch_api_products():
            # print(record)
            insertion = Product(**record)
            self.session.add(insertion)

        self.session.commit()
