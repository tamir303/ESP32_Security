import logging
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from logging import StreamHandler


class ELKHandler(logging.Handler):
    def __init__(self, es_host='localhost', es_port=9200, index="logs"):
        super().__init__()
        self.es = Elasticsearch([{'host': es_host, 'port': es_port}])
        self.index = index

    def emit(self, record):
        log_entry = self.format(record)
        doc = {
            "@timestamp": datetime.utcnow().isoformat(),
            "log": log_entry,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        try:
            self.es.index(index=self.index, body=doc)
        except Exception as e:
            print(f"Failed to send log to ELK: {e}")


class Logger:
    def __init__(self, name, debug_env_var="DEBUG"):
        # Create a base logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Check DEBUG environment variable
        debug_mode = os.getenv(debug_env_var, "True").lower() in ["true", "1"]

        # Console handler (for all cases)
        console_handler = StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if not debug_mode:
            # Add ELK handler when not in debug mode
            elk_handler = ELKHandler(es_host='localhost', es_port=9200, index="my_log_index")
            elk_handler.setLevel(logging.INFO)  # Only log INFO and above to ELK
            elk_handler.setFormatter(formatter)
            self.logger.addHandler(elk_handler)

    def get_logger(self):
        return self.logger


# Usage example
# logger = Logger(__name__).get_logger()
# logger.info("This is an informational log message.")
# logger.error("This is an error message.")
