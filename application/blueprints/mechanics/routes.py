from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from application.extensions import db
from application.models import Mechanic,  ServiceTicket
from application.extensions import cache

from application.blueprints.mechanics import mechanics_bp
from application.blueprints.mechanics.schemas import (
    mechanic_schema,
    mechanics_schema,
)





# First, POST Route: Create a mechanic
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    """
    Create a new mechanic
    ---
    tags:
      - Mechanics

    summary: Create a mechanic
    description: Creates a new mechanic account in the Mechanic Shop API.

    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: MechanicPayload
          type: object
          required:
            - name
            - email
            - phone
            - salary
          properties:
            name:
              type: string
              example: Alex Rivera
            email:
              type: string
              example: alex@example.com
            phone:
              type: string
              example: 555-123-4567
            salary:
              type: number
              format: float
              example: 65000.00

    responses:
      201:
        description: Mechanic successfully created
        schema:
          id: MechanicResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Alex Rivera
            email:
              type: string
              example: alex@example.com
            phone:
              type: string
              example: 555-123-4567

      400:
        description: Invalid mechanic data

      409:
        description: A mechanic with that email already exists
    """
    try:
        mechanic = mechanic_schema.load(
            request.get_json(),
            session=db.session,
        )
    except ValidationError as error:
        return jsonify(error.messages), 400

    try:
        db.session.add(mechanic)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "message": "A mechanic with that email already exists."
        }), 409
    
    cache.clear()

    return mechanic_schema.jsonify(mechanic), 201





# Second, GET Route: Retrieve all mechanics 
@mechanics_bp.route("/", methods=["GET"])
# Caching this GET route reduces repeated database queries when the
# mechanics list is requested frequently but has not recently changed
@cache.cached(timeout=60)
def get_mechanics():
    """
    Get all mechanics
    ---
    tags:
      - Mechanics

    summary: Get all mechanics
    description: Returns a list of all mechanics in the Mechanic Shop API.

    responses:
      200:
        description: Mechanics retrieved successfully
        schema:
          type: array
          items:
            $ref: '#/definitions/MechanicResponse'
    """
    mechanics = db.session.execute(
        db.select(Mechanic)
    ).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200





# Third, GET Route: Retrieve one mechanic
@mechanics_bp.route("/<int:id>", methods=["GET"])
def get_mechanic(id):
    """
    Get one mechanic
    ---
    tags:
      - Mechanics

    summary: Get a mechanic by ID
    description: Returns a single mechanic using the mechanic's unique ID.

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: The unique ID of the mechanic

    responses:
      200:
        description: Mechanic retrieved successfully
        schema:
          $ref: '#/definitions/MechanicResponse'

      404:
        description: Mechanic not found
    """
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    return mechanic_schema.jsonify(mechanic), 200





# Fourth, PUT Route: Update a mechanic
@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    """
    Update a mechanic
    ---
    tags:
      - Mechanics

    summary: Update a mechanic
    description: Updates one or more fields for an existing mechanic.

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: The unique ID of the mechanic to update

      - name: body
        in: body
        required: true
        schema:
          id: MechanicUpdatePayload
          type: object
          properties:
            name:
              type: string
              example: Updated Mechanic
            email:
              type: string
              example: updatedmechanic@example.com
            phone:
              type: string
              example: 555-888-9999
            salary:
              type: number
              format: float
              example: 72000.00

    responses:
      200:
        description: Mechanic updated successfully
        schema:
          $ref: '#/definitions/MechanicResponse'

      400:
        description: Request body must contain JSON data

      404:
        description: Mechanic not found

      409:
        description: A mechanic with that email already exists
    """
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    # reads the JSON body sent to your Flask route and stores the converted Python data in the 
    # data variable so the rest of your function can use it
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body must contain JSON data."
        }), 400

    mechanic.name = data.get(
        "name",
        mechanic.name,
    )

    mechanic.email = data.get(
        "email",
        mechanic.email,
    )

    mechanic.phone = data.get(
        "phone",
        mechanic.phone,
    )

    mechanic.salary = data.get(
        "salary",
        mechanic.salary,
    )

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "message": "A mechanic with that email already exists."
        }), 409
    
    cache.clear()

    return mechanic_schema.jsonify(mechanic), 200





# Fifth, GET Mechanics by most tickets 
@mechanics_bp.route("/most-tickets", methods=["GET"])
def get_mechanics_by_ticket_count():
    """
    Get mechanics by ticket count
    ---
    tags:
      - Mechanics

    summary: Get mechanics ranked by service ticket count
    description: Returns all mechanics ordered from highest to lowest by the number of service tickets assigned to them.

    responses:
      200:
        description: Mechanics retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Alex Rivera
              email:
                type: string
                example: alex@example.com
              phone:
                type: string
                example: 555-123-4567
              salary:
                type: number
                format: float
                example: 65000.00
              ticket_count:
                type: integer
                example: 3
    """
    mechanics = db.session.execute(
        db.select(
            Mechanic,
            # counts the service tickets associated with each mechanic
            db.func.count(ServiceTicket.id).label("ticket_count")
        )
        # joins mechanics to their tickets
        .outerjoin(Mechanic.service_tickets)
        # groups the rows by mechanic so each mechanic gets one count
        .group_by(Mechanic.id)
        # sorts from highest ticket count to lowest
        .order_by(db.func.count(ServiceTicket.id).desc())
    ).all()

    results = []

    for mechanic, ticket_count in mechanics:
        results.append({
            "id": mechanic.id,
            "name": mechanic.name,
            "email": mechanic.email,
            "phone": mechanic.phone,
            "salary": mechanic.salary,
            "ticket_count": ticket_count
        })

    return jsonify(results), 200





# Sixth, DELETE Route: Delete a mechanic 
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    """
    Delete a mechanic
    ---
    tags:
      - Mechanics

    summary: Delete a mechanic
    description: Deletes a mechanic from the Mechanic Shop API using the mechanic's unique ID.

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: The unique ID of the mechanic to delete

    responses:
      200:
        description: Mechanic deleted successfully

      404:
        description: Mechanic not found
    """
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    db.session.delete(mechanic)
    db.session.commit()
    
    cache.clear()

    return jsonify({
        "message": "Mechanic deleted successfully."
    }), 200