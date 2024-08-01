import json

from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging


logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
KAFKA_BROKER_1 = "13.209.12.0:19094"
producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER_1])
future = producer.send('my-topic', b'hello2')

# produce json messages
producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER_1], value_serializer=lambda m: json.dumps(m).encode('ascii'))
producer.send('my-topic', {'key2': 'value2'})

producer.flush()
