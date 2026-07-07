import requests
BASE_URL = "https://world.openfoodfacts.org/api/v0/product/"
def fetch_product(item_id):
    response = requests.get(f"{BASE_URL}{item_id}.json")
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 1:
            product = data.get('product', {})
            return {
                'id': product.get('code'),
                'name': product.get('product_name'),
                'quantity': product.get('quantity'),
                'price': product.get('price'),
                
            }
        return None