import requests
import time


def get_nickname_in_targets(page, result, targets):
    print('find nicknames page from :', page)
    PAGE = str(page)
    DATE = "2024-07-31"
    MAPLE_APIKEY = "test_2c34f5907ba49f2393578fc965ebb8b500b124212d3189eeb6298a0918de8042efe8d04e6d233bd35cf2fabdeb93fb0d"
    url = 'https://open.api.nexon.com/maplestory/v1/ranking/overall?date=' + DATE + "&page=" + PAGE
    headers = {
        'accept': 'application/json',
        'x-nxopen-api-key': MAPLE_APIKEY
    }
    response = requests.get(url, headers=headers)
    while response.status_code != 200:
        print(response.status_code, 'waiting for server response')
        time.sleep(1)
        response = requests.get(url, headers=headers)

    table = response.json()
    arr = table['ranking']
    for node in arr:
        name = node['character_name']
        if len(name) in targets:
            result[len(name)].append(name)



