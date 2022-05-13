import dataclasses
import json
from unittest import mock
from unittest.mock import patch

from _pytest.fixtures import fixture
from main import MessageFabric, Producer


@fixture
def message_fabric():
    return MessageFabric()


@fixture
def messages_store():
    return []


@fixture
@patch("main.KafkaProducer")
def producer(mock_kafka_producer, messages_store):
    producer = Producer("test", "test_topic")
    producer._producer.send = mock.Mock(
        side_effect=lambda x, y: messages_store.append(json.loads(y))
    )
    return producer


def test_message_generate(message_fabric):
    message = message_fabric.comment_message()
    assert len(message.name) >= 0
    assert len(message.text) >= 0
    assert len(message.address) >= 0


def test_message_send(producer, messages_store):
    message = producer._fabric.comment_message()
    producer._send_message(message)
    assert dataclasses.asdict(message) in messages_store
