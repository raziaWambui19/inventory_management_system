import requests

base = "http://127.0.0.1:5000"


def make_request(method, path, **kwargs):
    return requests.request(method, f"{base}{path}", **kwargs)


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

            make_request(
                "POST",
                "/inventory",
                json={"id": item_id, "name": name, "quantity": quantity},
            )

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
            make_request("GET", f"/inventory/product/barcode/{barcode}")

        elif choice == "6":
            name = input("Enter item name to search: ")
            response = make_request("GET", "/inventory/product/search", params={"name": name})
            print(response.json())

        elif choice == "7":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
