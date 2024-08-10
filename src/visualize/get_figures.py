from src.processor import Visualizer
import pandas as pd

df = pd.read_csv("result/result.csv")
outputpath = "result/figure/score_distribution"
title = "[Low level] | Distribution of Scores by 0.1 Intervals (Non-zero Counts Only)"
Visualizer.get_distribution(df, outputpath, title)

recommended_df = df[df['score'] >= 0.95][['name']].sample(n=50, random_state=42)
recommended_df.to_csv('result/result-recommended.csv', header=True, index=False)


df = pd.read_csv("result/result-high.csv")
outputpath = "result/figure/high_score_distribution"
title = "[High level] | Distribution of Scores by 0.1 Intervals (Non-zero Counts Only)"
Visualizer.get_distribution(df, outputpath, title)


df = pd.read_csv("result/result-no-final-consonant.csv")
outputpath = "result/figure/no_final_consonant_score_distribution"
title = "'[No Final Consonant] | Distribution of Scores by 0.1 Intervals (Non-zero Counts Only)'"
Visualizer.get_distribution(df, outputpath, title)

