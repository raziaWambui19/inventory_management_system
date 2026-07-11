from flask import Blueprint, jsonify, request

from models.inventory import (
    add_item as inventory_add_item,
    delete_item as inventory_delete_item,
    get_inventory as inventory_get_inventory,
    get_item_by_id as inventory_get_item_by_id,
    import_item as inventory_import_item,
    update_item as inventory_update_item,
)
from services.openfoodfacts import fetch_product, search_products_by_name


inventory_bp = Blueprint("inventory", __name__)


def _json_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None
    return data


@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory_get_inventory()), 200


@inventory_bp.route("/inventory/<item_id>", methods=["GET"])
def get_item(item_id):
    item = inventory_get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/inventory/import/<barcode>", methods=["POST"])
def import_product(barcode):
    product = inventory_import_item(barcode)
    if product is None:
        return jsonify({"error": "Product was not found or is already in inventory"}), 404
    return jsonify(product), 201


@inventory_bp.route("/inventory", methods=["POST"])
def add_item():
    data = _json_object()
    if data is None or not {"id", "name", "quantity"}.issubset(data):
        return jsonify({"error": "JSON body must include id, name, and quantity"}), 400
    if not str(data["id"]).strip() or not str(data["name"]).strip():
        return jsonify({"error": "id and name must not be empty"}), 400

    item = inventory_add_item(data)
    if item is None:
        return jsonify({"error": "An item with this id already exists"}), 409
    return jsonify(item), 201


@inventory_bp.route("/inventory/<item_id>", methods=["PATCH"])
def update_item(item_id):
    data = _json_object()
    if data is None:
        return jsonify({"error": "Request body must be a JSON object"}), 400

    allowed_fields = {"name", "quantity"}
    update_data = {key: value for key, value in data.items() if key in allowed_fields}
    if not update_data or set(data) - allowed_fields:
        return jsonify({"error": "Only name and quantity may be updated"}), 400
    if "name" in update_data and not str(update_data["name"]).strip():
        return jsonify({"error": "name must not be empty"}), 400

    item = inventory_update_item(item_id, update_data)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/inventory/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    if not inventory_delete_item(item_id):
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted"}), 200


@inventory_bp.route("/inventory/product/barcode/<barcode>", methods=["GET"])
def get_product(barcode):
    item = fetch_product(barcode)
    if item is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/inventory/product/search", methods=["GET"])
def search_products():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify({"error": "Query parameter 'name' is required"}), 400

    products = search_products_by_name(name)
    if products is None:
        return jsonify({"error": "Product search service is temporarily unavailable"}), 503
    return jsonify(products), 200
