import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
USER = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
MNG_HOST = os.getenv("MNG_HOST")
MNG_PORT = os.getenv("MNG_PORT")
