inventory = []
def get_inventory():
    return inventory

def get_item_by_id(item_id):
    for item in inventory:
        if item['id'] == item_id:
            return item
    return None

def add_item(item):
    item["id"] = int(item["id"])  # Ensure the ID is an integer
    inventory.append(item)
    return item

def update_item(item_id, new_data):
    item = get_item_by_id(item_id)
    if item:
        item.update(new_data)
        return item
    return None

def delete_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        inventory.remove(item)
        return True
    return False