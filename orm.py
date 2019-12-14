# coding: utf-8
import constants as ct
import API_scripts as api
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

"""
Manage ORM
"""

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(10), primary_key=True)
    categories_fr = Column(String(250), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(INTEGER(10), primary_key=True)
    code = Column(String(13), nullable=False, unique=False)
    url = Column(String(250), nullable=False)
    brands = Column(String(100))
    product_name = Column(String(200), nullable=False, index=True)
    category_id = Column(ForeignKey('category.id'), nullable=False, index=True)
    product_quantity = Column(String(20))
    nutrition_grade_fr = Column(CHAR(1), index=True)
    stores = Column(String(100))

    category = relationship('Category')

    def __repr__(self):
        return "<Product(code='%s', url='%s', brands='%s',product_name='%s', category_id='%s', product_quantity='%s', nutrition_grade_fr='%s', stores='%s')>" % (self.code, self.url, self.brands, self.product_name, self.category_id, self.nutrition_grade_fr, self.stores)


class ProductSave(Base):
    __tablename__ = 'product_save'

    id = Column(INTEGER(10), primary_key=True)
    date = Column(DateTime, nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    product_replace_id = Column(ForeignKey(
        'product.id'), nullable=False, index=True)

    product = relationship(
        'Product', primaryjoin='ProductSave.product_id == Product.id')
    product_replace = relationship(
        'Product', primaryjoin='ProductSave.product_replace_id == Product.id')


class Connection:

    def __init__(self):
        self.source = ct.connection_source
        self.engine = create_engine(self.source)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_product_columns(self, column):
        mapper = inspect(Product)
        if column in mapper.attrs:
            return True
        else:
            return False
        # for column in mapper.attrs:
        #     print(column.key)

    def add_categories(self):

        for entry in ct.categories:
            insertion = Category(categories_fr=entry)
            self.session.add(insertion)
            self.session.commit()

    def add_products(self):
        """
        Add in table product records from API's consultation for every category
        """

        # create a mapper that references Product()'s Columns
        mapper = inspect(Product)
        apig = api.Api_consult()

        # Loop on records in Category()
        for instance in self.session.query(Category).order_by(Category.id):
            response = apig.api_get_results(instance.categories_fr, 1)

            # Loop on pages
            for page in range(1, apig.pages):

                if page != 1:
                    response = apig.api_get_results(
                        instance.categories_fr, page)

                # Loop on records
                for record in response["products"]:

                    # Using Dictionnary comprehension for
                    # keeping only interresting datas
                    record = {k: v for (k, v) in record.items()
                              if k in mapper.attrs and k != "id"
                              and v is not None}

                    record["category_id"] = instance.id

                    # Using Dictionnary unpacking
                    # for initializing insertion argument
                    insertion = Product(**record)
                    print(record)
                    print("--------------------------------------")
                    # processing session add and commit.
                    self.session.add(insertion)
                    self.session.commit()
