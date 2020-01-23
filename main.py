# coding: utf-8
from off.display import HomeScreen
from off.db_staff import DbFetcher


def main():
    """Verify if database is OK and run Home screen if so."""

    db = DbFetcher()
    db.verify_database()
    HomeScreen()


if __name__ == "__main__":
    main()
