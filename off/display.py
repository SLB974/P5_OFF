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
