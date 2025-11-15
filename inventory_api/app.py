from inventory_api.external_api import fetch_product_by_name
from flask import Flask, jsonify

app = Flask(__name__)

# Mock database (in-memory list)
inventory = [
    {
        "id": 1,
        "name": "Example Product",
        "brand": "Sample Brand",
        "quantity": 5,
        "price": 3.99,
        "barcode": "0000",
        "ingredients": "Sample ingredients"
    }
]

# GET all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

# GET single item by ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# POST new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["name", "quantity", "price"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create new item
    new_id = max([i["id"] for i in inventory]) + 1 if inventory else 1
    new_item = {
        "id": new_id,
        "name": data.get("name"),
        "brand": data.get("brand", "Unknown"),
        "quantity": data.get("quantity"),
        "price": data.get("price"),
        "barcode": data.get("barcode"),
        "ingredients": data.get("ingredients", "Unknown"),
    }

    inventory.append(new_item)
    return jsonify(new_item), 201

# PATCH update item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    # Update only the fields provided
    for key in ["name", "brand", "quantity", "price", "barcode", "ingredients"]:
        if key in data:
            item[key] = data[key]

    return jsonify(item), 200

# DELETE remove an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

# FETCH product from external API and add to inventory
@app.route("/inventory/fetch/<string:name>", methods=["GET"])
def fetch_and_add_product(name):
    """
    Fetch a product by name from the external OpenFoodFacts API
    and add it to the local inventory database.
    """
    product_data = fetch_product_by_name(name)

    if not product_data:
        return jsonify({"error": "Product not found from external API"}), 404

    new_id = max([i["id"] for i in inventory]) + 1 if inventory else 1

    product_data.update({
        "id": new_id,
        "price": 0.0,
        "quantity": 0,
        "barcode": None,
    })

    inventory.append(product_data)
    return jsonify(product_data), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
