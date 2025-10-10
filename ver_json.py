import requests
import json

url = "https://mtpe-candidatos.empleosperu.gob.pe/api/jobs?limit=1&offset=0"
response = requests.get(url)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
