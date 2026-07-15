# Inventory Management System

A Flask-based inventory management system with CRUD APIs, OpenFoodFacts integration, a CLI client, and pytest tests.

## Features
- Manage inventory items through REST endpoints
- Search products by barcode or name using the OpenFoodFacts API
- Import product data into the inventory store
- Use a simple command-line client to interact with the API

<<<<<<< HEAD
## Running the API
=======
- CRUD endpoints for inventory items
- OpenFoodFacts barcode lookup and import
- Command-line client
- Isolated pytest test suite

## Design overview

The application uses a Flask REST API and a CLI client. Each route is designed around a clear input, an action on the inventory data, and an output response.

### Route design

- GET /inventory
  - Input: none
  - Output: a JSON list of all inventory items
  - Trigger: selected from the CLI menu as "Get Inventory"

- GET /inventory/<id>
  - Input: item id from the URL
  - Output: a single item JSON object or an error message
  - Trigger: used when the CLI or client wants to inspect one item

- POST /inventory
  - Input: JSON body containing id, name, quantity
  - Output: newly created item JSON or an error if the item already exists
  - Trigger: selected from the CLI menu as "Add Item"

- PATCH /inventory/<id>
  - Input: item id from the URL and a JSON body with updated fields
  - Output: updated item JSON or an error if the item is missing
  - Trigger: selected from the CLI menu as "Update Item"

- DELETE /inventory/<id>
  - Input: item id from the URL
  - Output: a success message or an error if the item is missing
  - Trigger: selected from the CLI menu as "Delete Item"

- GET /inventory/product/barcode/<barcode>
  - Input: barcode from the URL
  - Output: product details fetched from OpenFoodFacts
  - Trigger: selected from the CLI menu as "Search by Barcode"

- GET /inventory/product/search?name=<name>
  - Input: a product name query parameter
  - Output: one or more product matches from OpenFoodFacts
  - Trigger: selected from the CLI menu as "Search by Name"

- POST /inventory/import/<barcode>
  - Input: barcode from the URL
  - Output: imported product saved into inventory
  - Trigger: used when the application wants to persist a discovered product

### Data design

Inventory items are stored as JSON objects with a string ID and product details. Each item contains at least:

```json
{
  "id": "3017620422003",
  "name": "Chocolate spread",
  "quantity": "400 g",
  "brand": "Nutella",
  "category": "Snacks",
  "ingredients": "Sugar, palm oil, hazelnuts..."
}
```

This structure mirrors the OpenFoodFacts-style data while ensuring every item in the inventory array includes an ID.

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

>>>>>>> 08f3df8 (last commit)
```bash
python app.py
```

## Running the CLI
```bash
python cli.py
```

## Running tests
```bash
pytest -q
```
