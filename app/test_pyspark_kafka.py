import sys
from proceesor import Consumer

if __name__ != "__main__":
    print("This is a main py, not a module")
    sys.exit(1)

kafka_broker = "mykafka1:19094"
kafka_topic = "test-nickname-2"
consumer = Consumer.SparkConsumer("test_pyspark", loglevel="INFO")
consumer.get_topic_all(kafka_broker, kafka_topic)

