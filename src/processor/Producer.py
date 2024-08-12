import json
from collections import defaultdict
from kafka import KafkaProducer


def send_message(brokers: str, topics: str, data: dict, logger) -> None:
    # 프로듀서 인스턴스 생성
    producer = KafkaProducer(bootstrap_servers=[brokers],
                             value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    def on_send_success(record_metadata):
        logger.info(f"Message delivered to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

    def on_send_error(excp):
        logger.info(f"Error sending message: {excp}")

    try:
        # Kafka로 메시지 전송
        future = producer.send(topics, data)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)

        # 전송이 완료될 때까지 기다림
        producer.flush()

    except Exception as e:
        logger.info(f"Error producing message: {e}")
    finally:
        producer.close()



# produce json messages

