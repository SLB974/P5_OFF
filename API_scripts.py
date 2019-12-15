# coding: utf-8
from constants import connection_source
import requests


class Api_consult:

    """
    Manage API's consultations
    """

    def __init__(self):
        self.source = connection_source
        self.pages = 1

    def api_get_results(self, category, page=1):
        """
        API's GET consultation
        """

        url = "https://fr.openfoodfacts.org/category/" + \
            category + "/" + str(page) + ".json"

        response = requests.get(url)
        response = response.json()

        return response
