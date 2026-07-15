import requests

base = "http://127.0.0.1:5000"


class ApiResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def make_request(method, path, **kwargs):
    try:
        return requests.request(method, f"{base}{path}", **kwargs)
    except requests.RequestException as exc:
        return ApiResponse(503, {"error": f"The API server is unavailable: {exc}"})


def _extract_item_payload(response):
    if response is None:
        return None

    try:
        payload = response.json()
    except Exception:
        return None

    if isinstance(payload, dict) and payload.get("id"):
        return payload

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict) and item.get("id"):
                return item

    return None


def _prompt_to_add_item(response):
    item = _extract_item_payload(response)
    if not item:
        return None

    choice = input("Add this item to inventory? (y/n): ").strip().lower()
    if choice != "y":
        return None

    return make_request("POST", "/inventory", json=item)


def main():
    while True:
        print("1. Get Inventory")
        print("2. Add Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. SEARCH ITEM BY BARCODE")
        print("6. SEARCH ITEM BY NAME")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            response = make_request("GET", "/inventory")
            print(response.json())

        elif choice == "2":
            item_id = input("Enter item ID: ")
            name = input("Enter item name: ")
            quantity = input("Enter item quantity: ")
            make_request("POST", "/inventory", json={"id": item_id, "name": name, "quantity": quantity})

        elif choice == "3":
            item_id = input("Enter item ID to update: ")
            new_quantity = input("Enter new item quantity: ")
            make_request("PATCH", f"/inventory/{item_id}", json={"quantity": new_quantity})
            print(f"Item {item_id} updated with new quantity: {new_quantity}")

        elif choice == "4":
            item_id = input("Enter item ID to delete: ")
            print(make_request("DELETE", f"/inventory/{item_id}").json())

        elif choice == "5":
            barcode = input("Enter item barcode to search: ")
            response = make_request("GET", f"/inventory/product/barcode/{barcode}")
            try:
                print(response.json())
            except ValueError:
                pass
            if response.status_code >= 400:
                print("Unable to fetch the product from the API server.")
            else:
                _prompt_to_add_item(response)

        elif choice == "6":
            name = input("Enter item name to search: ")
            response = make_request("GET", "/inventory/product/search", params={"name": name})
            try:
                print(response.json())
            except ValueError:
                pass
            if response.status_code >= 400:
                print("Unable to fetch search results from the API server.")
            else:
                _prompt_to_add_item(response)

        elif choice == "7":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
