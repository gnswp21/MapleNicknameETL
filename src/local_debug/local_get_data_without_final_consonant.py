from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, StructType, StructField, BooleanType
from pyspark.sql import SparkSession
from typing import Any, Dict
import sys


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

    # Get data_without_final_consonant
    @udf(BooleanType())
    # 종성 유무를 판단하는 사용자 정의 함수
    def has_no_final_consonant(name):
        # 한글 유니코드의 시작과 끝을 정의합니다.
        start_code = 0xAC00
        end_code = 0xD7A3
        for char in name:
            # 입력된 문자가 한글이 아니면 필터링
            if not start_code <= ord(char) <= end_code:
                return False

            # 유니코드 상의 한글 음절을 계산
            base = ord(char) - start_code
            jongseong = base % 28
            # 종성이 있으면 (jongseong 값이 0이 아님,) False 필터링
            if jongseong != 0:
                return False
        return True

    # 'name' 열에서 종성이 없는 이름만 필터링
    df = df.filter(has_no_final_consonant(col("name")))
    # Save data frame
    output_path = "s3a://maple-nickname-etl-bucket-outputs/low_level_data_without_final_consonant.csv"
    df.coalesce(1).write.mode("overwrite").csv(output_path, header=True)
    spark.stop()


if __name__ == "__main__":
    kwargs = dict(zip(["job_name"], sys.argv[1:]))
    run(kwargs)
