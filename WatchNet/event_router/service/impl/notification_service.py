from event_router.etc.logger import Logger
from event_router.service.abstract_service import AbstractMicroservice
logger = Logger(__name__).get_logger()


class NotificationService(AbstractMicroservice):
    async def send(self, data):
        await self.kafka_service.send_message(self.topic, data)

    async def handle(self, data):
        logger.info(data)
