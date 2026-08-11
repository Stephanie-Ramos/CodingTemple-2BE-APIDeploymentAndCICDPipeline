import unittest

from application import create_app
from application.extensions import db, cache
from config import TestingConfig


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            cache.clear()

    def tearDown(self):
        with self.app.app_context():
            cache.clear()
            db.session.remove()
            db.drop_all()
    
    
    
    
    # First, Positive: POST Route: Create a mechanic
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Test Mechanic",
            "email": "mechanic@email.com",
            "phone": "555-222-3333",
            "salary": 65000.00
        }

        response = self.client.post(
            "/mechanics/",
            json=mechanic_payload
        )

        self.assertEqual(
            response.status_code,
            201
        )

        data = response.get_json()

        self.assertEqual(
            data["name"],
            "Test Mechanic"
        )

        self.assertEqual(
            data["email"],
            "mechanic@email.com"
        )
    # First, Negative Duplicate Email Test: POST Route: Create a mechanic
    def test_create_mechanic_duplicate_email(self):
        mechanic_payload = {
            "name": "Test Mechanic",
            "email": "duplicate@mechanic.com",
            "phone": "555-222-3333",
            "salary": 65000.00
        }

        first_response = self.client.post(
            "/mechanics/",
            json=mechanic_payload
        )

        self.assertEqual(
            first_response.status_code,
            201
        )

        second_response = self.client.post(
            "/mechanics/",
            json=mechanic_payload
        )

        self.assertEqual(
            second_response.status_code,
            409
        )

        data = second_response.get_json()

        self.assertEqual(
            data["message"],
            "A mechanic with that email already exists."
        )
    
    
    
    
    
    
    # Second, Positive Test: GET Route: Retrieve all mechanics 
    def test_get_mechanics(self):
        # Create a mechanic first
        self.client.post(
            "/mechanics/",
            json={
                "name": "Test Mechanic",
                "email": "getmechanic@email.com",
                "phone": "555-444-5555",
                "salary": 65000.00
            }
        )

        response = self.client.get(
            "/mechanics/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            len(data),
            1
        )

        self.assertEqual(
            data[0]["name"],
            "Test Mechanic"
        )
    # Second, Negative Empty List Test: GET Route: Retrieve all mechanics 
    def test_get_mechanics_empty(self):
        response = self.client.get(
            "/mechanics/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data,
            []
        )
        
    
    
    
    
    # Third, Positive Test: GET Route: Retrieve one mechanic
    def test_get_mechanic_by_id(self):
        create_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Single Mechanic",
                "email": "singlemechanic@email.com",
                "phone": "555-777-8888",
                "salary": 70000.00
            }
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        mechanic_data = create_response.get_json()

        mechanic_id = mechanic_data["id"]

        response = self.client.get(
            f"/mechanics/{mechanic_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["id"],
            mechanic_id
        )

        self.assertEqual(
            data["email"],
            "singlemechanic@email.com"
        )
    # Third, Negative Test: GET Route: Retrieve one mechanic
    def test_get_mechanic_not_found(self):
        response = self.client.get(
            "/mechanics/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic not found."
        )
    
    
    
    
    # Fourth, Positive Test: PUT Route: Update a mechanic
    def test_update_mechanic(self):
        create_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Original Mechanic",
                "email": "originalmechanic@email.com",
                "phone": "555-111-2222",
                "salary": 65000.00
            }
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        mechanic_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/mechanics/{mechanic_id}",
            json={
                "name": "Updated Mechanic",
                "salary": 72000.00
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["name"],
            "Updated Mechanic"
        )

        self.assertEqual(
            data["salary"],
            72000.00
        )
    # Fourth, Negative Test: PUT Route: Update a mechanic
    # A useful negative test is updating a mechanic that does not exist:
    def test_update_mechanic_not_found(self):
        response = self.client.put(
            "/mechanics/9999",
            json={
                "name": "Does Not Exist"
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic not found."
        )
    # Fourth, Negative Part II Test: PUT Route: Update a mechanic
    # And because your route explicitly checks for an empty body, add:
    def test_update_mechanic_empty_body(self):
        create_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Test Mechanic",
                "email": "emptybody@email.com",
                "phone": "555-111-2222",
                "salary": 65000.00
            }
        )

        mechanic_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/mechanics/{mechanic_id}",
            json={}
        )

        self.assertEqual(
            response.status_code,
            400
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Request body must contain JSON data."
        )
    
    
    
    
    
    # Fifth, Positive Test: GET Mechanics by most tickets
    def test_get_mechanics_by_ticket_count(self):
        self.client.post(
            "/mechanics/",
            json={
                "name": "Mechanic One",
                "email": "mechanic1@email.com",
                "phone": "555-111-1111",
                "salary": 65000.00
            }
        )

        self.client.post(
            "/mechanics/",
            json={
                "name": "Mechanic Two",
                "email": "mechanic2@email.com",
                "phone": "555-222-2222",
                "salary": 70000.00
            }
        )

        response = self.client.get(
            "/mechanics/most-tickets"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            len(data),
            2
        )

        self.assertIn(
            "ticket_count",
            data[0]
        )
        
        # Neither mechanic has a service ticket yet,
        # so both ticket counts should be 0
        self.assertEqual(
            data[0]["ticket_count"],
            0
        )

        self.assertEqual(
            data[1]["ticket_count"],
            0
        )
    # Fifth, Negative Empty Database Test: GET Mechanics by most tickets
    def test_get_mechanics_by_ticket_count_empty(self):
        response = self.client.get(
            "/mechanics/most-tickets"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data,
            []
        )
        
    
    
    
    
    # Sixth, Positive Test: DELETE Route: Delete a mechanic
    def test_delete_mechanic(self):
        # Create a mechanic
        create_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Delete Mechanic",
                "email": "deletemechanic@email.com",
                "phone": "555-333-4444",
                "salary": 65000.00
            }
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        # Get the ID of the newly created mechanic
        mechanic_id = create_response.get_json()["id"]

        # Delete the mechanic
        response = self.client.delete(
            f"/mechanics/{mechanic_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic deleted successfully."
        ) 
        
        # Try to retrieve the deleted mechanic
        check_response = self.client.get(
            f"/mechanics/{mechanic_id}"
        )

        # The mechanic should no longer exist
        self.assertEqual(
            check_response.status_code,
            404
        )
    # Sixth, Negative Test: DELETE Route: Delete a mechanic
    def test_delete_mechanic_not_found(self):
        response = self.client.delete(
            "/mechanics/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic not found."
        )
