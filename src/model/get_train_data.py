from app.proceesor import MapleAPI_Parser
import pandas as pd
from collections import defaultdict


for i in range(2, 51):
    result = defaultdict(list)
    MapleAPI_Parser.get_nickname_in_targets(i, result, [2])
    df = pd.DataFrame(result[2], columns=['name'])
    df.to_csv("data/sample.csv", mode="a", index=False)












