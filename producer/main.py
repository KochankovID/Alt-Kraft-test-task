import dataclasses
import json
import random
import time
from pprint import pprint

import settings
from faker import Faker
from kafka import KafkaProducer


@dataclasses.dataclass
class Message:
    name: str
    text: str
    address: str


class MessageFabric:
    def __init__(self):
        self._fake = Faker()

    def comment_message(self) -> Message:
        return Message(self._fake.name(), self._fake.text(), self._fake.address())


class Producer:
    def __init__(self, kafka_url: str, topic: str):
        self._topic = topic
        self._fabric = MessageFabric()
        self._producer = KafkaProducer(bootstrap_servers=kafka_url)

    def run(self):
        while True:
            message = self._fabric.comment_message()
            self._send_message(message)
            pprint(message)
            time.sleep(settings.MESSAGE_DELAY * random.random())

    def _send_message(self, message: Message):
        self._producer.send(
            self._topic,
            json.dumps(dataclasses.asdict(message)).encode(),
        )


if __name__ == "__main__":
    print("Start producer!")
    producer = Producer(settings.KAFKA_URL, settings.TOPIC)
    producer.run()
