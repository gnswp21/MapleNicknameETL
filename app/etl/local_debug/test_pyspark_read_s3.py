import os
from pyspark.sql import  SparkSession
from pyspark.sql.functions import  *
from pyspark.sql.types import  *
from app.processor.SparkConsumer import SparkConsumer
from app.model import model
#S3에서 데이터 읽기
spark = (SparkSession.builder.
         appName("S3 test").
         getOrCreate())
s3_input_path = "s3a://maple-nickname-etl-bucket-datalake/test-ranking.parquet"
df = spark.read.parquet(s3_input_path, header=True, inferSchema=True)
df.show()

result_df = df.withColumn("one", explode(col("ranking")))
final_df = result_df.select(
    col("page"),
    col("one.character_level").alias("level"),
    col("one.character_name").alias("name")
)
final_df.show()
filtered_df = final_df.filter(
    (col("level") < 63) & (col("name").rlike(r'^.{2}$'))
)
filtered_df = filtered_df.withColumn(
    "score", model.get_cosine_similarity(col("name"))
)
filtered_df.show()
spark.stop()







