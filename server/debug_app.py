import traceback

def run_debug():
    try:
        print("Starting debug process...")
        
        print("Importing modules...")
        from app import create_app, db
        print("App and db imported successfully.")
        
        from models import Player, Location, Event
        print("Models imported successfully.")

        print("Creating app...")
        app = create_app()
        print("App created successfully.")

        print("Checking configuration...")
        print("SQLAlchemy Database URI:", app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set'))
        print("Debug mode:", app.config.get('DEBUG', 'Not set'))

        print("Checking models...")
        for model in [Player, Location, Event]:
            print(f"  - {model.__name__}")
        
        print("Attempting to create tables...")
        with app.app_context():
            db.create_all()
        print("Tables created successfully.")
        
        print("Debug process completed without errors.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    run_debug()