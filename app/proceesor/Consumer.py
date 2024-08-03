from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, from_json, col
from pyspark.sql.types import StringType, ArrayType, StructType, StructField, TimestampType, IntegerType


class SparkConsumer:
    def __init__(self, app_name, loglevel, config=None):
        self.app_name = app_name
        self.loglevel = loglevel
        self.config = config

    def get_topic_all(self, kafka_broker, kafka_topic):
        spark = (SparkSession.builder.
                 appName(self.app_name).
                 getOrCreate())
        spark.sparkContext.setLogLevel(self.loglevel)
        # Kafka에서 배치 데이터 읽기
        df = spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_broker) \
            .option("subscribe", kafka_topic) \
            .option("startingOffsets", "earliest") \
            .option("enable.auto.commit", "false") \
            .load()
        # value열 을 UTF-8로 디코딩하여 (binary -> JSON)으로 변환
        decoded_df = df.selectExpr("CAST(value AS STRING) as json_str")
        # # JSON 스키마 정의 # JSON 문자열을 파싱하여 DataFrame으로 변환
        schema = StructType([
            StructField("start_page", IntegerType(), True),
            StructField("end_page", IntegerType(), True),
            StructField("nicknames", ArrayType(StringType()), True)
        ])
        json_df = decoded_df.withColumn("parsed_json", from_json(col("json_str"), schema))
        # # 데이터프레임 출력
        mydf = json_df.select(
                       "parsed_json.start_page",
                       "parsed_json.end_page",
                       "parsed_json.nicknames"
                        )
        mydf.show()
        spark.stop()

        return mydf

