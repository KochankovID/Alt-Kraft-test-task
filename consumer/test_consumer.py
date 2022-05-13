import dataclasses
from unittest import mock
from unittest.mock import patch

from _pytest.fixtures import fixture
from main import CommentHandler, Consumer


@fixture
def messages_store():
    return []


@fixture
@patch("main.MongoClient")
def comment_handler(mock_mongo_client, messages_store):
    comment_handler = CommentHandler("test_url")
    comment_handler._db.comments.insert_many = mock.Mock(
        side_effect=lambda x: [messages_store.append(item) for item in list(x)]
    )
    return comment_handler


@fixture
@patch("main.KafkaConsumer")
def consumer(mock_kafka_consumer, comment_handler, test_messages_per_topic):
    consumer = Consumer(mock_kafka_consumer(), {"test": comment_handler})
    consumer._consumer.poll = mock.Mock(return_value=test_messages_per_topic)
    return consumer


@dataclasses.dataclass
class MockRecord:
    value: dict


@dataclasses.dataclass(unsafe_hash=True)
class MockTopic:
    topic: str


@fixture
def test_messages():
    return [
        MockRecord(
            value={"name": "Test name", "text": "Test text", "address": "Test address"}
        ),
        MockRecord(
            value={"name": "Test name", "text": "Test text", "address": "Test address"}
        ),
    ]


@fixture
def test_messages_per_topic():
    return {
        MockTopic("test"): [
            MockRecord(
                value={
                    "name": "Test name",
                    "text": "Test text",
                    "address": "Test address",
                }
            ),
            MockRecord(
                value={
                    "name": "Test name",
                    "text": "Test text",
                    "address": "Test address",
                }
            ),
        ]
    }


def test_comment_handler(comment_handler, messages_store, test_messages):
    comment_handler(test_messages)
    assert messages_store == [message.value for message in test_messages]


def test_consumer(consumer, messages_store, test_messages):
    consumer._read_message()
    assert messages_store == [message.value for message in test_messages]
