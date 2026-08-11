# Imports Python's built-in testing framework
import unittest
# imports your Flask application factory
from application import create_app
# imports your SQLAlchemy database object
from application.extensions import db

from config import TestingConfig


# Everything related to Customer routes will go inside this class
class TestCustomers(unittest.TestCase):

    # This method runs before every test
    def setUp(self):
        # creates the tables 
        self.app = create_app(TestingConfig)

        # creates a fake client that can make requests to your Flask API
        # lets unittest automatically verify your routes instead of writing project
        self.client = self.app.test_client()

    # tearDown() cleans everything after every test
    # Then the next test starts fresh 
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_app_is_testing(self):
        self.assertTrue(
            self.app.config["TESTING"]
        )
            
    
    
    
    
    # First, Positive Test: POST create customer 
    # test_: Python's unittest framework knows that it should run this method automatically
    def test_create_customer(self):
        # creates fake customer information specifically for the test
        customer_payload = {
            "name": "Test Customer",
            "email": "testcustomer@email.com",
            "phone": "555-555-5555",
            "password": "password123"
        }
        # acts like Postman sending: POST /customers/
        response = self.client.post(
            "/customers/",
            json=customer_payload
        )
        # Check status code
        # expects the API to return status code 201
        self.assertEqual(response.status_code, 201)
        
        # Convert response JSON into a Python dictionary
        data = response.get_json()

        # Check returned customer information
        self.assertEqual(
            data["name"],
            "Test Customer"
        )

        self.assertEqual(
            data["email"],
            "testcustomer@email.com"
        ) 
    # First, Negative Test: POST create customer
    # negative test because your email field is unique, so the API should reject the second customer instead of creating a duplicate
    def test_create_customer_duplicate_email(self):
        # This creates the JSON data that will be sent to the Customer POST route. It acts like the body you would enter in Swagger. 
        customer_payload = {
            "name": "Test Customer",
            "email": "duplicate@email.com",
            "phone": "555-555-5555",
            "password": "password123"
        }

        # Create the first customer
        first_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        # This checks that the first customer is successfully created
        self.assertEqual(first_response.status_code, 201)

        # Try to create another customer
        # using the same email
        second_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        # The second request should fail
        self.assertEqual(
            second_response.status_code,
            400
        )
        
        # takes the JSON response from Flask and turns it into a Python dictionary
        data = second_response.get_json()

        # checks that the API returned the specific error message you expected
        self.assertEqual(
            data["message"],
            "Email already exists"
        )
        
    
    
    
        
    # Second, Positive Test: GET all customers
    def test_get_customers(self):
        # This uses Flask's test client to send a fake HTTP GET request to
        # response: The response from your Flask route gets stored in
        response = self.client.get(
            "/customers/"
        )

        # This checks that the route returned
        self.assertEqual(
            response.status_code,
            200
        )

        # The Flask route returns JSON
        # get_json() converts that JSON response into a Python object, usually a dictionary
        data = response.get_json()

        # assertIn() means: Verify that this value exists inside another value
        self.assertIn(
            "customers",
            data
        )

        self.assertIn(
            "page",
            data
        )

        self.assertIn(
            "per_page",
            data
        )

        self.assertIn(
            "total_pages",
            data
        )

        self.assertIn(
            "total_customers",
            data
        )
    # Second, Empty Page Negative Test: GET all customers
    def test_get_customers_empty_page(self):
        response = self.client.get(
            "/customers/?page=999"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["customers"],
            []
        )
        
    
    
    
    
    # Third, Positive Test: GET customer by id
    def test_get_customer_by_id(self):
        customer_payload = {
            "name": "Test Customer",
            "email": "customerbyid@email.com",
            "phone": "555-111-2222",
            "password": "password123"
        }

        create_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        created_customer = create_response.get_json()

        customer_id = created_customer["id"]

        response = self.client.get(
            f"/customers/{customer_id}"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["id"],
            customer_id
        )

        self.assertEqual(
            data["email"],
            "customerbyid@email.com"
        )
    # Third, Negative Test: GET customer by id
    def test_get_customer_not_found(self):
        response = self.client.get(
            "/customers/9999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Customer not found"
        )





    # Fourth, Positive Test: POST Update customer 
    def test_update_customer(self):
        # Create a customer
        customer_payload = {
            "name": "Original Customer",
            "email": "update@email.com",
            "phone": "555-111-1111",
            "password": "password123"
        }

        create_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        customer_data = create_response.get_json()
        customer_id = customer_data["id"]

        # Login to get JWT
        login_response = self.client.post(
            "/customers/login",
            json={
                "email": "update@email.com",
                "password": "password123"
            }
        )

        self.assertEqual(
            login_response.status_code,
            200
        )

        token = login_response.get_json()["token"]

        # Update the same authenticated customer
        response = self.client.put(
            f"/customers/{customer_id}",
            json={
                "name": "Updated Customer",
                "email": "update@email.com",
                "phone": "555-222-3333"
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["name"],
            "Updated Customer"
        )

        self.assertEqual(
            data["phone"],
            "555-222-3333"
        )
    # Fourth, Negative Test: POST Update customer 
    def test_update_other_customer_forbidden(self):
        # Create customer 1
        first_customer = {
            "name": "Customer One",
            "email": "customer1@email.com",
            "phone": "555-111-1111",
            "password": "password123"
        }

        first_response = self.client.post(
            "/customers/",
            json=first_customer
        )

        # Create customer 2
        second_customer = {
            "name": "Customer Two",
            "email": "customer2@email.com",
            "phone": "555-222-2222",
            "password": "password123"
        }

        second_response = self.client.post(
            "/customers/",
            json=second_customer
        )

        second_customer_id = second_response.get_json()["id"]

        # Login as customer 1
        login_response = self.client.post(
            "/customers/login",
            json={
                "email": "customer1@email.com",
                "password": "password123"
            }
        )

        token = login_response.get_json()["token"]

        # Customer 1 tries to update customer 2
        response = self.client.put(
            f"/customers/{second_customer_id}",
            json={
                "name": "Unauthorized Update"
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(
            response.status_code,
            403
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "You are not authorized to update this customer"
        )
    
    
    
    
    
    #Five, Positive Test: Customer Log in 
    def test_customer_login(self):
        customer_payload = {
            "name": "Login Customer",
            "email": "login@email.com",
            "phone": "555-333-4444",
            "password": "password123"
        }

        create_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        response = self.client.post(
            "/customers/login",
            json={
                "email": "login@email.com",
                "password": "password123"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertIn(
            "token",
            data
        )
    # Five, Negative Test: Customer Log in 
    def test_customer_login_invalid_password(self):
        customer_payload = {
            "name": "Login Customer",
            "email": "invalidlogin@email.com",
            "phone": "555-333-4444",
            "password": "password123"
        }

        self.client.post(
            "/customers/",
            json=customer_payload
        )

        response = self.client.post(
            "/customers/login",
            json={
                "email": "invalidlogin@email.com",
                "password": "wrongpassword"
            }
        )

        self.assertEqual(
            response.status_code,
            401
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Invalid email or password"
        )
        
        
        
        
            
    #Six, Positive Test: Logged-In Customer accessing tickets
    def test_get_my_tickets(self):
        customer_payload = {
            "name": "Ticket Customer",
            "email": "tickets@email.com",
            "phone": "555-333-4444",
            "password": "password123"
        }

        create_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        # Login
        login_response = self.client.post(
            "/customers/login",
            json={
                "email": "tickets@email.com",
                "password": "password123"
            }
        )

        self.assertEqual(
            login_response.status_code,
            200
        )

        token = login_response.get_json()["token"]

        # Request authenticated customer's tickets
        response = self.client.get(
            "/customers/my-tickets",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        # Customer has no tickets yet
        self.assertEqual(
            data,
            []
        )
    #Six, Negative Test (no token): Logged-In Customer accessing tickets
    def test_get_my_tickets_without_token(self):
        response = self.client.get(
            "/customers/my-tickets"
        )

        self.assertEqual(
            response.status_code,
            401
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Authorization token is missing"
        )
        
        
        
        
        
    # Seven, Positive Test: Delete Customer
    def test_delete_customer(self):
        customer_payload = {
            "name": "Delete Customer",
            "email": "delete@email.com",
            "phone": "555-444-5555",
            "password": "password123"
        }

        # Create customer
        create_response = self.client.post(
            "/customers/",
            json=customer_payload
        )

        self.assertEqual(
            create_response.status_code,
            201
        )

        customer_id = create_response.get_json()["id"]

        # Login
        login_response = self.client.post(
            "/customers/login",
            json={
                "email": "delete@email.com",
                "password": "password123"
            }
        )

        token = login_response.get_json()["token"]

        # Delete own account
        response = self.client.delete(
            f"/customers/{customer_id}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Customer deleted successfully"
        )
        
        check_response = self.client.get(
            f"/customers/{customer_id}"
        )

        self.assertEqual(
            check_response.status_code,
            404
        ) 
    # Seventh, Negative Test: Delete a Customer
    def test_delete_other_customer_forbidden(self):
        # Create customer 1
        first_response = self.client.post(
            "/customers/",
            json={
                "name": "Customer One",
                "email": "delete1@email.com",
                "phone": "555-111-1111",
                "password": "password123"
            }
        )

        # Create customer 2
        second_response = self.client.post(
            "/customers/",
            json={
                "name": "Customer Two",
                "email": "delete2@email.com",
                "phone": "555-222-2222",
                "password": "password123"
            }
        )

        second_customer_id = second_response.get_json()["id"]

        # Login as customer 1
        login_response = self.client.post(
            "/customers/login",
            json={
                "email": "delete1@email.com",
                "password": "password123"
            }
        )

        token = login_response.get_json()["token"]

        # Customer 1 attempts to delete customer 2
        response = self.client.delete(
            f"/customers/{second_customer_id}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(
            response.status_code,
            403
        )

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "You are not authorized to delete this customer"
        )