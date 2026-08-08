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
    # Finds the service ticket 
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({
            "message": "Service ticket not found"
        }), 404

    # gets the JSON body sent by Postman 
    data = request.get_json()

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