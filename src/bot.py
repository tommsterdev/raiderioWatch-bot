import discord
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import random
import urllib3
from urllib3 import exceptions
import json
import logging


intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
URL_ENDPOINT = os.getenv("API_URL")


client = discord.Client(intents=intents)

http = urllib3.PoolManager(num_pools=10)


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith("!rat"):
        percent_rat = random.randint(1, 101)
        result = f"{message.author.nick} is {percent_rat}% rat"
        await message.channel.send(result)

    if message.content.startswith("!"):
        result = await parse_command(message.content)
        if not result:
            return
        await message.channel.send(result)


async def parse_command(message: str) -> str:
    if len(message) == 1:
        return ""
    # remove '!' and parse into words
    parsed_message = message[1:].split()
    command: str = parsed_message[0]
    args: List[str] = parsed_message[1:]
    result = f"received command {command} with arguments {args}"
    match command:

        case "score":
            result = await get_score(args)

        case "leaderboard":
            result = await get_leaderboard()

        case "ilvl":
            result = await get_ilvl(args)

        case "best":
            result = await get_best_run(args)

        case "twr":
            result = await get_best_weekly_run(args)

        case _:
            result = ""

    return result


async def get_score(args: List[str]) -> str:
    res = await request_score(args)
    return f"{res['character'].capitalize()}, {res['realm'].capitalize()} m+ score {res['score']}"


async def get_leaderboard() -> str:
    return f"not implemented"


async def get_ilvl(args: List[str]) -> str:
    return f"not implemented for args={args}"


async def get_best_run(args: List[str]) -> str:
    return f"not implemented for args={args}"


async def get_best_weekly_run(args: List[str]) -> str:
    return f"not implemented for args={args}"


async def request_score(query: List[str]) -> Dict[str, Any]:
    if len(query) < 1:
        return {
            "statusCode": 401,
            "error": "bad request",
        }
    elif len(query) < 2:
        realm = "Tichondrius"
    else:
        realm = query[1].capitalize()
    character = query[0].capitalize()
    # TODO: set API for query parameters
    # endpoint = f'{URL_ENDPOINT}?name={name}&realm={realm}'
    endpoint = f"{URL_ENDPOINT}?character={character}&realm={realm}"
    print(endpoint)

    try:
        response = http.request(
            method="GET", url=endpoint, headers={"Content-Type": "application/json"}
        )

        if response.status != 200:
            data = json.loads(response.data.decode("utf-8"))
            print(data)
            logging.info(f"response status code={response.status}, {data}")
            return {
                "statusCode": 401,
                "error": "bad request to api",
            }
        # decode

        data = json.loads(response.data.decode("utf-8"))

        score = data.get("score")

    except exceptions.HTTPError as e:
        return {
            "statusCode": 400,
            "Error": str(e),
        }
    else:
        region = data.get("region", "us")
        # construct response object
        result = {
            "character": character,
            "realm": realm,
            "region": region,
            "score": score,
        }
    return result


client.run(TOKEN)


# if __name__ == '__main__':
#     main()
