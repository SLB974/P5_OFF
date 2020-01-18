
# P5_OFF PURPOSE

- Request API OpenFoodFacts

- Save records in database

- User interface for database's requests and save


## INFORMATIONS FOR USERS AND DEVELOPPERS

- Please copy **`env.sample.py`** to  **`env.py`** and fill your personal informations for database connection.

- Please execute **`pip install -r requirements.txt`** in terminal to install proper environment


## INFORMATIONS FOR USERS

- Please execute **`python main.py`** in terminal to launch interface.

- User journey is clearly defined in user interface.

=============================================================================

## INFORMATIONS FOR DEVELOPPERS

- P5_OFF main files are located in **`P5_OFF`** main folder.

- P5_OFF files regarding classes, usual constants and functions are located in **`off`** subfolder.

- P5_OFF template text files for user interface in terminal are located in **`scr`** subfolder.

- P5_OFF GitHub repository url : <https://github.com/SLB974/P5_OFF>


### ABOUT USER INTERFACE

- Please execute **`python main.py`** in terminal to launch user interface.

- **`display.py`** file contains classes that manage user interface.

- Please see docstrings in **`display.py`** for further information.

=============================================================================

### ABOUT DATABASE MANAGEMENT

- Please source **`sql_script.sql`** in mySQL console to reset database (file joined).

- **`orm.py`** file contains classes for SQLAlchemy ORM management.

- **`db_staff.py`** contains classes for fetching and recording in database.

- Please see docstrings in **`db_staff.py`** for further information.


### ABOUT API'S REQUEST AND RECORD IN DATABASE

- Please don't forget to reset database before launching **`db_demo.py`** file.

- Please execute **`db_demo.py`** to launch script that manages API's requests and record in database.

- **`api_scrapper.py`** contains classes for requesting API and cleaning results.

- Please see docstrings in **`api_scrapper.py`** for further information.
