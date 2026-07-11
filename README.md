# Inventory Management System

A Flask REST API and command-line client for creating, viewing, updating, deleting, and importing inventory items.

## Features

- CRUD endpoints for inventory items
- OpenFoodFacts barcode lookup and import
- Command-line client
- Isolated pytest test suite

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`. In another terminal, run `python cli.py` to use the command-line client.

The CLI can fetch a product by barcode without saving it, search products by name, or import a barcode result into inventory.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/inventory` | Retrieve all inventory items |
| GET | `/inventory/<id>` | Retrieve one inventory item |
| POST | `/inventory` | Create an item; JSON requires `id`, `name`, and `quantity` |
| PATCH | `/inventory/<id>` | Update an item's `name` and/or `quantity` |
| DELETE | `/inventory/<id>` | Delete an item |
| POST | `/inventory/import/<barcode>` | Import a barcode product into inventory |
| GET | `/inventory/product/barcode/<barcode>` | Look up an OpenFoodFacts product without saving it |
| GET | `/inventory/product/search?name=<name>` | Search OpenFoodFacts products by name |

Example create request body:

```json
{
  "id": "1",
  "name": "Item 1",
  "quantity": 10
}
```

## Tests

```bash
python -m pytest
```

Tests use temporary inventory files and mock the external product service, so they do not alter `data/inventory.json` or require network access.

Product searches depend on OpenFoodFacts availability. The API returns `503` with a clear error message when that service is temporarily unavailable.

## Project structure

```text
inventory_management_system/
├── app.py
├── cli.py
├── data/inventory.json
├── models/inventory.py
├── routes/inventory_routes.py
├── services/openfoodfacts.py
└── tests/
    ├── test_api.py
    └── test_cli.py
```
