# coding: utf-8
from off._usual_def import clear_screen, exit_script, format_for_screen
from off._constants import mess, mess0, mess1, mess2, mess3, mess4, mess5
from off._constants import mess6, mess7, mess8
from off.orm import Session, Category, Product, engine
from sqlalchemy.sql import text
from off.db_staff import Db_off


class Screen:

    """ Mother Class for displaying """

    def __init__(self, message):

        self.message = message
        self.references = {}
        self.list_ref = {}
        self.session = Session()
        self.db = Db_off()

    def message_display(self):

        clear_screen()

        response = self.response()

        if response is None:
            self.message_display()
        else:
            return response

    def response(self):

        resp = input(self.message + mess0)

        if resp == '0':
            exit_script()

        resp = self.list_ref[resp]

        if str(resp) not in self.references.keys():
            return None
        else:
            return int(resp)

    def fill_references(self, m_table, m_filter, m_order, m_field):

        dcount = 1

        records = self.session.query(m_table).filter(
            m_filter).order_by(m_order)

        for record in records:
            row = record.__dict__

            self.references[str(row['id'])] = row[m_field]
            self.list_ref[str(dcount)] = row['id']
            self.message = self.message + \
                (format_for_screen(dcount, row[m_field])) + "\n"
            dcount += 1


class Home_scr(Screen):

    """ Class for managing home screen """

    def __init__(self, message):

        Screen.__init__(self, message)
        self.references = {'1': 1, '2': 2}
        self.list_ref = {'1': 1, '2': 2}
        self.action(self.message_display())

    def action(self, option):

        if option == 1:
            cs = Category_scr(mess2)

        if option == 2:
            hs = History_scr(mess5)


class Category_scr(Screen):

    """ Class for category choosing screen """

    def __init__(self, message):

        Screen.__init__(self, message)
        self.fill_references(Category, Category.id ==
                             Category.id, Category.id, 'categories_fr')
        self.action(self.message_display())

    def action(self, option):

        ps = Product_scr(mess3, option)


class Product_scr(Screen):

    """ Class for product choosing screen """

    def __init__(self, message, id):

        self.id = id
        Screen.__init__(self, message)
        self.fill_references(Product, Product.category_id == self.id,
                             Product.product_name, 'product_name')
        self.action(self.message_display())

    def action(self, option):

        pds = Product_details_scr(mess4, option, self.id)


class Product_details_scr(Screen):

    def __init__(self, message, id, id_cat):
        self.id = id
        self.id_cat = id_cat
        self.max_nutriscore = 'F'
        Screen.__init__(self, message)
        self.fill_product_info()
        self.fill_references()
        self.message_display()

    def fill_product_info(self):
        records = self.session.query(Product).filter(Product.id == self.id)
        for record in records:
            row = record.__dict__
            info = "Produit : " + row['product_name'] + "\n"
            info = info + "Code : " + row['code'] + "\n"
            info = info + "url : " + row['url'] + "\n"
            info = info + "Marque : " + row['brands'] + "\n"
            info = info + "Quantité par packaging : " + \
                str(row['product_quantity']) + "\n"
            info = info + "Magasins : " + row['stores'] + "\n"
            info = info + "Nutriscore : " + \
                str(row['nutrition_grade_fr']) + "\n\n"
            info = info + mess5
            self.max_nutriscore = str(row['nutrition_grade_fr'])

            # if self.max_nutriscore == 'a':
            #     info = info + messt

            self.message = self.message + info

    def fill_references(self):

        dcount = 1
        records = self.session.query(Product).filter(
            Product.category_id == self.id_cat,
            Product.nutrition_grade_fr < self.max_nutriscore).order_by(
                Product.product_name)
        for record in records:
            row = record.__dict__

            self.references[str(row['id'])] = row['product_name']
            self.list_ref[str(dcount)] = row['id']
            self.message = self.message + \
                (format_for_screen(dcount, row['product_name'])) + "\n"
            dcount += 1


class History_scr(Screen):
    pass


class Home_screen:
    """ Manage Home page display """

    def __init__(self):
        self.references = {}
        self.valid_responses = ['0', '1', '2']
        self.message = mess1
        self.message_display()

    def message_display(self):
        clear_screen()
        print(self.message)

        response = self.response()

        if response is None:
            self.message_display()
        else:
            self.action(response)

    def response(self):
        resp = input(mess0)
        if resp not in self.valid_responses:
            return None
        else:
            return int(resp)

    def action(self, option):
        if option == 0:
            exit_script()

        if option == 1:
            cs = Category_screen()

        if option == 2:
            hs = History_screen()


class Category_screen:
    """ Manage option 1 - Choose Category page """

    def __init__(self):
        self.references = {}
        self.category = 0
        self.message = mess2
        self.valid_responses = ['0']
        self.message_display()

    def fill_references(self):
        db = Db_off()
        for instance in db.fetch_categories():
            self.references[str(instance['id'])] = instance['category']
            print(format_for_screen(int(instance['id']), instance['category']))

    def message_display(self):
        clear_screen()
        print(self.message)
        print(mess)
        self.fill_references()

        response = self.response()

        if response is None:
            self.message_display()
        else:
            self.action(response)

    def response(self):
        resp = input(mess0)

        if int(resp) == 0:
            exit_script()

        if resp not in self.references.keys():
            return None
        else:
            return int(resp)

    def action(self, option):

        ps = Product_screen()
        ps.category = option
        ps.message_display()


class Product_screen:
    """ Manage Choose Product page """

    def __init__(self):
        self.category = 0
        self.references = {}
        self.list_ref = {}
        self.message = mess3
        self.session = Session()

    def fill_references(self):
        dcount = 1
        for instance in self.session.query(Product).filter(
                Product.category_id == self.category).order_by(Product.id):
            print(instance['id'], instance[m_field])
            # self.references[str(instance.id)] = instance.product_name
            # self.list_ref[str(dcount)] = instance.id
            # print(format_for_screen(dcount, instance.product_name))
            dcount += 1

    def message_display(self):
        clear_screen()
        print(self.message)
        print(mess)
        self.fill_references()

        response = self.response()
        # print(response)
        # print(self.references)

        if response is None:
            self.message_display()
        else:
            self.action(response)

    def response(self):
        resp = input(mess0)

        if int(resp) == 0:
            exit_script()

        resp = self.list_ref[resp]

        if str(resp) not in self.references.keys():
            return None
        else:
            return int(resp)

    def action(self, option):
        pi = Product_informations()
        pi.product = option
        pi.message_display()


class Product_informations:

    def __init__(self):
        self.product = 0
        self.references = {}
        self.message = mess4
        self.session = Session()

    def message_display(self):
        clear_screen()
        print(self.message)
        print(mess)
        self.fill_references()

        response = self.response()

        if response is None:
            self.message_display()
        else:
            self.action(response)

    def response(self):
        pass

    def product_details(self):
        db = Db_off()
        instance = db.fetch_product_details(self.product)

        message = "Voici les informations sur le produit " + instance.product_name + " :\n"
        message = message + "Code : " + instance.code + "\n"
        message = message + "url : " + instance.url + "\n"
        message = message + "Marques : " + instance.brands + "\n"
        message = message + "Quantité par produit : " + instance.product_quantity + "\n"
        message = message + \
            "Nutriscore (fr) : " + instance.nutrition_grade_fr + "\n"
        message = message + "Magasins où acheter : " + instance.stores + "\n\n"

        message = message + "Voici les produits que nous vous conseillons d'essayer"


class History_screen:
    """ Manage option 2 - Fetch substituted products """

    def __init__(self):
        self.history = 0
        self.product = 0
        self.substitute = 0
        self.reference = {}

    def message(self):
        pass

    def response(self):
        pass


# class Screen:

#     def home_screen(self):
#         exit_script()
#         print(mess1)
#         self.home_response()

#     def home_response(self):
#         response = input(mess0)

#         if response not in ('0', '1', '2'):
#             self.home_screen

#         if response = '1':
#             self.screen_category()

#         elif response = '2':
#             self.screen_history()

#     def category_screen(self):

#         exit_script()
#         print('Choisissez une catégorie dans la liste.')
#         print('')

#         offs = off_scrapper.OFF_scrapper()
#         self.reference = {}

#         for instance in offs.fetch_categories():
#             self.reference[str(instance['id'])] = instance['category']
#             print(str(instance['id']) + ' - ' + instance['category'])

#         print('')

#     def product_screen(self):
#         pass

#     def history_screen(self):
#         pass
