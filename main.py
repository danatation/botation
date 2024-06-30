import random, logging, datetime
from typing import Literal
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands
from christtt import christtt_albums, christtt_tracks, album_responses, track_responses

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='^', intents=intents)

@bot.event
async def on_ready():
	print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		print(f'plup: {message.content}')
	else:
		if random.randint(0, 6) == 1:
			for album in christtt_albums:
				if album in message.content.lower():
					response = random.choice(album_responses).format(album=album)
					await message.reply(f'{response} \nhttps://christtt.bandcamp.com/album/{christtt_albums[album]}')
				for track in christtt_tracks[album]:
					if track in message.content.lower():
						response = random.choice(track_responses).format(album=album, track=track)
						await message.reply(f'{response} \nhttps://christtt.bandcamp.com/track/{christtt_tracks[album][track]}')
		else:
			print(f'{message.author}: {message.content}')

@bot.tree.command(name='coinflip')
async def coinflip(interaction: discord.Interaction):
	if random.randint(0, 1) == 1:
		await interaction.response.send_message('heads...')
	else:
		await interaction.response.send_message('tails...')

@bot.tree.command(name='send_meme')
async def send_meme(interaction: discord.Interaction, filetype: Literal['video', 'image'], name: str=''):
	video_dir = Path('/home/bulb/Videos/Memes')
	image_dir = Path('/home/bulb/Pictures/Memes')

	if filetype == 'video':
		cwd = video_dir
	if filetype == 'image':
		cwd = image_dir
	
	files = sorted(cwd.glob('*'))
	if name != '':
		file_names = [file.name for file in files]
		file_index = file_names.index(name)
		# await interaction.followup.send(f'{name} does not exist. Fucking moron. try adding .mp4 at the end or soemthig')
		file = files[file_index]
	else:
		file_index = random.randint(0, len(files))
		file = files[file_index]

	date_added = datetime.datetime.fromtimestamp(file.stat().st_mtime, tz=datetime.timezone.utc)

	attachment = discord.File(file)

	embed = discord.Embed(title=f'{file.name}', timestamp=date_added)
	await interaction.response.defer()
	
	if filetype == 'image':
		embed.set_image(url=f'attachment://{file.name}')
		await interaction.followup.send(embed=embed, file=attachment)
	else:
		await interaction.followup.send(embed=embed)
		await interaction.channel.send(file=attachment)

@bot.tree.command(name='sync')
async def sync(interaction: discord.Interaction, method: Literal['global', 'local']):
	await interaction.response.send_message(f'syncing {method}ly...', ephemeral=True)
	if method == 'global':
		await bot.tree.sync(guild=interaction.guild)
	else:
		await bot.tree.sync()

with open('token.txt', 'r') as f:
	bot.run(f.read())