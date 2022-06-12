
from discord.ext.commands import Cog, command
from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import get
from discord import Embed
from typing import Optional

def get_color():
	with open("./data/txt/color_code.txt", "r", encoding="utf-8") as tf:
		return tf.read()

color = int(get_color())

def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
	params = " ".join(params)
	return f"```{cmd_and_aliases} {params}```"

class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx
	#change command per page in help menu
		super().__init__(data, per_page=5)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title="Help", description="Welcome to CopyPasta Bot help dialog", colour=color)
		embed.set_footer(text=f"{offset} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")
		embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)
		return embed

	async def format_page(self, menu, entries):
		fields=[]
		for entry in entries:
			fields.append((entry.brief, syntax(entry)))
		return await self.write_page(menu, fields)

class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command("help")

	async def cmd_help(self, ctx, command):
		embed = Embed(title=f"Help with {command}", description=syntax(command), colour=color)
		embed.add_field(name="Command description", value=command.help)
		await ctx.send(embed=embed)

	@command(name="help", brief="Show help for commands", help="Show all description and syntax for all commands. Type in command name as argument to show help for specific command.")
	async def show_help(self, ctx, cmd: Optional[str]):
		if cmd is None:
			menu = MenuPages(source=HelpMenu(ctx, list(sorted(self.bot.commands, key=lambda c: c.cog.qualified_name))), delete_message_after=True, timeout=60.0)
			await menu.start(ctx)
		else:
			if (command := get(self.bot.commands, name=cmd)):
				await self.cmd_help(ctx, command)
			else:
				await ctx.send("That command does not exist.")

	@Cog.listener()
	async def on_ready(self):
		print("help cog ready")

def setup(bot):
	bot.add_cog(Help(bot))

