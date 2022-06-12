from discord.ext.commands import Bot as BotBase, CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, when_mentioned_or, has_permissions, command
from discord.errors import HTTPException, Forbidden
from discord import Intents, Embed, File
from datetime import datetime
from ..db import db
from glob import glob
import os


OWNER_IDS = [413332103690846208]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTION = (CommandNotFound, BadArgument)

def get_color():
	with open("./data/txt/color_code.txt", "r", encoding="utf-8") as tf:
		return tf.read()

color = int(get_color())
	
def get_prefix(bot, message):
	PREFIX = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
	return when_mentioned_or(PREFIX)(bot, message)

class Bot(BotBase):
	def __init__(self):
		self.ready = False
		self.guild = None
		super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS, intents=Intents.all())

	def setup(self):
		self.load_extension("lib.cogs.copypasta")
		self.load_extension("lib.cogs.help")
		self.load_extension("lib.cogs.meta")
		self.load_extension("lib.cogs.misc")
		# for cog in COGS:
		# 	self.load_extension(f"lib.cogs.{cog}")
		# 	print(f"{cog} cog loaded")

	def run(self):
		print("running setup")
		self.setup()
		with open("./lib/bot/token", "r", encoding="utf-8") as tf:
			token = tf.read()
		self.TOKEN = token

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	def update_db(self):
		for guild in self.guilds:
			db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)", (guild.id,))
		db.commit()
		
	async def on_connect(self):
		print("bot connected")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_ready(self):
		if not self.ready:	
			# self.guild = self.get_guild(761083310654619659)
			# self.stdout = self.get_channel(761083310654619662)
			self.update_db()
			meta = self.get_cog("Meta")
			await meta.set()
			self.ready = True
			print("bot ready")
			# embed = Embed(title="Now online", description="CopyPasta bot is now online.", color=color, timestamp=datetime.utcnow())
			# await self.stdout.send(embed=embed)
		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong.")
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass
		elif isinstance(exc, BadArgument):
			pass
		elif isinstance(exc, HTTPException):
			await ctx.send("Unable to send message.")
		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more arguments are missing.")
		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f"The command is on cooldown. Try again in {exc.retry_after:,.2f} seconds.")
		elif hasattr(exc, "orginal"):
			if isinstance(exc, Forbidden):
				await ctx.send("I do not have permission to do that.")
			else:
				raise exc.original
		else: 
			raise exc

bot = Bot()
