from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 설정 추가, 모든 도메인 허용


@app.route('/calculate_score', methods=['POST'])
def get_score():
    def get_embeddings(text_list):
        inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=128)
        outputs = model(**inputs)
        # BERT의 마지막 층의 hidden states 사용
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        return embeddings
    name = request.json.get('user_input')
    # 쿼리 파라미터에서 'name'을 가져옵니다.
    new_embeddings = get_embeddings([name])
    # 코사인 유사성을 사용하여 유사성 측정
    similarity_scores = cosine_similarity(new_embeddings, train_embeddings)
    diagonal_values = np.diag(similarity_scores[0])
    # 대각선 요소들의 평균 계산
    average_diagonal_similarity = np.mean(diagonal_values)
    # 결과 출력
    score = np.around(average_diagonal_similarity, 3)
    score = str(score)
    return score


if __name__ == '__main__':
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    embeddings_df = pd.read_csv("mean_embeddings.csv")
    train_embeddings = embeddings_df.values.tolist()
    app.run(debug=True, port=5000)
