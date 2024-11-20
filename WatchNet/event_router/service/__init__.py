from .service_handler import MicroserviceHandler
from ..etc.logger import Logger

__all__ = ['microservice_handler']
logger = Logger(__name__).get_logger()

# Initialize Kafka service and register microservices
try:
    microservice_handler = MicroserviceHandler()
    logger.info('Microservice handler initialized')
except Exception as e:
    logger.error(e)
    raise e
