# coding: utf-8
from off.display import Home_scr
from off.db_staff import Db_off


def main():

    # Home_scr()
    db = Db_off()
    db.source_sql_script()


if __name__ == "__main__":
    main()
