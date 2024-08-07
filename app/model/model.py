import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel


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
    embeddings_df = pd.read_csv("data/mean_embeddings.csv")
    train_embeddings = embeddings_df.values.tolist()
    new_embeddings = get_embeddings(tokenizer, model, [name])
    # 코사인 유사성을 사용하여 유사성 측정
    similarity_scores = cosine_similarity(new_embeddings, train_embeddings)
    return float(similarity_scores[0][0])
