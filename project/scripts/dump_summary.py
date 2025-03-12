import json

import requests

url_base = "http://localhost:8004"  # local
payload = {"url": "testurl"}
url_summaries = f"{url_base}/summaries/"
res = requests.post(url=url_summaries, data=json.dumps(payload))
print(res.status_code)
print(res.json())
