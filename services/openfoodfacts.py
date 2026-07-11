import requests


BASE_URL = "https://world.openfoodfacts.net/api/v0/product/"
SEARCH_URL = "https://world.openfoodfacts.net/cgi/search.pl"
REQUEST_TIMEOUT_SECONDS = 10
PRODUCT_FIELDS = "code,product_name,quantity"
HEADERS = {
    "User-Agent": "inventory-management-system/1.0 (local development)",
}


def fetch_product(barcode):
    """Fetch a product from OpenFoodFacts, returning None when unavailable."""
    try:
        response = requests.get(
            f"{BASE_URL}{barcode}.json",
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    if data.get("status") != 1:
        return None

    return _format_product(data.get("product", {}))


def search_products_by_name(name, page_size=10):
    """Return up to ``page_size`` products that match a product name."""
    try:
        response = requests.get(
            SEARCH_URL,
            params={
                "action": "process",
                "search_simple": 1,
                "search_terms": name,
                "json": 1,
                "page_size": page_size,
                "fields": PRODUCT_FIELDS,
            },
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        products = response.json().get("products", [])
    except (requests.RequestException, ValueError, AttributeError):
        return None

    return [product for raw_product in products if (product := _format_product(raw_product))]


def _format_product(product):
    code = product.get("code")
    if not code:
        return None
    return {
        "id": str(code),
        "name": product.get("product_name") or "Unknown product",
        "quantity": product.get("quantity") or "Unknown",
    }
