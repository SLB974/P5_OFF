# coding: utf-8
from off.my_constants import conn_source
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String, Table
from sqlalchemy import create_engine, Index, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Manage ORM
"""
engine = create_engine(conn_source)
Session = sessionmaker(bind=engine, autoflush=True)
Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(10), primary_key=True,
                autoincrement=True, nullable=False)
    category = Column(String(250), nullable=False, unique=True)
    my_category = Column(Boolean)


class Product(Base):
    __tablename__ = 'product'

    id = Column(INTEGER(10), primary_key=True,
                autoincrement=True, nullable=False)
    code = Column(String(15), nullable=False, unique=True)
    url = Column(String(150), nullable=False, unique=True)
    brands = Column(String(100))
    product_name = Column(String(200), nullable=False, unique=True)
    product_quantity = Column(String(20))
    nutrition_grade_fr = Column(CHAR(1))


class Store(Base):
    __tablename__ = 'store'

    id = Column(INTEGER(10), primary_key=True,
                autoincrement=True, nullable=True)
    store = Column(String(250), nullable=False, unique=True)


class ProductSave(Base):
    __tablename__ = 'product_save'

    id = Column(INTEGER(10), primary_key=True)
    date = Column(DateTime, nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    product_replace_id = Column(ForeignKey('product.id'),
                                nullable=False, index=True)

    product = relationship('Product',
                           primaryjoin='ProductSave.product_id == Product.id')
    product_replace = relationship('Product',
                                   primaryjoin='ProductSave.product_replace_id \
                                       == Product.id')


class CategoriesT(Base):
    __tablename__ = 'categories_t'
    __table_args__ = (
        Index('product_categories', 'product_id', 'category_id', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    category_id = Column(ForeignKey('category.id'), index=True)

    category = relationship('Category')
    product = relationship('Product')


class StoresT(Base):
    __tablename__ = 'stores_t'
    __table_args__ = (
        Index('product_stores', 'product_id', 'store_id', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    store_id = Column(ForeignKey('store.id'), index=True)

    product = relationship('Product')
    store = relationship('Store')
