import os
import http.client
import json
from datetime import datetime, timedelta

from pymongo import MongoClient


def lambda_handler(event, context):
    conn = http.client.HTTPSConnection("tiktok-creative-center-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': os.environ["RAPIDAPI_KEY"],  # Pobierz z zmiennej środowiskowej
        'x-rapidapi-host': "tiktok-creative-center-api.p.rapidapi.com"
    }

    conn.request("GET", "/api/trending/hashtag?page=1&limit=20&period=120&country=US&sort_by=popular", headers=headers)

    res = conn.getresponse()
    data = res.read()

    jsonData = json.loads(data.decode("utf-8"))

    trend_list = jsonData["data"]["list"]

    MONGO_URI = os.environ["MONGODB_URI"]  # Pobierz z zmiennej środowiskowej

    client = MongoClient(MONGO_URI)
    db = client["Hacknarok"]
    collection = db["TikTok"]

    for trend in trend_list:
        hashtag_name = trend.get("hashtag_name") or None
        country = trend.get("country_info", {}).get("value") or None
        is_promoted = trend.get("is_promoted") or False
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
            "date": datetime.now()
        })

    return {
        'statusCode': 200,
        'body': json.dumps('Data inserted successfully')
    }
