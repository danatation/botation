import random

import discord
from discord import app_commands
from discord.ext import commands

from utils import rand_speech


class Coinflip(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name='coinflip', description='Use only in dire situations.')
	async def coinflip(self, interaction: discord.Interaction):
		if random.randint(0, 1) == 1:
			reply = rand_speech('heads')
		else:
			reply = rand_speech('tails')
		await interaction.response.send_message(reply)


async def setup(bot):
	await bot.add_cog(Coinflip(bot))
