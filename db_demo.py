# coding: utf-8
from off.db_staff import Db_write, Db_off

""" Demo script for original data importation in database """


def main():

    db = Db_write()
    db.reset_database()
    db.add_my_categories()
    db.add_product_records()


if __name__ == '__main__':
    main()
