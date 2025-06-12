import json

import requests
from spotipy_anon import SpotifyAnon

with open("operations.json", "r") as fobj:
    operations = json.load(fobj)

session = requests.Session()
auth = SpotifyAnon(requests_session=session)


def by_name(operation_type: str, operation_name: str, variables: dict):
    operation = operations.get(operation_type, {}).get(operation_name)
    if not operation:
        raise NameError(f"{operation_type}: {operation_name} not found")
    item = {
        "extensions": {
            "persistedQuery": {
                "sha256Hash": list(operation)[0],
                "version": 1
            },
        },
        "operationName": operation_name,
        "variables": variables
    }
    headers = {
        "authorization": "Bearer " + auth.get_access_token(),
    }
    response = session.post(f"https://api-partner.spotify.com/pathfinder/v2/{operation_type}", json=item,
                            headers=headers)
    response.raise_for_status()
    if response.content:
        return response.json()
    else:
        raise Exception


if __name__ == "__main__":
    a = by_name("query", "home",
                {
                    "facet": "",
                    "sectionItemsLimit": 10,
                    "sp_t": "07f6a0ea0c1deea7f895536b0e09cd88",
                    "timeZone": "Europe/Berlin"
                })
    print(a)
