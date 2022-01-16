import requests
import json

url = 'http://127.0.0.1:8000/'

r = requests.get(url + "FindByAddress/20")
print(r.json())

r = requests.get(url + "FindAunt")
print(r.json())

