# coding: utf-8
import jinja2

from off.default.utils import clear_screen, exit_script, format_for_screen
from off.default.constants import mess0
from off.db_staff import DbFetcher, DbWriter


class Screen:
    """Mother Class for displaying.

    Class variables :
    ---------------
    message     :   string message that will appear in terminal
    dict_ref    :   dict to link order of appearance to item's id
    list_item   :   list for formatted items for screen
    dbf         :   initialize class for database's fetching
    dbw         :   initialize class for database's writing

    Operation :
    ---------   - Fill references after fetching database if necessary
                - Initialize message for terminal
                - display message in terminal templating text file(s)
                - wait for input response
                - verify response's validity (if in link_ref)
                - daugther classes manage next screen regarding response
    """

    def __init__(self):

        self.message = ''
        self.dict_ref = {}
        self.list_item = []
        self.choice = 0
        self.dbf = DbFetcher()
        self.dbw = DbWriter()

    def fill_references(self, m_query):
        """ Fill references, dict_ref, and list_item
            from database query
            Parameter :     m_query (recordet)
        """

        dcount = 1

        for record in m_query:

            self.dict_ref[str(dcount)] = record.id
            self.list_item.append(format_for_screen(dcount, record.reference))
            dcount += 1

    def message_initialize(self, file):
        """Prepare message for terminal.

        Parameter   : file (text file for templating)
        recordset   : recordset to render

        return      : string
        """

        record = {'items': self.list_item}
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = jinja_env.get_template('scr/' + file)

        return template.render(record)

    def message_display(self):
        """Display message in terminal and wait for response.

        - if non-compliant response then display message again
        - else return user's choice

        return      : integer
        """

        clear_screen()

        response = self.response()

        if response is None:

            return self.message_display()

        else:

            return response

    def response(self):
        """Wait for user's choice.

        - exit if 0
        - return None if non-compliant
        - return item's id linked to user's choice (integer)
        """

        resp = input(self.message + mess0)

        if resp == '0':
            exit_script()

        if str(resp) not in self.dict_ref:
            return None

        else:

            resp = self.dict_ref[str(resp)]
            return int(resp)


class HomeScreen(Screen):

    """Class for displaying home screen."""

    def __init__(self):

        super().__init__()
        self.dict_ref = {'1': 1, '2': 2}
        self.message = self.message_initialize('scr_0.txt')
        self.action(self.message_display())

    def action(self, option):
        """"""

        if option == 1:
            CategoryScreen()

        if option == 2:
            HistoryScreen()


class CategoryScreen(Screen):

    """Class for displaying category screen."""

    def __init__(self):

        super().__init__()
        self.fill_references(self.dbf.fetch_categories())
        self.message = self.message_initialize('scr_1.txt')
        self.action(self.message_display())

    def action(self, option):

        ProductScreen(option)


class ProductScreen(Screen):

    """Class for displaying product screen.

    Class variables:
        ---------------
        id      : integer to reference product's id in use
        cat_id  : integer to reference category's id in use
    """

    def __init__(self, cat_id):

        self.id = 0
        self.cat_id = cat_id
        super().__init__()
        self.fill_references(self.dbf.fetch_products(self.cat_id))
        self.message = self.message_initialize('scr_11.txt')
        self.action(self.message_display())

    def action(self, option):

        ProductDetailsScreen(option, self.cat_id)


class ProductDetailsScreen(Screen):

    """Class for displaying product's details and  suggesting product of
    replacement.

    Class variables:
        ---------------
        prod_id             : integer to reference product's id in use
        cat_id              : integer to reference category's id in use
        max_nutriscore      : string to reference nutriscore in use
        prod_replacement    : integer to reference replacement id in use
    """

    def __init__(self, prod_id, cat_id):
        self.prod_id = prod_id
        self.cat_id = cat_id
        self.max_nutriscore = 'f'
        self.prod_replacement = 0
        super().__init__()
        self.message = self.message_initialize()
        self.action(self.message_display())

    def message_initialize(self):
        """ Prepare message for terminal
            replace mother class function
            return : string
            """
        # about product's details
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = jinja_env.get_template('scr/scr_12.txt')
        record = self.dbf.fetch_product_details(self.prod_id)
        message = template.render(record)
        self.max_nutriscore = str(record['nutrition_grade_fr'])

        self.prod_replacement = (self.dbf.fetch_product_replacement
                                 (self.prod_id,
                                  self.cat_id,
                                  self.max_nutriscore)
                                 )

        if self.prod_replacement != 0:

            # about replacement product's details
            template = jinja_env.get_template('scr/scr_15.txt')
            record = self.dbf.fetch_product_details(self.prod_replacement)
            message = message + '\n\n' + template.render(record)

            # about replacement product's stores
            template = jinja_env.get_template('scr/scr_14.txt')
            record = self.dbf.fetch_product_stores(self.prod_replacement)
            record = {'items': [x for item in record for x in item]}
            message = message + '\n\n' + template.render(record)

            # about user's choice
            template = jinja_env.get_template('scr/scr_16.txt')
            message = message + '\n\n' + template.render(record)

            self.dict_ref = {'1': 1, '2': 2}

        else:

            # about best choice
            template = jinja_env.get_template('scr/scr_17.txt')
            message = message + '\n\n' + template.render(record)

            self.dict_ref = {'1': 2}

        return message

    def action(self, option):
        """Manage what to do regarding response."""

        if option == 1:

            self.dbw.add_product_substitution(
                self.prod_id,
                self.prod_replacement
            )

            ReplacementSave(
                self.cat_id,
                self.prod_id,
                self.prod_replacement
            )

        if option == 2:

            ProductScreen(self.cat_id)


class ReplacementSave(Screen):

    """Class for displaying record's confirmation.

    Class variables:
    ---------------
    cat_id              : integer to reference category's id in use
    prod_id             : integer to reference product's id in use
    prod_replacement    : integer to reference replacement'id in use
    """

    def __init__(self, cat_id, prod_id, repl_id):
        self.cat_id = cat_id
        self.prod_id = prod_id
        self.prod_replacement = repl_id
        super().__init__()
        self.dict_ref = {'1': 1}
        self.message = self.message_initialize()
        self.action(self.message_display())

    def message_initialize(self):
        """prepare message for terminal.

        replace mother classe function
        """

        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = jinja_env.get_template('scr/scr_18.txt')
        return template.render()

    def action(self, option):
        """Manage what to do regarding response."""

        HomeScreen()


class HistoryScreen(Screen):

    """Class for displaying recorded substitutions."""

    def __init__(self):

        super().__init__()
        self.fill_references(self.dbf.fetch_replacement_records())

        if len(self.list_item) != 0:

            self.message = self.message_initialize('scr_19.txt')

        else:
            self.message = self.message_initialize('scr_20.txt')

        self.action(self.message_display())

    def fill_references(self, m_query):
        """Fill references, dict_ref, and list_item from database query.

        replace mother class method.

        Parameter :     m_query (recordet)
        """

        dcount = 1

        for record in m_query:

            reference = (record.replacement
                         + ' POUR REMPLACER '
                         + record.product)

            self.list_item.append(format_for_screen(dcount, reference))
            dcount += 1

        self.dict_ref = {'1': 1}

    def action(self, option):

        HomeScreen()
