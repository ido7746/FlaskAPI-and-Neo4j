import requests
import json

url = 'http://127.0.0.1:8000/'

print("+++++++++heyyyyyyyy++++++++++++")
r = requests.get(url + "FindByAddress/20")
print("+++++++++heyyyyyyyy++++++++++++")
print(r.json())
print("+++++++++heyyyyyyyy++++++++++++")

r = requests.get(url + "FindAunt")
print(r.json())

