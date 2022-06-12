from discord.ext.commands import Cog, command, BucketType, cooldown, CheckFailure, has_permissions
from ..db import db

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="prefix", brief="Change server prefix" ,help="Change command prefix to the text typed as argument.")
	@cooldown(1, 10, BucketType.user)
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new: str):
		if len(new) > 5:
			await ctx.send("The prefix cannot be more than 5 characters.")
		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
			await ctx.send(f"Prefix is set to {new}.")

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("You need the Manage Message permission to do that.")


	@Cog.listener()
	async def on_ready(self):
		print("misc cog ready")

def setup(bot):
	bot.add_cog(Misc(bot))