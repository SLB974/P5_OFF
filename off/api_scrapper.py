# coding: utf-8
from off.default_constants import conn_source, criterias
import requests
from sqlalchemy import inspect
from off.orm import Product, Session, Category


class Api_consult:

    """
    Manage API's consultations
    """

    def __init__(self):
        self.source = conn_source
        self.doubled_code = set()
        self.doubled_name = set()
        self.session = Session()

    def get_results(self, category):
        """
        API's GET consultation
        parameters : category = searching category
        """
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"

        criterias['tag_1'] = category

        response = requests.get(url, params=criterias)
        response = response.json()

        return response

    def api_scrapp_and_clean(self):
        """ Fetch products from API and clean datas for export to database"""

        # Create a mapper that references Product()'s Columns
        mapper = inspect(Product())

        # Loop on categories
        for instance in self.session.query(Category).order_by(Category.id):

            print("Filling products for Category " +
                  str(instance.category)+"...")

            response = self.get_results(instance.category)

            # Loop on records in API's response
            for record in response["products"]:

                if record['product_name'].lower().strip() not in \
                    self.doubled_name and record['code'] not in \
                        self.doubled_code and 'nutrition_grade_fr' in record \
                        and record['nutrition_grade_fr'] != '':

                    record_categories = record['categories'].split(',')
                    record_categories = (
                        v for v in record_categories if v != '')

                    record_stores = record['stores'].split(',')
                    record_stores = (v for v in record_stores if v != '')

                    record_products = {k: v for (k, v) in record.items()
                                       if k in mapper.attrs and k != "id"}

                    self.doubled_name.add(
                        record_products['product_name'].lower().strip())
                    self.doubled_code.add(record_products['code'])

                    yield record_products, record_categories, \
                        record_stores, instance.id
