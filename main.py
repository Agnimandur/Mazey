import os
from discord.ext import commands
from discord_components import Button, Select, SelectOption, ComponentsBot
from maze import Maze


bot = ComponentsBot("$")

bot.author_id = 880558753064300545
INVITE = "https://discord.com/api/oauth2/authorize?client_id=939012914050900069&permissions=8&scope=bot"

@bot.event 
async def on_ready():
	print("I'm in")
	print(bot.user)

extensions = [
	'cogs.developer','cogs.error','cogs.player'
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

token = os.environ['DISCORD_BOT_SECRET']
bot.run(token)