import requests
import time
from datetime import datetime
import os


def get_ranking_page(page, logger):
    PAGE = str(page)
    DATE = datetime.now().strftime('%Y-%m-%d')
    MAPLE_API_KEY = os.getenv("MAPLE_API_KEY")
    url = 'https://open.api.nexon.com/maplestory/v1/ranking/overall?date=' + DATE + "&page=" + PAGE
    headers = {
        'accept': 'application/json',
        'x-nxopen-api-key': MAPLE_API_KEY
    }
    response = requests.get(url, headers=headers)
    while response.status_code != 200:
        logger.info('response :{response.status_code} -waiting for server response')
        time.sleep(1)
        response = requests.get(url, headers=headers)

    table = response.json()
    return table['ranking']


