from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128), nullable=False)  
    background = db.Column(db.String(50), nullable=False)  
    game_states = relationship('GameState', back_populates='player')
    locations = relationship('Location', secondary=player_location, back_populates='players')

    serialize_rules = ('-password_hash', '-game_states', '-locations.players')

    # Hash the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password correctness
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'background': self.background,
            'locations': [location.to_dict() for location in self.locations]
        }

    # Additional properties based on background
    @property
    def strengths(self):
        if self.background == "Veteran Officer":
            return ["Experienced", "High morale boost", "Better negotiation"]
        elif self.background == "Rookie Officer":
            return ["High energy", "Quick to respond", "Innovative thinking"]
        elif self.background == "Community Liaison":
            return ["High trust from citizens", "Good communication skills"]
        elif self.background == "Tactical Expert":
            return ["Strategic thinking", "Excellent crisis management"]

    @property
    def weaknesses(self):
        if self.background == "Veteran Officer":
            return ["Old-fashioned thinking", "Slower physical abilities"]
        elif self.background == "Rookie Officer":
            return ["Lack of experience", "Lower trust from senior officers"]
        elif self.background == "Community Liaison":
            return ["Limited combat training", "Viewed as too lenient"]
        elif self.background == "Tactical Expert":
            return ["Poor interpersonal skills", "Sometimes too aggressive"]

class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    players = relationship('Player', secondary=player_location, back_populates='locations')
    events = relationship('Event', back_populates='location')
    
    serialize_rules = ('-players.locations', '-events.location')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location = relationship('Location', back_populates='events')
    
    serialize_rules = ('-location.events',)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'location': self.location.to_dict()
        }

# New GameState model to track game progress
class GameState(db.Model, SerializerMixin):
    __tablename__ = 'game_states'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    current_day = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer, default=0)
    resources = db.Column(db.JSON, default={"personnel": 100, "equipment": 100, "public_support": 100, "morale": 100})
    player = relationship('Player', back_populates='game_states')

    def to_dict(self):
        return {
            'id': self.id,
            'current_day': self.current_day,
            'score': self.score,
            'resources': self.resources,
            'player': self.player.to_dict()
        }
