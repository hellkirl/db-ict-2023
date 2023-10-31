import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
USER = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
