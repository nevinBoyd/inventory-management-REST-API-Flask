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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
