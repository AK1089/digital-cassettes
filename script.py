# a very very basic bot
import disnake
from disnake.ext import commands
from os import getenv

# prefix > for commands
bot: commands.Bot = commands.Bot(">")

@bot.command(name="echo")
async def echo(ctx: commands.Context, *text: list[str]):
    await ctx.send(" ".join(text))

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.errors.CommandNotFound): return
    else: raise error

@bot.event
async def on_ready():
    bot.remove_command("help")

bot.run(getenv("DISCORD_BOT_TOKEN"))
