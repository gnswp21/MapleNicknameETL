from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import numpy as np

app = Flask(__name__, template_folder='C:\\Users\\family\\Projects\\etl\\MapleNicknameETL\\app\\web\\templates')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        def get_embeddings(text_list):
            inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=128)
            outputs = model(**inputs)
            # BERT의 마지막 층의 hidden states 사용
            embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            return embeddings
        name = request.form['user_input']
        # 쿼리 파라미터에서 'name'을 가져옵니다.
        new_texts = [name]
        new_embeddings = get_embeddings(new_texts)
        # 코사인 유사성을 사용하여 유사성 측정
        similarity_scores = cosine_similarity(new_embeddings, train_embeddings)
        diagonal_values = np.diag(similarity_scores[0])

        # 대각선 요소들의 평균 계산
        average_diagonal_similarity = np.mean(diagonal_values)
        # 결과 출력
        score = np.around(average_diagonal_similarity, 3)
        return f'Score : {score}! '
        # return redirect(url_for('home'))  # 폼 제출 후 페이지를 새로고침합니다.
    return render_template('index.html', title='홈페이지', content='텍스트를 입력하고 제출하세요!')

if __name__ == '__main__':
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    embeddings_df = pd.read_csv("mean_embeddings.csv")
    train_embeddings = embeddings_df.values.tolist()
    app.run(debug=True, port=5000)
