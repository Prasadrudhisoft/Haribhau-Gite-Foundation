from dbutils.pooled_db import PooledDB
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# Create connection pool
pool = PooledDB(
    creator=pymysql,
    maxconnections=20,
    mincached=5, 
    maxcached=10,
    blocking=True,
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database'),
    cursorclass=pymysql.cursors.DictCursor 
)

def get_connection():
    return pool.connection()