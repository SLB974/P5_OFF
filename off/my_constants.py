# coding: utf-8
from env import login, password, host, dbase
from env import quantity_of_records_to_fetch

"""
Constants for off_api
"""
conn_source = f"mysql://{login}:{password}@{host}/{dbase}?charset=utf8mb4"
categories = ["Fromages blancs", "Poissons fumés", "Nouilles",
              "Pizzas", "Boissons"]
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
mess = "\n 0 - Quitter l'application\n\n"
messt = "-----------------------------------------------------------------------\n"
mess0 = "\nQuel est votre choix ? "
mess1 = "Bienvenue dans l'application Pur Beurre.\n" + \
    "Veuillez faire un choix dans la liste ci-dessous.\n\n" + \
    "0 - Quitter l'application.\n\n" + \
    "1 - Quel aliment souhaitez-vous remplacer ?\n" + \
    "2 - Retrouver mes aliments substitués.\n\n"

mess2 = "Veuillez choisir une catégorie dans la liste ci-dessous. \n" + mess
mess3 = "Veuillez choisir un produit dans la liste ci-dessous. \n" + mess
mess4 = messt + "Voici les informations concernant le produit choisi : \n" + messt + "\n"
mess5 = messt + "Voici les produits de substitution que nous vous proposons : \n"
mess5 = mess5 + \
    "(Ces produits ont un nutriscore meilleur pour la santé)\n" + messt + "\n"
mess6 = "\nVeuillez choisir un produit de substitution dans la liste ci-dessus.\n"
mess7 = "Choisissez dans la liste un enregistrement.\n\n" + mess
mess8 = "Il n'existe pas de produit meilleur pour la santé dans notre base de données\n"
mess8 = "Voici les produits de même valeur nutritionnelle dans notre base de données\n"
mess8 = mess8 + " 0 - Quitter l'application\n" + \
    " 1 - Retour écran précédent\n" + mess0
