import logging
from datetime import datetime
from pathlib import Path

import discord
from discord.ext import commands


class MessageLogger(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		Path('./logs').mkdir(exist_ok=True)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		formatted_message = self.format_message(message)
		formatted_reply = ''

		if message.reference is not None and message.reference.message_id is not None:
			reference = await message.channel.fetch_message(message.reference.message_id)
			formatted_reply = f'⬐ Replying to {self.format_message(reference)}'
			print(formatted_reply)
		print(formatted_message)

		with open(f'logs/{message.channel}.txt', 'a') as f:
			if formatted_reply != '':
				f.write(formatted_reply)
				f.write('\n')
			f.write(formatted_message)
			f.write('\n')

	def format_message(self, message: discord.Message) -> str:
		content = message.content
		date = message.created_at.strftime('%H:%M:%S')

		if message.author == self.bot.user:
			author = 'plup'
		else:
			author = message.author

		if message.attachments != []:
			attachments = message.attachments
		else:
			attachments = ''

		return f'{date} {author}: "{message.content}" {attachments}'

async def setup(bot):
	await bot.add_cog(MessageLogger(bot))