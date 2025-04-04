import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWD")
)