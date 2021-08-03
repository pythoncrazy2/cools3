import os
import discord
#from keepalive import keep_alive
import requests
import json
import random
from discord.ext import commands
client = commands.Bot(command_prefix="yavor")

def get_fact():
  response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en%22")
  json_data = json.loads(response.text)
  fact = json_data["text"]
  return(fact)

@client.event
async def on_ready():
  print('ok and')

@client.event
async def on_message(message):
  if message.author.id == 720671710264950784:
    await message.channel.send('danamer')
    
    
    
@client.command()
async def fact(ctx):
    await ctx.send(get_fact())
    

@client.command(aliases=["hi"])
async def hello(ctx):
    mylist = ["Hello!", "Greetings, mortal.", "Hi there!", "Nice to meet you!", "Hey.", "Ahoy!", "‘Ello, gov’nor!"]
    await message.channel.send(random.choice(mylist))

@client.command()
async def whoami(ctx):
    await message.channel.send(message.author)


#keep_alive()
client.run('ODUzODE1NTMwMDgzMDU3NjY0.YMa3rQ.1slIk_BuRjX0XwROW-rzvYQk9OA')