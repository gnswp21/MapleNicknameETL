# MapleNicknameETL
aws s3 cp kafka-consume-spark-test.py s3://maple-nickname-etl-bucket-scripts
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.4 spark-local-test.py


# kafka Producer
cd /root/spark/app
python3 app/test_produce_topics.py


# spark kafka에서 데이터 받기
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.3 \
app/test_pyspark_kafka.py


# spark로 s3 연결
spark-submit \
--packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.526 \
app/test_pyspark_s3.py