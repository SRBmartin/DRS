from app import create_app
from flask import current_app, request, make_response
from alembic.config import Config
from alembic import command
import os
import sys

print('[DEBUG] Starting the application...')

app = create_app()

def run_migrations():
    alembic_ini_path = os.path.join(os.path.dirname(__file__), 'app', 'Infrastructure', 'persistence', 'migrations', 'alembic.ini')
    
    if not os.path.exists(alembic_ini_path):
        print(f"alembic.ini not found at {alembic_ini_path}")
        sys.exit(1)
    
    alembic_cfg = Config(alembic_ini_path)
    
    try:
        command.upgrade(alembic_cfg, "head")
        print("Database migrated successfully.")
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    with app.app_context():
        run_migrations()
    app.run(debug=True)