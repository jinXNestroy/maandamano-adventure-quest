from app import app, db
from models import Player, Location, Event
import random

def seed_database():
    print("Seeding database...")

    # Clear existing data
    db.drop_all()
    db.create_all()

    # Seed Players
    players = [
        Player(name="Amani", background="Student"),
        Player(name="Juma", background="Activist"),
        Player(name="Zuri", background="Journalist"),
        Player(name="Kibo", background="Teacher")
    ]
    db.session.add_all(players)
    db.session.commit()

    # Seed Locations
    locations = [
        Location(name="Uhuru Park", description="A large recreational park in central Nairobi"),
        Location(name="Kibera", description="One of the largest urban slums in Africa"),
        Location(name="University of Nairobi", description="The largest university in Kenya"),
        Location(name="Kenyatta International Convention Centre", description="An iconic building in Nairobi's skyline"),
        Location(name="Karura Forest", description="An urban forest in Nairobi")
    ]
    db.session.add_all(locations)
    db.session.commit()

    # Seed Events
    events = [
        Event(description="A peaceful protest is forming", location_id=1),
        Event(description="Community leaders are holding a meeting", location_id=2),
        Event(description="Students are organizing a sit-in", location_id=3),
        Event(description="A press conference is being held", location_id=4),
        Event(description="Environmental activists are planting trees", location_id=5)
    ]
    db.session.add_all(events)
    db.session.commit()

    # Assign random locations to players
    for player in players:
        for location in random.sample(locations, k=random.randint(1, len(locations))):
            player.locations.append(location)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()