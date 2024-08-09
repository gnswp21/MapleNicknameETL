import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from app.processor.SparkConsumer import SparkConsumer

spark = (SparkSession.builder.
         appName("S3 test").
         getOrCreate())
s3_output_path = "s3a://maple-nickname-etl-bucket-datalake/test-ranking.parquet"

kafka_broker = os.getenv("MYKAFKA")
kafka_topic = "maple-ranking"
consumer = SparkConsumer("test_pyspark", loglevel="INFO")
df = consumer.get_messages_from_beginning(spark, kafka_broker, kafka_topic, 20)
# 데이터 처리 (예: 데이터 출력)
df.write \
    .format("parquet") \
    .mode("append") \
    .save(s3_output_path)
spark.stop()

