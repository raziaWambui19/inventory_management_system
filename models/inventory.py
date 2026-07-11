import json
from pathlib import Path

from services.openfoodfacts import fetch_product


FILE_NAME = Path(__file__).resolve().parents[1] / "data" / "inventory.json"


def load_inventory():
    with open(FILE_NAME, 'r') as f:
        return json.load(f)

def save_inventory(inventory):
    if not os.path.exists("FILE_NAME"):
        os.makedirs("data", exist_ok=True)
        with open(FILE_NAME, 'w') as f:
            json.dump([], f)
    
    with open(FILE_NAME, 'w') as f:
        json.dump(inventory, f, indent=4)

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
    inventory = load_inventory()    
    for item in inventory:
        if item['id'] == item_id:
            return item
    return None


def add_item(item):
    item["id"] = int(item["id"])  # Ensure the ID is an integer
    inventory = load_inventory()    
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
