import random

from discord.ext import commands
from discord import ui
import discord

from utils import bulb_speech


class CaptchaGiver(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if random.randint(0, 100) == 0 and message.author != self.bot.user:
			view = CaptchaButton()
			await message.reply('We have detected abnormal activity from your device. You\'ll need to verify if you\'re a human by solving an anonymous Captcha.', view=view)

class CaptchaButton(ui.View):
	@ui.button(
		label='Take Captcha',
		emoji='🤖',
		style=discord.ButtonStyle.danger
	)
	async def on_click(self, interaction: discord.Interaction, button: ui.Button):
		captcha_modal = CaptchaModal()
		await interaction.response.send_modal(captcha_modal)

class CaptchaModal(ui.Modal, title='Captcha'):
	short_question = [
		'Who was the first person to walk on the Moon?',
		'What is Valve\'s biggest game yet?',
		'do you fw vns',
		'When is my birthday?',
		'Do you have a lover? (answer truthfully)',
		'Do you promise to never cause harm on anyone?',
		'Are you a virgin? (answer truthfully)',
		'Do you find the big hit "Hawk Tuah" funny?',
		'Do you like cats?'
	]
	
	long_question = [
		'Write a short essay on global warming.',
		'Write a short essay about inflation.',
		'Confess all of your sins here.',
		'Write a Stephen King book in under an hour.'
	]

	short_challenge = ui.TextInput(label=random.choice(short_question))
	long_challenge = ui.TextInput(label=random.choice(long_question), style=discord.TextStyle.paragraph)
	math_challenge = ui.TextInput(label=f'Solve {random.randint(0, 100)} {random.choice(['+', '-', '/', '*', '^'])} {random.randint(0, 100)}')


	async def on_submit(self, interaction: discord.Interaction) -> None:
		embed = discord.Embed()
		embed.add_field(name=self.short_challenge.label, value=self.short_challenge.value)
		embed.add_field(name=self.long_challenge.label, value=self.long_challenge.value)
		embed.add_field(name=self.math_challenge.label, value=self.math_challenge.value)
		await interaction.response.send_message(f'User {interaction.user.mention} has answered the Capthca. Here are their answers!', embed=embed)
		if isinstance(interaction.channel, discord.TextChannel):
			await interaction.channel.send('You have not passed the Captcha. A human worker will evaluate your account and determine if you\'re a real person.')

async def setup(bot):
	await bot.add_cog(CaptchaGiver(bot))