import http.client
import json
from pymongo import MongoClient

conn = http.client.HTTPSConnection("tiktok-creative-center-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "1e66fa7cdemsh8222358b1d09243p18a33cjsncedf664a581d",
    'x-rapidapi-host': "tiktok-creative-center-api.p.rapidapi.com"
}

conn.request("GET", "/api/trending/hashtag?page=1&limit=20&period=120&country=US&sort_by=popular", headers=headers)

res = conn.getresponse()
data = res.read()

jsonData = json.loads(data.decode("utf-8"))

trend_list = jsonData["data"]["list"]

uri = "mongodb+srv://root:root@hacknarok.quwkjxf.mongodb.net/?retryWrites=true&w=majority&appName=Hacknarok"

client = MongoClient(uri)
db = client["Hacknarok"]
collection = db["Tiktok"]

for trend in trend_list:
    hashtag_name = trend.get("hashtag_name") or None
    country = trend.get("country_info", {}).get("value") or None
    is_promoted = trend.get("is_promoted") or False
    timestamp = trend.get("trend") or []
    creators = trend.get("creators") or []
    publish_count = trend.get("publish_cnt") or 0
    video_views = trend.get("video_views") or 0

    all_nicknames = []
    for creator in creators:
        all_nicknames.append(creator.get("nick_name"))

    print(hashtag_name, country, is_promoted, all_nicknames, publish_count, video_views)

    collection.insert_one({
        "title": hashtag_name,
        "country": country,
        "is_promoted": is_promoted,
        "creators": all_nicknames,
        "publish_count": publish_count,
        "video_views": video_views,
        "timestamps": timestamp,
    })
