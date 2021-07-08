
token = "ODUzODE1NTMwMDgzMDU3NjY0.YMa3rQ.1slIk_BuRjX0XwROW-rzvYQk9OA"
import discord
import discordslashcommands as dsc
from discord.ext import commands
import random
from google_trans_new import google_translator  
translator = google_translator()  

import asyncio
client = commands.Bot(command_prefix="+")

@client.command(name="st", help="Translates the text")
async def st(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=2).flatten()
    i=0
    for msg in messages:
        if i==0:
            i+=1
        else:
            strs=msg.content
            a= translator.translate(strs,lang_tgt='en')
            # a= await g.translate(a,"es")
            # a=await g.translate(a,"zh")
            # a=await g.translate(a,"zh")
            # a= await g.translate(a,"th")
            # a=await g.translate(a,"ko")
            # a=await g.translate(a,"ja")
            # a= await g.translate(a,"eo")
            # a= await g.translate(a,"en")
            await ctx.send(a)
client.run(token)