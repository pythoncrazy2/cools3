
token = "ODUzODE1NTMwMDgzMDU3NjY0.YMa3rQ.1slIk_BuRjX0XwROW-rzvYQk9OA"
import discord
import discordslashcommands as dsc
from discord.ext import commands
import random
import glob
client = commands.Bot(command_prefix="+")


@client.event
async def on_interaction(member, interaction):
    interaction.call_on_message("+")  # we do anything here, but we translate to a classic message


@client.command(name="amogus", help="Posts a random image related to the popular game Among us. Run by +amogus")
async def amoguspasta(ctx):
    file_path_type = ["./amogusimg/*.png", "./amogusimg/*.jpg"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    await ctx.send(file=discord.File(random_image))


@client.event
async def on_ready():
    manager = dsc.Manager(client)  # DON'T FORGET THAT


client.run(token)