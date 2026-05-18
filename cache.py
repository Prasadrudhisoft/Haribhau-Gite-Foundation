import redis
import json
from dotenv import load_dotenv
import os

load_dotenv()

redis_client = None
def init_cache():
    global redis_client

    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    redis_client = redis.from_url(
        f"redis://{host}:{port}",
        encoding = "utf-8",
        decode_responses = True
    )

    print("Redis Server Connected")

def get_cache(key: str):
    try:
        value = redis_client.get(key)

        if value is None:
            return None
        
        return json.loads(value)
    except Exception as e:
        print("Get Cache Error")
        return None

def set_cache(key:str, value, ttl: int = 300):
    try:
        json_value = json.dumps(value, default=str)
        redis_client.setex(key, ttl,json_value)
    except Exception as e:
        print("Set Cache Error")
        return None

def delete_cache(*keys):
    try:
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print("delete cache error")
        return None