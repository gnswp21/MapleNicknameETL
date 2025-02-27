### 필수 요구 사항
- Python 3.9 이상
- Docker
# kafka Broker
## Setting
-  ec2 노드 생성, 도커 설치
- .env 파일 생성 후 환경변수 입력
- 예시
  ```text
  MYKAFKA=<my-broker-ip:port>
  ```
## Build and Run
```commandline
docker build -t mykafka -f dockerbuild/kafka/Dockerfile-kafka .
docker compose -f dockerbuild/kafka/docker-compose.yml  up -d
docker logs -f mykafka
```
# Producer (MapleAPI data extract
## Setting
-  ec2 노드 생성, 도커 설치
- .env 파일 생성 후 환경변수 입력
- 예시
```text
MYKAFKA=<my-broker-ip:port>
MAPLE_API_KEY=<my-api-key>
```
## Build and Run
```commandline
docker build -t producer -f dockerbuild/producer/Dockerfile-producer .
docker compose -f dockerbuild/producer/docker-compose.yml  up -d
docker logs -f producer
```

# 로컬 디버그
## setting
-  도커설치
- .env 파일 생성 후 환경변수 입력
- 예시
```commandline
SPARK_HADOOP_FS_S3A_ACCESS_KEY=<my-access-key>
SPARK_HADOOP_FS_S3A_SECRET_KEY=<my-secret-key>
MYKAFKA=<my-broker-ip:port>
MAPLE_API_KEY=<my-api-key>
```
## Build and Run
### local
```commandline
docker build -t local -f ./dockerbuild/local/Dockerfile-local .
docker compose -f ./dockerbuild/local/docker-compose-model.yml  up -d
docker logs -f local
```
- 실행할 파이썬 작업에 맞춰 도커 컴포즈 파일을 변경


# Emr on Eks
## Setting
- aws eks 생성
- aws emr virtual cluster 생성
- aws ecr 생성 후 이미지 등록
- job-run.json, job-run-model.json, job-run-without-final.json
  - 가상클러스터 아이디 입력
  - 이미지 태그 입력
  - 환경변수 입력

## Build and Run
```commandline
docker build -t <image-name> -f .\emr_on_eks\Dockerfile-emr .
docker tag <image-name> <aws-user-id>.dkr.ecr.ap-northeast-2.amazonaws.com/<ecr-repo-name>
docker push <aws-user-id>.dkr.ecr.ap-northeast-2.amazonaws.com/<ecr-repo-name>
aws emr-containers start-job-run --cli-input-json file://emr_on_eks/job-run.json
```
- 실행할 emr on eks 작업에 맞춰 도커 job-run.json 파일을 변경