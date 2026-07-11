import requests

BASE_URL = "http://127.0.0.1:5000"
REQUEST_TIMEOUT_SECONDS = 10


def print_response(response):
    print("Status Code:", response.status_code)
    try:
        print(response.json())
    except ValueError:
        print(response.text)


def make_request(method, path, **kwargs):
    try:
        response = requests.request(
            method, f"{BASE_URL}{path}", timeout=REQUEST_TIMEOUT_SECONDS, **kwargs
        )
    except requests.RequestException as error:
        print(f"Request failed: {error}")
        return
    print_response(response)

def main():
    while True:
        print("\n1. Get Inventory")
        print("2. Fetch Product by Barcode")
        print("3. Import Item by Barcode")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Search Products by Name")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            make_request("GET", "/inventory")

        elif choice == '2':
            barcode = input("Enter product barcode: ").strip()
            if barcode:
                make_request("GET", f"/inventory/product/barcode/{barcode}")
            else:
                print("Barcode cannot be empty.")

        elif choice == '3':
            barcode = input("Enter product barcode: ")

            make_request("POST", f"/inventory/import/{barcode}")

        elif choice == '4':
            item_id = input("Enter item ID to update: ")
            new_quantity = input("Enter new item quantity: ")

            make_request(
                "PATCH", f"/inventory/{item_id}", json={"quantity": new_quantity}
            )

        elif choice == '5':
            item_id = input("Enter item ID to delete: ")

            make_request("DELETE", f"/inventory/{item_id}")

        elif choice == '6':
            name = input("Enter product name: ").strip()
            if name:
                make_request("GET", "/inventory/product/search", params={"name": name})
            else:
                print("Product name cannot be empty.")

        elif choice == '7':
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
