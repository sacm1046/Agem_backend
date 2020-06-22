from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime
db = SQLAlchemy()

class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    reservations = db.relationship('Reservation', backref='worker')
    moperations = db.relationship('MOperation', backref='worker')

    def __repr__(self):
        return 'Worker %r' % self.email

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = True)
    price = db.Column(db.Integer, nullable = True)
    duration = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return 'Product %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'duration': self.duration
        }

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.Integer, nullable = False)
    phone = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return 'Client %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer,primary_key = True)
    time = db.Column(db.String(255), nullable = False)
    date = db.Column(db.String(255), nullable = False)
    detail = db.Column(db.PickleType, nullable=False)
    total = db.Column(db.Integer,nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable = False)
    client = db.relationship(Client, backref = backref('children', cascade = 'all, delete'))

    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'))
    
    def __repr__(self):
        return 'Reservation %r' % self.detail

    def serialize(self):
        return{
            'id': self.id,
            'time': self.time,
            'date': self.date,
            'detail': self.detail,
            'total': self.total,
            'client': self.client.serialize(),
            'worker': self.worker.serialize()
        }

class ROperation(db.Model):
    __tablename__ = 'roperations'
    id = db.Column(db.Integer,primary_key = True)
    detail = db.Column(db.PickleType, nullable=False)
    total = db.Column(db.Integer,nullable=False)

    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable = False)
    reservation = db.relationship(Reservation, backref = backref('children', cascade = 'all, delete'))

    def __repr__(self):
        return 'Operation %r' % self.detail

    def serialize(self):
        return{
            'id': self.id,
            'detail': self.detail,
            'total': self.total,
            'reservation': self.reservation.serialize()
        }

class MOperation(db.Model):
    __tablename__ = 'moperations'
    id = db.Column(db.Integer,primary_key = True)
    detail = db.Column(db.PickleType, nullable=False)
    time = db.Column(db.String(255), nullable = False)
    date = db.Column(db.String(255), nullable = False)
    total = db.Column(db.Integer,nullable=False)

    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'))

    def __repr__(self):
        return 'Operation %r' % self.detail

    def serialize(self):
        return{
            'id': self.id,
            'detail': self.detail,
            'time': self.time,
            'date': self.date,
            'total': self.total,
            'worker': self.worker.serialize()
        }
