import json
import sys
from collections import defaultdict
from proceesor import MapleAPI_Parser, Producer

if __name__ != "__main__":
    print("This is a main py, not a module")
    sys.exit(1)

kafka_broker = "mykafka1:19094"
kafka_topic = "test-nickname-2"
result = defaultdict(list)
page = 330074
end = 2
for i in range(end):
    MapleAPI_Parser.get_nickname_in_targets(page+i, result, [2, 3])
print(f'send message to {kafka_topic}:')
json_data = {'start_page':page, 'end_page':page+end, 'nicknames':result[2]}
print(result[2])
Producer.produce_topic(kafka_broker, kafka_topic, json_data)


