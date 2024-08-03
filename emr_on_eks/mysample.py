import os
import sys
import pyspark.sql.functions as F
from pyspark.sql import SparkSession


spark = SparkSession \
    .builder \
    .appName("mysample") \
    .getOrCreate()

output_path = sys.argv[1]
region = os.getenv("AWS_REGION")
df = spark.createDataFrame([(i,) for i in range(1, 11)], ["sample"])
df.coalesce(1).write.mode("overwrite").csv(output_path)
spark.stop()
