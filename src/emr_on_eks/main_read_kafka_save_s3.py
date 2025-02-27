import os
from pyspark.sql.functions import *
from pyspark.sql import SparkSession

from typing import Any, Dict
from src.processor.SparkConsumer import SparkConsumer


def run(kwargs: Dict[Any,Any]):
    spark = (
        SparkSession.builder.appName(f"{kwargs['job_name']}")
        .getOrCreate()
    )
    spark.sparkContext.addPyFile("/etl/dependency_packages.zip")

    # Setting kafka
    kafka_broker = os.getenv("MYKAFKA")
    kafka_topic = "maple-ranking"

    # Setting logger
    log4j_logger = spark._jvm.org.apache.log4j
    LOGGER = log4j_logger.LogManager.getLogger(__name__)

    # Getting kafka message as dataframe
    consumer = SparkConsumer("test_pyspark")
    df = consumer.get_messages_from_beginning_decoding(spark, kafka_broker, kafka_topic, nums=10**6)

    result_df = df.withColumn("one", explode(col("ranking")))
    final_df = result_df.select(
        col("page"),
        col("one.character_level").alias("level"),
        col("one.character_name").alias("name")
    )
    df = final_df.filter(
        (col("level") <= 61) & (col("name").rlike(r'^.{2}$'))
    )
    LOGGER.info(f"---> save df{df.head()}")

    # Saving dataframe
    s3_output_path = "s3a://maple-nickname-etl-bucket-datalake/ranking.csv"
    LOGGER.info(f"---> START save df at  {s3_output_path}")
    df.write \
        .format("csv") \
        .option("encoding", "UTF-8") \
        .mode("overwrite") \
        .save(s3_output_path)

    spark.stop()


if __name__ == "__main__":
    # convert positional args to kwargs
    kwargs = dict(zip(["job_name", "MYKAFKA"], sys.argv[1:]))
    run(kwargs)
