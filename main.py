import asyncio
import logging as log
from pathlib import Path

import discord
from discord.ext import commands

from utils import rand_speech

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='^', intents=intents)
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

@bot.event
async def on_ready():
	message = rand_speech(f'The bot has succesfully logged in as {bot.user}')
	log.info(message)

async def load_extensions():
	for cog in Path('./cogs').glob('*'):
		if cog.stem not in ['__init__', '__pycache__']:
			await bot.load_extension(f'cogs.{cog.stem}')

async def main():
	async with bot:
		await load_extensions()
		with open('token.txt', 'r') as f:
			token = f.read()
		await bot.start(token)

if __name__ == '__main__':
	asyncio.run(main())