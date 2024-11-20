from abc import ABC, abstractmethod

from event_router.etc.logger import Logger
from event_router.service.kafka_service import KafkaService
from typing import Any

logger = Logger(__name__).get_logger()


class AbstractMicroservice(ABC):
    _instance = None

    @classmethod
    def get_instance(cls, topic, group_id):
        """
        Provides a global instance of a Microservice, creating it if it does not exist.
        """
        if cls._instance is None:
            cls._instance = cls(topic, group_id)
        return cls._instance

    def __init__(self, topic, group_id):
        self.topic = topic
        self.group_id = group_id
        self.kafka_service = KafkaService.get_instance()
        self.kafka_service.create_consumer(self.topic, self.group_id, self.handle)
        self.kafka_service.create_producer(self.topic)
        logger.info(f'Kafka service created for {self.topic} - {self.group_id}')

    @abstractmethod
    async def send(self, data):
        """
        Abstract method to send data to a Kafka topic.
        Each microservice will implement its own version.
        """
        pass

    @abstractmethod
    async def handle(self, data: Any):
        """
        Abstract method to handle incoming data.
        Each microservice will implement its own version.
        """
        pass
