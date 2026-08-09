from flask import jsonify, request
from marshmallow import ValidationError

from application.blueprints.service_tickets import service_tickets_bp
from application.blueprints.service_tickets.schemas import (
    service_ticket_schema,
    service_tickets_schema,
)
from application.extensions import db
from application.models import (
    Customer,
    Mechanic,
    ServiceTicket,
    Inventory,
)





# POST create service ticket
@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    """
    Create a service ticket
    ---
    tags:
      - Service Tickets

    summary: Create a service ticket
    description: Creates a new service ticket for an existing customer.

    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ServiceTicketPayload
          type: object
          required:
            - vin
            - service_date
            - service_description
            - customer_id
          properties:
            vin:
              type: string
              example: 1HGCM82633A123456
            service_date:
              type: string
              format: date
              example: "2026-08-08"
            service_description:
              type: string
              example: Oil change and tire rotation
            customer_id:
              type: integer
              example: 1

    responses:
      201:
        description: Service ticket successfully created
        schema:
          id: ServiceTicketResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            vin:
              type: string
              example: 1HGCM82633A123456
            service_date:
              type: string
              format: date
              example: "2026-08-08"
            service_description:
              type: string
              example: Oil change and tire rotation
            customer_id:
              type: integer
              example: 1

      400:
        description: Invalid service ticket data or missing customer ID

      404:
        description: Customer not found
    """
    # looks inside python dictionary for the "customer_id" key and retrieves its value
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body must contain JSON data."
        }), 400

    # Get the customer ID
    customer_id = data.get("customer_id")

    if not customer_id:
        return jsonify({
            "message": "customer_id is required."
        }), 400

    # Find the customer
    customer = db.session.get(
        Customer,
        customer_id,
    )

    if not customer:
        return jsonify({
            "message": "Customer not found."
        }), 404

    try:
        service_ticket = service_ticket_schema.load(
            data,
            session=db.session,
        )
    except ValidationError as error:
        return jsonify(error.messages), 400

    db.session.add(service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(
        service_ticket
    ), 201





# GET all service tickets
@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    """
    Get all service tickets
    ---
    tags:
      - Service Tickets

    summary: Get all service tickets
    description: Returns a list of all service tickets in the Mechanic Shop API.

    responses:
      200:
        description: Service tickets retrieved successfully
        schema:
          type: array
          items:
            $ref: '#/definitions/ServiceTicketResponse'
    """
    service_tickets = db.session.execute(
        db.select(ServiceTicket)
    ).scalars().all()

    return service_tickets_schema.jsonify(
        service_tickets
    ), 200





# GET service ticket by ID
@service_tickets_bp.route(
    "/<int:ticket_id>",
    methods=["GET"],
)
def get_service_ticket(ticket_id):
    """
    Get a service ticket by ID
    ---
    tags:
      - Service Tickets

    summary: Get a service ticket by ID
    description: Returns a single service ticket using its unique ticket ID.

    parameters:
      - name: ticket_id
        in: path
        required: true
        type: integer
        description: The unique ID of the service ticket

    responses:
      200:
        description: Service ticket retrieved successfully
        schema:
          $ref: '#/definitions/ServiceTicketResponse'

      404:
        description: Service ticket not found
    """
    service_ticket = db.session.get(
        ServiceTicket,
        ticket_id,
    )

    if not service_ticket:
        return jsonify({
            "message": "Service ticket not found."
        }), 404

    return service_ticket_schema.jsonify(
        service_ticket
    ), 200





# PUT assign mechanic to ticket id 
@service_tickets_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>",
    methods=["PUT"],
)
def assign_mechanic(ticket_id, mechanic_id):
    """
    Assign a mechanic to a service ticket
    ---
    tags:
      - Service Tickets

    summary: Assign a mechanic to a service ticket
    description: Assigns an existing mechanic to an existing service ticket.

    parameters:
      - name: ticket_id
        in: path
        required: true
        type: integer
        description: The ID of the service ticket

      - name: mechanic_id
        in: path
        required: true
        type: integer
        description: The ID of the mechanic to assign

    responses:
      200:
        description: Mechanic assigned successfully
        schema:
          $ref: '#/definitions/ServiceTicketResponse'

      404:
        description: Service ticket or mechanic not found

      409:
        description: Mechanic is already assigned to this service ticket
    """
    service_ticket = db.session.get(
        ServiceTicket,
        ticket_id,
    )

    if not service_ticket:
        return jsonify({
            "message": "Service ticket not found."
        }), 404

    # Find the mechanic
    mechanic = db.session.get(
        Mechanic,
        mechanic_id,
    )

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    if mechanic in service_ticket.mechanics:
        return jsonify({
            "message": "Mechanic is already assigned to this service ticket."
        }), 409

    service_ticket.mechanics.append(mechanic)

    db.session.commit()

    return service_ticket_schema.jsonify(
        service_ticket
    ), 200





#  PUT Edit mechanic in service tickets 
@service_tickets_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_ticket_mechanics(ticket_id):
    """
    Edit mechanics assigned to a service ticket
    ---
    tags:
      - Service Tickets

    summary: Edit mechanics on a service ticket
    description: Adds and removes mechanics assigned to an existing service ticket.

    parameters:
      - name: ticket_id
        in: path
        required: true
        type: integer
        description: The ID of the service ticket

      - name: body
        in: body
        required: true
        schema:
          id: EditTicketMechanicsPayload
          type: object
          properties:
            add_ids:
              type: array
              items:
                type: integer
              example:
                - 1
                - 2
            remove_ids:
              type: array
              items:
                type: integer
              example:
                - 3

    responses:
      200:
        description: Service ticket mechanics updated successfully
        schema:
          $ref: '#/definitions/ServiceTicketResponse'

      404:
        description: Service ticket or mechanic not found
    """
    # Finds the service ticket 
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({
            "message": "Service ticket not found"
        }), 404

    # gets the JSON body sent by Postman 
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Request body must contain JSON data."
        }), 400

    # extract the two mechanic ID lists 
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    # Add - goes through every mechanic you want to add
    for mechanic_id in add_ids:
        # looks up the mechanic
        mechanic = db.session.get(Mechanic, mechanic_id)
        
        if not mechanic:
            return jsonify({
                "message": f"Mechanic {mechanic_id} not found"
            }), 404
            
        if mechanic not in ticket.mechanics:
            # updates the many-to-many relationship 
            ticket.mechanics.append(mechanic)

    # Remove - goes through every mechanic you want to remove
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        
        if not mechanic:
            return jsonify({
                "message": f"Mechanic {mechanic_id} not found"
            }), 404

        if mechanic in ticket.mechanics:
            # updates the many-to-many relationship 
            ticket.mechanics.remove(mechanic)


    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200





# PUT remove mechanic from ticket id 
@service_tickets_bp.route(
    "/<int:ticket_id>/remove-mechanic/<int:mechanic_id>",
    methods=["PUT"],
)
def remove_mechanic(ticket_id, mechanic_id):
    """
    Remove a mechanic to a service ticket
    ---
    tags:
      - Service Tickets

    summary: Assign a mechanic to a service ticket
    description: Assigns an existing mechanic to an existing service ticket.

    parameters:
      - name: ticket_id
        in: path
        required: true
        type: integer
        description: The ID of the service ticket

      - name: mechanic_id
        in: path
        required: true
        type: integer
        description: The ID of the mechanic to assign

    responses:
      200:
        description: Mechanic assigned successfully
        schema:
          $ref: '#/definitions/ServiceTicketResponse'

      404:
        description: Service ticket or mechanic not found

      409:
        description: Mechanic is already assigned to this service ticket
    """
    service_ticket = db.session.get(
        ServiceTicket,
        ticket_id,
    )

    if not service_ticket:
        return jsonify({
            "message": "Service ticket not found."
        }), 404

    mechanic = db.session.get(
        Mechanic,
        mechanic_id,
    )

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    if mechanic not in service_ticket.mechanics:
        return jsonify({
            "message": "Mechanic is not assigned to this service ticket."
        }), 404

    service_ticket.mechanics.remove(mechanic)

    db.session.commit()

    return service_ticket_schema.jsonify(
        service_ticket
    ), 200





# PUT Add Part to Service Ticket
@service_tickets_bp.route(
    "/<int:ticket_id>/add-part/<int:inventory_id>",
    methods=["PUT"]
)
def add_part_to_ticket(ticket_id, inventory_id):
    """
    Add an inventory part to a service ticket
    ---
    tags:
      - Service Tickets

    summary: Add a part to a service ticket
    description: Assigns an existing inventory part to an existing service ticket.

    parameters:
      - name: ticket_id
        in: path
        required: true
        type: integer
        description: The ID of the service ticket

      - name: inventory_id
        in: path
        required: true
        type: integer
        description: The ID of the inventory part to add

    responses:
      200:
        description: Inventory part added successfully
        schema:
          $ref: '#/definitions/ServiceTicketResponse'

      400:
        description: Part is already assigned to this service ticket

      404:
        description: Service ticket or inventory part not found
    """
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({
            "message": "Service ticket not found"
        }), 404

    part = db.session.get(Inventory, inventory_id)

    if not part:
        return jsonify({
            "message": "Inventory part not found"
        }), 404

    if part in ticket.parts:
        return jsonify({
            "message": "Part is already assigned to this service ticket"
        }), 400

    ticket.parts.append(part)

    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200