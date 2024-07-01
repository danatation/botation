import datetime
import platform
import random
from pathlib import Path
from typing import Literal, TypedDict

import discord
from discord import TextChannel, app_commands
from discord.ext import commands, tasks

from utils import bulb_speech


class ResponseInfo(TypedDict):
	file: Path
	attachment: discord.File
	embed: discord.Embed

class MemeSender(commands.Cog):
	def __init__(self, bot):
		self.bot = bot		

	def select_meme(self, filetype: Literal['video', 'image'], name: str='') -> ResponseInfo:
		if platform.machine == 'aarch64':
			# Bot is running off a phone
			if filetype == 'video':
				meme_dir = Path('/storage/emulated/0/Movies/Memes/')
			else:
				meme_dir = Path('/storage/emulated/0/Pictures/Memes')
		else:
			if filetype == 'video':
				meme_dir = Path('/home/bulb/Videos/Memes')
			else:
				meme_dir = Path('/home/bulb/Pictures/Memes')
		
		files = sorted(meme_dir.glob('*'))
		if name != '':
			file_names = [file.name for file in files]
			file_index = file_names.index(name)
			# await interaction.followup.send(f'{name} does not exist. Fucking moron. try adding .mp4 at the end or soemthig')
			file = files[file_index]
		else:
			file = random.choice(files)

		date_added = datetime.datetime.fromtimestamp(file.stat().st_mtime, tz=datetime.timezone.utc)

		attachment = discord.File(file)

		embed = discord.Embed(title=f'{file.name}', timestamp=date_added)

		return {
			'file': file,
			'attachment': attachment,
			'embed': embed
		}

	@app_commands.command(name='send_meme', description='If no name is specified, this sends a random meme from my computer')
	async def send_meme(self, interaction: discord.Interaction, filetype: Literal['video', 'image'], name: str=''):
		
		response_data = self.select_meme(filetype, name=name)
		embed = response_data['embed']
		file = response_data['file']
		attachment = response_data['attachment']

		await interaction.response.defer()
		
		if filetype == 'image':
			embed.set_image(url=f'attachment://{file.name}')
			await interaction.followup.send(embed=embed, file=attachment)
		elif isinstance(interaction.channel, TextChannel):
			await interaction.followup.send(embed=embed)
			await interaction.channel.send(file=attachment)
		else:
			await interaction.followup.send(bulb_speech('something went wrong'))

	@tasks.loop(minutes=30)
	async def send_task(self):
		channel = self.bot.get_channel(1243988547048964258)

		if random.randint(0, 1) == 1:
			response_info = self.select_meme('video')
			await channel.send(embed=response_info['embed'])
			await channel.send(file=response_info['attachment'])
		else:
			response_info = self.select_meme('image')
			await channel.send(embed=response_info['embed'], file=response_info['attachment'])

	@commands.Cog.listener()
	async def on_ready(self):
		if not self.send_task.is_running():
			self.send_task.start()

async def setup(bot):
	await bot.add_cog(MemeSender(bot))