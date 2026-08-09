import unittest

from application import create_app
from application.extensions import db
from config import TestingConfig


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    
    
    
    # First, Positive Test: POST create an inventory part
    def test_create_inventory(self):
        inventory_payload = {
            "name": "Brake Pad",
            "price": 75.50
        }

        response = self.client.post(
            "/inventory/",
            json=inventory_payload
        )

        self.assertEqual(
            response.status_code,
            201
        )

        data = response.get_json()

        self.assertEqual(
            data["name"],
            "Brake Pad"
        )

        self.assertEqual(
            data["price"],
            75.50
        )
    # First, Negative Test: POST create an inventory part
    def test_create_inventory_missing_price(self):
        response = self.client.post(
            "/inventory/",
            json={
                "name": "Brake Pad"
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )
    
    
    
    
    # Second, Positive Test: GET read inventory
    def test_get_inventory(self):
        # Create an inventory part first
        create_response = self.client.post(
            "/inventory/",
            json={
                "name": "Brake Pad",
                "price": 75.50
            }
        )

        # Make sure the inventory part was created
        self.assertEqual(
            create_response.status_code,
            201
        )

        # Request all inventory parts
        response = self.client.get(
            "/inventory/"
        )

        # GET request should succeed
        self.assertEqual(
            response.status_code,
            200
        )

        # Convert JSON response into Python data
        data = response.get_json()

        # We created one inventory part
        self.assertEqual(
            len(data),
            1
        )

        # Verify its data
        self.assertEqual(
            data[0]["name"],
            "Brake Pad"
        )

        self.assertEqual(
            data[0]["price"],
            75.50
        )
    # Second, Negative Empty-Inventory Test: GET read inventory
    def test_get_inventory_empty(self):
        # Request inventory without creating anything first
        response = self.client.get(
            "/inventory/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        # Empty database should return an empty list
        self.assertEqual(
            data,
            []
        )
        
        
        
        
        
    # Third, Positive Test: GET read inventory part by ID
    def test_get_inventory_by_id(self):
        # Create an inventory part
        create_response = self.client.post(
            "/inventory/",
            json={
                "name": "Oil Filter",
                "price": 18.99
            }
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        inventory_id = create_response.get_json()["id"]

        # Retrieve that inventory part by ID
        response = self.client.get(
            f"/inventory/{inventory_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["id"],
            inventory_id
        )

        self.assertEqual(
            data["name"],
            "Oil Filter"
        )

        self.assertEqual(
            data["price"],
            18.99
        )
    # Third, Negative Test: GET read inventory part by ID
    def test_get_inventory_not_found(self):
        response = self.client.get(
            "/inventory/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Inventory part not found"
        )
        
        
        
        
    # Fourth, Positive Test: PUT update inventory part by ID
    def test_update_inventory(self):
        create_response = self.client.post(
            "/inventory/",
            json={
                "name": "Brake Pad",
                "price": 75.50
            }
        )

        inventory_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/inventory/{inventory_id}",
            json={
                "name": "Premium Brake Pad",
                "price": 89.99
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["name"],
            "Premium Brake Pad"
        )

        self.assertEqual(
            data["price"],
            89.99
        )
    # Fourth, Negative Test: PUT update inventory part by ID
    def test_update_inventory_not_found(self):
        response = self.client.put(
            "/inventory/9999",
            json={
                "name": "Missing Part"
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Inventory part not found"
        )




    # Fifth, Positive Test: DELETE delete inventory part by ID
    def test_delete_inventory(self):
        create_response = self.client.post(
            "/inventory/",
            json={
                "name": "Delete Part",
                "price": 25.00
            }
        )

        inventory_id = create_response.get_json()["id"]

        response = self.client.delete(
            f"/inventory/{inventory_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Inventory part deleted successfully"
        )

        check_response = self.client.get(
            f"/inventory/{inventory_id}"
        )

        self.assertEqual(
            check_response.status_code,
            404
        )
    # Fifth, Negative Test: DELETE delete inventory part by ID
    def test_delete_inventory_not_found(self):
        response = self.client.delete(
            "/inventory/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Inventory part not found"
        )
