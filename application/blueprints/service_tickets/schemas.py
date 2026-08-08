from application.extensions import ma
from application.models import ServiceTicket

from application.blueprints.mechanics.schemas import MechanicSchema
from application.blueprints.inventory.schemas import InventorySchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

    mechanics = ma.Nested(
        "MechanicSchema",
        many=True,
        # mechanics should be assigned through the assign-mechanic route rather 
        # than passed directly when creating a ticket
        dump_only=True,
    )
    
    parts = ma.Nested(
        "InventorySchema",
        many=True,
        dump_only=True,
    )


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)