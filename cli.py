import requests

from services.openfoodfacts import search_products_by_name

base = "http://127.0.0.1:5000"


<<<<<<< HEAD
class ApiResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
=======
class SafeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
>>>>>>> 08f3df8 (last commit)

    def json(self):
        return self._payload


def make_request(method, path, **kwargs):
    try:
        return requests.request(method, f"{base}{path}", **kwargs)
    except requests.RequestException as exc:
<<<<<<< HEAD
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
=======
        return SafeResponse({"error": f"API unavailable: {exc}"}, 503)


def parse_response(response):
    try:
        return response.json()
    except (ValueError, requests.exceptions.JSONDecodeError, AttributeError):
        status_code = getattr(response, "status_code", None)
        text = getattr(response, "text", "")
        if status_code and text:
            return {"error": f"HTTP {status_code}: {text}"}
        return {"error": "The API returned an invalid response."}


def save_product_to_inventory(product):
    if not product:
        return None

    if isinstance(product, dict) and product.get("id"):
        return make_request("POST", "/inventory", json=product)

    if isinstance(product, list):
        created_items = []
        for item in product:
            if isinstance(item, dict) and item.get("id"):
                created_items.append(save_product_to_inventory(item))
        return created_items
>>>>>>> 08f3df8 (last commit)

    return None


<<<<<<< HEAD
def _prompt_to_add_item(response):
    item = _extract_item_payload(response)
    if not item:
        return None

    choice = input("Add this item to inventory? (y/n): ").strip().lower()
    if choice != "y":
        return None

    return make_request("POST", "/inventory", json=item)


=======
>>>>>>> 08f3df8 (last commit)
def main():
    while True:
        print("1. Get Inventory")
        print("2. Add Item")
        print("3. Update Item")
        print("4. Delete Item")
<<<<<<< HEAD
        print("5. SEARCH ITEM BY BARCODE")
        print("6. SEARCH ITEM BY NAME")
=======
        print("5. Search by Barcode")
        print("6. Search by Name")
>>>>>>> 08f3df8 (last commit)
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            response = make_request("GET", "/inventory")
<<<<<<< HEAD
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
=======
            print(parse_response(response))

        elif choice == "2":
            item_id = input("Enter item ID: ").strip()
            name = input("Enter item name: ").strip()
            quantity = input("Enter item quantity: ").strip()

            if not item_id or not name or not quantity:
                print("Invalid input. Please provide an ID, name, and quantity.")
                continue

            response = make_request(
                "POST",
                "/inventory",
                json={"id": item_id, "name": name, "quantity": quantity},
            )
            print(parse_response(response))

        elif choice == "3":
            item_id = input("Enter item ID to update: ").strip()
            if not item_id:
                print("Invalid input. Please provide an item ID.")
                continue

            new_quantity = input("Enter new item quantity: ").strip()
            if not new_quantity:
                print("Invalid input. Please provide a quantity.")
                continue

            response = make_request("PATCH", f"/inventory/{item_id}", json={"quantity": new_quantity})
            print(parse_response(response))

        elif choice == "4":
            item_id = input("Enter item ID to delete: ").strip()
            if not item_id:
                print("Invalid input. Please provide an item ID.")
                continue

            response = make_request("DELETE", f"/inventory/{item_id}")
            print(parse_response(response))

        elif choice == "5":
            barcode = input("Enter item barcode to search: ").strip()
            if not barcode:
                print("Invalid input. Please provide a barcode.")
                continue

            response = make_request("GET", f"/inventory/product/barcode/{barcode}")
            payload = parse_response(response)
            print(payload)
            if getattr(response, "status_code", 200) < 400:
                save_product_to_inventory(payload)

        elif choice == "6":
            name = input("Enter item name to search: ").strip()
            if not name:
                print("Invalid input. Please provide a product name.")
                continue

            response = make_request("GET", "/inventory/product/search", params={"name": name})
            payload = parse_response(response)

            if isinstance(payload, dict) and payload.get("error") == "Product not found":
                fallback_results = search_products_by_name(name)
                if fallback_results:
                    payload = fallback_results
                    print(payload)
                    save_product_to_inventory(payload)
                    continue

            print(payload)
            if getattr(response, "status_code", 200) < 400:
                save_product_to_inventory(payload)
>>>>>>> 08f3df8 (last commit)

        elif choice == "7":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
