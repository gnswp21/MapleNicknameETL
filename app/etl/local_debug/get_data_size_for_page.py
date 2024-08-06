from app.processor.MapleAPI_Parser import *
from collections import defaultdict
import json
page = 1
result = defaultdict(list)
for page in range(1, 2):
    get_ranking_page(page, result)
# print(result)

serialized_message = json.dumps(result)
message_size = len(serialized_message.encode('utf-8'))

# print(f"Serialized message: {serialized_message}")
print(f"Message size in bytes: {message_size}")
print(message_size * 23000, "Byte")
print(f"Total data size is {message_size * 23000 / 10**9:.3}GB")
