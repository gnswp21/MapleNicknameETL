from transformers import BertTokenizer, BertModel
# import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# 사전 학습된 BERT 모델과 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


# 입력 데이터를 BERT의 input format으로 변환하는 함수
def get_embeddings(text_list):
    inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model(**inputs)
    # BERT의 마지막 층의 hidden states 사용
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings


# 4000개의 학습 데이터 임베딩
train_texts = pd.read_csv("data/sample.csv")["name"].tolist()
train_embeddings = get_embeddings(train_texts)
df = pd.DataFrame(train_embeddings)
df.to_csv("data/embeddings.csv", mode="w", index=False)
# 평균 임베딩
column_means = df.mean()
average_df = pd.DataFrame([column_means.tolist()], columns=column_means.index)
average_df.to_csv("data/mean_embeddings.csv", mode="w", index=False)

