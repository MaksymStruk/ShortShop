# ShortShop API

A modern, async e-commerce API built with FastAPI, PostgreSQL, and Redis. Features product management, shopping cart functionality, and comprehensive API documentation.

## 🚀 Features

- **Product Management** - Complete CRUD operations for products with variants, images, and recommendations
- **Shopping Cart** - Session-based cart management with item operations
- **Product Variants** - Support for different sizes, colors, and stock status
- **Product Recommendations** - Link related products for better user experience
- **RESTful API** - Complete CRUD operations with comprehensive documentation
- **Docker Support** - Easy deployment with Docker Compose
- **Async Architecture** - Fully asynchronous operations for better performance
- **Unit Tests** - Comprehensive test coverage for all API endpoints

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Primary database
- **Celery** - Distributed task queue for background processing
- **Redis** - Message broker and result backend for Celery
- **Pydantic** - Data validation and serialization
- **Loguru** - Advanced logging

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/MaksymStruk/ShortShop.git
cd ShortShop
```

### 2. Create .env from .env-sample
You can use demo data from .env-sample

### 3. Start the Application
```bash
docker compose up --build --detach
```

### 4. Access the Application
- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

### 5. (Unfinished) Run Tests
```bash
docker compose exec backend pytest -v
```

### 6. (Unfinished) Run Pylint
```bash
pylint backend/app/ --rcfile=backend/.pylintrc
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/
```

### Health Endpoints

#### API Root
```http
GET /
```

#### Health Check
```http
GET /health
```

### Product Endpoints

#### Get All Products
```http
GET /api/v1/product/
```
**Query Parameters:**
- `skip` (int, optional): Number of products to skip (default: 0)
- `limit` (int, optional): Maximum products to return (default: 100)

#### Get Product by ID
```http
GET /api/v1/product/{product_id}
```

#### Create Product
```http
POST /api/v1/product/
```
**Request Body:**
```json
{
    "name": "Product name (required, 1-120 chars)",
    "price": 99.99,
    "description": "Product description (required)",
    "lifetime_guarantee": true,
    "variants": [
        {
            "color": "Red",
            "size": "M",
            "in_stock": true
        }
    ],
    "images": [
        {
            "color": "Red",
            "image_url": "https://example.com/image.jpg"
        }
    ]
}
```

#### Update Product
```http
PUT /api/v1/product/{product_id}
```
**Request Body:** (all fields optional)
```json
{
    "name": "Updated product name",
    "price": 149.99,
    "description": "Updated description",
    "lifetime_guarantee": false
}
```

#### Delete Product
```http
DELETE /api/v1/product/{product_id}
```

### Product Image Endpoints

#### Add Image to Product
```http
POST /api/v1/product/{product_id}/images
```
**Request Body:**
```json
{
    "image_url": "https://example.com/image1.jpg"
}
```

#### Delete Product Image
```http
DELETE /api/v1/product/{product_id}/images/{image_id}
```

### Product Variant Endpoints

#### Add Variant to Product
```http
POST /api/v1/product/{product_id}/variants
```
**Request Body:**
```json
{
    "color": "Blue",
    "size": "L",
    "in_stock": true
}
```
**Size Values:** `XS`, `S`, `M`, `L`, `XL`, `XXL`

#### Update Variant
```http
PUT /api/v1/product/variant/{variant_id}
```
**Request Body:**
```json
{
    "color": "Green",
    "size": "XL",
    "in_stock": false
}
```

#### Delete Variant
```http
DELETE /api/v1/product/variant/{variant_id}
```

### Product Recommendation Endpoints

#### Add Recommendation
```http
POST /api/v1/product/{product_id}/recommendations/{rec_id}
```
Adds a product recommendation. `rec_id` is the ID of the recommended product.

#### Get Recommendations
```http
GET /api/v1/product/{product_id}/recommendations
```
Returns list of recommended products for the given product.

#### Delete Recommendation
```http
DELETE /api/v1/product/recommendations/{rec_id}
```
Deletes a recommendation by recommendation ID.

### Cart Endpoints

#### Create Cart
```http
POST /api/v1/cart/
```
**Request Body:**
```json
{
    "session_id": "unique-session-id"
}
```

#### Get Cart
```http
GET /api/v1/cart/{session_id}
```
Returns cart with all items for the given session ID.

#### Clear Cart
```http
DELETE /api/v1/cart/{session_id}
```
Removes all items from the cart.

### Cart Item Endpoints

#### Add Item to Cart
```http
POST /api/v1/cart/{session_id}/items
```
**Request Body:**
```json
{
    "variant_id": 1,
    "quantity": 2
}
```
If cart doesn't exist, it will be created automatically.

#### Update Item Quantity
```http
PUT /api/v1/cart/{session_id}/items/{item_id}
```
**Request Body:**
```json
{
    "quantity": 5
}
```

#### Delete Item from Cart
```http
DELETE /api/v1/cart/{session_id}/items/{item_id}
```
Removes a specific item from the cart.

## 🏗️ Project Structure

```
ShortShop/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration and middleware
│   │   ├── db/             # Database configuration
│   │   ├── log/            # Logging setup
│   │   ├── models/         # SQLAlchemy models (Product, Cart, etc.)
│   │   ├── routers/        # API endpoints (server, product, cart)
│   │   ├── schemas/        # Pydantic schemas (validation)
│   │   ├── services/       # Business logic (product_service, cart_service)
│   │   └── main.py         # Project start point
│   ├── logs/               # Logs folder
│   ├── tests/              # Unit tests
│   ├── .pylintrc           # Pylint configuration
│   ├── Dockerfile          # Dockerfile
│   ├── pytest.ini          # Pytest configuration
│   └── requirements.txt    # Python dependencies
├── .dockerignore           # Environment .dockerignore file
├── .env                    # Environment variables
├── .env-sample             # Environment variables sample
├── .gitignore              # Environment .gitignore file
├── docker-compose.yml      # Container orchestration
└── README.md               # Project informational file
```