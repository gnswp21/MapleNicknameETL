import pandas as pd
from transformers import BertTokenizer, BertModel
import os
import sys

# sys.path와 os.listdir()는 경로 문제를 확인하기 위한 코드입니다. 필요에 따라 유지하거나 제거하세요.
print(sys.path)
print(os.listdir())

from src.model.model import get_embedding_score

# 청크 사이즈 정의
chunk_size = 5000

# 초기 설정 및 파일 읽기
high_df = pd.read_csv("../../data/mean_high_level_embeddings.csv")
low_df = pd.read_csv("../../data/mean_low_level_embeddings.csv")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bertmodel = BertModel.from_pretrained('bert-base-uncased')

# 중간 결과를 저장할 파일 초기화
temp_output_file = "../../result/temp-result-embedding.csv"
# 컬럼 헤더를 추가하기 위해 빈 데이터프레임 생성
cnt = chunk_size
# CSV 파일을 청크 단위로 읽어와서 처리
for chunk in pd.read_csv("../../result/result.csv", chunksize=chunk_size):
    print(f'---> START : {cnt - chunk_size} ~ {cnt} ')
    chunk.drop(columns=['score'], inplace=True)
    # get_embedding_score 함수를 각 이름에 적용
    chunk['embedding_score'] = chunk['name'].apply(lambda x: get_embedding_score(tokenizer, bertmodel, x, high_df, low_df))

    # embedding_score를 기준으로 정렬
    chunk = chunk.sort_values(by='embedding_score', ascending=False)

    # 처리된 청크를 결과 파일에 추가 저장
    chunk.to_csv(temp_output_file, mode="a", header=False, index=False)
    print(f'---> DONE : {cnt - chunk_size} ~ {cnt}')
    cnt += chunk_size

final_df = pd.read_csv(temp_output_file)
final_df = final_df.sort_values(by='embedding_score', ascending=False)

# 최종 결과를 저장할 파일에 저장
final_output_file = "../../result/result-embedding-all.csv"
final_df.to_csv(final_output_file, mode="w", index=False)

# 임시 파일 삭제
os.remove(temp_output_file)