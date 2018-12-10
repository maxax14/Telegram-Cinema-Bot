import json

with open("src/keys.json") as f:
    keys = json.load(f)

TG_API_TOKEN = keys["TG_API_TOKEN"]
TG_PROXY_KEY = keys["TG_PROXY_KEY"]
