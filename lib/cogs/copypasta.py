from discord.ext.commands import Cog, command, BucketType, cooldown, CheckFailure, has_permissions, CommandInvokeError
from discord import Embed
from datetime import datetime
from typing import Optional
from ..db import db

def get_color():
	with open("./data/txt/color_code.txt", "r", encoding="utf-8") as tf:
		return tf.read()

color = int(get_color())

def polish(tuplelist):
	normallist = []
	for tuple in tuplelist:
		normallist.append("".join(tuple))
	return normallist

class CopyPasta(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.cp_list = None

	@command(name="copypasta", aliases=["cp"] ,brief="Show copypasta", help="Show all the copypasta. Enter copypasta id to show spcific copypasta content.")
	async def show_copypasta(self, ctx, cp_id: Optional[str]):
		if cp_id is None:
			cp_tuplelist = db.records("SELECT CopyPastaID, Content FROM copypasta WHERE GuildID = ?", ctx.guild.id)
			if len(cp_tuplelist)>=1:
				await ctx.send(f"{ctx.author.mention} Showing all copypastas.")
				embed = Embed(title="Copypasta", color=color)
				for cp in cp_tuplelist:
					if len(cp[1])<=100:
						embed.add_field(name=cp[0], value=f"{cp[1]}", inline=False)
					else:
						embed.add_field(name=cp[0], value=f"{cp[1][:170]}...", inline=False)
				await ctx.send(embed=embed)
			else:
				await ctx.send("There is currenly no copypasta for this server. Please add one using add command.")
		else:
			cp_tuplelist = db.record("SELECT Content FROM copypasta WHERE GuildID = ? AND CopyPastaID = ?", ctx.guild.id, cp_id)
			if cp_tuplelist is None:
				await ctx.send("I can't find that copypasta.")
				return 0
			await ctx.send(f"{ctx.author.mention} {cp_tuplelist[0]}")

	@command(name="search", brief="Search copypasta", help="Search copypasta by typing in keywords.")
	@cooldown(1, 5, BucketType.user)
	async def search_copypasta(self, ctx, *, keyword):
		cp_tuplelist = db.records("SELECT CopyPastaID, Content FROM copypasta WHERE GuildID = ? AND Content LIKE ?", ctx.guild.id, f"%{keyword}%")
		if len(cp_tuplelist)<1:
			await ctx.send("I can't find copypasta with your keyword.")
			return 0
		await ctx.send(f"{ctx.author.mention}Showing all matched copypastas.")
		embed = Embed(title="Copypasta", color=color)
		for cp in cp_tuplelist:
			embed.add_field(name=cp[0], value=f"{cp[1]}", inline=False)
		await ctx.send(embed=embed)


	@command(name="add", brief="Add copypasta", help="Add your own copypasta by entering copypasta id and content as arguments.")
	@cooldown(1, 5, BucketType.user)
	async def add_copypasta(self, ctx, cp_id, *, copypasta):
		cp_tuplelist = db.records("SELECT CopyPastaID FROM copypasta WHERE GuildID = ?", ctx.guild.id)
		for cp in cp_tuplelist:
			if cp[0] == cp_id:
				await ctx.send("Duplicated copypasta id. Please try again with another id.")
				return 0				
		db.multiexec("INSERT INTO copypasta (CopyPastaID, GuildID, Content) VALUES (?, ?, ?)", (cp_id,ctx.guild.id, copypasta))
		db.commit()
		await ctx.send("Copypasta added. Thanks for contributing.")

	@command(name="edit", brief="Edit copypasta", help="Change specific copypasta content by inserting copypasta id and new content as arguments.")
	@cooldown(1, 5, BucketType.user)
	async def edit_copypasta(self, ctx, cp_id, *, copypasta):
		cp_tuplelist = db.records("SELECT CopyPastaID FROM copypasta WHERE GuildID = ? AND CopyPastaID=?", ctx.guild.id, cp_id)
		if len(cp_tuplelist)<1:
			await ctx.send("The copypasta is not found.")
			return 0
		else:
			db.multiexec("UPDATE copypasta SET Content = ? WHERE CopyPastaID = ? AND GuildID = ?", (copypasta, cp_id, ctx.guild.id))
			db.commit()
			await ctx.send("Copypasta edited. Thanks for contributing.")

	@command(name="delete", brief="Delete copypasta", help="Delete a copypasta by entering copypasta id as argument.")
	@cooldown(1, 5, BucketType.user)
	async def delete_copypasta(self, ctx, cp_id):
		cp_tuplelist = db.records("SELECT CopyPastaID FROM copypasta WHERE GuildID = ? AND CopyPastaID=?", ctx.guild.id, cp_id)
		if len(cp_tuplelist)<1:
			await ctx.send("The copypasta is not found.")
			return 0
		else:
			db.multiexec("DELETE FROM copypasta WHERE CopyPastaID = ? AND GuildID = ?", (cp_id, ctx.guild.id))
			db.commit()
			await ctx.send(f"{cp_id} deleted... :(")

	@Cog.listener()
	async def on_ready(self):
		print("copypasta cog ready")

def setup(bot):
	bot.add_cog(CopyPasta(bot))