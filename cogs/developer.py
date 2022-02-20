import discord
from discord.ext import commands
import time
import requests
from maze import Maze
from replit import db
import json

from discord_components import ActionRow, Button, ButtonStyle, Select, SelectOption

class Developer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return ctx.channel.category.name=='Mazey' or ctx.author.guild_permissions.administrator

	@commands.command(name='setup',help='Setup the Mazey Bot')
	async def setup(self,ctx):
		mazey = await ctx.guild.create_category('Mazey')
		for i in [1,2,3]:
			await mazey.create_text_channel(f"game {i}")

	@commands.command(name='cancel',help="Manually end an ongoing game.")
	async def cancel(self,ctx):
		if str(ctx.channel.id) not in db.keys():
			await ctx.reply("No active game!")
		else:
			del db[str(ctx.channel.id)]
			await ctx.reply("Game cancelled!")

	@commands.command(name='mazejson',help="Fetch the json of an ongoing game")
	async def mazejson(self,ctx):
		if str(ctx.channel.id) not in db.keys():
			await ctx.reply("No active game!")
		else:
			d = json.loads(db[str(ctx.channel.id)])
			await ctx.send(str(d))

def setup(bot):
	bot.add_cog(Developer(bot))