import hashlib
from datetime import datetime, timedelta
from pydantic import BaseModel
from event_router.etc.config import get_config

settings = get_config()


def hash_api_key(api_key: str) -> str:
    """Hashes the API key using SHA-256."""
    hashed_key = hashlib.sha256(f"{api_key}{settings.api_key_secret}".encode()).hexdigest()
    return hashed_key


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """Verifies if the provided API key matches the stored hashed key."""
    return hash_api_key(api_key) == hashed_key


def generate_api_key() -> str:
    """Generates a new API key (this can be done using UUID or other methods)."""
    # For simplicity, using current timestamp + random number
    return f"{int(datetime.timestamp(datetime.now()))}{str(datetime.now().microsecond)}"
