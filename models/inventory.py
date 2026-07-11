import json
from pathlib import Path

from services.openfoodfacts import fetch_product


FILE_NAME = Path(__file__).resolve().parents[1] / "data" / "inventory.json"


def load_inventory():
    """Return the inventory, creating an empty data file when needed."""
    path = Path(FILE_NAME)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")

    with path.open("r", encoding="utf-8") as file:
        inventory = json.load(file)

    if not isinstance(inventory, list):
        raise ValueError("Inventory data must be a list")
    return inventory


def save_inventory(inventory):
    path = Path(FILE_NAME)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)
    temporary_path.replace(path)


def get_inventory():
    return load_inventory()


def get_item_by_id(item_id):
    for item in load_inventory():
        if str(item.get("id")) == str(item_id):
            return item
    return None


def add_item(item):
    inventory = load_inventory()
    item = {**item, "id": str(item["id"])}
    if any(str(existing.get("id")) == item["id"] for existing in inventory):
        return None

    inventory.append(item)
    save_inventory(inventory)
    return item


def update_item(item_id, new_data):
    inventory = load_inventory()
    for item in inventory:
        if str(item.get("id")) == str(item_id):
            item.update(new_data)
            save_inventory(inventory)
            return item
    return None


def delete_item(item_id):
    inventory = load_inventory()
    for index, item in enumerate(inventory):
        if str(item.get("id")) == str(item_id):
            del inventory[index]
            save_inventory(inventory)
            return True
    return False


def import_item(barcode):
    product = fetch_product(barcode)
    if not product or not product.get("id"):
        return None
    return add_item(product)
