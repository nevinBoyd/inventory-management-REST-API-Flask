import requests

def fetch_product_by_name(name):
    """
    Query OpenFoodFacts API for a product by name.
    Returns a simplified dict with name, brand, and ingredients,
    or None if no results or request error.
    """
    try:
        # Make request to OpenFoodFacts product search
        response = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
            }
        )
        data = response.json()

        # Validate results exist
        if data.get("count", 0) > 0:
            product = data["products"][0]

            # Extract and normalize fields for local use
            return {
                "name": product.get("product_name", "Unknown"),
                "brand": product.get("brands", "Unknown"),
                "ingredients": product.get("ingredients_text", "Unknown"),
            }

        return None

    except Exception:
        # Gracefully fail if API request fails
        return None
