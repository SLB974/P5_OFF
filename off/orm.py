# coding: utf-8
from off._constants import connection_source
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String, Table
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Manage ORM
"""
engine = create_engine(connection_source)
Session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = Base.metadata


class Store(Base):
    __tablename__ = 'store'

    id = Column(INTEGER(10), primary_key=True)
    stores = Column(String(250), nullable=False)


t_stores_t = Table(
    'stores_t', metadata,
    Column('product_id', INTEGER(10)),
    Column('stores', String(100)),
    Column('stores_id', INTEGER(10))
)


t_categories_t = Table(
    'categories_t', metadata,
    Column('product_id', INTEGER(10)),
    Column('categories', String(100)),
    Column('categories_id', INTEGER(10))
)


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(10), primary_key=True)
    categories_fr = Column(String(250), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(INTEGER(10), primary_key=True)
    code = Column(String(15), nullable=False)
    url = Column(String(150), nullable=False)
    brands = Column(String(100))
    product_name = Column(String(200), nullable=False, index=True)
    category_id = Column(ForeignKey('category.id'), nullable=False, index=True)
    categories = Column(String(150))
    product_quantity = Column(String(20))
    nutrition_grade_fr = Column(CHAR(1), index=True)
    stores = Column(String(100))

    category = relationship('Category')


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
