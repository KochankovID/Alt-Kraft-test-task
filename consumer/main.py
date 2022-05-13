import json
from pprint import pprint
from typing import Callable, Dict, List

import settings
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from pymongo import MongoClient
from pymongo.database import Database


class Consumer:
    POLL_TIMEOUT = 1000

    def __init__(
        self,
        consumer: KafkaConsumer,
        topic_handlers: Dict[str, Callable[[List[ConsumerRecord]], None]],
    ):
        self._consumer = consumer
        self._topic_handlers = topic_handlers

    def run(self):
        while True:
            self._read_message()

    def _read_message(self):
        record_map = self._consumer.poll(
            timeout_ms=self.POLL_TIMEOUT,
        )
        for tp, records in record_map.items():
            if tp.topic in self._topic_handlers:
                self._topic_handlers[tp.topic](records)


class CommentHandler:
    def __init__(self, mongo_url: str):
        client = MongoClient(mongo_url)
        self._db: Database = client.social_network

    def __call__(self, records: List[ConsumerRecord]):
        self._db.comments.insert_many(record.value for record in records)
        pprint([record.value for record in records])


if __name__ == "__main__":
    print("Start consumer!")

    consumer = Consumer(
        KafkaConsumer(
            settings.TOPIC,
            group_id=settings.CONSUMER_GROUP,
            bootstrap_servers=settings.KAFKA_URL,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        ),
        {settings.TOPIC: CommentHandler(settings.MONGO_URL)},
    )
    consumer.run()
