import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
from transformers import pipeline


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
    embeddings_df = pd.read_csv("data/mean_high_level_embeddings.csv")
    train_embeddings = embeddings_df.values.tolist()
    new_embeddings = get_embeddings(tokenizer, model, [name])
    # 코사인 유사성을 사용하여 유사성 측정
    similarity_scores = cosine_similarity(new_embeddings, train_embeddings)
    return float(similarity_scores[0][0])


def get_similarities(tokenizer, model, name, high_df, low_df):
    # model
    name_embedding = get_embeddings(tokenizer, model, [name])
    # get  embedding
    high_embeddings = high_df.values.tolist()
    # 코사인 유사성을 사용하여 유사성 측정
    high_similarity_scores = cosine_similarity(name_embedding, high_embeddings)

    # get traing embedding
    low_embedding = low_df.values.tolist()
    # 코사인 유사성을 사용하여 유사성 측정
    low_similarity_scores = cosine_similarity(name_embedding, low_embedding)
    return float(high_similarity_scores[0][0]), float(low_similarity_scores[0][0])


def get_embedding_score(tokenizer, model, name, high_df, low_df):
    # model
    name_embedding = get_embeddings(tokenizer, model, [name])
    # get  embedding
    high_embeddings = high_df.values.tolist()
    # 코사인 유사성을 사용하여 유사성 측정
    high_similarity_scores = cosine_similarity(name_embedding, high_embeddings)

    # get traing embedding
    low_embedding = low_df.values.tolist()
    # 코사인 유사성을 사용하여 유사성 측정
    low_similarity_scores = cosine_similarity(name_embedding, low_embedding)
    return float(high_similarity_scores[0][0]) - float(low_similarity_scores[0][0])


def senti(names):

    # 감정 분석을 위한 파이프라인 로드
    sentiment_analysis = pipeline("sentiment-analysis")

    # 감정 분석 수행
    results = sentiment_analysis(names)
    scores = []
    for result in results:
        scores.append(result['score'] if result['label'] == 'POSITIVE' else -result['score'])
    return scores


if __name__ == "__main__":
    names = pd.read_csv("data/result-embedding.csv")["Name"].head(50).to_list()
    senti(names)
