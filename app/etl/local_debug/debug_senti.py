from app.model.model import *
import pandas as pd
import sys
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel

names = pd.read_csv("../../../data/train-data.csv", header=0).filter('name')
names = names['name'].to_list()
print(names)
# senti_scores = senti(names)
# print(senti_scores[:20])
# result = [names, senti_scores]
# # #
# df = pd.DataFrame({"Name": names, "Senti_scores": senti_scores})
# df = df.sort_values(by="Senti_scores", ascending=False)
# df.to_csv("../../../data/result-high-senti.csv", mode="w", index=False)