# coding: utf-8
from off.db_staff import Db_write


def main():
    db = Db_write()
    db.add_my_categories()
    db.add_product_records()


if __name__ == '__main__':
    main()
