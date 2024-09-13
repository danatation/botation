import random

from discord.ext import commands

from utils.christtt_data import (album_responses, christtt_albums,
                                 christtt_tracks, track_responses)


class ChristttReference(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author != self.bot.user and random.randint(0, 6) == 1:
			for album in christtt_albums:
				if album in message.content.lower():
					response = random.choice(album_responses).format(album=album)
					reply = f'{response} \nhttps://christtt.bandcamp.com/album/{christtt_albums[album]}'
					await message.reply(reply)
				for track in christtt_tracks[album]:
					if track in message.content.lower():
						response = random.choice(track_responses).format(album=album, track=track)
						reply = f'{response} \nhttps://christtt.bandcamp.com/track/{christtt_tracks[album][track]}'
						await message.reply(reply)


async def setup(bot):
	await bot.add_cog(ChristttReference(bot))
