from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from event_router.controller.v1 import v1_router
from .etc.logger import Logger
from event_router.service.kafka_service import KafkaService
from event_router.etc.config import get_config
from event_router.etc.multicast import listen_for_multicast
from .service.user_service import authenticate_user

import os
import asyncio

app = FastAPI()

# Include routers
app.include_router(v1_router, prefix="/api")
logger = Logger(__name__).get_logger()
settings = get_config()
security = HTTPBearer()


@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting up...")
        await asyncio.create_task(listen_for_multicast())
    except Exception as e:
        logger.error(e)


@app.on_event("shutdown")
async def shutdown_event():
    try:
        KafkaService.get_instance().close()
    except Exception as e:
        logger.error(f"Failed to close kafka service \ntrace: {e}")
    logger.info("Shutting down...")


@app.get("/")
def read_root(credentials: HTTPBasicCredentials = Depends(security)):
    """Root endpoint that returns all configuration parameters."""
    api_key = credentials.credentials

    if not authenticate_user(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    config_params = {
        "debug": settings.debug,
        "profile": settings.profile,
        "kafka_url": settings.kafka_url,
        "kafka_port": settings.kafka_port,
        "api_key_secret": settings.api_key_secret,
        "database_url": settings.database_url,
        "environment_variables": dict(os.environ)  # Include all environment variables
    }

    return config_params
