import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

conn = psycopg2.connect(db_url)
print("Opened database successfully")


async def get_data(db):
    """
    Same as db.fetchone()
    """
    for row in db:
        return row[0]


cur = conn.cursor()
