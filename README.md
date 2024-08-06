# MapleNicknameETL
aws s3 cp kafka-consume-spark-test.py s3://maple-nickname-etl-bucket-scripts
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.4 spark-local-test.py


# kafka Producer
cd /root/spark/app
python3 app/test_produce_topics.py


# spark kafka에서 데이터 받기
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.3 \
app/etl/local_debug/test_pyspark_kafka.py


# spark로 s3 연결
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.3,org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.526 \
--conf spark.hadoop.fs.s3a.access.key=${SPARK_HADOOP_FS_S3A_ACCESS_KEY} \
--conf spark.hadoop.fs.s3a.secret.key=${SPARK_HADOOP_FS_S3A_SECRET_KEY} \
app/etl/local_debug/test_pyspark_save_s3.py

# s3에 저장된 df 읽기
spark-submit \
--packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.526 \
--conf spark.hadoop.fs.s3a.access.key=${SPARK_HADOOP_FS_S3A_ACCESS_KEY} \
--conf spark.hadoop.fs.s3a.secret.key=${SPARK_HADOOP_FS_S3A_SECRET_KEY} \
app/etl/local_debug/test_pyspark_read_s3.py


메이플 API를 활용하여, 두글자 닉네임의 희귀도를 조사합니다.

<현재 구현>
1. BERT 모델로  두글자 닉네임의 임베딩을 구해 평균 임베딩을 서버측에 저장
2. 입력으로 두글자 닉네임이 들어오면 서버에 저장된 임베딩과 비교를 통해 레어도를 구함
3. 구해진 레어도를 응답하여 웹페이지에 게시
   <추후 구현>
1. 현재 삭제 예정인  혹은 추후 삭제된 ID들의 레어도 순위 정렬하여 공개
2. 구글 검색을 통해 일상 생활에 사용되는 단어와 유사한지를 레어도 점수 지표에 추가
   <API  추가 요청 사유>
1. 더욱 정확한 모델링
2. 전 랭킹 혹은 8/20에 삭제예정인 아이들의 레어도 측정 후 공개하기 위해서