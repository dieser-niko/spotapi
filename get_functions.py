import json
import re

import requests

s = requests.Session()

# source files for other .js links
response = s.get("https://open.spotify.com")
js_links = re.findall(r"<script src=\"(?P<link>.[^\"]+)\"><\/script>", response.text)
response = s.get("https://open.spotify.com/service-worker.js")
js_links += re.findall(r"'(?P<link>https:\/\/open\.spotifycdn\.com.[^']+\.js)'", response.text)

all_results = {}

function_re = re.compile(r'(?P<i>\d+):\([a-z,]+\)=>')
dict_re = re.compile(r'{')
call_re = re.compile(r'[a-z]\(\d+\)')
operation_re = re.compile(r'\("(?P<name>\w+)","(?P<type>\w+)","(?P<hash>[\da-f]{64})",(?P<value>.[^)]+)\)')

# going through each script mentioned in the source files
for link in list(set(js_links)):
    results = {}
    all_results[link] = results
    print(link)
    response = s.get(link)
    for query in function_re.finditer(response.text):
        start = query.span()[1]
        counter = 1
        index = 0
        for index, char in enumerate(response.text[start + 1:]):
            match char:
                case "{":
                    counter += 1
                case "}":
                    counter -= 1
                    if not counter:
                        break
        if not index:
            continue

        function = response.text[start:start + index + 2]

        function_index = query.group("i")
        if function_index not in results:
            results[function_index] = {"calls": call_re.findall(function), "variables": [], "operations": {}}

        # search variables
        for query in dict_re.finditer(function):
            start = query.span()[1]
            counter = 1
            index = 0
            for index, char in enumerate(function[start:]):
                match char:
                    case "{":
                        counter += 1
                    case "}":
                        counter -= 1
                        if not counter:
                            break
            if not index:
                continue
            result = function[start - 1:start + index + 1]
            if "=" in result or ":" not in result or "return" in result:
                continue
            results[function_index]["variables"].append(result)

        # search operations
        queries = operation_re.findall(function)
        for query in queries:
            name = query[0]
            # item = {"type": query[1], "hash": query[2], "value": query[3]}
            if query[1] not in results[function_index]["operations"]:
                results[function_index]["operations"][query[1]] = {}
            if name not in results[function_index]["operations"][query[1]]:
                results[function_index]["operations"][query[1]][name] = {}
            if query[2] not in results[function_index]["operations"][query[1]][name]:
                results[function_index]["operations"][query[1]][name][query[2]] = []
            results[function_index]["operations"][query[1]][name][query[2]].append(link)

with open("functions.json", "w", encoding="utf-8") as fobj:
    json.dump(all_results, fobj, indent=4)
