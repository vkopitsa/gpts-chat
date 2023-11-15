import redis

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)
