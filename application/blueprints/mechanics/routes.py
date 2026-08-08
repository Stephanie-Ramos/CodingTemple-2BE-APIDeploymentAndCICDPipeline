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


# POST Route: Create a mechanic
@mechanics_bp.route("/", methods=["POST"])
# Caching this GET route reduces repeated database queries when the
# mechanics list is requested frequently but has not recently changed
@cache.cached(timeout=60)
def create_mechanic():
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

    return mechanic_schema.jsonify(mechanic), 201


# GET Route: Retrieve all mechanics 
@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    mechanics = db.session.execute(
        db.select(Mechanic)
    ).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200


# GET Route: Retrieve one mechanic
@mechanics_bp.route("/<int:id>", methods=["GET"])
def get_mechanic(id):
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    return mechanic_schema.jsonify(mechanic), 200


# POST Route: Update a mechanic
@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
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

    return mechanic_schema.jsonify(mechanic), 200


# GET Mechanics by most tickets 
@mechanics_bp.route("/most-tickets", methods=["GET"])
def get_mechanics_by_ticket_count():
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


# DELETE Route: Delete a mechanic 
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({
            "message": "Mechanic not found."
        }), 404

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({
        "message": "Mechanic deleted successfully."
    }), 200