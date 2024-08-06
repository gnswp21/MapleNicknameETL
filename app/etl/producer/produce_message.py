from collections import defaultdict
from app.processor import MapleAPI_Parser, Producer
import os
import logging

kafka_broker = os.environ.get("MYKAFKA")
kafka_topic = "maple-ranking"
result = defaultdict(list)

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨 설정
    format='%(asctime)s %(levelname)s - %(message)s',  # 로그 포맷 설정
    handlers=[
        logging.StreamHandler(),  # 로그를 콘솔로 출력
        logging.FileHandler('app/etl/producer/producer.log')  # 로그를 파일로 저장
    ]
)

logger = logging.getLogger(__name__)

# 330071 ~ 352775 약 2만 3천 초당 3회 약 3시간 쿼리
start = 330050
end = 353000

for page in range(start, end):
    response = MapleAPI_Parser.get_ranking_page(page)
    logger.info(f'Send message to {kafka_topic} page: {page}')
    json_data = {'page': page, 'ranking': response}
    Producer.send_message(kafka_broker, kafka_topic, json_data)