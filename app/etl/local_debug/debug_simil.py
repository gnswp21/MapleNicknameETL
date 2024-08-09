from app.model.model import *
import pandas as pd
import sys
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel

names = pd.read_csv("../../../data/low_level_data_without_final_consonant.csv", header=0)["Name"]
result = []
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
high_df = pd.read_csv("../../../data/mean_high_level_embeddings.csv")
low_df = pd.read_csv("../../../data/mean_low_level_embeddings.csv")
for name in names:
    hi, lo = get_similarities(tokenizer, model, name, high_df, low_df)
    result.append([name, hi, lo])


df = pd.DataFrame(result, columns=["Name", "Hi", "Lo"])

df["Score"] = df["Hi"] - df["Lo"]
df = df.sort_values(by="Score", ascending=False)

df.to_csv("../../../data/result-embedding.csv", index=False)