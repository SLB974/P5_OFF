# coding: utf-8
import constants as ct
import requests
import json


class Api_consult:

    """
    Manage API's consultations
    """

    def __init__(self):
        self.source = ct.connection_source
        self.count = 0
        self.pages = 0

    def api_get_results(self, category, page):
        """
        API's GET consultation
        """

        url = "https://fr.openfoodfacts.org/category/" + \
            category + "/" + str(page) + ".json"
        response = requests.get(url)
        response = response.json()

        # attribute record's count
        self.count = response["count"]

        # attribute response's pages to consult
        self.pages = self.calculate_pages(self.count)

        return response

    def calculate_pages(self, records):
        """
        calculate how many pages to reach every record
        """
        records = int(records/20)
        if records > 10:
            records = 2
        if records < 1:
            records = 1
        return records
