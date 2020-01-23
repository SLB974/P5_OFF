
# P5_OFF PURPOSE

- Request API OpenFoodFacts

- Save records in database

- User interface for database's requests and save

## GENERAL INFORMATIONS

- Please use Python 3.6 or later.

- Please note that our MySQL server version is 8.0.16

- Please rename **`env.sample.py`** in **`env.py`** and fill your personal informations for database connection and API requests' length.

- Please, use virtual environment. Follow [this link for further information](https://docs.python.org/fr/3/tutorial/venv.html).

- Please execute **`pip install -r requirements.txt`** in terminal to install proper environment

- Please execute command **`SOURCE sql_script.sql;`** in mySQL terminal to set database (file joined).

## INFORMATIONS FOR USERS

- Please execute **`python main.py`** in terminal to launch interface.

- User journey is clearly defined in user interface.

=============================================================================

## INFORMATIONS FOR DEVELOPPERS

- P5_OFF main files are located in **`P5_OFF`** main folder.

- P5_OFF contants.py and utils.py are located in **``P5_OFF/default``**

- P5_OFF files regarding classes are located in **`P5_OFF/off`** subfolder.

- P5_OFF template text files for user interface in terminal are located in **`P5_OFF/scr`** subfolder.

- P5_OFF GitHub repository url : <https://github.com/SLB974/P5_OFF>

### ABOUT USER INTERFACE

- Please execute **`python main.py`** in terminal to launch user interface.

- **`display.py`** file contains classes that manage user interface.

- Please see docstrings in **`display.py`** for further information.

- Please note that when attempting to launch main.py :

        - if database off_db is not initialized, programm will alert to install database at first.

        - if database is initialized but empty, programm will run initial filling before launching user interface.

=============================================================================

### ABOUT DATABASE MANAGEMENT

- Please source **`sql_script.sql`** in MySQL terminal to initialize database (file joined).

- **`orm.py`** file contains classes for SQLAlchemy ORM management.

- **`db_staff.py`** contains classes for fetching and recording in database.

- Please see docstrings in **`db_staff.py`** for further information.

### ABOUT API'S REQUEST

- **`api_scrapper.py`** contains classes for requesting API and cleaning results.

- Please see docstrings in **`api_scrapper.py`** for further information.
