import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, text

load_dotenv()

db_url = os.environ.get('DATABASE_URL')
print(f"Testing connection with URL: {db_url}")

try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Success! Connection established.")
except Exception as e:
    print(f"Failed to connect: {e}")

# Try with 127.0.0.1 if localhost failed
new_url = db_url.replace('@localhost/', '@127.0.0.1/')
print(f"\nTesting alternative connection with URL: {new_url}")

try:
    engine = create_engine(new_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Success! Connection established via 127.0.0.1.")
except Exception as e:
    print(f"Failed to connect: {e}")
