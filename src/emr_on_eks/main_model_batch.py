import logging

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession

from typing import Any, Dict

from transformers import pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sentiment_analysis_batch(names):
    model = pipeline("sentiment-analysis")  # Load model inside the function
    results = model(names)
    scores = [result['score'] if result['label'] == 'POSITIVE' else -result['score'] for result in results]
    return scores

def run(kwargs: Dict[Any, Any]):
    spark = (
        SparkSession.builder.appName(f"{kwargs['job_name']}")
        .getOrCreate()
    )
    spark.sparkContext.addPyFile("/my_src/dependency_packages.zip")

    # Read df from s3
    s3_input_path = "s3a://maple-nickname-etl-bucket-datalake/ranking.csv"
    schema = StructType([
        StructField("page", StringType(), True),
        StructField("level", StringType(), True),
        StructField("name", StringType(), True)
    ])
    df = spark.read.csv(s3_input_path, schema=schema, header=True)

    # Apply the UDF to process batches of rows
    def process_partition(iterator):
        try:
            names = [row['name'] for row in iterator]
            scores = sentiment_analysis_batch(names)
            return [(name, score) for name, score in zip(names, scores)]
        except Exception as e:
            logger.error(f"Error in process_partition: {e}")
            raise

    processed_rdd = df.rdd.mapPartitions(process_partition)
    processed_df = processed_rdd.toDF(["name", "score"])
    df = (df
          .join(processed_df, on="name", how="inner")
          .orderBy(col("score").desc()))
    output_path = "s3a://maple-nickname-etl-bucket-outputs/ranking_with_scores.csv"
    df.coalesce(1).write.mode("overwrite").csv(output_path, header=True)
    spark.stop()

if __name__ == "__main__":
    # Convert positional args to kwargs
    kwargs = dict(zip(["job_name"], sys.argv[1:]))
    run(kwargs)
