from flask import Flask, jsonify

app = Flask(__name__)

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

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
