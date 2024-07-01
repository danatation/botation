import random
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from utils import bulb_speech


class JokeCalculator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name='math', description='Proven scientifically accurate. May have tiny inaccuracies due to rounding errors')
	async def math(self, interaction: discord.Interaction, operand1: float, operator: Literal['+', '-', '*', '/', '**'], operand2: float):
		
		if operator == '/' and operand2 == 0:
			result = 'Fuck you'
		else:
			result = eval(f'{operand1}{operator}{operand2}')

		if isinstance(result, float):
			result += random.randint(-5, 5)

		reply = bulb_speech(f'{operand1} {operator} {operand2} is equal to {result}')
		await interaction.response.send_message(reply)

async def setup(bot):
	await bot.add_cog(JokeCalculator(bot))