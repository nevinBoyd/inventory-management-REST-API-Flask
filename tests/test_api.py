import pytest
from unittest.mock import patch
from inventory_api.app import app, inventory

@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset inventory before each test to ensure isolation."""
    inventory.clear()
    inventory.append({
        "id": 1,
        "name": "Example Product",
        "brand": "Sample Brand",
        "quantity": 5,
        "price": 3.99,
        "barcode": "0000",
        "ingredients": "Sample ingredients"
    })

# Test GET /inventory returns list of items
def test_get_inventory():
    with app.test_client() as client:
        # Send Get request for all inventory items
        response = client.get("/inventory")

        # Response is ok and return data as list
        assert response.status_code == 200
        assert type(response.get_json()) is list

# Test Get /inventory/<id> retuns 404 if item not found
def test_get_item_not_found():
    with app.test_client() as client:
        # Request a non-existent item
        response = client.get("/inventory/999")

        # 404 response and error message
        assert response.status_code == 404
        assert response.get_json()["error"] == "Item not found"

# Test POST /inventory to add a new item
def test_add_item():
    with app.test_client() as client:
        # Arrange test data for new product
        new_item = {
            "name": "Test Product",
            "quantity": 5,
            "price": 9.99
        }

        # Send POST request to create item
        response = client.post("/inventory", json=new_item)
        
        # Item created successfully with correct data
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Test Product"
        assert data["quantity"] == 5
        assert data["price"] == 9.99
        assert "id" in data  # ID auto-generate

# Test PATCH /inventory/<id> updates an existing item
def test_update_item():
    with app.test_client() as client:
        # Create an item to update
        new_item = {
            "name": "PatchTest",
            "quantity": 1,
            "price": 1.00
        }
        create_response = client.post("/inventory", json=new_item)
        created_item = create_response.get_json()
        item_id = created_item["id"]

        # Update quantity only
        update_data = {"quantity": 10}
        response = client.patch(f"/inventory/{item_id}", json=update_data)

        # Quantity updated and response is OK
        assert response.status_code == 200
        updated_item = response.get_json()
        assert updated_item["quantity"] == 10
        assert updated_item["name"] == "PatchTest"  # Unchanged

# Test DELETE /inventory/<id> removes an existing item
def test_delete_item():
    with app.test_client() as client:
        # Create an item to delete
        item_to_delete = {
            "name": "DeleteTest",
            "quantity": 2,
            "price": 5.00
        }
        create_response = client.post("/inventory", json=item_to_delete)
        created_item = create_response.get_json()
        item_id = created_item["id"]

        # Delete the item
        delete_response = client.delete(f"/inventory/{item_id}")

        # Successful delete response
        assert delete_response.status_code == 200
        assert delete_response.get_json()["message"] == "Item deleted"

        # Confirm item is truly gone
        confirm_response = client.get(f"/inventory/{item_id}")
        assert confirm_response.status_code == 404

# Test external API fetch adds a product to local inventory
@patch("inventory_api.app.fetch_product_by_name")
def test_fetch_external_product(mock_fetch):
    with app.test_client() as client:
        # Mock simple product data from fetch
        mock_fetch.return_value = {
                "name": "Mocked Almond Milk",
                "brand": "MockBrand",
                "ingredients": "Mocked ingredients"
            }
        
        # Call Flask route
        response = client.get("/inventory/fetch/almond%20milk")

        assert response.status_code == 201

        data = response.get_json()

        # Expected fields added into inventory
        assert data["name"] == "Mocked Almond Milk"
        assert data["brand"] == "MockBrand"
        assert data["ingredients"] == "Mocked ingredients"
        assert "id" in data
        assert data["price"] == 0.0
        assert data["quantity"] == 0
        
