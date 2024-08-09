# 소개
EMR on EKS 를 구성하기 위한 준비. 앞서 미리 설정한 IAM ROLE이 있다는 가정

# 설치
## 준비물
- IAM ROLE
- AWS, EKSCTL

## EKS 클러스터 생성
```commandline
eksctl create cluster `
--name Maple-Nickname-ETL-cluster `
--region ap-northeast-2 `
--with-oidc `
--instance-types=m5.xlarge `
--managed `
--profile default

```
## EMR container 생성
```
eksctl create iamidentitymapping `
    --cluster Maple-Nickname-ETL-cluster `
    --namespace default `
    --service-name "emr-containers" `
    --profile default

```

## 신뢰정책 업데이트
```commandline
aws emr-containers update-role-trust-policy `
--cluster-name Maple-Nickname-ETL-cluster `
--namespace default `
--role-name EMRContainers-JobExecutionRole
```

## 가상 클러스터 등록
```commandline
aws emr-containers create-virtual-cluster `
--cli-input-json file://./create-virtual-cluster-request.json `
--name Maple-Nickname-ETL-virtual-cluster
```

## S3 버켓, 로그그룹 생성 생성
### S3 버켓
maple-nickname-etl-bucket-outputs
maple-nickname-etl-bucket-logging
maple-nickname-etl-bucket-scripts
### 로그 그룹
maple-nickname-etl-log-group
### 스파크 서브밋 스크립트 작성 후 S3 버킷으로 전송
aws s3 cp kafka-consume-spark-test.py


## 

# 실행 - start-job-run
```commandline
docker build -t emr6.5_maple -f .\emr_on_eks\Dockerfile-emr .
docker tag emr6.5_maple 691487686124.dkr.ecr.ap-northeast-2.amazonaws.com/emr6.5_maple_repo
docker push 691487686124.dkr.ecr.ap-northeast-2.amazonaws.com/emr6.5_maple_repo
aws emr-containers start-job-run --cli-input-json file://emr_on_eks/job-run.json
```


# 실행 - spark-submit
```commandline
kubectl run -it maple-nickname-etl `
--image=996579266876.dkr.ecr.ap-northeast-2.amazonaws.com/spark/emr-7.1.0:latest `
--command -n default /bin/bash


export MASTER_URL=k8s://https://4756231A65037AB06F1F1DC74122C51A.gr7.ap-northeast-2.eks.amazonaws.com

```


```
$SPARK_HOME/bin/spark-submit \
 --class org.apache.spark.examples.SparkPi \
 --master $MASTER_URL \
 --conf spark.kubernetes.container.image=996579266876.dkr.ecr.ap-northeast-2.amazonaws.com/spark/emr-7.1.0:latest \
 --conf spark.kubernetes.authenticate.driver.serviceAccountName=root \
 --deploy-mode cluster \
 --conf spark.kubernetes.namespace=default \
 local:///usr/lib/spark/examples/jars/spark-examples.jar 2
```

# 자주 사용하는 emr eks 명령어
## 버츄얼 클러스터 조회
aws emr-containers list-virtual-clusters --state RUNNING
## job 조회
aws emr-containers describe-job-run `
--id 0000000349bj6mcibs3 `
--virtual-cluster-id mw8ugmd0ps5n1bmc8j1xwnjhs

## job 중지
aws emr-containers cancel-job-run `
--id 0000000349cq676e032 `
--virtual-cluster-id mw8ugmd0ps5n1bmc8j1xwnjhs

## aws s3로 스크립트 전송
aws s3 cp app s3://maple-nickname-etl-bucket-scripts/app

# 트러블슈팅
aws cloudformation delete-stack --stack-name eksctl-Maple-Nickname-ETL-cluster-cluster --region ap-northeast-2
--virtual-cluster-id 0rpc5iz1ahqdtua7gylvbhg80
aws emr-containers cancel-job-run --id 0000000348cspfsg6kv --virtual-cluster-id 0rpc5iz1ahqdtua7gylvbhg80

aws emr-containers list-virtual-clusters --state RUNNING