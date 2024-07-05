import random	

from discord.ext import commands
import discord


class AnnoyingReactor(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		unfunny_list = [
			'vro',
			'freaky',
			'𝓯𝓻𝓮𝓪𝓴𝔂',
			'👅',
			'john pork',
			'hawk tuah'
		]

		emojis = ['😂', '😹', '🖕', '🤣', '🫃', '🪑', '📴']

		if message.content.lower() in unfunny_list:
			await message.add_reaction(random.choice(emojis))

async def setup(bot):
	await bot.add_cog(AnnoyingReactor(bot))