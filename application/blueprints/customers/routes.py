# Import Statements
# request: Represents the HTTP request sent by the client
# jsonify(): Converts Python objects into JSON responses
from flask import request, jsonify
# Whenever Marshmallow validates incoming JSON and finds invalid data, it raises a ValidationError
from marshmallow import ValidationError

# Imports your SQLAlchemy database object
from application.extensions import db

# tells Flask-Limiter to restrict how often that route can be called. Ex. 5 per minute
# to protect endpoints from excessive repeated requests
from application.extensions import limiter
# makes your Flask-Caching object available in the customer routes file
from application.extensions import cache

# This imports two authentication tools from your auth.py file
# encode_token is used after a customer successfully logs in. It creates a JWT token containing information such as the customer ID
# token_required is the decorator you use to protect routes so only authenticated customers with a valid Bearer Token can access them
from application.utils.auth import encode_token, token_required

# Imports the Customer model: Whenever you need to create, retrieve, update, or delete customers, you work with this model
from application.models import Customer, ServiceTicket

# Imports the Customer Blueprint: Every route below belongs to this blueprint
from application.blueprints.customers import customers_bp
# Imports the Marshmallow schemas 
from application.blueprints.customers.schemas import (customer_schema, customers_schema, login_schema)
# This imports the schema used to serialize multiple service tickets
from application.blueprints.service_tickets.schemas import service_tickets_schema

from sqlalchemy.exc import IntegrityError





# POST create customer
# the full URL becomes POST /customers/
@customers_bp.route("/", methods=["POST"])
# Defines the function that runs when someone creates a customer 
def create_customer():
    """
    Create a new customer
    ---
    tags:
      - Customers

    summary: Create a customer
    description: Creates a new customer account in the Mechanic Shop API.

    parameters:
      - in: body
        name: body
        required: true
        schema:
            id: CustomerPayload
            type: object
            required:
                - name
                - email
                - phone
                - password
            properties:
                name:
                    type: string
                    example: Jane Doe
                email:
                    type: string
                    example: jane@example.com
                phone:
                    type: string
                    example: 555-123-4567
                password:
                    type: string
                    example: password123

    responses:
        201:
            description: Customer successfully created
            schema:
                id: CustomerResponse
                type: object
                properties:
                    id:
                        type: integer
                        example: 1
                    name:
                        type: string
                        example: Jane Doe
                    email:
                        type: string
                        example: jane@example.com
                    phone:
                        type: string
                        example: 555-123-4567

        400:
            description: Invalid customer data
    """
    
    try:
        # Uses Marshmallow to validate and deserialize the incoming JSON
        customer = customer_schema.load(
            # Retrieves the JSON body sent by Postman
            request.get_json(),
            partial=True,
            # Allows Marshmallow to create a SQLAlchemy model object connected to your database session
            session=db.session
        )
    # If Marshmallow detects invalid JSON, execution comes here
    except ValidationError as error:
        # Returns message and status code
        return jsonify(error.messages), 400

    # Adds the new Customer object to SQLAlchemy's session
    db.session.add(customer)
    
    try:
        # Permanently inserts the customer into the database
        db.session.commit()

    except IntegrityError:
        # Resets the failed transaction
        db.session.rollback()
        
        return jsonify({
            "message": "Email already exists"
        }), 400
    

    # This clears everything currently stored in Flask-Caching 
    # Throw away the existing cached responses so the next request retrieves fresh data
    cache.clear()

    # Returns new customer into JSON and status code
    return customer_schema.jsonify(customer), 201





# GET All Customers
@customers_bp.route("/", methods=["GET"])
# Add Rate Limiting 
# Rate limiting helps prevent excessive requests and protects the API
# from repeated login attempts or request abuse
@limiter.limit("5 per minute")
def get_customers():
    """
    Get all customers
    ---
    tags:
      - Customers

    summary: Create a customer
    description: Creates a new customer account in the Mechanic Shop API.

    parameters:
      - name: page
        in: query
        required: false
        type: integer
        default: 1
        description: Page number to return 
        
    
      - name: per_page
        in: query
        required: false
        type: integer
        default: 5
        description: Number of customers to return per page

    responses:
        200:
            description: Customers retrieved successfully
            schema:
                type: object
                properties:
                    customers:
                        type: array
                        items: 
                            $ref: '#/definitions/CustomerResponse'
                        
                    page:
                        type: integer
                        example: 1
                    per_page:
                        type: integer
                        example: 5
                    total_pages:
                        type: integer
                        example: 2
                    total_customers:
                        type: integer
                        example: 7
    """    
    
    # The first page
    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    # show five customers per page
    per_page = request.args.get(
        "per_page",
        default=5,
        type=int
    )
    
    # takes a SQLAlchemy query and splits the results into pages
    pagination = db.paginate(
        db.select(Customer),
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "customers": customers_schema.dump(
            pagination.items
        ),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_customers": pagination.total
    }), 200





# GET One Customer
@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    """
    Get one customer
    ---
    tags:
      - Customers

    summary: Get a customer by ID
    description: Returns a single customer using the customer's unique ID.

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: The unique ID of the customer

    responses:
      200:
        description: Customer retrieved successfully
        schema:
          $ref: '#/definitions/CustomerResponse'

      404:
        description: Customer not found
    """
    
    # Looks for the customer whose primary key equals id 
    customer = db.session.get(Customer, id)

    # Checks whether the customer exists 
    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    # Returns the customer as JSON.
    return customer_schema.jsonify(customer), 200


# PUT updates a customer 
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
# This protects the route with your JWT authentication decorator
# The request must include a valid Bearer Token
# The decorator reads the token, extracts the authenticated customer's ID, and passes that value into the function
@token_required
# The function receives two different IDs 
def update_customer(auth_customer_id, customer_id):
    """
    Update a customer
    ---
    tags:
      - Customers

    summary: Update a customer
    description: Updates the authenticated customer's account information.

    security:
      - BearerAuth: []

    parameters:
      - name: customer_id
        in: path
        required: true
        type: integer
        description: The ID of the customer to update

      - name: body
        in: body
        required: true
        schema:
          id: CustomerUpdatePayload
          type: object
          properties:
            name:
              type: string
              example: Updated Customer
            email:
              type: string
              example: updated@example.com
            phone:
              type: string
              example: 555-222-3333

    responses:
      200:
        description: Customer updated successfully
        schema:
          $ref: '#/definitions/CustomerResponse'

      403:
        description: Not authorized to update this customer

      404:
        description: Customer not found
    """
    
    # checks whether the logged-in customer is trying to update their own account 
    if auth_customer_id != customer_id:
        return jsonify({
            "message": "You are not authorized to update this customer"
        }), 403
    
    # This asks SQLAlchemy to find the Customer whose primary key matches customer_id 
    # it essentially looks for customer_id
    customer = db.session.get(Customer, customer_id)

    # checks whether the customer exists 
    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404
    
    # customer_data: becomes a Customer object
    # customer_schema.load(): validates and deserializes that JSON
    # request.json: gets the JSON sent by Postman
    # partial=True: the user does not have to provide every customer field during an update
    customer_data = customer_schema.load(
        request.json,
        partial=True
    )

    data = request.get_json()

    if "name" in data:
        customer.name = data["name"]

    if "email" in data:
        customer.email = data["email"]

    if "phone" in data:
        customer.phone = data["phone"]
    

    db.session.commit()
    
    cache.clear()

    # Returns the updated customer 
    return customer_schema.jsonify(customer), 200





# POST Customer Login Route
# Creates POST /customers/login
@customers_bp.route("/login", methods=["POST"])
# allows the client to attempt this route up to five times per minute
@limiter.limit("5 per minute")
def login():
    """
    Customer login
    ---
    tags:
      - Customers

    summary: Log in a customer
    description: Authenticates a customer using email and password and returns a JWT token.

    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CustomerLoginPayload
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: customer@example.com
            password:
              type: string
              example: password123

    responses:
      200:
        description: Login successful
        schema:
          id: LoginResponse
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

      401:
        description: Invalid email or password
    """
    # There is no customer ID in the URL because the server determines who the customer is from their credentials
    data = login_schema.load(request.json)

    # searches the customers table for the first customer whose email matches the submitted email 
    customer = Customer.query.filter_by(
        # Find the customer WHERE email = submitted email
        email=data.email
    ).first()

    # checks two conditions:
    # makes sure a matching customer was actually found
    # compares the stored password with the submitted password 
    if customer and customer.password == data.password:
        # creates a JWT for that customer
        token = encode_token(customer.id)

        return jsonify({
            "token": token
        }), 200
    # If either the email or password is wrong 
    return jsonify({
        "message": "Invalid email or password"
    }), 401





# GET all of my tickets   
# creates: GET /customers/my-tickets in the URL
@customers_bp.route("/my-tickets", methods=["GET"])
# requires a valid JWT
@token_required
# There is no customer ID in the URL
# receives the authenticated customer ID from @token_required
def get_my_tickets(customer_id):
    """
    Get authenticated customer's service tickets
    ---
    tags:
      - Customers

    summary: Get my service tickets
    description: Returns all service tickets belonging to the authenticated customer.

    security:
      - BearerAuth: []

    responses:
      200:
        description: Service tickets retrieved successfully
        schema:
          type: array
          items:
            type: object

      401:
        description: Authentication token is missing or invalid
    """
        
    # starts executing a SQLAlchemy query and selects service ticket records
    tickets = db.session.execute(
        db.select(ServiceTicket).where(
            # Ex: Only customer 4's tickets are returned.
            ServiceTicket.customer_id == customer_id
        )
    ).scalars().all()

    return service_tickets_schema.jsonify(tickets), 200





# DELETE a customer 
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@token_required
# auth_customer_id: receives authentication from the JWT
def delete_customer(auth_customer_id, customer_id):
    """
    Delete a customer
    ---
    tags:
      - Customers

    summary: Delete a customer
    description: Deletes the authenticated customer's account.

    security:
      - BearerAuth: []

    parameters:
      - name: customer_id
        in: path
        required: true
        type: integer
        description: ID of the customer to delete

    responses:
      200:
        description: Customer deleted successfully

      403:
        description: Not authorized to delete this customer

      404:
        description: Customer not found

      401:
        description: Authentication token is missing or invalid
    """
    # prevents one authenticated customer from deleting another customer's account 
    if auth_customer_id != customer_id:
        return jsonify({
            "message": "You are not authorized to delete this customer"
        }), 403
        
    # Looks for the customer in the database
    customer = db.session.get(Customer, customer_id)

    # Checks whether it exists 
    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    # Marks the customer for deletion 
    db.session.delete(customer)
    # Actually removes the customer from MySQL 
    db.session.commit()

    cache.clear()

    # Returns message
    return jsonify({
        "message": "Customer deleted successfully"
    }), 200