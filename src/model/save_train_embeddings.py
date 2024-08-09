from transformers import BertTokenizer, BertModel
import pandas as pd


# 입력 데이터를 BERT의 input format으로 변환하는 함수
def get_embeddings(text_list):
# 사전 학습된 BERT 모델과 토크나이저 로드
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model(**inputs)
    # BERT의 마지막 층의 hidden states 사용
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings


# 평균 로우 레벨 임베딩


file_path = "../../data/low_level_data.csv"
chunk_size = 5000

# 초기 빈 데이터프레임 생성
all_means = []

# CSV 파일을 청크 단위로 읽기
for chunk in pd.read_csv(file_path, header=None, names=["page", "level", "name"], chunksize=chunk_size):
    # 각 청크에 대해 임베딩 계산
    train_embeddings = get_embeddings(chunk["name"].to_list())
    df = pd.DataFrame(train_embeddings)

    # 각 청크의 평균 계산
    mean_df = df.mean()
    all_means.append(mean_df)

# 모든 청크의 평균을 종합하여 최종 평균 계산
final_mean = pd.concat(all_means, axis=1).mean(axis=1)
average_df = pd.DataFrame([final_mean.tolist()], columns=final_mean.index)
average_df.to_csv("../../data/mean_low_level_embeddings.csv", mode="w", index=False)
#
# # 평균 하이 레벨 임베딩
# train_texts = pd.read_csv("../../data/low_level_data.csv.csv")["name"].tolist()
# train_embeddings = get_embeddings(train_texts)
# df = pd.DataFrame(train_embeddings)
# mean_df = df.mean()
# mean_df.to_csv("../../data/mean_high_level_embeddings.csv", mode="w", index=False)
