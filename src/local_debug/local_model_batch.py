from pyspark.sql.functions import col
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql import SparkSession
from typing import Any, Dict
from transformers import pipeline
import sys


def sentiment_analysis_batch(names):
    model = pipeline("sentiment-analysis")  # 모델을 파티션 내에서 로드
    results = model(names)
    scores = [result['score'] if result['label'] == 'POSITIVE' else -result['score'] for result in results]
    return scores

def run(kwargs: Dict[Any, Any]):
    spark = (
        SparkSession.builder.appName(f"{kwargs['job_name']}")
        .getOrCreate()
    )

    spark.sparkContext.addPyFile("/etl/dependency_packages.zip")

    # Read df from S3
    s3_input_path = "s3a://maple-nickname-etl-bucket-datalake/ranking-remain.csv"
    schema = StructType([
        StructField("page", StringType(), True),
        StructField("level", StringType(), True),
        StructField("name", StringType(), True)
    ])
    df = spark.read.csv(s3_input_path, schema=schema, header=False)

    # Apply the UDF to process batches of rows
    def process_partition(iterator):
        try:
            names = [row['name'] for row in iterator]
            scores = sentiment_analysis_batch(names)
            return [(name, score) for name, score in zip(names, scores)]
        except Exception as e:
            print(f"Error in process_partition: {e}")
            raise

    processed_rdd = df.rdd.mapPartitions(process_partition)
    processed_df = processed_rdd.toDF(["name", "score"])
    df = (df
          .join(processed_df, on="name", how="inner")
          .orderBy(col("score").desc()))
    output_path = "s3a://maple-nickname-etl-bucket-outputs/ranking_with_scores-remain.csv"
    df.coalesce(1).write.mode("overwrite").csv(output_path, header=True)
    spark.stop()


if __name__ == "__main__":
    kwargs = dict(zip(["job_name"], sys.argv[1:]))
    run(kwargs)
