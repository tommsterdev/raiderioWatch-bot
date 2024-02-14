import json
import asyncio
import urllib3
from typing import Dict, List
from urllib3 import PoolManager
from urllib3.exceptions import TimeoutError, MaxRetryError
from dotenv import load_dotenv
import os

# send http request
# construct response object *
# return response object

# types
JSON = int | str | float | bool | None | Dict[str, "JSON"] | List["JSON"]
JSONObject = dict[str, "JSON"]

http = PoolManager(num_pools=10)
load_dotenv()

URL_ENDPOINT = os.getenv("API_URL")

async def build_request_url(name: str, realm: str) -> str:
    print(f'building api endpoint url for {URL_ENDPOINT}?character={name}&realm={realm}')
    return f"{URL_ENDPOINT}?character={name}&realm={realm}"


def http_get_sync(url: str) -> JSONObject:
    try:
        response = http.request("GET", url=url)

    except urllib3.exceptions.TimeoutError as e:
        print(f'could not retrieve data from{e.url}')

    except urllib3.exceptions.MaxRetryError as e:
        print(f'could not retrieve data from{e.url}')
        
    return response.json()

async def http_get(url: str) -> JSONObject:
    return await asyncio.to_thread(http_get_sync, url)

