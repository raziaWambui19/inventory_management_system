import json
import os
FILE_NAME = "data/inventory.json"

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
    with open(FILE_NAME, 'w') as f:
        json.dump(inventory, f, indent=4)


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
        if item['id'] == item_id:
            item.update(new_data)
            save_inventory(inventory)
            return item
    return None

def delete_item(item_id):
    inventory = load_inventory()
    for item in inventory:
        if item['id'] == item_id:
            inventory.remove(item)
            save_inventory(inventory)
            return True
    return False