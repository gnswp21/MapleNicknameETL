import json
import sys
from collections import defaultdict
from app.proceesor import MapleAPI_Parser, Producer

result = defaultdict(list)
# page = 330074
page = 400000
end = 2
for i in range(end):
    MapleAPI_Parser.get_nickname_in_targets(page+i, result, [2, 3])
json_data = {'start_page':page, 'end_page':page+end-1, 'nicknames':result[2]}
print(json_data)


