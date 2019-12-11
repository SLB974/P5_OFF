# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(10), primary_key=True)
    categories_fr = Column(String(250), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(INTEGER(10), primary_key=True)
    code = Column(INTEGER(10), unique=True)
    url = Column(String(250), nullable=False)
    brands = Column(String(100), nullable=False)
    product_name_fr = Column(String(200), nullable=False, index=True)
    category_id = Column(ForeignKey('category.id'),
                         nullable=False, unique=True)
    product_quantity = Column(String(20))
    nutrition_grade_fr = Column(CHAR(1), nullable=False, index=True)
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
