from discord.ext.commands import Cog, command, BucketType, cooldown, BadArgument
from discord import Member
from typing import Optional

class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="hello", aliases=["hi"])
	@cooldown(1, 5, BucketType.user)
	async def greet(self, ctx):
		await ctx.send(f"Hello {ctx.author.mention}!")

	@command(name="not_normally", aliases=["notnormally"])
	@cooldown(1, 5, BucketType.user)
	async def not_normally(self, ctx):
		with open("./data/txt/not_normally.txt", "r", encoding="utf-8") as nn:
			await ctx.send(ctx.author.mention + " " +nn.read())
	
	@command(name="slap", aliases=["hit"])
	@cooldown(1, 5, BucketType.user)
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
		await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}")

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("I can't find that member.")

	@Cog.listener()
	async def on_ready(self):
		#print("fun cog ready")
		return

def setup(bot):
	#bot.add_cog(Fun(bot))
	return