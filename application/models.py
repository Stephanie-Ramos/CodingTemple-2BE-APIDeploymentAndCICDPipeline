# Imports Python’s date type
from datetime import date
# Imports the List type hint.
from typing import List

# Imports four SQLAlchemy tools
from sqlalchemy import ForeignKey, String, Table, Column
# Imports tools used to define modern SQLAlchemy models
# mapped_column: Creates a database column inside a model 
# relationship: Defines how model objects are connected
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Imports the SQLAlchemy extension object to access SQLAlchemy metadata
from application.extensions import db


# Junction Table
service_mechanics = Table(
    'service_mechanics',
    # Associates the table with your SQLAlchemy database metadata.
    db.metadata,
    # primary_key=True: Makes service_ticket_id part of the association table’s combined primary key
    Column('service_ticket_id', ForeignKey('service_tickets.id'), primary_key=True),
    # Creates a column
    # ForeignKey("mechanics.id"): Connects mechanic_id to the id column in the mechanics table.
    Column('mechanic_id', ForeignKey('mechanics.id'), primary_key=True)
)

# Junction Table
service_inventory = Table(
    "service_inventory",
    db.metadata,
    Column("service_ticket_id", ForeignKey("service_tickets.id"),primary_key=True),
    Column("inventory_id", ForeignKey("inventory.id"), primary_key=True)
)

# Creates a SQLAlchemy model named Customer
# it inherits from db.Model, SQLAlchemy recognizes it as a database model
class Customer(db.Model):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Creates the relationship between a customer and their service tickets: one to many relationship
    # cascade="all, delete-orphan": deleting a customer may also delete their service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer', cascade="all, delete-orphan") 
    

class ServiceTicket(db.Model):
    # Sets its MySQL table name 
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    # A VIN can contain both letters and numbers and is normally 17 characters long
    vin: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(nullable=False) 
    service_description: Mapped[str] = mapped_column(String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    
    # Creates the Python-side relationship to the associated customer
    customer: Mapped['Customer'] = relationship(back_populates='service_tickets') 
    # Creates the list of mechanics assigned to this service ticket
    mechanics: Mapped[List['Mechanic']] = relationship(secondary=service_mechanics, back_populates='service_tickets')
    parts: Mapped[List["Inventory"]] = relationship(secondary=service_inventory, back_populates="service_tickets")
    

class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)
    
    # One customer can have many tickets, but each ticket belongs to one customer 
    service_tickets: Mapped[List['ServiceTicket']] = relationship(secondary=service_mechanics, back_populates='mechanics')
    
    
class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    service_tickets: Mapped[List["ServiceTicket"]] = relationship(secondary=service_inventory,back_populates="parts")



# This file defines the database structure and relationships for your Mechanic Shop API using SQLAlchemy. It tells 
# Flask-SQLAlchemy what tables should exist in your MySQL database, what information each table stores, and how 
# the tables relate to one another.