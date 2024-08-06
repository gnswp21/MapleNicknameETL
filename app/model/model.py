import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import numpy as np

# 입력 데이터를 BERT의 input format으로 변환하는 함수
def get_embeddings(tokenizer, model, text_list):
    inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model(**inputs)
    # BERT의 마지막 층의 hidden states 사용
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings

def get_cosine_similarity(name):
    # model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    # get traing embedding
    embeddings_df = pd.read_csv("../../data/mean_embeddings.csv")
    train_embeddings = embeddings_df.values.tolist()
    new_embeddings = [name]
    # 코사인 유사성을 사용하여 유사성 측정
    similarity_scores = cosine_similarity(new_embeddings, train_embeddings)
    # 대각선 요소 추출
    diagonal_values = np.diag(similarity_scores[0])
    # 대각선 요소들의 평균 계산
    average_diagonal_similarity = np.mean(diagonal_values)
    return average_diagonal_similarity

