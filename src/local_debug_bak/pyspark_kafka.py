import os
import sys
from app.processor import SparkConsumer


kafka_broker = os.getenv("MYKAFKA")
kafka_topic = "maple-ranking"
consumer = SparkConsumer.SparkConsumer("test_pyspark", loglevel="INFO")
df = consumer.get_messages_from_beginning(kafka_broker, kafka_topic, 20)

