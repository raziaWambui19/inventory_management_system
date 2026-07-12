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


@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory_get_inventory()), 200


@inventory_bp.route("/inventory/<item_id>", methods=["GET"])
def get_item(item_id):
    item = inventory_get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@inventory_bp.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
    # validate required fields
    if not data or not data.get("id") or not data.get("name") or not data.get("quantity"):
        return jsonify({"error": "Invalid request body"}), 400

    item = inventory_add_item(data)
    if item is None:
        return jsonify({"error": "An item with this id already exists"}), 409
    return jsonify(item), 201


@inventory_bp.route("/inventory/<item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    # Do not allow changing IDs via patch
    if "id" in data and str(data.get("id")) != str(item_id):
        return jsonify({"error": "Cannot change item id"}), 400

    item = inventory_update_item(item_id, data)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@inventory_bp.route("/inventory/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    if not inventory_delete_item(item_id):
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted"}), 200


@inventory_bp.route("/inventory/product/barcode/<barcode>", methods=["GET"])
def get_product_by_barcode(barcode):
    item = fetch_product(barcode)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Product not found"}), 404


@inventory_bp.route("/inventory/product/search", methods=["GET"])
def search_products():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name query parameter required"}), 400

    results = search_products_by_name(name)
    if results is None:
        return jsonify({"error": "External service unavailable"}), 503
    return jsonify(results), 200