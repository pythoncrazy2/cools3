import pandas as pd
import csv
cpdict2 = pd.read_csv('copy.csv',sep=",", header=None, index_col=0, squeeze=True,quoting=3,error_bad_lines=False, engine="python").to_dict()

cpdict=cpdict2

i=0
listofnames=""
for key, value in cpdict.items():
    listofnames+=str(str(i+1)+" "+ str(key)+"\n")

    i+=1
cptitles=list(cpdict)
print(cptitles)
def redcav():
    cpdict2 = pd.read_csv('copy.csv',sep=",", header=None, index_col=0, squeeze=True,quoting=3,error_bad_lines=False, engine="python").to_dict()

    cpdict=cpdict2

    i=0
    listofnames=""
    for key, value in cpdict.items():
        listofnames+=str(str(i+1)+" "+ str(key)+"\n")

        i+=1
    cptitles=list(cpdict)
    print(cptitles)




import asyncpraw,random
r = asyncpraw.Reddit(
    client_id="Fg-ERt721_7aBg",
    client_secret="7EQSbKaCdzlt_saWVmfhtkbKvqnn9g",
    user_agent="__Encrypt__",
    username="__Encrypt__",
    passwor="Curly55!!",
)








import discord
from discord.ext import commands
from discord.ext import tasks
import os
import glob, random
from PIL import Image, ImageDraw, ImageSequence,ImageFont
from textwrap import wrap
client = commands.Bot(command_prefix="+")
import async_google_trans_new as gt
with open('subnames.txt') as f:
    nameofsubs = [line.rstrip() for line in f]
subnames={}
temp=[]
a=0
async def gen_memes(subname):
    subreddit = await r.subreddit(subname)
    top = subreddit.new(limit = 1000)
    if subname in nameofsubs:
        a=0
    else:
        nameofsubs.append(subname)
        with open("subname.txt", "a+") as file_object:
    # Move read cursor to the start of file.
            file_object.seek(0)
    # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")
    # Append text at the end of file
            file_object.write(subname)
    async for submission in top:
        temp.append(submission)
        subnames[subname]=temp


 # 

@client.command(name="rd",aliases=['memes'])
async def meme23(ctx,subname):
    try:
        random_sub = random.choice(subnames[subname])
    except:
        await gen_memes(subname)
        random_sub = random.choice(subnames[subname])

    name = random_sub.title
    url = random_sub.url
    ups = random_sub.score
    link = random_sub.permalink
    comments = random_sub.num_comments
    embed = discord.Embed(title=name,url=f"https://reddit.com{link}", color=ctx.author.color)
    embed.set_image(url=url)
    embed.set_footer(text = f"👍{ups} 💬{comments}")
    await ctx.send(embed=embed)
    print(subname)

from csv import writer
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file

        csv_writer.writerow(list_of_elem)

@client.command(name="add",help="Add's a copypasta")
async def add(ctx):
    def check(msg):
        return msg.author == ctx.author

    await ctx.send("Title of the ebic copypasta to append? (Note: This is how you will summon it. Also pings don't work(I am preventing spam pinging))")

    message = await client.wait_for("message", check=check)
    titleofpasta = message.content
    await ctx.send("Actual copypasta now:")

    message = await client.wait_for("message", check=check)
    pasta = message.content
    pasta = pasta.replace(',', '')

    list2=[]
    list2.append(titleofpasta.encode('utf-8'))
    list2.append(pasta.encode('utf-8'))
    append_list_as_row("copy.csv",list2)
    redcav()

    await ctx.send("Done :smiley:")






#for filename in os.listdir('./cogs'):
#    if filename.endswith('.py'):
 #      client.load_extension(f'cogs.{filename[:-3]}')
token = "ODQwMjczNzUzMDY0ODY1ODI0.YJVz6g.lLrdKBxbkw1Q5gVTlnw2RkpHF98"

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Currently in " +str(len(client.guilds))+" servers"))
    print("I am online")

@client.command(help="Tells the ping of the bot in milliseconds. Run by +ping")
async def ping(ctx) :
    await ctx.send("Latency is: " + str(client.latency)*1000)

@client.command(help="Nu-uh")
async def nick(ctx,strs) :
    await ctx.guild.me.edit(nick=strs)

@client.command(name="whoami",help="Tells who you are. Run by +whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command(name= 'copypasta',help="Gets a copypasta from the subreddit r/copypasta. Run by +copypasta")
async def copypastas(ctx) :
    sub = await r.subreddit('copypasta')
    posts = [post async for post in sub.new(limit=500)]
    random_post_number = random.randint(0, 500)
    random_post = posts[random_post_number]
    while len(random_post.selftext)>2000 or random_post.selftext.strip()=="":
        random_post_number = random.randint(0, 500)
        random_post = posts[random_post_number]
    await ctx.send(random_post.selftext)
    
@client.command(name="sus",help="Posts a message, and whoever responds next is sus! Run by +sus")
async def on_message(message):

    await message.channel.send(':rotating_light: :rotating_light: :rotating_light: Someone here is sus!!! :rotating_light: :rotating_light: :rotating_light:')
    def check(m):
        return message.author == m.author
    msg = await client.wait_for('message', timeout=600.0, check=check)
    if  msg.content.lower():
        s=str(msg.author)
        a=s[:s.find("#")]
        await message.channel.send("@"+a+" were the imposter :flushed:")


@client.command(name= 'cptitle',help="Posts the titles of all the current customized saved copypasta's. Run by +cptitle")
async def copypasta(ctx) :
    redcav()
    await ctx.send(listofnames)

@client.command(name="amogus", help="Posts a random image related to the popular game Among us. Run by +amogus")
async def amoguspasta(ctx):
    file_path_type = ["./amogusimg/*.png", "./amogusimg/*.jpg"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    await ctx.send(file=discord.File(random_image))
@client.command(name= 'cp', help="Gives a copypasta given a title or the number next to it given from the cptitle command. Run by +cp (name) or +cp (number).")
async def cptitle(ctx, cpname) :
    redcav()
    if cpname.isdigit():
        if int(cpname)-1<len(cptitles):
            await ctx.send(cpdict[cptitles[int(cpname)-1]])
        else:
            await ctx.send("Sorry, but that number is too big. We only have "+len(cpname)+" copypastas.")
    else:
        if str(cpname.lower()) in cpdict:
            a=cpdict[str(cpname.lower())]
            if len(a)<=2000:
                await ctx.send(str(a))
            else:
                b=wrap(a, 2000)
                for element in b:
                    embedVar = discord.Embed(title=str(cpname),description=element.encode("UTF-8"),color=0x9CAFBE)
                    await ctx.channel.send(embed=embedVar)

        else:
            await ctx.send("I'm sorry to say that that isn't a valid name. Please use cptitle to check the current names.")

@client.command(name="cpy", help="Makes a message appropriate for the subreddit r/BrawlStarsCompetitve. Run by +cpy")
async def cpy(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=2).flatten()
    i=0
    for msg in messages:
        if i==0:
            i+=1
        else:
            str=msg.content.lower().replace("bad faith","being realistic").replace("ad hominem","stating the truth").replace("casuals", "r/BrawlstarsCompetive").replace("good game","shit game").replace("supercell","$$upercell").replace("new brawler","new p2w op cashcow").replace("balance","shitty exuse for balancing")
            await ctx.send(str)

@client.command(name="owo", help="Makes a message appropriate for the owo. Run by +owo")
async def cpy2(ctx):
    channel = ctx.channel
    messages = await channel.history(limit=2).flatten()
    i=0
    for msg in messages:
        if i==0:
            i+=1
        else:
            str=msg.content.lower().replace("r","w")
            await ctx.send(str)


@client.command(name="sm",help="spams the living bejesus of out the chat. Unavaiable for most users")
async def sm(ctx,i):
    a=0
    while int(a)<int(i) and "Encrypt" in ctx.message.author.name:
        sub = await r.subreddit('copypasta')
        posts = [post async for post in sub.new(limit=500)]
        random_post_number = random.randint(0, 500)
        random_post = posts[random_post_number]
        while len(random_post.selftext)>2000 and len(random_post.selftext)>1:
            random_post_number = random.randint(0, 500)
            random_post = posts[random_post_number]
        await ctx.send(random_post.selftext)
        a+=1
@client.command(name="meme",help="makes a meme given a tempelate! A example is +meme(command) samething(name of meme template) gelatin(first additional text to be shown) gay(another aditional text to be shown). After this you put additional parameters, such as the words to use")
async def meme(ctx,name_of_meme_template,name_of_1st_text):
    name1=name_of_meme_template
    
    title_font = ImageFont.truetype('Fonts/One-Regular.ttf', 50)
    if name1.lower()=="samething":
        name2=name_of_1st_text.split(",")[0]
        name3=name_of_1st_text.split(",")[1]
        img = Image.open('./memeimg/samething.png')
        draw = ImageDraw.Draw(img)
        draw.text((100, 100),name2,(0,0,0),font=title_font)
        draw.text((650, 100),name3,(0,0,0),font=title_font)
        img.save('sample-out.jpg')
        await ctx.send(file=discord.File("sample-out.jpg"))
    if name1.lower()=="1984":
       
        import io

        im = Image.open('1984.gif')

        frames = []

        for frame in ImageSequence.Iterator(im):

            title_font = ImageFont.truetype('Fonts/One-Regular.ttf',50)
            d = ImageDraw.Draw(frame)
            d.text((10, 100),name_of_1st_text,(0,0,0),font=title_font)
            del d

            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)

            frames.append(frame)

            frames[0].save('out.gif', save_all=True, append_images=frames[1:])

        
        
        await ctx.send(file=discord.File("out.gif"))

@client.command(name="lc", help="Posts a random image related to the popular animal la creatura. Run by +lc")
async def lc(ctx):
    file_path_type = ["./LC/*.mp4"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    await ctx.send(file=discord.File(random_image))

@client.command(name="gay", help="Given a user(pinging them), makes their avatar gay. Run by +gay")
async def gay(ctx,*,  avamember : discord.Member=None):
    import cv2
    fileout=str(avamember)+".jpeg"
    await avamember.avatar_url.save(fileout)
    bg = cv2.imread('gay.png', cv2.IMREAD_COLOR) 
    fg = cv2.imread(fileout, cv2.IMREAD_COLOR)
    dim = (503, 503) 
    resized_bg = cv2.resize(bg, dim, interpolation = cv2.INTER_AREA) 
    resized_fg = cv2.resize(fg, dim, interpolation = cv2.INTER_AREA)
    blend = cv2.addWeighted(resized_bg, 0.5, resized_fg, 0.8, 0.0)
    cv2.imwrite('blended.png', blend)
    await ctx.send(file=discord.File("blended.png"))

@client.command(name="bi",help="Given a user(pinging them), makes their avatar bi. Run by +bi")
async def bi(ctx,*,  avamember : discord.Member=None):
    import cv2
    fileout=str(avamember)+"bi"+".jpeg"
    await avamember.avatar_url.save(fileout)
    bg = cv2.imread('bi.jpg', cv2.IMREAD_COLOR) 
    fg = cv2.imread(fileout, cv2.IMREAD_COLOR)
    dim = (503, 503) 
    resized_bg = cv2.resize(bg, dim, interpolation = cv2.INTER_AREA) 
    resized_fg = cv2.resize(fg, dim, interpolation = cv2.INTER_AREA)
    blend = cv2.addWeighted(resized_bg, 0.5, resized_fg, 0.8, 0.0)
    cv2.imwrite('blendedbi.png', blend)
    await ctx.send(file=discord.File("blendedbi.png"))


g = gt.AsyncTranslator()
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
            a=await g.translate(strs,"la")
            a=await g.translate(a,"es")
            a=await g.translate(a,"zh")
            a=await g.translate(a,"zh")
            a=await g.translate(a,"th")
            a=await g.translate(a,"ko")
            a=await g.translate(a,"ja")
            a=await g.translate(a,"eo")
            a=await g.translate(a,"en")
            await ctx.send(a)
            
@tasks.loop(seconds = 600)
async def myLoop():
    print("gen memes")
    for element in nameofsubs:
        await gen_memes(element)

myLoop.start()
client.run(token)

  

