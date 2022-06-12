from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Activity, ActivityType
from ..db import db

class Meta(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def set(self):
		await self.bot.change_presence(activity=Activity(name="hentai", type=ActivityType.watching))

	@command(name="ping", brief="Show bot ping", help="Show bot ping.")
	async def show_ping(self, ctx):
		await ctx.send(f"Pong! DSWP latency: {self.bot.latency*1000:,.0f} ms.")

	@Cog.listener()
	async def on_ready(self):
		print("meta cog ready")

def setup(bot):
	bot.add_cog(Meta(bot))