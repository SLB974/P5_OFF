# coding: utf-8
from env import login, password, host, dbase
from env import quantity_of_records_to_fetch

"""
Constants for off_api
"""
conn_source = f"mysql://{login}:{password}@{host}/{dbase}?charset=utf8mb4"
categories = ["Fromages blancs", "Poissons", "Nouilles",
              "Pizzas", "Boissons", "Epicerie"]
criterias = {
    'search_simple': 1,
    'action': 'process',
    'tagtype_0': 'countries',
    'tag_contains_0': 'contains',
    'tag_0': 'france',
    'tagtype_1': 'categories',
    'tag_contains_1': 'contains',
    'tag_1': None,
    'tagtype_2': 'brands',
    'tag_contains_2': 'does_not_contain',
    'tag_2': '',
    'tagtype_3': 'stores',
    'tag_contains_3': 'does_not_contain',
    'tag_3': '',
    'tagtype_4': 'nutrition_grade_fr',
    'tag_contains_4': 'does not contain',
    'tag_4': None,
    'tagtype_5': 'product_name',
    'tag_contains_5': 'does_not_contain',
    'tag_5': None,
    'tagtype_6': 'categories_lc',
    'tag_contains_6': 'contains',
    'tag_6': 'fr',
    'tagtype_7': 'labels_lc',
    'tag_contains_7': 'contains',
    'tag_7': 'fr',
    # 'sort_by': 'unique_scans_n',
    'page_size': quantity_of_records_to_fetch,
    'json': 1
}
mess0 = "\nQuel est votre choix ? "
mess1 = ("Veuillez installer la base de données \n" +
         "depuis la console MySQL en lançant la commande \n" +
         "'SOURCE sql_script.sql;' puis relancez \n" +
         "l'application.")
