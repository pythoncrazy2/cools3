import asyncio, discord, random, json, time, os, PIL, textwrap
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from . import Message, FuzzySearch, GetImage, Utils, DL, DisplayName

def setup(bot):
	# Add the bot and deps
	settings = bot.get_cog("Settings")
	bot.add_cog(Humor(bot, settings))

# This module is for random funny things I guess...

class Humor(commands.Cog):

	def __init__(self, bot, settings, listName = "Adjectives.txt"):
		self.bot = bot
		global Utils, DisplayName
		Utils = self.bot.get_cog("Utils")
		DisplayName = self.bot.get_cog("DisplayName")
		self.settings = settings
		# Setup our adjective list
		self.adj = []
		marks = map(chr, range(768, 879))
		self.marks = list(marks)
		if os.path.exists(listName):
			with open(listName) as f:
				for line in f:
					self.adj.append(line)
		try: self.image = Image.open('images/dosomething.png')
		except: self.image = Image.new("RGBA",(500,500),(0,0,0,0))
		try: self.s_image = Image.open("images/Stardew.png")
		except: self.s_image = Image.new("RGBA",(319,111),(0,0,0,0))
		try: self.slap_image = Image.open("images/slap.png")
		except: self.slap_image = Image.new("RGBA",(800,600),(0,0,0,0))
		self.slap_words = ("walloped","slapped","demolished","obliterated","bonked","smacked")
		self.stardew_gifts = (
			"prismatic shard",
			"seaweed",
			"green algae",
			"diamond",
			"red mushrooms",
			"wool",
			"coal",
			"duck feather",
			"cave carrot",
			"solar essence",
			"vinegar",
			"sweet gem berry",
			"truffle",
			"fish",
			"snail",
			"frozen tear",
			"chicken statue",
			"bone flute",
			"pufferfish",
			"Joja Cola",
			"trash",
			"egg",
			"crispy bass",
			"fish taco",
			"cookie",
			"garlic",
			"weeds",
			"honey",
			"gizmo",
			"cloth",
			"geode"
		)
		self.stardew_responses = (
			"I'm just here for my annual check-up! Don't worry, I'm not preg... I mean, I'm not sick! Heh.",
			"...I hate this.",
			"Buh... Life.",
			"You wish to date me? After how I treated you at first?",
			"What do you want? Leave me alone.",
			"You!!! Was that some kind of sick prank?! Those are very private!",
			"Did you know that my nephew loves 'Beer'? I gave it to him one year and he wouldn't stop talking about it.",
			"Ugh... that's such a stupid gift.",
			"Don't you have work to do?",
			"I'm just here for the free coffee.",
			"I'll be honest. I don't want to dance with you",
			"Me?... Oh, I'm thankful for... how about I just show you when we get home tonight?",
			"Thanks!",
			"Oh, is it my birthday today? I guess it is. Thanks. This is nice.",
			"I wanted to talk to you in private...",
			"Ew... No.",
			"Sometimes I stop and realize that I'm nothing more than a bag of juicy, squishy flesh.",
			"Ah... an Fish Taco! Thanks.",
			"No u.",
			"Thanks... I hate it.",
			"I really should scrub my floorboards today. I think an algae is starting to form.",
			"That was some way to ring in the new year last night...",
			"You scared me, sneaking into my room like that!",
			"So there you have it. You probably figured I hated this chair.",
			"This... Are you trying to hurt me even more?",
			"I thought we had something special... I guess I was wrong.",
			"This... They gave this to me in Gotoro prison camp. I've been trying to forget about that. *shudder*",
			"If I stay perfectly still, perhaps a resplendent butterfly will bless my nose with a landing.",
			"My basket! Thank you. This means a lot to me.",
			"But... You don't need to try and 'help' me... I know best how to live my own life... okay?",
			"This is a great gift. Thank you!",
			"Oh, a birthday gift! Thank you.",
			"All my customers... Here?!?",
			"Grr... sounds like these raccoons are back again. Filthy varmints...",
			"Sometimes I look for crawdads in the river. Don't tell Aunt Marnie... but I fed one to a cow once."
		)
					
	@commands.command(pass_context=True)
	async def zalgo(self, ctx, *, message = None):
		"""Ỉ s̰hͨo̹u̳lͪd͆ r͈͍e͓̬a͓͜lͨ̈l̘̇y̡͟ h͚͆a̵͢v͐͑eͦ̓ i͋̍̕n̵̰ͤs͖̟̟t͔ͤ̉ǎ͓͐ḻ̪ͨl̦͒̂ḙ͕͉d͏̖̏ ṡ̢ͬö̹͗m̬͔̌e̵̤͕ a̸̫͓͗n̹ͥ̓͋t̴͍͊̍i̝̿̾̕v̪̈̈͜i̷̞̋̄r̦̅́͡u͓̎̀̿s̖̜̉͌..."""
		if message == None:
			await ctx.send("Usage: `{}zalgo [message]`".format(ctx.prefix))
			return

		suppress = True

		
		words = message.split()
		try:
			iterations = int(words[len(words)-1])
			words = words[:-1]
		except Exception:
			iterations = 1
			
		if iterations > 100:
			iterations = 100
		if iterations < 1:
			iterations = 1
			
		zalgo = " ".join(words)
		for i in range(iterations):
			if len(zalgo) > 2000:
				break
			zalgo = self._zalgo(zalgo)
		
		zalgo = zalgo[:2000]


		await Message.Message(message=zalgo).send(ctx)
		#await ctx.send(zalgo)
		
	def _zalgo(self, text):
		words = text.split()
		zalgo = ' '.join(''.join(c + ''.join(random.choice(self.marks)
				for _ in range(i // 2 + 1)) * c.isalnum()
				for c in word)
				for i, word in enumerate(words))
		return zalgo

	@commands.command(pass_context=True)
	async def holy(self, ctx, *, subject : str = None):
		"""Time to backup the Batman!"""
		
		if subject == None:
			await ctx.send("Usage: `{}holy [subject]`".format(ctx.prefix))
			return
		

			suppress = True

		
		matchList = []
		for a in self.adj:
			if a[:1].lower() == subject[:1].lower():
				matchList.append(a)
		
		if not len(matchList):
			# Nothing in there - get random entry
			# msg = "*Whoah there!* That was *too* holy for Robin!"
			word = random.choice(self.adj)
			word = word.strip().capitalize()
			subject = subject.strip().capitalize()
			msg = "*Holy {} {}, Batman!*".format(word, subject)
		else:
			# Get a random one
			word = random.choice(matchList)
			word = word.strip().capitalize()
			subject = subject.strip().capitalize()
			msg = "*Holy {} {}, Batman!*".format(word, subject)
		
		msg = Utils.suppressed(ctx,msg)
		await ctx.send(msg)
		
	@commands.command(pass_context=True)
	async def fart(self, ctx):
		"""PrincessZoey :P"""
		fartList = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
		randnum = random.randint(0, len(fartList)-1)
		msg = '{}'.format(fartList[randnum])
		await ctx.send(msg)
		
	@commands.command(pass_context=True)
	async def french(self, ctx):
		"""Speaking French... probably..."""
		fr_list = [ "hon", "fromage", "baguette" ]
		punct   = [ ".", "!", "?", "...", "!!!", "?!" ]
		fr_sentence = []
		for i in range(random.randint(3, 20)):
			fr_sentence.append(random.choice(fr_list))
		# Capitalize the first letter of the first word
		fr_sentence[0] = fr_sentence[0][:1].upper() + fr_sentence[0][1:]
		totally_french = " ".join(fr_sentence) + random.choice(punct)
		await ctx.send(totally_french)

	@commands.command(pass_context=True)
	async def german(self, ctx):
		"""Speaking German... probably..."""
		de_list = [ "BIER", "sauerkraut", "auto", "weißwurst", "KRANKENWAGEN" ]
		punct   = [ ".", "!", "?", "...", "!!!", "?!" ]
		de_sentence = []
		for i in range(random.randint(3, 20)):
			de_sentence.append(random.choice(de_list))
		if random.randint(0,1):
			# Toss "rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz" in there somewhere
			de_sentence[random.randint(0,len(de_sentence)-1)] = "rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz"
		# Capitalize the first letter of the first word
		de_sentence[0] = de_sentence[0][:1].upper() + de_sentence[0][1:]
		totally_german = " ".join(de_sentence) + random.choice(punct)
		await ctx.send(totally_german)


	@commands.command(pass_context=True)
	async def memetemps(self, ctx):
		"""Get Meme Templates"""
		url = "https://api.imgflip.com/get_memes"
		result_json = await DL.async_json(url)
		templates = result_json["data"]["memes"]

		templates_string_list = []
		
		fields = []
		for template in templates:
			fields.append({ "name" : template["name"], "value" : "`" + str(template["id"]) + "`", "inline" : False })
		await Message.Embed(title="Meme Templates", fields=fields).send(ctx)

	@commands.command(pass_context=True)
	async def meme(self, ctx, template_id = None, text_zero = None, text_one = None):
		"""Generate Memes!  You can get a list of meme templates with the memetemps command.  If any fields have spaces, they must be enclosed in quotes."""


		if text_one == None:
			# Set as space if not included
			text_one = " "

		if any((x==None for x in (template_id,text_zero,text_one))):
			msg = "Usage: `{}meme [template_id] [text#1] [text#2]`\n\n Meme Templates can be found using `$memetemps`".format(ctx.prefix)
			return await ctx.send(msg)

		templates = await self.getTemps()

		chosenTemp = gotName = None

		idMatch   = FuzzySearch.search(template_id, templates, 'id', 1)
		if idMatch[0]['Ratio'] == 1:
			# Perfect match
			chosenTemp = idMatch[0]['Item']['id']
			gotName    = idMatch[0]['Item']['name']
		else:
			# Imperfect match - assume the name
			nameMatch = FuzzySearch.search(template_id, templates, 'name', 1)
			chosenTemp = nameMatch[0]['Item']['id']
			gotName    = nameMatch[0]['Item']['name']

		url = "https://api.imgflip.com/caption_image"
		payload = {'template_id': chosenTemp, 'username':'CorpBot', 'password': 'pooter123', 'text0': text_zero, 'text1': text_one }
		result_json = await DL.async_post_json(url, payload)
		result = result_json["data"]["url"]
		await Message.Embed(
			url=result,
			title=text_zero + " - " + text_one if text_one != " " else text_zero,
			image=result,
			color=ctx.author,
			footer='Powered by imgflip.com - using template id {}: {}'.format(chosenTemp,gotName)
		).send(ctx)

	async def getTemps(self):
		url = "https://api.imgflip.com/get_memes"
		result_json = await DL.async_json(url)
		templates = result_json["data"]["memes"]
		if templates:
			return templates
		return None
