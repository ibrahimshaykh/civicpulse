from redis.asyncio import Redis

from app.core.config import Settings


def build_redis_client(s: Settings) -> Redis:
    return Redis(
        host=s.redis_host,
        port=s.redis_port,
        password=s.redis_password.get_secret_value(),
        db=s.redis_db,
        decode_responses=True,
        socket_connect_timeout=5,
    )
