# coding: utf-8
from off._constants import connection_source, criterias
import requests


class Api_consult:

    """
    Manage API's consultations
    """

    def __init__(self):
        self.source = connection_source

    def get_results(self, category, quantity=10):
        """
        API's GET consultation
        parameters :
        category = searching category
        quantity = number of results
        """
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        criterias['page_size'] = quantity
        criterias['tag_1'] = category

        response = requests.get(url, params=criterias)
        response = response.json()

        return response
