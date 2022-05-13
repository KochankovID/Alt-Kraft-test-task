from environs import Env

env = Env()
env.read_env(".env")

KAFKA_HOST = env("KAFKA_HOST", "localhost")
KAFKA_PORT = env("KAFKA_PORT", 9092)
KAFKA_URL = f"{KAFKA_HOST}:{KAFKA_PORT}"

MONGO_HOST = env("MONGO_HOST", "localhost")
MONGO_PORT = env("MONGO_PORT", "27017")
MONGO_USER = env("MONGO_USER", "root")
MONGO_PASSWORD = env("MONGO_PASSWORD", "example")
MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

TOPIC = env("TOPIC", "comments")
CONSUMER_GROUP = env("CONSUMER_GROUP", "group 1")

print(env.__dict__)
