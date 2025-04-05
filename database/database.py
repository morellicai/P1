import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connectar():
    conn = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("USERNAME"),
        password = os.getenv("PASSWD")
    )
    return conn