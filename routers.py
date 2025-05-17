from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, schemas
from dependencies import get_db
from datetime import datetime
from typing import List, Optional

router = APIRouter()

# --- Product Endpoints ---
@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/products/", response_model=List[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

# --- Inventory Endpoints ---
@router.get("/inventory/", response_model=List[schemas.Inventory])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(crud.models.Inventory).all()

@router.get("/inventory/low-stock/", response_model=List[schemas.Inventory])
def low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    return crud.get_low_stock(db, threshold)

@router.put("/inventory/{product_id}/", response_model=schemas.Inventory)
def update_inventory(product_id: int, stock: int, db: Session = Depends(get_db)):
    inv = crud.update_inventory(db, product_id, stock)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inv

# --- Sales Endpoints ---
@router.post("/sales/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)

@router.get("/sales/", response_model=List[schemas.Sale])
def list_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales(db, skip=skip, limit=limit)

@router.get("/sales/by-date/", response_model=List[schemas.Sale])
def sales_by_date(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return crud.get_sales_by_date_range(db, start, end)

@router.get("/sales/by-product/{product_id}/", response_model=List[schemas.Sale])
def sales_by_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_sales_by_product(db, product_id)

@router.get("/sales/by-category/{category_id}/", response_model=List[schemas.Sale])
def sales_by_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_sales_by_category(db, category_id)

@router.get("/revenue/", response_model=List)
def revenue(period: str = Query('daily', enum=['daily', 'weekly', 'monthly', 'annual']), db: Session = Depends(get_db)):
    return crud.get_revenue_by_period(db, period)

@router.get("/revenue/compare/")
def compare_revenue(start1: datetime, end1: datetime, start2: datetime, end2: datetime, db: Session = Depends(get_db)):
    return crud.compare_revenue(db, start1, end1, start2, end2) 