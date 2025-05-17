from db import SessionLocal, engine, Base
import models
from datetime import datetime, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    # Categories
    categories = [models.Category(name="Electronics"), models.Category(name="Books"), models.Category(name="Clothing")]
    db.add_all(categories)
    db.commit()
    # Products
    products = [
        models.Product(name="iPhone 14", description="Apple smartphone", category_id=1, price=999.99, brand="Apple"),
        models.Product(name="Kindle Paperwhite", description="E-reader", category_id=2, price=129.99, brand="Amazon"),
        models.Product(name="Levi's Jeans", description="Denim jeans", category_id=3, price=59.99, brand="Levi's"),
        models.Product(name="Samsung TV", description="Smart TV", category_id=1, price=499.99, brand="Samsung"),
        models.Product(name="Python Programming Book", description="Learn Python", category_id=2, price=39.99, brand="O'Reilly"),
    ]
    db.add_all(products)
    db.commit()
    # Inventory
    for p in db.query(models.Product).all():
        inv = models.Inventory(product_id=p.id, stock=random.randint(5, 50))
        db.add(inv)
    db.commit()
    # Sales (Amazon & Walmart)
    channels = ["Amazon", "Walmart"]
    for p in db.query(models.Product).all():
        for i in range(10):
            sale = models.Sale(
                product_id=p.id,
                quantity=random.randint(1, 5),
                total_price=p.price * random.randint(1, 5),
                sale_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                channel=random.choice(channels)
            )
            db.add(sale)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Demo data inserted.") 