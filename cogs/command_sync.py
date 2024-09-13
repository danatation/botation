from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands


class CommandSync(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name='sync',
	                      description='Syncs newly added/modified commands. \
	                                  You will most likely need to restart your client right after')
	async def sync(self, interaction: discord.Interaction, method: Literal['global', 'local']):
		await interaction.response.send_message(f'syncing {method}ly...', ephemeral=True)
		if method == 'global':
			await self.bot.tree.sync(guild=interaction.guild)
		else:
			await self.bot.tree.sync()


async def setup(bot):
	await bot.add_cog(CommandSync(bot))
