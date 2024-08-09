import os
import sys

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

from typing import Any, Dict

from transformers import pipeline

from app.processor.SparkConsumer import SparkConsumer
from app.model import model


# UDF 정의


def run(kwargs: Dict[Any, Any]):
    spark = (
        SparkSession.builder.appName(f"{kwargs['job_name']}")
        .getOrCreate()
    )
    spark.sparkContext.addPyFile("/my_src/dependency_packages.zip")

    sentiment_analysis = pipeline("sentiment-analysis")

    @udf(returnType=FloatType())
    def get_sentiment_score(name):
        result = sentiment_analysis(name)[0]
        score = result['score'] if result['label'] == 'POSITIVE' else -result['score']
        return float(score)

    # read df from s3
    s3_input_path = "s3a://maple-nickname-etl-bucket-datalake/ranking.csv"
    schema = StructType([
        StructField("page", StringType(), True),
        StructField("level", StringType(), True),
        StructField("name", StringType(), True)
    ])
    df = spark.read.csv(s3_input_path, schema=schema).limit(5)
    df = df.withColumn("score", get_sentiment_score(col("name")))
    df.show()
    spark.stop()


if __name__ == "__main__":
    # convert positional args to kwargs
    kwargs = dict(zip(["job_name"], sys.argv[1:]))
    run(kwargs)
