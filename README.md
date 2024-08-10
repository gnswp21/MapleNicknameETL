
# 프로젝트 : MapleNickNameETL
1. 메이플 API를 활용하여, 약 13만개의 삭제 예정인 두글자 닉네임을 조사하여 Huggingface의 감정분석모델을 통해 분석합니다.
2. 삭제 예정인 13만개의 닉네임 중 추천 닉네임을 찾습니다.

## 아키텍처
![아키텍쳐](architecture.png)
### 구조
- Producer(ec2.t3.medium): 메이플 API로 데이터 추출 및 브로커로 전송
- Kafka broker(ec2.t3.medium): 데이터 중계 및 임시보관
- Emr on Eks(ec2.m5.xlarge * 2) : Pyspark로 데이터 컨슘 및 데이터 처리 후 S3에 저장
- local_debug(spark): emr 작업 전, 로컬에서 빠르게 Pyspark 코드를 로컬디버깅 할 수 있는 구성
- visualize: s3에서 데이터를 프로젝트로 저장 후, 데이터 분석을 위해 데이터 시각화


### ETL 파이프라인
1. MapleAPI를 통해 랭킹 데이터를 추출
2. 랭킹 데이터를 카프카 브로커에 전송
3. Emr on Eks를 이용해 카프카 브로커에서 랭킹 데이터를 데이터프레임으로 변환 후 전처리 후 S3에 저장
4. S3에 저장된 전처리된 데이터를 읽어와 Hugginfface 모델에 인풋으로 입력
5. (4)의 결과를 다시 S3에 저장
6. s3에 저장된 데이터를 로컬에 저장 후 해당 데이터를 이용해 시각화 및 분석

## 주요 구현
### emr on eks - main_model_batch 

## 결과 및 분석
### 결과 분석
![고레벨 분포](result/figure/high_score_distribution.png)
![저레벨(삭제예정) 분포](result/figure/score_distribution.png)

### 한계
1. 너무 오래 걸린 작업 시간
각 단어마다 점수를 내서 정렬하는데(main_model_batch) 3시간이 소요되었다. 십삼만개가 그리 많은 데이터가 아님에도 생각보다 오래 걸렸다.
이유는 세가지로 생각된다.
   1. 너무 적은 성능의 eks 구성
   2. transformer 모델의 cpu only 사용
   3. main_model_batch.py의 UDF 함수 구현 및 적용에서 비효율 발생
2. 받침 없는 글자 체크 못함
![아키텍처 다이어그램](result/figure/no_final_consonant_score_distribution.png)
위는 

## 설치 및 실행 방법
홈 디렉토리에 HowToBuildAndRun.md를 참고해주세요


