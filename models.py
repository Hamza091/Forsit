from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Float, nullable=False)
    brand = Column(String(100))
    inventory = relationship('Inventory', uselist=False, back_populates='product')
    sales = relationship('Sale', back_populates='product')
    category = relationship('Category', back_populates='products')

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True)
    stock = Column(Integer, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    product = relationship('Product', back_populates='inventory')
    changes = relationship('InventoryChange', back_populates='inventory')

class InventoryChange(Base):
    __tablename__ = 'inventory_changes'
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    change = Column(Integer, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    inventory = relationship('Inventory', back_populates='changes')

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, server_default=func.now())
    channel = Column(String(50))  # e.g., Amazon, Walmart
    product = relationship('Product', back_populates='sales') 