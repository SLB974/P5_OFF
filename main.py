# coding: utf-8
from off.display import Home_scr
from off.db_staff import Db_fetch


def main():
    """ Verify if database is OK
        and run Home screen if so
        """

    db = Db_fetch()
    db.verify_database()
    Home_scr()


if __name__ == "__main__":
    main()
