from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os

from models import db, Player, Location, Event
from config import Config

def create_app(config_class=Config):
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    CORS(app)
    
    class PlayerResource(Resource):
        def get(self, id=None):
            if id:
                player = Player.query.get_or_404(id)
                return player.to_dict()
            else:
                players = Player.query.all()
                return [player.to_dict() for player in players]
        
        def post(self):
            data = request.json
            new_player = Player(name=data['name'], background=data['background'])
            db.session.add(new_player)
            db.session.commit()
            return new_player.to_dict(), 201
        
        def patch(self, id):
            player = Player.query.get_or_404(id)
            data = request.json
            for key, value in data.items():
                setattr(player, key, value)
            db.session.commit()
            return player.to_dict()
        
        def delete(self, id):
            player = Player.query.get_or_404(id)
            db.session.delete(player)
            db.session.commit()
            return '', 204

    class LocationResource(Resource):
        def get(self):
            locations = Location.query.all()
            return [location.to_dict() for location in locations]
        
        def post(self):
            data = request.json
            new_location = Location(name=data['name'], description=data['description'])
            db.session.add(new_location)
            db.session.commit()
            return new_location.to_dict(), 201

    class EventResource(Resource):
        def get(self):
            events = Event.query.all()
            return [event.to_dict() for event in events]
        
        def post(self):
            data = request.json
            new_event = Event(description=data['description'], location_id=data['location_id'])
            db.session.add(new_event)
            db.session.commit()
            return new_event.to_dict(), 201
    
    api.add_resource(PlayerResource, '/players', '/players/<int:id>')
    api.add_resource(LocationResource, '/locations')
    api.add_resource(EventResource, '/events')
    
    @app.route('/')
    def home():
        return "Welcome to Maandamano Adventure Quest API!"
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()