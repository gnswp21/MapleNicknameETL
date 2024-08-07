from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, from_json, col
from pyspark.sql.types import StringType, ArrayType, StructType, StructField, TimestampType, IntegerType, LongType


class SparkConsumer:
    def __init__(self, app_name, loglevel, config=None):
        self.app_name = app_name
        self.loglevel = loglevel
        self.config = config

    def get_messages_from_beginning(self, spark, kafka_broker, kafka_topic, nums):
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

        character_schema = StructType([
            StructField("date", StringType(), True),
            StructField("ranking", IntegerType(), True),
            StructField("character_name", StringType(), True),
            StructField("world_name", StringType(), True),
            StructField("class_name", StringType(), True),
            StructField("sub_class_name", StringType(), True),
            StructField("character_level", IntegerType(), True),
            StructField("character_exp", LongType(), True),  # 경험치는 LongType 사용
            StructField("character_popularity", IntegerType(), True),
            StructField("character_guildname", StringType(), True)
        ])

        # # JSON 스키마 정의 # JSON 문자열을 파싱하여 DataFrame으로 변환
        schema = StructType([
            StructField("page", IntegerType(), True),
            StructField("ranking", ArrayType(character_schema), True)  # ranking 필드는 character_schema의 배열
        ])

        json_df = decoded_df.withColumn("parsed_json", from_json(col("json_str"), schema))
        # # 데이터프레임 출력
        mydf = json_df.select(
            "parsed_json.page",
            "parsed_json.ranking"

        ).limit(nums)
        return mydf
