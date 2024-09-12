from app import app, db
from models import Player, Location, Event, GameState
import random

def seed_database():
    print("Seeding database...")

    # Clear existing data
    db.drop_all()
    db.create_all()

    # Seed Players
    players = [
        Player(name="Amani", email="amani@example.com", background="Veteran Officer"),
        Player(name="Juma", email="juma@example.com", background="Rookie Officer"),
        Player(name="Zuri", email="zuri@example.com", background="Community Liaison"),
        Player(name="Kibo", email="kibo@example.com", background="Tactical Expert")
    ]
    
    # Set passwords for players
    for player in players:
        player.set_password("password123")  # Set a default password for all players

    db.session.add_all(players)
    db.session.commit()

    # Seed Locations
    locations = [
        Location(name="Uhuru Park", description="A large recreational park in central Nairobi"),
        Location(name="Kibera", description="One of the largest urban slums in Africa"),
        Location(name="University of Nairobi", description="The largest university in Kenya"),
        Location(name="Kenyatta International Convention Centre", description="An iconic building in Nairobi's skyline"),
        Location(name="Gikomba Market", description="A busy market district known for second-hand clothes and demonstrations"),
        Location(name="Eastleigh", description="A bustling part of Nairobi where demonstrations often occur")
    ]
    db.session.add_all(locations)
    db.session.commit()

    # Seed Events
    events = [
        Event(description="A large protest is forming at Uhuru Park to demand better living conditions", location_id=1),
        Event(description="Demonstrators are gathering in Kibera to protest rising food prices", location_id=2),
        Event(description="Students are marching from the University of Nairobi, protesting education budget cuts", location_id=3),
        Event(description="Protesters have gathered at the Kenyatta International Convention Centre to speak against government corruption", location_id=4),
        Event(description="A demonstration is occurring in Gikomba Market, focusing on traders' rights and market conditions", location_id=5),
        Event(description="Demonstrators in Eastleigh are protesting police brutality and demanding justice", location_id=6)
    ]
    db.session.add_all(events)
    db.session.commit()

    # Seed GameState for each player
    for player in players:
        new_game_state = GameState(
            player_id=player.id,
            resources={
                "personnel": random.randint(80, 100),
                "equipment": random.randint(80, 100),
                "morale": random.randint(80, 100),
                "public_support": random.randint(80, 100)
            },
            score=0,
            current_day=1
        )
        db.session.add(new_game_state)

    db.session.commit()

    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
