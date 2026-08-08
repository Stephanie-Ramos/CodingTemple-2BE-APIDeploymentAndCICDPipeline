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
            
    
    # First Route: POST create customer 
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
        
    # negative test because your email field is unique, so the API should reject the second customer instead of creating a duplicate
    def test_create_customer_duplicate_email(self):
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
        
        data = second_response.get_json()

        self.assertEqual(
            data["message"],
            "Email already exists"
        )
        
