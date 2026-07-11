import pytest

from app import app
from models import inventory


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Provide a fresh inventory store for every test."""
    inventory_file = tmp_path / "inventory.json"
    inventory_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(inventory, "FILE_NAME", inventory_file)

    app.testing = True
    with app.test_client() as test_client:
        yield test_client


def create_item(client, item_id="1"):
    return client.post(
        "/inventory", json={"id": item_id, "name": "Item 1", "quantity": 10}
    )


def test_post(client):
    response = create_item(client)
    assert response.status_code == 201
    assert response.get_json()["id"] == "1"


def test_get_inventory_is_empty_for_a_new_test(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_patch(client):
    create_item(client)
    response = client.patch("/inventory/1", json={"quantity": 20})
    assert response.status_code == 200
    assert response.get_json()["quantity"] == 20


def test_delete(client):
    create_item(client)
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert client.get("/inventory/1").status_code == 404


def test_duplicate_id_is_rejected(client):
    create_item(client)
    response = create_item(client)
    assert response.status_code == 409


def test_invalid_request_bodies_are_rejected(client):
    assert client.post("/inventory", json={"id": "1"}).status_code == 400
    assert client.patch("/inventory/1", json={"id": "2"}).status_code == 400


def test_external_api_is_mocked(client, monkeypatch):
    product = {"id": "3017620422003", "name": "Chocolate spread", "quantity": "400 g"}
    monkeypatch.setattr("routes.inventory_routes.fetch_product", lambda barcode: product)

    response = client.get("/inventory/product/barcode/3017620422003")
    assert response.status_code == 200
    assert response.get_json() == product


def test_search_products_by_name(client, monkeypatch):
    products = [{"id": "1", "name": "Chocolate spread", "quantity": "400 g"}]
    monkeypatch.setattr(
        "routes.inventory_routes.search_products_by_name", lambda name: products
    )

    response = client.get("/inventory/product/search?name=chocolate")
    assert response.status_code == 200
    assert response.get_json() == products


def test_search_products_requires_name(client):
    assert client.get("/inventory/product/search").status_code == 400


def test_search_products_reports_an_unavailable_service(client, monkeypatch):
    monkeypatch.setattr("routes.inventory_routes.search_products_by_name", lambda name: None)

    response = client.get("/inventory/product/search?name=mango")
    assert response.status_code == 503
