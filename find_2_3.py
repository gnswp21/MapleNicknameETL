import requests
from collections import defaultdict
import pandas as pd
import time


def find_2_3(page, result):
    print('find name page from :', page)
    PAGE = str(page)
    DATE = "2024-07-31"
    MAPLE_APIKEY = "test_2c34f5907ba49f2393578fc965ebb8b500b124212d3189eeb6298a0918de8042efe8d04e6d233bd35cf2fabdeb93fb0d"
    url = 'https://open.api.nexon.com/maplestory/v1/ranking/overall?date=' + DATE + "&page=" + PAGE
    headers = {
        'accept': 'application/json',
        'x-nxopen-api-key': MAPLE_APIKEY
    }

    response = requests.get(url, headers=headers)
    time.sleep(1)
    print(response.status_code)
    if response.status_code != 200:
        df = pd.DataFrame(result)
        df.to_csv('sample_352774'+str(page)+'_temp.csv')

    table = response.json()
    arr = table['ranking']
    for node in arr:
        name = node['character_name']
        if len(name) <= 2:
            print(name)
        if len(name) <= 3:
            result[len(name)].append(name)


start_page = 1
result = defaultdict(list)
for i in range(start_page,  start_page+30):
    find_2_3(i, result)

df = pd.DataFrame(result[2])
df.to_csv('sample_'+str(start_page)+'+30-2.csv', index=False,  encoding='utf-8-sig', mode='w')

# df = pd.DataFrame(result[3])
# df.to_csv('sample_'+str(start_page)+'-100-3.csv', index=False,  encoding='utf-8-sig', mode='w')


