from pprint import pprint

from environs import Env

env = Env()
env.read_env(".env")

KAFKA_HOST = env("KAFKA_HOST", "localhost")
KAFKA_PORT = env("KAFKA_PORT", 9092)
KAFKA_URL = f"{KAFKA_HOST}:{KAFKA_PORT}"

TOPIC = env("TOPIC", "comments")
MESSAGE_DELAY = env.float("MESSAGE_DELAY", 0.5)
pprint(env.__dict__)
