# a very very basic bot
import disnake
from disnake.ext import commands
from os import getenv

# lets us know in the console (for manual runs) that we're in
print("[Python] Bot started!")

# prefix > for commands, and all intents
bot: commands.Bot = commands.Bot(">", intents=disnake.Intents.all())

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
