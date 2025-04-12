import http.client
import json

conn = http.client.HTTPSConnection("tiktok-creative-center-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "1e66fa7cdemsh8222358b1d09243p18a33cjsncedf664a581d",
    'x-rapidapi-host': "tiktok-creative-center-api.p.rapidapi.com"
}

conn.request("GET", "/api/trending/hashtag?page=1&limit=20&period=120&country=US&sort_by=popular", headers=headers)

res = conn.getresponse()
data = res.read()

# # Parse JSON string to dict
jsonData = json.loads(data.decode("utf-8"))

print(json.dumps(jsonData, indent=2))
