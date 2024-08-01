import requests


def find_last_page(page):
    print('find last page from :', page)
    PAGE = str(page)
    DATE = "2024-07-31"
    MAPLE_APIKEY = "test_2c34f5907ba49f2393578fc965ebb8b500b124212d3189eeb6298a0918de8042efe8d04e6d233bd35cf2fabdeb93fb0d"
    url = 'https://open.api.nexon.com/maplestory/v1/ranking/overall?date=' + DATE + "&page=" + PAGE
    headers = {
        'accept': 'application/json',
        'x-nxopen-api-key': MAPLE_APIKEY
    }

    response = requests.get(url, headers=headers)
    table = response.json()
    arr = table['ranking']
    return not len(arr)


def find_start_page(page):
    print('request start page :', page)
    PAGE = str(page)
    DATE = "2024-07-31"
    MAPLE_APIKEY = "test_2c34f5907ba49f2393578fc965ebb8b500b124212d3189eeb6298a0918de8042efe8d04e6d233bd35cf2fabdeb93fb0d"
    url = 'https://open.api.nexon.com/maplestory/v1/ranking/overall?date=' + DATE + "&page=" + PAGE
    headers = {
        'accept': 'application/json',
        'x-nxopen-api-key': MAPLE_APIKEY
    }

    response = requests.get(url, headers=headers)
    table = response.json()
    arr = table['ranking']
    for i, node in enumerate(arr):
        if node['character_level'] <= 61:
            return True
    return False


l = 300000
r = 370000
first_page = -1
cnt = 0
while l <= r:
    mid = (l + r) // 2
    cnt += 1
    if find_start_page(mid):
        first_page = mid
        r = mid - 1
    else:
        l = mid + 1

print("First page = ", first_page)  # 330071
print("total query = ", cnt)  # 16


l = 340000
r = 370000
last_page = -1
cnt = 0
while l <= r:
    mid = (l + r) // 2
    cnt += 1
    if find_last_page(mid):
        last_page = mid
        r = mid - 1
    else:
        l = mid + 1

print("Last page = ", last_page)   # 352775
print("total query = ", cnt)  # 15