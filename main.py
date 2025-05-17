from fastapi import FastAPI
from routers import router
from fastapi.responses import PlainTextResponse

app = FastAPI(title="E-commerce Admin API")

# Routers will be included here
# from routers import sales, inventory, products
# app.include_router(sales.router)
# app.include_router(inventory.router)
# app.include_router(products.router)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "E-commerce Admin API is running."}

@app.get("/documentation", response_class=PlainTextResponse)
def documentation():
    with open("DATABASE_SCHEMA.md", "r", encoding="utf-8") as f:
        return f.read() 