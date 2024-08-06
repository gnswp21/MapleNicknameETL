from collections import defaultdict
from app.processor import MapleAPI_Parser, Producer
import os

kafka_broker = os.environ.get("MYKAFKA")
kafka_topic = "maple-ranking"
result = defaultdict(list)
# 330071 ~ 352775 약 2만 3천 초당 3회 약 3시간 쿼리
start = 330050
end = 353000
for page in range(start, end):
    response = MapleAPI_Parser.get_ranking_page(page)
    print(f'send message to {kafka_topic} page : {page}')
    json_data = {'page': page, 'ranking': response}
    Producer.send_message(kafka_broker, kafka_topic, json_data)


