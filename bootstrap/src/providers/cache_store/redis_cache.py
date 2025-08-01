import redis
import json
import ssl
from src.utils.logs import get_custom_logger
from src.env import REDIS_HOSTNAME, REDIS_PORT, REDIS_PASSWORD

logger = get_custom_logger("redis_cache")

class RedisCacheProvider:
    
    def __init__(self, **kwargs):
        # Set low connect and socket timeouts for faster failure if Redis is slow/unreachable
        _REDIS_HOSTNAME = kwargs.get('REDIS_HOSTNAME', REDIS_HOSTNAME)
        _REDIS_PORT = kwargs.get('REDIS_PORT', REDIS_PORT)
        _REDIS_PASSWORD = kwargs.get('REDIS_PASSWORD', REDIS_PASSWORD)
        _DB = kwargs.get('REDIS_DB', 0)
        logger.info("Initializing Redis cache provider...")
        logger.debug(f"Connecting to {_REDIS_HOSTNAME}:{_REDIS_PORT}")
        if _REDIS_HOSTNAME in ["localhost", "redis"]:
            logger.info("Using local Redis instance")
            ssl_cert = None
            ssl_required = False
        else:
            logger.info("Using AWS ElastiCache Redis instance with SSL")
            ssl_cert = ssl.CERT_REQUIRED
            ssl_required = True
        self.client = redis.Redis(
            host=_REDIS_HOSTNAME,
            port=int(_REDIS_PORT),
            password=_REDIS_PASSWORD,
            db=_DB,
            ssl=ssl_required,
            ssl_cert_reqs=ssl_cert,
            decode_responses=True,
            socket_connect_timeout=20,  # seconds
            socket_timeout=20,          # seconds
        )
        try:
            self.client.ping()
            logger.info("Connected to Redis cache.")
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    def get(self, key: str):
        try:
            value = self.client.get(key)
            if value is not None:
                logger.info(f"Cache hit for key: {key}")
                return value
            else:
                logger.info(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None

    def set(self, key: str, value, ex: int = 3600):
        try:
            self.client.set(key, value, ex=ex)
            logger.info(f"Value set in cache for key: {key}")
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")

    def ingest(self, data: dict, ex: int = 3600):
        """
        Ingests multiple key-value pairs into Redis cache.
        """
        try:
            with self.client.pipeline() as pipe:
                for key, value in data.items():
                    pipe.set(key, value, ex=ex)
                pipe.execute()
            logger.info(f"Ingested {len(data)} items into cache.")
        except Exception as e:
            logger.error(f"Error ingesting data into Redis: {e}")

    def get_json(self, key: str):
        """
        Get a JSON value from Redis and deserialize it.
        """
        try:
            value = self.client.get(key)
            if value is not None:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(value)
            else:
                logger.info(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting JSON key {key} from Redis: {e}")
            return None

    def set_json(self, key: str, value, ex: int = 3600):
        """
        Serialize a value as JSON and store it in Redis.
        """
        try:
            value_to_store = json.dumps(value)
            self.client.set(key, value_to_store, ex=ex)
            logger.info(f"JSON value set in cache for key: {key}")
        except Exception as e:
            logger.error(f"Error setting JSON key {key} in Redis: {e}")

    def ingest_json(self, data: dict, ex: int = 3600):
        """
        Ingest multiple key-value pairs as JSON into Redis cache.
        """
        try:
            with self.client.pipeline() as pipe:
                for key, value in data.items():
                    value_to_store = json.dumps(value)
                    pipe.set(key, value_to_store, ex=ex)
                pipe.execute()
            logger.info(f"Ingested {len(data)} JSON items into cache.")
        except Exception as e:
            logger.error(f"Error ingesting JSON data into Redis: {e}")
    
    def check_queue_size(self, queue_name: str):
        """
        Check the size of a Redis list representing a queue.
        """
        try:
            size = self.client.llen(queue_name)
            logger.info(f"Queue '{queue_name}' size: {size}")
            return size
        except Exception as e:
            logger.error(f"Error checking queue size for '{queue_name}': {e}")
            return None

    def get_client(self):
        return self.client.client()
    
    def get_url(self, mask_password: bool = True) -> str:
        """
        Returns the Redis connection URL.
        If mask_password is True, the password will be replaced with '***'.
        """
        host = self.client.connection_pool.connection_kwargs.get('host', 'localhost')
        port = self.client.connection_pool.connection_kwargs.get('port', 6379)
        db = self.client.connection_pool.connection_kwargs.get('db', 0)
        password = self.client.connection_pool.connection_kwargs.get('password', None)
        scheme = 'rediss' if self.client.connection_pool.connection_kwargs.get('ssl', False) else 'redis'
        if password:
            pw = '***' if mask_password else password
            url = f"{scheme}://:{pw}@{host}:{port}/{db}"
        else:
            url = f"{scheme}://{host}:{port}/{db}"
        return url

cache = RedisCacheProvider()
# Usage example 
# cache = RedisCacheProvider()
# cache.set('foo', {'bar': 1})
# print(cache.get('foo'))
# cache.ingest({'a': {'x': 1}, 'b': [1,2,3]})