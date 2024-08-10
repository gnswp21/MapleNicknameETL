# from typing import data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_distribution(df, output_path, title): # -> two figure
    # 'score' 열을 0.1 단위로 그룹화하면서 라벨을 구간으로 설정
    score = 'score'
    bins = np.arange(-1, 1.1, 0.1)
    labels = [f'({bins[i]:.1f}, {bins[i+1]:.1f}]' for i in range(len(bins)-1)]
    grouped = df.groupby(pd.cut(df['score'], bins=bins, labels=labels, include_lowest=True))

    # 각 그룹에 속하는 데이터의 개수 계산
    counts = grouped.size().sort_index(ascending=False)
    counts_filtered = counts[counts > 0]
    fig, ax = plt.subplots(figsize=(10, 6))  # 그래프 크기 설정
    ax.axis('off')  # 축을 표시하지 않음
    table = ax.table(cellText=counts_filtered.reset_index().values,
                     colLabels=['Score Range', 'Number of Entries'],
                     cellLoc='center',
                     loc='center')

    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # 표 크기 조절
    plt.savefig(output_path + "_table.png", bbox_inches='tight', dpi=300)

    plt.figure(figsize=(10, 6))
    counts_filtered.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('Score Range')
    plt.ylabel('Number of Entries')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.savefig(output_path+".png")

