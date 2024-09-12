from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

from models import db, Player, Location, Event, GameState
from config import Config

def create_app(config_class=Config):
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    CORS(app)

    # Initialize JWT Manager
    jwt = JWTManager(app)
    
    class SignupResource(Resource):
        def post(self):
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            background = data.get('background')

            # Validate input
            if not name or not email or not password or not background:
                return make_response(jsonify({'message': 'All fields are required'}), 400)

            # Ensure background is one of the four choices
            if background not in ["Veteran Officer", "Rookie Officer", "Community Liaison", "Tactical Expert"]:
                return make_response(jsonify({'message': 'Invalid background. Choose from Veteran Officer, Rookie Officer, Community Liaison, or Tactical Expert'}), 400)

            # Check if email already exists
            if Player.query.filter_by(email=email).first():
                return make_response(jsonify({'message': 'Email is already registered'}), 400)

            # Create new player
            new_player = Player(name=name, email=email, background=background)
            new_player.set_password(password)

            db.session.add(new_player)
            db.session.commit()

            # Generate JWT token
            access_token = create_access_token(identity=new_player.id)

            return make_response(jsonify({'access_token': access_token, 'player': new_player.to_dict()}), 201)

    class LoginResource(Resource):
        def post(self):
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return make_response(jsonify({'message': 'Email and password are required'}), 400)

            player = Player.query.filter_by(email=email).first()
            if not player or not player.check_password(password):
                return make_response(jsonify({'message': 'Invalid credentials'}), 401)

            access_token = create_access_token(identity=player.id)
            return make_response(jsonify({'access_token': access_token, 'player': player.to_dict()}), 200)

    class PlayerResource(Resource):
        @jwt_required()
        def get(self, id=None):
            if id:
                player = Player.query.get_or_404(id)
                return player.to_dict()
            else:
                players = Player.query.all()
                return [player.to_dict() for player in players]

        @jwt_required()
        def patch(self, id):
            player = Player.query.get_or_404(id)
            data = request.json
            for key, value in data.items():
                setattr(player, key, value)
            db.session.commit()
            return player.to_dict()

    class GameStateResource(Resource):
        @jwt_required()
        def get(self, player_id):
            game_state = GameState.query.filter_by(player_id=player_id).first_or_404()
            return game_state.to_dict()

        @jwt_required()
        def post(self, player_id):
            game_state = GameState.query.filter_by(player_id=player_id).first_or_404()
            data = request.json
            action = data.get('action')

            # Handle actions based on the event (you can expand on this)
            if action == "take_immediate_action":
                game_state.resources["personnel"] -= 10
                game_state.score += 10
            elif action == "gather_more_information":
                game_state.resources["equipment"] -= 5
                game_state.score += 5
            elif action == "delegate_to_team":
                game_state.resources["public_support"] += 5
                game_state.score += 15
            elif action == "minimal_intervention":
                game_state.resources["morale"] -= 10
                game_state.score += 20

            game_state.current_day += 1
            db.session.commit()
            
            return game_state.to_dict(), 200

    api.add_resource(SignupResource, '/auth/signup')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(PlayerResource, '/players', '/players/<int:id>')
    api.add_resource(GameStateResource, '/game_state/<int:player_id>')
    
    @app.route('/')
    def home():
        return "Welcome to Maandamano Adventure Quest API!"
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
