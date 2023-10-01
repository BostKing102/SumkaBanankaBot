import discord
from discord.ext import commands
import os
import asyncio
from logger import *
logger = logging.getLogger("bot")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event # создаем событие
async def on_ready(): # бот зашел в сеть
    print('[SYSTEM]: основной файл успешно запущена!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Проверяем АнтиБлат')) # создаем активность боту
    await bot.tree.sync()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def start():
    await load()
    await bot.start('MTExODU3MTk5NjU5MTE4MTkyNQ.GLH6nH.W8pzceg8WprAz7g06etQ5y76le1JO9FKmnSWkk')

asyncio.run(start())