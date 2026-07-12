import json
from pathlib import Path
from typing import Optional

from services.openfoodfacts import fetch_product


FILE_NAME = Path(__file__).resolve().parents[1] / "data" / "inventory.json"


def load_inventory():
    path = Path(FILE_NAME)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except ValueError:
            return []


def save_inventory(inventory):
    path = Path(FILE_NAME)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)
    temporary_path.replace(path)


def get_inventory():
    return load_inventory()


def get_item_by_id(item_id: str) -> Optional[dict]:
    inventory = load_inventory()
    for item in inventory:
        if str(item.get("id")) == str(item_id):
            return item
    return None


def add_item(item: dict) -> Optional[dict]:
    # validate required fields
    if not item or not item.get("id") or not item.get("name") or not item.get("quantity"):
        return None

    # ensure id stored as string
    item = {**item, "id": str(item.get("id"))}

    inventory = load_inventory()

    # reject duplicate ids
    for existing in inventory:
        if str(existing.get("id")) == str(item.get("id")):
            return None

    inventory.append(item)
    save_inventory(inventory)
    return item


def update_item(item_id: str, new_data: dict) -> Optional[dict]:
    inventory = load_inventory()
    for item in inventory:
        if str(item.get("id")) == str(item_id):
            item.update(new_data)
            # ensure id remains a string
            item["id"] = str(item.get("id"))
            save_inventory(inventory)
            return item
    return None


def delete_item(item_id: str) -> bool:
    inventory = load_inventory()
    for index, item in enumerate(inventory):
        if str(item.get("id")) == str(item_id):
            del inventory[index]
            save_inventory(inventory)
            return True
    return False


def import_item(barcode: str) -> Optional[dict]:
    product = fetch_product(barcode)
    if not product or not product.get("id"):
        return None
    return add_item(product)
