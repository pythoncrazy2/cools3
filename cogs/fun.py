import random
import urllib.parse
import sqlite3
import asyncio
import aiohttp
import discord
from discord.ext import commands


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

def setup(bot):
    bot.add_cog(fun(bot))