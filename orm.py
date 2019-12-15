# coding: utf-8
import constants as ct
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

"""
Manage ORM
"""
engine = create_engine(ct.connection_source)
session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(10), primary_key=True)
    categories_fr = Column(String(250), nullable=False)

    def __init__(self, id, categories_fr):
        self.id = id
        self.categories_fr = categories_fr


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

    def __init__(self, id, code, url, brands, product_name, category_id,
                 product_name, product_quantity, nutrition_grade_fr, stores):

        self.id = id
        self.code = code
        self.url
        self.brands = brands
        self.product_name = product_name
        self.category_id = category_id
        self.product_quantity = product_quantity
        self.nutrition_grade_fr = nutrition_grade_fr
        self.stores = stores


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

    def __init__(self, date, product_id, product_replace_id):
        self.date = date
        self.product_id = product_id
        self.product_replace_id = product_replace_id
