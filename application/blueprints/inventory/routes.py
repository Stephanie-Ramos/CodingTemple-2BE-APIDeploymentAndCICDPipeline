# jsonify converts Python dictionaries into JSON responses
# request gives you access to the incoming HTTP request. It allows it to read JSON sent in the Postman request body
from flask import jsonify, request

# This imports your Inventory blueprint 
from application.blueprints.inventory import inventory_bp
# This imports two Marshmallow schema objects: one and many
from application.blueprints.inventory.schemas import (inventory_schema, inventories_schema)

# This imports your SQLAlchemy database object.
from application.extensions import db
# This imports your Inventory model from models.py 
# The model represents the MySQL inventory table
from application.models import Inventory

from marshmallow import ValidationError





# First, POST create an inventory part
@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    """
    Create an inventory part
    ---
    tags:
      - Inventory

    summary: Create an inventory part
    description: Creates a new inventory part in the Mechanic Shop API.

    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: InventoryPayload
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
              example: Brake Pad
            price:
              type: number
              format: float
              example: 75.50

    responses:
      201:
        description: Inventory part successfully created
        schema:
          id: InventoryResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Brake Pad
            price:
              type: number
              format: float
              example: 75.50

      400:
        description: Invalid inventory data
    """
    try: 
        inventory_data = inventory_schema.load(
            # request.json reads the JSON body sent from Postman
            # inventory_schema.load(...) validates and deserializes that JSON.
            request.json,
            # gives Marshmallow access to your SQLAlchemy session while creating that model object.
            session=db.session
        )
    except ValidationError as error:
        return jsonify(error.messages), 400

    # Adds the new Inventory object to SQLAlchemy's current database session 
    db.session.add(inventory_data)
    db.session.commit()

    return inventory_schema.jsonify(
        inventory_data
    ), 201
    
    
    
    
    
# Second, GET read inventory 
@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    """
    Get all inventory parts
    ---
    tags:
      - Inventory

    summary: Get all inventory parts
    description: Returns a list of all inventory parts in the Mechanic Shop API.

    responses:
      200:
        description: Inventory parts retrieved successfully
        schema:
          type: array
          items:
            $ref: '#/definitions/InventoryResponse'
    """
    # This queries the database 
    inventory = db.session.execute(
        # Select Inventory records 
        db.select(Inventory)
    ).scalars().all()

    # Uses the plural schema to serialize the list into JSON 
    return inventories_schema.jsonify(
        inventory
    ), 200





# Third, GET read inventory part by ID
@inventory_bp.route(
    "/<int:inventory_id>",
    methods=["GET"]
)
# Defines the function and receives the ID from the URL 
def get_inventory_by_id(inventory_id):
    """
    Get an inventory part by ID
    ---
    tags:
      - Inventory

    summary: Get an inventory part by ID
    description: Returns a single inventory part using its unique inventory ID.

    parameters:
      - name: inventory_id
        in: path
        required: true
        type: integer
        description: The unique ID of the inventory part

    responses:
      200:
        description: Inventory part retrieved successfully
        schema:
          $ref: '#/definitions/InventoryResponse'

      404:
        description: Inventory part not found
    """
    # Looks for an Inventory record by primary key 
    inventory = db.session.get(
        Inventory,
        inventory_id
    )

    # Checks whether a matching part was found 
    if not inventory:
        # If nothing exists
        return jsonify({
            "message": "Inventory part not found"
        }), 404

    # If the part exists, serialize the single item and return it with 200 OK
    return inventory_schema.jsonify(
        inventory
    ), 200





# Fourth, PUT update inventory part by ID
@inventory_bp.route(
    "/<int:inventory_id>",
    methods=["PUT"]
)
# Receives the ID from the URL
def update_inventory(inventory_id):
    """
    Update an inventory part
    ---
    tags:
      - Inventory

    summary: Update an inventory part
    description: Updates one or more fields for an existing inventory part.

    parameters:
      - name: inventory_id
        in: path
        required: true
        type: integer
        description: The unique ID of the inventory part to update

      - name: body
        in: body
        required: true
        schema:
          id: InventoryUpdatePayload
          type: object
          properties:
            name:
              type: string
              example: Premium Brake Pad
            price:
              type: number
              format: float
              example: 89.99

    responses:
      200:
        description: Inventory part updated successfully
        schema:
          $ref: '#/definitions/InventoryResponse'

      404:
        description: Inventory part not found
    """
    # Fetches the existing inventory item from MySQL
    inventory = db.session.get(
        Inventory,
        inventory_id
    )
    
    # Checks if it exists
    if not inventory:
        return jsonify({
            "message": "Inventory part not found"
        }), 404

    # request.json reads the updated data from Postman
    # instance=inventory: tells Marshmallow to update this existing Inventory object instead of creating a new one
    # partial=True: means you do not have to send every field
    # session=db.session: gives Marshmallow access to the SQLAlchemy session
    updated_inventory = inventory_schema.load(
        request.json,
        instance=inventory,
        partial=True,
        session=db.session
    )

    db.session.commit()

    return inventory_schema.jsonify(updated_inventory), 200





# Fifth, DELETE delete inventory part by ID
@inventory_bp.route(
    "/<int:inventory_id>",
    methods=["DELETE"]
)
def delete_inventory(inventory_id):
    """
    Delete an inventory part
    ---
    tags:
      - Inventory

    summary: Delete an inventory part
    description: Deletes an inventory part using its unique inventory ID.

    parameters:
      - name: inventory_id
        in: path
        required: true
        type: integer
        description: The unique ID of the inventory part to delete

    responses:
      200:
        description: Inventory part deleted successfully

      404:
        description: Inventory part not found
    """
    inventory = db.session.get(
        Inventory,
        inventory_id
    )

    if not inventory:
        return jsonify({
            "message": "Inventory part not found"
        }), 404

    db.session.delete(inventory)
    db.session.commit()

    return jsonify({
        "message": "Inventory part deleted successfully"
    }), 200
    
    