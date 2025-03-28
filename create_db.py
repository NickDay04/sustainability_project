import mysql.connector
import os
import time
from dotenv import load_dotenv

load_dotenv()

print("[INFO] Establishing database connection")
while True:
    try:
        my_db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            passwd=os.getenv("MYSQL_PASSWORD")
        )
        break
    except:
        print("[INFO] Database not ready for connection yet. If this error persists, check MySQL setup.")
        time.sleep(5)

cursor = my_db.cursor()

print("[INFO] Creating dev database")
cursor.execute("CREATE DATABASE dev")

print("[INFO] Populating database")
from app import app
from models import init_db
init_db()