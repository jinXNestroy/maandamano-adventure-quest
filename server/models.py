from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Association table for many-to-many relationship between Player and Location
player_location = db.Table('player_location',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id'), primary_key=True),
    db.Column('visit_count', db.Integer, default=0)
)

class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    background = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    locations = relationship('Location', secondary=player_location, back_populates='players')
    
    serialize_rules = ('-locations.players',)

class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    players = relationship('Player', secondary=player_location, back_populates='locations')
    events = relationship('Event', back_populates='location')
    
    serialize_rules = ('-players.locations', '-events.location')

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location = relationship('Location', back_populates='events')
    
    serialize_rules = ('-location.events',)