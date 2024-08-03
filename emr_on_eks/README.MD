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
--ssh-access `
--ssh-public-key myKeyPair `
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
--cli-input-json file://./create-virtual-cluster-request.json
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

# 실행



```commandline
aws emr-containers start-job-run `
--cli-input-json file://./start-job-run-request-sample.json
```

## job reqeust 파일

# 트러블슈팅
aws cloudformation delete-stack --stack-name eksctl-Maple-Nickname-ETL-cluster-cluster --region ap-northeast-2
--virtual-cluster-id 0rpc5iz1ahqdtua7gylvbhg80
aws emr-containers cancel-job-run --id 0000000348cspfsg6kv --virtual-cluster-id 0rpc5iz1ahqdtua7gylvbhg80

aws emr-containers list-virtual-clusters --state RUNNING