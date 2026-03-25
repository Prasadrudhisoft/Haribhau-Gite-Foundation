import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.environ.get('host'),
        user=os.environ.get('user'),
        password=os.environ.get('password'),
        database=os.environ.get('database')
    )