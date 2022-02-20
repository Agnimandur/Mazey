import discord
from discord.ext import commands
import time
import requests
from maze import Maze
from replit import db
import json

from discord_components import ActionRow, Button, ButtonStyle, Select, SelectOption

class Player(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return ctx.channel.category.name=='Mazey'
	
	@commands.command(name='maze',brief="creates a maze. Reach the goal to win!",help="Create a maze with dimensions NxM. Due to restrictions, N and M must be even, and 6 <= N,M <= 50. The goal is to reach the red square using the buttons to move around. Use the seed parameter to play the same maze multiple times. Press cancel to terminate the game.")
	async def mazeCommand(self,ctx,N,M,seed=None):
		if str(ctx.channel.id) in db.keys(): return
		
		async def callback(interaction):
			channel = interaction.raw_data['message']['channel_id']
			if channel not in db.keys(): return
			d = json.loads(db[channel])
			m = Maze(d['maze'],d['center'],d['player'],message=d['message'],moves=d['moves'])
			if m.player != ctx.author.id and (not ctx.author.guild_permissions.administrator): return

			gameMessage = await ctx.channel.fetch_message(m.message)
			if interaction.custom_id=="cancel":
				del db[str(ctx.channel.id)]
				await gameMessage.delete()
				await interaction.send("Game cancelled!")
			elif m.move(interaction.custom_id):
				db[channel] = json.dumps(m.__dict__)
				if m.atgoal():
					await gameMessage.edit(m.render_maze(),delete_after=10)
					del db[str(ctx.channel.id)]
					await interaction.send(f"Congratulations {ctx.author.mention}, you finished the maze in only {m.moves} moves! The best path was {m.fastest()} moves.")
				else:
					await interaction.edit_origin(m.render_maze())
			else:
				await interaction.send("INVALID MOVE!")

		N = int(N)
		M = int(M)
		m = Maze(N,M,ctx.author.id,seed=seed)
		message = await ctx.send(m.render_maze(),components=ActionRow([
				self.bot.components_manager.add_callback(
					Button(style=ButtonStyle.blue, custom_id="left",label="Left"), callback,
				),self.bot.components_manager.add_callback(
					Button(style=ButtonStyle.blue, custom_id="right", label="Right"), callback,
				),self.bot.components_manager.add_callback(
					Button(style=ButtonStyle.blue, custom_id="up", label="Up"), callback,
				),self.bot.components_manager.add_callback(
					Button(style=ButtonStyle.blue, custom_id="down", label="Down"), callback,
				),self.bot.components_manager.add_callback(
					Button(style=ButtonStyle.red, custom_id="cancel", label="Cancel"), callback,
				)
		]))
		m.message = message.id
		db[str(ctx.channel.id)] = json.dumps(m.__dict__)	

def setup(bot):
	bot.add_cog(Player(bot))