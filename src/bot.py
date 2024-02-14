import discord
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import json
import logging
import random
from discord.ext import commands
from discord.ext.commands import Context
from requests import http_get, build_request_url



intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


#client = discord.Client(intents=intents)



@bot.event
async def on_ready() -> None:
    print(f"We have logged in as {bot.user}")


# @bot.event
# async def on_message(message: discord.Message) -> None:
#     if message.author == bot.user:
#         return

#     if message.content.startswith("!rat"):
#         percent_rat = random.randint(1, 101)
#         result = f"{message.author.nick} is {percent_rat}% rat"
#         await message.channel.send(result)


@bot.command(name='test')
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command(name='rat')
async def rat(ctx, arg: Optional[str]):
    if not arg:
        arg = ctx.author.nick
    percent_rat = random.randint(1, 101)
    result = f"{arg} is {percent_rat}% rat"
    await ctx.send(result)

@bot.command(name='roll')
async def roll(ctx):
    await ctx.send('Rolling 1-100')
    rolled = random.randint(1, 101)
    result = f'{ctx.author.nick} rolled {rolled}'
    await ctx.send(result)


@bot.command(name='score', help='gets m+ score for player')
async def get_score(ctx, name: str, realm: Optional[str] = 'Tichondrius'):
    logging.info('get_score called')
    endpoint = await build_request_url(name.capitalize(), realm.capitalize())
    res = await http_get(url=endpoint)
    await ctx.send(f"{res['character']}, {res['realm']} m+ score {res['score']}")

@bot.command(name='ilvl')
async def get_ilvl(ctx, name: str, realm: Optional[str] = 'Tichondrius'):
    endpoint = await build_request_url(name.capitalize(), realm.capitalize())
    res = await http_get(url=endpoint)
    await ctx.send(f"{res['character']}, {res['realm']} ilvl {res['ilvl']}")


async def get_leaderboard() -> str:
    return f"not implemented"

async def get_best_run(args: List[str]) -> str:
    return f"not implemented for args={args}"


async def get_best_weekly_run(args: List[str]) -> str:
    return f"not implemented for args={args}"


bot.run(TOKEN)


# if __name__ == '__main__':
#     main()
