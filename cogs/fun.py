import random
import urllib.parse
import sqlite3
import asyncio
import aiohttp
import discord
from discord.ext import commands
import re
import requests
import urllib.request
from discord.ext.commands import clean_content
from .constants import ball, emoji_dict, regionals
from typing import Optional, Union
import contextlib

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def has_dupe(self, duper: Union[str, list]) -> bool:
        collect_my_duper = list(filter(lambda x: x != "⃣", duper))
        #  ⃣ appears twice in the number unicode thing, so that must be stripped
        return len(set(collect_my_duper)) != len(collect_my_duper)
    def replace_combos(self, react_me: str) -> str:
        for combo in emoji_dict["combination"]:
            if combo[0] in react_me:
                react_me = react_me.replace(combo[0], combo[1], 1)
        return react_me

    # used in [p]react, replaces e.g. 'aaaa' with '🇦🅰🍙🔼'
    def replace_letters(self, react_me: str):
        for char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
            char_count = react_me.count(char)
            if char_count > 1:  # there's a duplicate of this letter:
                if len(emoji_dict[char]) >= char_count:
                    # if we have enough different ways to say the letter to complete the emoji chain
                    i = 0
                    while i < char_count:
                        # moving goal post necessitates while loop instead of for
                        if emoji_dict[char][i] not in react_me:
                            react_me = react_me.replace(char, emoji_dict[char][i], 1)
                        else:
                            # skip this one because it's already been used by another replacement (e.g. circle emoji used to replace O already, then want to replace 0)
                            char_count += 1
                        i += 1
            else:
                if char_count == 1:
                    react_me = react_me.replace(char, emoji_dict[char][0])
        return react_me




    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    def userOnline(self, memberList):
        online = []
        for i in memberList:
            if i.status == discord.Status.online and i.bot == False:
                online.append(i)
        return online

    
    @commands.command()
    async def praise(self, ctx):
        '''Praise the Sun'''
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def css(self, ctx):
        '''Counter Strike: Source'''
        await ctx.send('http://i.imgur.com/TgPKFTz.gif')

    @commands.command()
    async def countdown(self, ctx):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('**:ok:** DING DING DING')

    @commands.command(aliases=['cat', 'randomcat'])
    async def neko(self, ctx):
        '''Random cats pictures nyan ~'''
        #http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                res = await r.json()
                emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
                await ctx.send(random.choice(emojis) + res['file'])


    @commands.command(aliases=['rand'])
    async def random(self, ctx, *arg):
        '''Returns a random number or member
        Use:
        -----------
        +random
            Returns a random number between 1 and 100
        +random coin
            Flips a coin (heads or tails)
        +random 6
            Returns a random number between 1 and 6
        +random 10 20
            Returns a random number between 10 and 20
        +random user
            Outputs a random user who is currently online
        
        +random choice Dani Eddy Shinobu
            Select a name from the list provided
        '''
        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['heads', 'tails']
                await ctx.send(f':arrows_counterclockwise: {random.choice(coin)}')
                return
            elif arg[0] == 'choice':
                choices = list(arg)
                choices.pop(0)
                await ctx.send(f':congratulations: The winner is {random.choice(choices)}')
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.guild.members)
                randomuser = random.choice(online)
                if ctx.channel.permissions_for(ctx.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                await ctx.send(f':congratulations: The winner is {user}')
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) == 2:
                start = int(arg[0])
                end = int(arg[1])
            await ctx.send(f'**:arrows_counterclockwise:** Random number({start} - {end}): {random.randint(start, end)}')

    @commands.command()
    async def python(self, ctx, member:str):
        '''Monty Python'''
        await ctx.send(f'R.I.P. {member}\nhttps://media.giphy.com/media/l41lGAcThnMc29u2Q/giphy.gif')

    @commands.command(aliases=['hypu', 'train'])
    async def hype(self, ctx):
        '''HYPE TRAIN CHOO CHOO'''
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)

    @commands.command()
    async def xkcd(self, ctx,  *searchterm: str):
        '''Shows the last or random XKCD comic
        Example:
        -----------
        :xkcd
        :xkcd random
        '''
        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl.format('/')) as r:
                js = await r.json()
                if ''.join(searchterm) == 'random':
                    randomComic = random.randint(0, js['num'])
                    async with cs.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], js['alt'], comicUrl, date)
                await ctx.send(msg)

    @commands.command(aliases=['witz', 'joke'])
    async def pun(self, ctx):
        '''Because everyone likes bad jokes'''
        puns  = [ 'What does one match say to the other match? \ n Come on, let\'s run away ' ,
                'How many Germans do you need to change a lightbulb? \ n One, we\'re humorless and efficient. ' ,
                'Where does the cat live? \ n In the kitty house. ' ,
                'How do two plastic surgeons greet each other? \ n "What kind of face are you doing today?" ' ,
                'Why Don\'t Vegans Eat Chicken? \ n Might contain egg ' ,
                '85% of women think their ass is too big, 10% too thin, 5% think it\'s as ok as it is and are happy that they married it ... ' ,
                'My girlfriend thinks I\'m curious ... \ n ... at least \' that\'s in her diary. ' ,
                '"Honey, I have to wash my T-shirt! Which washing machine program should I use?" - "What does it say on the t-shirt?" \ n "Slayer!" ' ,
                'Yesterday I told my boyfriend that I\'d always wanted to ride that Harry Potter thing. \ n "a broom?" "no, Hermione." ' ,
                'Why don\'t ants go to church? \ n They are sects. ' ,
                'What does a mathematician\'s tombstone say? \ n "He didn\'t expect that." ' ,
                'When a yoga teacher stretches his legs straight up and farts, what yoga figure is he doing? \ n A scented candle ' ,
                'Why did the balloon break? \ n For reasons of space. ' ,
                'I wanted to call Spiderman, but he had no network.' ,
                'What does a screw miss the most? A father ' ,
                'A panda walks across the street. Bamboo!' ]
        emojis = [':laughing:', ':smile:', ':joy:', ':sob:', ':rofl:']
        msg = f'{random.choice(emojis)} {random.choice(puns)}'
        await ctx.send(msg)

    @commands.command()
    async def combine(self, ctx, name1: clean_content, name2: clean_content):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = (discord.Embed(color=0x36393e, description = f"{ship}"))
        emb.set_author(name=f"{name1} + {name2}", icon_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        await ctx.send(embed=emb)

    @commands.command()
    async def ship(self, ctx, name1 : clean_content, name2 : clean_content):
        shipnumber = random.randint(0,100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(", 
                                                            'Just "friends"', 
                                                            '"Friends"', 
                                                            "Little to no love ;(", 
                                                            "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone", 
                                                     "Still in that friendzone ;(", 
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!", 
                                                     "But there's a small bit of love somewhere", 
                                                     "I sense a small bit of love!", 
                                                     "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!", 
                                                      "There is a bit of love there...", 
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", 
                                                          "It appears one sided!", 
                                                          "There's some potential!", 
                                                          "I sense a bit of potential!", 
                                                          "There's a bit of romance going on here!", 
                                                          "I feel like there's some romance progressing!", 
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!", 
                                                      "There's some love in the air!", 
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!", 
                                                       "I can see the love is there! Somewhere...", 
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(random.choice(["Love is in the air!", 
                                                              "I can definitely feel the love", 
                                                              "I feel the love! There's a sign of a match!", 
                                                              "There's a sign of a match!", 
                                                              "I sense a match!", 
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!", 
                                                           "There's a match made in heaven!", 
                                                           "It's definitely a match!", 
                                                           "Love is truely in the air!", 
                                                           "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                        ":sparkling_heart:", 
                                                                                                        ":heart_decoration:", 
                                                                                                        ":heart_exclamation:", 
                                                                                                        ":heartbeat:", 
                                                                                                        ":heartpulse:", 
                                                                                                        ":hearts:", 
                                                                                                        ":blue_heart:", 
                                                                                                        ":green_heart:", 
                                                                                                        ":purple_heart:", 
                                                                                                        ":revolving_hearts:", 
                                                                                                        ":yellow_heart:", 
                                                                                                        ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        await ctx.send(embed=emb)
        
    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, _ballInput: clean_content):
        """extra generic just the way you like it"""
        choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = random.choice(["It is certain ", 
                                        "It is decidedly so ", 
                                        "Without a doubt ", 
                                        "Yes, definitely ", 
                                        "You may rely on it ", 
                                        "As I see it, yes ",
                                        "Most likely ", 
                                        "Outlook good ", 
                                        "Yes ", 
                                        "Signs point to yes "]) + ":8ball:"

            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = random.choice(["Reply hazy try again ", 
                                        "Ask again later ", 
                                        "Better not tell you now ", 
                                        "Cannot predict now ", 
                                        "Concentrate and ask again "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
        elif choiceType == "(Negative)":
            prediction = random.choice(["Don't count on it ", 
                                        "My reply is no ", 
                                        "My sources say no ", 
                                        "Outlook not so good ", 
                                        "Very doubtful "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
        emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await ctx.send(embed=emb)


    @commands.command(aliases=['gay-scanner', 'gayscanner'])
    async def gay_scanner(self, ctx,* ,user: clean_content=None):
        """very mature command yes haha"""
        if not user:
            user = ctx.author.name
        gayness = random.randint(0,100)
        if gayness <= 33:
            gayStatus = random.choice(["No homo", 
                                       "Wearing socks", 
                                       '"Only sometimes"', 
                                       "Straight-ish", 
                                       "No homo bro", 
                                       "Girl-kisser", 
                                       "Hella straight"])
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = random.choice(["Possible homo", 
                                       "My gay-sensor is picking something up", 
                                       "I can't tell if the socks are on or off", 
                                       "Gay-ish", 
                                       "Looking a bit homo", 
                                       "lol half  g a y", 
                                       "safely in between for now"])
            gayColor = 0xFF69B4
        else:
            gayStatus = random.choice(["LOL YOU GAY XDDD FUNNY", 
                                       "HOMO ALERT", 
                                       "MY GAY-SENSOR IS OFF THE CHARTS", 
                                       "STINKY GAY", 
                                       "BIG GEAY", 
                                       "THE SOCKS ARE OFF", 
                                       "HELLA GAY"])
            gayColor = 0xFF00FF
        emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await ctx.send(embed=emb)


    @commands.command(aliases=['ud'])
    async def urban(self,ctx, *msg):
        """Searches on the Urban Dictionary."""
      
        word = ' '.join(msg)
        api = "http://api.urbandictionary.com/v0/define"

        # Send request to the Urban Dictionary API and grab info
        response = requests.get(api, params=[("term", word)]).json()
        embed = discord.Embed(description="No results found!", colour=0xFF0000)
        if len(response["list"]) == 0:
            return await ctx.send(embed=embed)
        # Add results to the embed
        embed = discord.Embed(title="Word", description=word, colour=embed.colour)
        embed.add_field(name="Top definition:", value=response['list'][0]['definition'])
        embed.add_field(name="Examples:", value=response['list'][0]['example'])
        await ctx.send(embed=embed)


    @commands.command(name="lick", aliases=["mlem"])
    async def lick(self, ctx, person: discord.Member):
        '''
        Mlem
        '''
        if person == ctx.author:
            return await ctx.reply("You can't lick yourself!", mention_author=False)

        if person == self.bot.user:
            return await ctx.reply("I don't like being licked!", mention_author=False)

        tastesLike = [
            "bacon",
            "tortilla chips",
            "chezborger",
            "ketchup on pasta",
            "bubblegum",
            "chicken",
            "honey",
            "a creeper",
            "corn",
            "butts",
            "a jolly rancher",
            "cheese",
            "pickles",
            "lemons",
            "cucumbers"
        ]

        await ctx.reply(f"{ctx.author.mention} licked {person.mention}! They taste like {random.choice(tastesLike)}!", mention_author=False)
    @commands.command()
    async def regional(self, ctx: commands.Context, *, msg: str) -> None:
        """Replace letters with regional indicator emojis."""
        regional_list = [regionals[x.lower()] if x.lower() in regionals else x for x in list(msg)]
        await ctx.send("\u200b".join(regional_list))
    @commands.command()
    async def react(
        self,
        ctx: commands.Context,
        msg: str,
        message: Optional[discord.Message],
    ) -> None:
        """
        Add letter(s) as reaction to previous message.
        `[message]` Can be a message ID from the current channel, a jump URL,
        or a channel_id-message_id from shift + copying ID on the message.
        """
        if message is None:
            async for messages in ctx.channel.history(limit=2):
                message = messages

        reactions = []
        non_unicode_emoji_list = []
        react_me = ""
        # this is the string that will hold all our unicode converted characters from msg

        # replace all custom server emoji <:emoji:123456789> with "<" and add emoji ids to non_unicode_emoji_list
        emotes = re.findall(r"<a?:(?:[a-zA-Z0-9]+?):(?:[0-9]+?)>", msg.lower())
        react_me = re.sub(r"<a?:([a-zA-Z0-9]+?):([0-9]+?)>", "", msg.lower())

        for emote in emotes:
            reactions.append(discord.utils.get(self.bot.emojis, id=int(emote.split(":")[-1][:-1])))
            non_unicode_emoji_list.append(emote)

        if self.has_dupe(non_unicode_emoji_list):
            return await ctx.send(
                "You requested that I react with at least two of the exact same specific emoji. "
                "I'll try to find alternatives for alphanumeric text, but if you specify a specific emoji must be used, I can't help."
            )

        react_me_original = react_me
        # we'll go back to this version of react_me if prefer_combine
        # is false but we can't make the reaction happen unless we combine anyway.

        if self.has_dupe(react_me):
            # there's a duplicate letter somewhere, so let's go ahead try to fix it.
            react_me = self.replace_combos(react_me)
            react_me = self.replace_letters(react_me)
            # print(react_me)
            if self.has_dupe(react_me):  # check if we were able to solve the dupe
                react_me = react_me_original
                react_me = self.replace_combos(react_me)
                react_me = self.replace_letters(react_me)
                if self.has_dupe(react_me):
                    # this failed too, so there's really nothing we can do anymore.
                    return await ctx.send(
                        "Failed to fix all duplicates. Cannot react with this string."
                    )

            for char in react_me:
                if (
                    char not in "0123456789"
                ):  # these unicode characters are weird and actually more than one character.
                    if char != "⃣":  # </3
                        reactions.append(char)
                else:
                    reactions.append(emoji_dict[char][0])
        else:  # probably doesn't matter, but by treating the case without dupes seperately, we can save some time
            for char in react_me:
                if char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
                    reactions.append(emoji_dict[char][0])
                else:
                    reactions.append(char)

        if message.channel.permissions_for(ctx.me).add_reactions:
            with contextlib.suppress(discord.HTTPException):
                for reaction in reactions:
                    await message.add_reaction(reaction)
        if message.channel.permissions_for(ctx.me).manage_messages:
            with contextlib.suppress(discord.HTTPException):
                await ctx.message.delete()
        else:
            await ctx.tick()

   




def setup(bot):
    bot.add_cog(fun(bot))


