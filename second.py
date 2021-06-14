
import discord
from discord.ext import commands
from discord.ext import tasks
import os
import glob, random
from PIL import Image, ImageDraw, ImageSequence,ImageFont
client = commands.Bot(command_prefix="+")
import async_google_trans_new as gt
token = "ODUzODE1NTMwMDgzMDU3NjY0.YMa3rQ.1slIk_BuRjX0XwROW-rzvYQk9OA"

@client.command()
async def c(ctx):
    def check(msg):
        return msg.author == ctx.author

    await ctx.send("Testing in progress")

    message = await client.wait_for("message", check=check)
    content = message.content
    await ctx.send(content)
    await ctx.send("Testing has finished")
client.run(token)