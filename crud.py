from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import func, extract
from datetime import datetime, timedelta

# Category CRUD

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Product CRUD

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Inventory CRUD

def get_inventory(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()

def update_inventory(db: Session, product_id: int, stock: int):
    inventory = get_inventory(db, product_id)
    if inventory:
        change = stock - inventory.stock
        inventory.stock = stock
        db.commit()
        db.refresh(inventory)
        db.add(models.InventoryChange(inventory_id=inventory.id, change=change))
        db.commit()
        return inventory
    return None

def get_low_stock(db: Session, threshold: int = 10):
    return db.query(models.Inventory).filter(models.Inventory.stock <= threshold).all()

# Sale CRUD

def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()

def get_sales_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.Sale).filter(models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date).all()

def get_sales_by_product(db: Session, product_id: int):
    return db.query(models.Sale).filter(models.Sale.product_id == product_id).all()

def get_sales_by_category(db: Session, category_id: int):
    return db.query(models.Sale).join(models.Product).filter(models.Product.category_id == category_id).all()

# Revenue Analysis

def get_revenue_by_period(db: Session, period: str = 'daily'):
    if period == 'daily':
        result = db.query(func.date(models.Sale.sale_date).label('date'), func.sum(models.Sale.total_price).label('revenue')).group_by(func.date(models.Sale.sale_date)).all()
        return [{"date": str(row.date), "revenue": float(row.revenue or 0)} for row in result]
    elif period == 'weekly':
        result = db.query(extract('year', models.Sale.sale_date).label('year'), extract('week', models.Sale.sale_date).label('week'), func.sum(models.Sale.total_price).label('revenue')).group_by('year', 'week').all()
        return [{"year": int(row.year), "week": int(row.week), "revenue": float(row.revenue or 0)} for row in result]
    elif period == 'monthly':
        result = db.query(extract('year', models.Sale.sale_date).label('year'), extract('month', models.Sale.sale_date).label('month'), func.sum(models.Sale.total_price).label('revenue')).group_by('year', 'month').all()
        return [{"year": int(row.year), "month": int(row.month), "revenue": float(row.revenue or 0)} for row in result]
    elif period == 'annual':
        result = db.query(extract('year', models.Sale.sale_date).label('year'), func.sum(models.Sale.total_price).label('revenue')).group_by('year').all()
        return [{"year": int(row.year), "revenue": float(row.revenue or 0)} for row in result]
    else:
        return []

def compare_revenue(db: Session, start1: datetime, end1: datetime, start2: datetime, end2: datetime):
    rev1 = db.query(func.sum(models.Sale.total_price)).filter(models.Sale.sale_date >= start1, models.Sale.sale_date <= end1).scalar() or 0
    rev2 = db.query(func.sum(models.Sale.total_price)).filter(models.Sale.sale_date >= start2, models.Sale.sale_date <= end2).scalar() or 0
    return {"period1": rev1, "period2": rev2} 