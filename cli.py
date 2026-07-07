import requests

base = "http://127.0.0.1:5000"

def main():
    while True:
        print("1. Get Inventory")
        print("2. Get Item by ID")
        print("3. Add Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            response = requests.get(f"{base}/inventory")
            print(response.json())

        elif choice == '2':
            item_id = input("Enter item ID: ")
            name = input("Enter item name: ")
            quantity = input("Enter item quantity: ")

            requests.request.post(
                base+"/inventory",
                json={
                    "id": item_id,
                    "name": name,
                    "quantity": quantity
                }
            )
            

        elif choice == '3':
            item_id = input("Enter item ID: ")
            quantity = input("Enter item quantity: ")
            requests.post(
                "http://127.0.0.1:5000/inventory",
                json={
                    "id": item_id,
                    "quantity": quantity
                }
            )
        elif choice == '4':
            item_id = input("Enter item ID to update: ")

            requests.put(
                "http://127.0.0.1:5000/inventory/"+item_id,
                json={
                    "id": item_id
                }
            )
          
            

        elif choice == '5':
            barcode = input("Enter product barcode: ")
            print(requests.get(f"{base}/product/{barcode}").json())

        elif choice == '6':
            break

if __name__ == "__main__":
    main()