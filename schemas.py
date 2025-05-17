from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    price: float
    brand: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

class InventoryBase(BaseModel):
    product_id: int
    stock: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_updated: datetime
    class Config:
        orm_mode = True

class InventoryChangeBase(BaseModel):
    inventory_id: int
    change: int

class InventoryChangeCreate(InventoryChangeBase):
    pass

class InventoryChange(InventoryChangeBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    channel: str

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sale_date: datetime
    class Config:
        orm_mode = True 