import asyncio
from threading import Thread
from event_router.etc.logger import Logger
from event_router.utils.json_utils import serialize_json, deserialize_json
from event_router.etc.config import get_config
import sys

if sys.version_info >= (3, 12, 0):
    import six

    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.errors import NoBrokersAvailable, KafkaError, TopicAlreadyExistsError
from kafka.admin import NewTopic

logger = Logger(__name__).get_logger()
settings = get_config()


class KafkaService:
    _instance = None

    def __init__(self, broker=f"{settings.kafka_url}:{settings.kafka_port}",):
        self.broker = broker
        self.admin_client = KafkaAdminClient(bootstrap_servers=broker)
        self.producers = {}
        self.consumers = {}

        # Check broker connectivity
        if not self._check_connection():
            raise ConnectionError(f"Could not connect to Kafka broker at {broker}")

    @classmethod
    def get_instance(cls, broker=f"{settings.kafka_url}:{settings.kafka_port}"):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init__(broker)
        return cls._instance

    def _check_connection(self):
        try:
            KafkaConsumer(bootstrap_servers=self.broker).close()
            return True
        except NoBrokersAvailable as e:
            logger.error("Kafka broker connection failed: %s", e)
            return False

    def topic_exists(self, topic):
        """
        Checks if the given topic exists in Kafka.
        :param topic: The topic to check.
        :return: True if the topic exists, False otherwise.
        """
        try:
            existing_topics = self.admin_client.list_topics()
            return topic in existing_topics
        except KafkaError as e:
            logger.error(f"Error checking topic existence: {e}")
            return False

    def create_topic(self, topic, num_partitions=1, replication_factor=1):
        """
        Creates a new topic in Kafka if it does not already exist.
        :param topic: The topic to create.
        :param num_partitions: The number of partitions for the topic.
        :param replication_factor: The replication factor for the topic.
        """
        if not self.topic_exists(topic):
            try:
                new_topic = NewTopic(name=topic, num_partitions=num_partitions, replication_factor=replication_factor)
                self.admin_client.create_topics([new_topic])
                logger.info(f"Topic '{topic}' created successfully.")
            except TopicAlreadyExistsError:
                logger.info(f"Topic '{topic}' already exists.")
            except KafkaError as e:
                logger.error(f"Error creating topic '{topic}': {e}")
        else:
            logger.info(f"Topic '{topic}' already exists.")

    def create_producer(self, topic):
        """
        Creates a Kafka producer for the specified topic if one does not already exist,
        and ensures the topic exists before creation.

        :param topic: The Kafka topic for which the producer is created.
        :return: A KafkaProducer instance associated with the specified topic.
        """
        if not self.topic_exists(topic):
            self.create_topic(topic)

        if topic not in self.producers:
            producer = KafkaProducer(
                client_id=f"{topic}_producer",
                bootstrap_servers=self.broker,
                value_serializer=serialize_json,
            )
            self.producers[topic] = producer
        return self.producers[topic]

    def create_consumer(self, topic, group_id, on_message):
        if topic not in self.consumers:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.broker,
                group_id=group_id,
                value_deserializer=deserialize_json,
                enable_auto_commit=False,
                session_timeout_ms=60000
            )
            self.consumers[topic] = consumer

            # Start a thread to handle message consumption
            thread = Thread(target=self._run_consumer, args=(consumer, on_message))
            thread.start()

    def _run_consumer(self, consumer, on_message):
        async def consume_messages():
            try:
                for message in consumer:
                    await on_message(message.value)
                    logger.info(
                        f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")
            except KafkaError as e:
                logger.error("Error consuming messages: %s", e)

        asyncio.run(consume_messages())

    async def send_message(self, topic, message):
        producer = self.create_producer(topic)
        future = producer.send(topic, message)

        try:
            result = future.get(timeout=10)
            logger.info(f"Message sent to {topic}: {result}")
        except KafkaError as e:
            logger.error("Failed to send message: %s", e)

    def close(self):
        for producer in self.producers.values():
            producer.close()
        for consumer in self.consumers.values():
            consumer.close()
        self.admin_client.close()
        KafkaService._instance = None
