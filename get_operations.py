"""
This script is outdated. It can only extract operations and their hashes from Spotify's JavaScript files.
"""

import json
import re

import requests

s = requests.Session()

# source files for other .js links
response = s.get("https://open.spotify.com")
js_links = re.findall(r"<script src=\"(?P<link>.[^\"]+)\"><\/script>", response.text)
response = s.get("https://open.spotify.com/service-worker.js")
js_links += re.findall(r"'(?P<link>https:\/\/open\.spotifycdn\.com.[^']+\.js)'", response.text)

results = {}

# going through each script mentioned in the source files
for link in js_links:
    print(link)
    response = s.get(link)
    queries = re.findall(r'\("(?P<name>\w+)","(?P<type>\w+)","(?P<hash>[\da-f]{64})",(?P<value>.[^)]+)\)',
                         response.text)
    for query in queries:
        name = query[0]
        # item = {"type": query[1], "hash": query[2], "value": query[3]}
        if query[1] not in results:
            results[query[1]] = {}
        if name not in results[query[1]]:
            results[query[1]][name] = {}
        if query[2] not in results[query[1]][name]:
            results[query[1]][name][query[2]] = []
        results[query[1]][name][query[2]].append(link)

with open("operations.json", "w", encoding="utf-8") as fobj:
    json.dump(results, fobj, indent=4)
