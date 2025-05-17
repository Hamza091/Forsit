# E-commerce Admin API

A FastAPI-based backend for e-commerce admin dashboards, providing sales, revenue, and inventory insights, as well as product management.

## Features
- Retrieve, filter, and analyze sales data
- Revenue analysis (daily, weekly, monthly, annual)
- Compare revenue across periods and categories
- Inventory management with low stock alerts
- Product registration

## Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL
- Docker

## Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/Hamza091/Forsit.git
cd Forsit
```

### 2. Configure Environment
Copy `.env.example` to `.env` and update DB credentials if needed.

### 3. Build and Run with Docker Compose
```
docker-compose up --build
```
- The API will be available at `http://localhost:8000`.
- MySQL will be available on port 3307 (host) mapped to 3306 (container).
- Demo data is loaded automatically on startup; no manual step is needed.

## API Endpoints

### Products
- `POST /products/` - Register a new product
- `GET /products/` - List all products

### Inventory
- `GET /inventory/` - View inventory status
- `GET /inventory/low-stock/` - Low stock alerts
- `PUT /inventory/{product_id}/` - Update inventory

### Sales
- `POST /sales/` - Register a sale
- `GET /sales/` - List sales
- `GET /sales/by-date/` - Sales by date range
- `GET /sales/by-product/{product_id}/` - Sales by product
- `GET /sales/by-category/{category_id}/` - Sales by category

### Revenue
- `GET /revenue/` - Revenue analysis (daily, weekly, monthly, annual)
- `GET /revenue/compare/` - Compare revenue between two periods

You can also access interactive API documentation via FastAPI's built-in Swagger UI at:
- `GET /docs` — interactive OpenAPI documentation for all endpoints.

## License
Confidential. For assessment use only. 
