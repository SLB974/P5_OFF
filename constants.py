# coding: utf-8
from sfc import conninfo

"""
Constants for off_api
"""

connection_source = f"mysql://root:{conninfo}@localhost/off_db?charset=utf8mb4"
categories = ["Fromages blancs", "Poissons fumés", "Cookies",
              "Pizzas", "Pâtes à tartiner"]
