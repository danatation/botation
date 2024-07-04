import asyncio
from datetime import datetime
import platform
import random
from pathlib import Path
from typing import List, Literal, TypedDict
from os import environ

import discord
from discord import IntegrationApplication, TextChannel, app_commands
from discord.ext import commands, tasks
from discord.webhook.async_ import interaction_message_response_params

import config
from utils import bulb_speech


class MemeSender(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def meme_picker(self, mimetype: Literal['video', 'image'] | None = None, name: str | None = None):
		paths = {
			'video': config.video_path,
			'image': config.image_path
		}

		if mimetype:
			work_dir = Path(paths[mimetype])
		else:
			work_dir = Path(random.choice(list(paths.values())))

		files = sorted(work_dir.glob('*'))
		# size_limit = discord.Guild.filesize_limit
		size_limit = 25 * 1_000_000 # servers have a limit of 25mb by default

		if name is None:
			while True:
				file = random.choice(files)
				if file.stat().st_size <= size_limit:
					return file 
		else:
			file = work_dir / name
			if file.exists():
				if file.stat().st_size <= size_limit:
					return file
				else:
					return 'The file is too big to be sent!'
			else:
				return 'The file couldn\'t be found!'

	@app_commands.command(name='send_meme', description='If no name is specified, this sends a random meme from my computer')
	async def meme_sender(self, interaction: discord.Interaction, filetype: Literal['video', 'image'] | None = None, name: str | None = None):
		file = self.meme_picker(filetype, name)

		if isinstance(file, str):
			message = bulb_speech(file)
			await interaction.response.send_message(message)
		elif isinstance(interaction.channel, discord.TextChannel):
			file_size = file.stat().st_size / 1_000_000 # in MB
			file_date = datetime.fromtimestamp(file.stat().st_ctime)

			if file.suffix in ['.mp4', '.mov']:
				attachment = discord.File(file, filename=file.name)
				embed = discord.Embed(timestamp=file_date, title=f'{file.name} · {file_size:.2f}MB')
				embed.set_image(url=f'attachment://{file.name}')
				await interaction.response.defer()
				await interaction.followup.send(file=attachment, embed=embed)
			else:
				attachment = discord.File(file, filename=file.name)
				await interaction.response.defer()
				await interaction.followup.send(f'{file.name} · {file_size:.2f}MB', file=attachment)
				await interaction.channel.send(f'{file_date.day}.{file_date.month}.{file_date.year} {file_date.hour}:{file_date.minute}')

	@tasks.loop(minutes=30)
	async def send_task(self):
		if self.send_task.current_loop == 0:
			return
		
		if config.meme_channel_id == None:
			return

		while True:
			file = self.meme_picker()
			if isinstance(file, Path):
				break
		channel = self.bot.get_channel(config.meme_channel_id)

		file_size = file.stat().st_size / 1_000_000 # in MB
		file_date = datetime.fromtimestamp(file.stat().st_ctime)

		if file.suffix in ['.mp4', '.mov']:
			attachment = discord.File(file, filename=file.name)
			embed = discord.Embed(timestamp=file_date, title=f'{file.name} · {file_size:.2f}MB')
			embed.set_image(url=f'attachment://{file.name}')
			await channel.send(file=attachment, embed=embed)
		else:
			attachment = discord.File(file, filename=file.name)
			await channel.send(f'{file.name} · {file_size:.2f}MB', file=attachment)
			await channel.send(f'{file_date.day}.{file_date.month}.{file_date.year} {file_date.hour}:{file_date.minute}')

	@commands.Cog.listener()
	async def on_ready(self):
		if not self.send_task.is_running():
			self.send_task.start()

async def setup(bot):
	await bot.add_cog(MemeSender(bot))