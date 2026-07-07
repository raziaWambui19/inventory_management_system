# Inventory Management System

## Project Overview

The Inventory Management System is a Flask-based REST API that allows users to manage inventory items through Create, Read, Update, and Delete (CRUD) operations. The project also integrates with the OpenFoodFacts API to retrieve real-time product information using a barcode. A Command Line Interface (CLI) is included to interact with the API.

---

## Features

- Flask REST API
- CRUD Operations
  - Create inventory items
  - View all inventory items
  - View a single inventory item
  - Update inventory items
  - Delete inventory items
- External API Integration using OpenFoodFacts
- Command Line Interface (CLI)
- Unit Testing with Pytest

---

## Technologies Used

- Python 
- Flask
- Requests
- Pytest
- Git & GitHub

---

## Project Structure

```
inventory_management_system/
│
├── app.py
├── cli.py
├── README.md
├── requirements.txt
│
├── data/
├── models/
│   └── inventory.py
│
├── routes/
│   └── inventory_routes.py
│
├── services/
│   └── openfoodfacts.py
│
└── tests/
    └── test_api.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/raziaWambui19/inventory_management_system.git
```

### 2. Navigate to the project folder

```bash
cd inventory_management_system
```

### 3. Create a virtual environment

Windows

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

### 5. Install the required packages

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server by running:

```bash
python app.py
```

The application will start on:

```
http://127.0.0.1:5000
```

---

## Running the CLI

Open a new terminal while the Flask server is running.

Activate the virtual environment if needed:

```bash
venv\Scripts\activate
```

Run:

```bash
python cli.py
```

Follow the on-screen menu to manage inventory items.

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /inventory | Retrieve all inventory items |
| GET | /inventory/<id> | Retrieve a single inventory item |
| POST | /inventory | Create a new inventory item |
| PATCH | /inventory/<id> | Update an inventory item |
| DELETE | /inventory/<id> | Delete an inventory item |
| GET | /product/<barcode> | Fetch product details from OpenFoodFacts |

---

## Running the Tests

To run all tests:

```bash
python -m pytest
```

To run only the API tests:

```bash
python -m pytest tests/test_api.py -v
```

If all tests pass, you should see output similar to:

```
==============================
5 passed in X.XXs
==============================
```

---

## External API

This project uses the OpenFoodFacts API to retrieve product information using a barcode.

Example endpoint:

```
GET /product/737628064502
```

---

## Author

Developed as part of the **Python REST API with Flask – Inventory Management System** Summative Lab.
