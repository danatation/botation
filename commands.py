import discord
from discord import commands
from discord.ext import app_commands

async def sync(interaction: discord.Interaction):
	await interaction.response.send_message('syncing...', ephemeral=True)
	await bot.tree.sync(guild=interaction.guild)