from pyspark.sql import  SparkSession
from pyspark.sql.functions import  *
from pyspark.sql.types import  *


spark = (SparkSession.builder.
         appName("S3 test").
         getOrCreate())

#S3에서 데이터 읽기
# s3_output_path = "s3a://maple-nickname-etl-bucket-datalake/test-sample.parquet"
#
# schema = StructType([
#     StructField("start_page", IntegerType(), True),
#     StructField("end_page", IntegerType(), True),
#     StructField("nicknames", ArrayType(StringType()), True)
# ])
# data = [(1111, 222, ["a", "b", "c"])]
# df = spark.createDataFrame(data, schema)

# 데이터 처리 (예: 데이터 출력)
# df.write \
#     .format("parquet") \
#     .mode("append") \
#     .save(s3_output_path)


s3_input_path = "s3a://maple-nickname-etl-bucket-datalake/test-sample.parquet"
df = spark.read.parquet(s3_input_path, header=True, inferSchema=True)
df.show()
spark.stop()

