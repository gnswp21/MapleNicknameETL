import pandas as pd


df = pd.read_csv("data/sample.csv")
filtered_df = df[~df['name'].str.contains('name')]
# filtered_df = filtered_df[:10]
df.to_csv("data/train-data.csv", mode="w", index=False)

