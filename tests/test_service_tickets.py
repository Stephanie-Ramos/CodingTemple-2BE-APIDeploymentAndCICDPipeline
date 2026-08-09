import unittest

from application import create_app
from application.extensions import db
from config import TestingConfig


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    # First, Positive Test: POST create service ticket
    # Because POST /service-tickets/ requires an existing customer, the positive test should create a customer first
    def test_create_service_ticket(self):
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Ticket Customer",
                "email": "ticketcustomer@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        self.assertEqual(
            customer_response.status_code,
            201
        )

        customer_id = customer_response.get_json()["id"]

        response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A123456",
                "service_date": "2026-08-08",
                "service_description": "Oil change and tire rotation",
                "customer_id": customer_id
            }
        )

        self.assertEqual(
            response.status_code,
            201
        )

        data = response.get_json()

        self.assertEqual(
            data["vin"],
            "1HGCM82633A123456"
        )

        self.assertEqual(
            data["customer_id"],
            customer_id
        )
    # First, Negative Test: POST create service ticket
    def test_create_service_ticket_customer_not_found(self):
        response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A654321",
                "service_date": "2026-08-08",
                "service_description": "Brake inspection",
                "customer_id": 9999
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Customer not found."
        )
    # First, Negative Part II Test: POST create service ticket
    # And another negative test for missing customer_id:
    def test_create_service_ticket_missing_customer_id(self):
        response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A999999",
                "service_date": "2026-08-08",
                "service_description": "Battery replacement"
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "customer_id is required."
        )
    
    
    
    
    
    # Second, Positive Test: GET all service tickets
    def test_get_service_tickets(self):
        # Create a customer first
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Ticket Customer",
                "email": "getticketcustomer@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create a service ticket
        self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A123456",
                "service_date": "2026-08-08",
                "service_description": "Oil change",
                "customer_id": customer_id
            }
        )

        # Retrieve all service tickets
        response = self.client.get(
            "/service-tickets/"
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
            data[0]["vin"],
            "1HGCM82633A123456"
        )
    # Second, Negative Empty List Test: GET all service tickets
    def test_get_service_tickets_empty(self):
        response = self.client.get(
            "/service-tickets/"
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
    
    
    
    
    # Third, Positive Test: GET service ticket by ID
    def test_get_service_ticket_by_id(self):
        # Create customer
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Ticket Customer",
                "email": "singleticketcustomer@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create service ticket
        create_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A123456",
                "service_date": "2026-08-08",
                "service_description": "Brake inspection",
                "customer_id": customer_id
            }
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        ticket_id = create_response.get_json()["id"]

        # Retrieve ticket by ID
        response = self.client.get(
            f"/service-tickets/{ticket_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["id"],
            ticket_id
        )

        self.assertEqual(
            data["vin"],
            "1HGCM82633A123456"
        )
    # Third, Negative Test: GET service ticket by ID
    def test_get_service_ticket_not_found(self):
        response = self.client.get(
            "/service-tickets/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Service ticket not found."
        )



    # Fourth, Positive Test: PUT assign mechanic to ticket id 
    def test_assign_mechanic_to_service_ticket(self):

        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Ticket Customer",
                "email": "assigncustomer@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A123456",
                "service_date": "2026-08-08",
                "service_description": "Engine inspection",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        mechanic_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Assigned Mechanic",
                "email": "assignedmechanic@email.com",
                "phone": "555-333-4444",
                "salary": 70000.00
            }
        )

        mechanic_id = mechanic_response.get_json()["id"]

        response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )
    # Fourth, Negative Test: PUT assign mechanic to ticket id
    # Service ticket does not exist 
    def test_assign_mechanic_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/9999/assign-mechanic/1"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Service ticket not found."
        )
    # Fourth, Negative Part II Test: PUT assign mechanic to ticket id
    # Mechanic does not exist
    def test_assign_mechanic_not_found(self):
        # Create customer
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Test Customer",
                "email": "mechanicnotfound@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create service ticket
        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A654321",
                "service_date": "2026-08-08",
                "service_description": "Engine inspection",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        # Try assigning a mechanic that doesn't exist
        response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/9999"
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
    # Fourth, Negative Part III Test: PUT assign mechanic to ticket id
    # Mechanic is already assigned
    def test_assign_mechanic_duplicate(self):
        # Create customer
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Duplicate Assignment Customer",
                "email": "duplicateassignment@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create service ticket
        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A999999",
                "service_date": "2026-08-08",
                "service_description": "Brake inspection",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        # Create mechanic
        mechanic_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Duplicate Mechanic",
                "email": "duplicateassignmentmechanic@email.com",
                "phone": "555-333-4444",
                "salary": 70000.00
            }
        )

        mechanic_id = mechanic_response.get_json()["id"]

        # First assignment should succeed
        first_response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(
            first_response.status_code,
            200
        )

        # Try assigning the same mechanic again
        second_response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(
            second_response.status_code,
            409
        )

        data = second_response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic is already assigned to this service ticket."
        )

    






    # Fifth, Positive Test: PUT Edit mechanic in service tickets
    def test_edit_ticket_mechanics(self):
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Edit Ticket Customer",
                "email": "editticket@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A654321",
                "service_date": "2026-08-08",
                "service_description": "Transmission service",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        mechanic_one_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Mechanic One",
                "email": "editmechanic1@email.com",
                "phone": "555-111-1111",
                "salary": 65000.00
            }
        )

        mechanic_one_id = mechanic_one_response.get_json()["id"]

        mechanic_two_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Mechanic Two",
                "email": "editmechanic2@email.com",
                "phone": "555-222-2222",
                "salary": 70000.00
            }
        )

        mechanic_two_id = mechanic_two_response.get_json()["id"]

        # Assign mechanic one first
        self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_one_id}"
        )

        # Remove mechanic one and add mechanic two
        response = self.client.put(
            f"/service-tickets/{ticket_id}/edit",
            json={
                "add_ids": [mechanic_two_id],
                "remove_ids": [mechanic_one_id]
            }
        )

        self.assertEqual(
            response.status_code,
            200
        ) 
    # Fifth, Negative Test: PUT Edit mechanic in service tickets
    def test_edit_ticket_mechanics_mechanic_not_found(self):
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Missing Mechanic Customer",
                "email": "missingmechanic@email.com",
                "phone": "555-333-4444",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A999999",
                "service_date": "2026-08-08",
                "service_description": "Suspension repair",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        response = self.client.put(
            f"/service-tickets/{ticket_id}/edit",
            json={
                "add_ids": [9999],
                "remove_ids": []
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic 9999 not found"
        )













    # Sixth, Positive Test: PUT remove mechanic from ticket id 
    def test_assign_mechanic_to_service_ticket(self):
        # Create customer
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Ticket Customer",
                "email": "assigncustomer@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create service ticket
        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A123456",
                "service_date": "2026-08-08",
                "service_description": "Engine inspection",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        # Create mechanic
        mechanic_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Assigned Mechanic",
                "email": "assignedmechanic@email.com",
                "phone": "555-333-4444",
                "salary": 70000.00
            }
        )

        mechanic_id = mechanic_response.get_json()["id"]

        # Assign mechanic
        response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )
    # Sixth, Negative Test: PUT remove mechanic from ticket id 
    def test_assign_mechanic_duplicate(self):
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Ticket Customer",
                "email": "duplicateassign@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A654321",
                "service_date": "2026-08-08",
                "service_description": "Transmission inspection",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        mechanic_response = self.client.post(
            "/mechanics/",
            json={
                "name": "Duplicate Mechanic",
                "email": "duplicatemechanic@email.com",
                "phone": "555-333-4444",
                "salary": 70000.00
            }
        )

        mechanic_id = mechanic_response.get_json()["id"]

        # First assignment
        first_response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(
            first_response.status_code,
            200
        )

        # Second assignment should fail
        second_response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(
            second_response.status_code,
            409
        )

        data = second_response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic is already assigned to this service ticket."
        )
    # Sixth, Negative Part II Test: PUT remove mechanic from ticket id 
    # add at least one 404 test
    def test_assign_mechanic_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/9999/assign-mechanic/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Service ticket not found."
        )




    # Seventh, Positive Test: PUT Add Part to Service Ticket
    def test_add_part_to_service_ticket(self):
        # Create customer
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Parts Customer",
                "email": "partscustomer@email.com",
                "phone": "555-111-2222",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create service ticket
        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A123456",
                "service_date": "2026-08-08",
                "service_description": "Brake repair",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        # Create inventory part
        inventory_response = self.client.post(
            "/inventory/",
            json={
                "name": "Brake Pad",
                "price": 75.50
            }
        )

        self.assertEqual(
            inventory_response.status_code,
            201
        )

        inventory_id = inventory_response.get_json()["id"]

        # Add part to service ticket
        response = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/{inventory_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )
    # Seventh, Negative Test: PUT Add Part to Service Ticket
    # duplicate-part negative test:
    def test_add_duplicate_part_to_service_ticket(self):
        # Create customer
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Duplicate Parts Customer",
                "email": "duplicateparts@email.com",
                "phone": "555-222-3333",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        # Create service ticket
        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A654321",
                "service_date": "2026-08-08",
                "service_description": "Brake repair",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        # Create inventory part
        inventory_response = self.client.post(
            "/inventory/",
            json={
                "name": "Brake Rotor",
                "price": 120.00
            }
        )

        inventory_id = inventory_response.get_json()["id"]

        # First assignment should work
        first_response = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/{inventory_id}"
        )

        self.assertEqual(
            first_response.status_code,
            200
        )

        # Second assignment should fail
        second_response = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/{inventory_id}"
        )

        self.assertEqual(
            second_response.status_code,
            400
        )

        data = second_response.get_json()

        self.assertEqual(
            data["message"],
            "Part is already assigned to this service ticket"
        )
    # Seventh, Negative Part II Test: PUT Add Part to Service Ticket
    # For a nonexistent ticket:
    def test_add_part_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/9999/add-part/1"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Service ticket not found"
        )
    # Seventh, Negative Part III Test: PUT Add Part to Service Ticket
    # for a nonexistent inventory part, we need a real ticket first
    def test_add_part_inventory_not_found(self):
        customer_response = self.client.post(
            "/customers/",
            json={
                "name": "Missing Part Customer",
                "email": "missingpart@email.com",
                "phone": "555-333-4444",
                "password": "password123"
            }
        )

        customer_id = customer_response.get_json()["id"]

        ticket_response = self.client.post(
            "/service-tickets/",
            json={
                "vin": "1HGCM82633A999999",
                "service_date": "2026-08-08",
                "service_description": "Suspension repair",
                "customer_id": customer_id
            }
        )

        ticket_id = ticket_response.get_json()["id"]

        response = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/9999"
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