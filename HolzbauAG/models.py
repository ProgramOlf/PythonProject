from flask_sqlalchemy import SQLAlchemy
from __init__ import db


# Define the Customer model
class Customer(db.Model):
    __tablename__ = 'customer_data'
    Customer_ID = db.Column(db.Integer, primary_key=True)
    Customer_First_Name = db.Column(db.String(50), nullable=False)
    Customer_Last_Name = db.Column(db.String(50), nullable=False)
    Last_name = db.Column(db.String(50), nullable=False)
    Age = db.Column(db.Integer)
    Country = db.Column(db.String(50))

    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.id}>'

# Define the Order model
class Order(db.Model):
    __tablename__ = 'order_data'
    Order_ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('customer_data.Customer_ID'), nullable=False)
    Price = db.Column(db.Float)
    Chair = db.Column(db.Integer)
    Stool = db.Column(db.Integer)
    Table = db.Column(db.Integer)
    Cabinet = db.Column(db.Integer)
    Dresser = db.Column(db.Integer)
    Couch = db.Column(db.Integer)
    Bed = db.Column(db.Integer)
    Shelf = db.Column(db.Integer)

    def __repr__(self):
        return f'<Order {self.id}>'