# a very very basic bot
import disnake
from disnake.ext import commands
from os import getenv, system

# lets us know in the console (for manual runs) that we're in
print("[Python] Bot started!")

# prefix > for commands, and all intents
bot: commands.Bot = commands.Bot(">", intents=disnake.Intents.all())

# repeats what you say
@bot.command(name="echo")
async def echo(ctx: commands.Context, *text):
    await ctx.send(" ".join(text))

# reboots the Pi on call (so we can do it remotely)
@bot.command(name="reboot")
async def reboot(ctx: commands.Context):

    # only I'm allowed to do this!
    if await bot.is_owner(ctx.author):
        await ctx.send("Rebooting now...")
        system('sudo reboot')
    else:
        await ctx.send("You do not have permission to perform this action.")

# ignores errors caused by nonexistent commands
@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.errors.CommandNotFound): return
    else: raise error

# removes the unnecessary help command
@bot.event
async def on_ready():
    bot.remove_command("help")

bot.run(getenv("DISCORD_BOT_TOKEN"))
