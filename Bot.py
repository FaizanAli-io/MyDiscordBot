# id 717711862481027194
# token NzE3NzExODYyNDgxMDI3MTk0.XteTrw.NSbyyWMpCVozub1P3s_tTkf7Mcw
# perms 75840
# https://discordapp.com/oauth2/authorize?client_id=717711862481027194&scope=bot&permissions=75840
# server ID 717716263693975564

import discord, sys, time, asyncio, random
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")

client = commands.Bot(command_prefix='!')
token = "NzE3NzExODYyNDgxMDI3MTk0.XteTrw.NSbyyWMpCVozub1P3s_tTkf7Mcw"
client.remove_command('help')


def m8ball():
    answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes – definitely", "You may rely on it", "As I see it", "Most Likely", "Outlook good", "Yes", "Signs point to yes", "Don’t count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "Reply hazy", "Try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again"]
    return random.choice(answers)

def _community_report(guild):
    idle, online, offline = 0, 0, 0
    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        elif str(m.status) == "offline":
            offline += 1
        else:
            idle += 1
    return online, offline, idle

'''
async def user_metrics_background_tasks():
    await client.wait_until_ready()
    global my_guild
    my_guild = client.get_guild(717716263693975564)

    while not client.is_closed():
        try:
            online, offline, idle = _community_report(my_guild)
            with open("usermetrics.csv", "a") as f:
                f.write(f"{int(time.time())+18000}, {online}, {offline}, {idle}\n")

            df = pd.read_csv("usermetrics.csv", names=['time', 'online', 'offline', 'idle'])
            df['date'] = pd.to_datetime(df['time'], unit='s')
            df['total'] = df['online'] + df['offline'] + df['idle']
            df.drop("time", 1, inplace=True)
            df.set_index("date", inplace=True)

            plt.clf()
            df['online'].plot()
            df['offline'].plot()
            df['idle'].plot()
            df['total'].plot()

            plt.legend()
            plt.xlabel('Time')
            plt.ylabel('Activity')
            plt.savefig("online.png")
            
            await asyncio.sleep(30)

        except Exception as e:
            print(str(e))
            await asyncio.sleep(2)
'''

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("With Your Heart :*)"))
    print(f"Locked and Loaded as {client.user}")

@client.command()
async def help(ctx, mod=None):
    global embedH
    author = ctx.message.author
    embedH = discord.Embed(
        title = 'Help Menu',
        description = 'List of commands you can use with this Bot',
        color = discord.Colour.green()
    )
    embedH.set_author(name='Tutorial Bot')

    if mod == None:
        embedH.set_footer(text='Type !help followed by a module name for the list of commands in that module eg. !help games')
        embedH.add_field(name="Games", value="Cards, Dice, Coinflips and a Magic8Ball", inline=False)
        embedH.add_field(name="Admin", value="Kick, Ban, Invite, and Moderate", inline=False)
        embedH.add_field(name="Survey", value="Member and Community reports", inline=False)
        embedH.add_field(name="Misc", value="Get Date, Time and other random stuff", inline=False)
    elif mod == 'games':
        embedH.add_field(name="!make_deck", value="Creates and shuffles a 52 card deck", inline=False)
        embedH.add_field(name="!draw", value="Draws the specified number of cards from the deck, must be less than the number of cards left in the deck (default is 1)", inline=False)
        embedH.add_field(name="!flip_coin", value="Flip a coin", inline=False)
        embedH.add_field(name="!roll_dice", value="Roll a dice of n number of sides (default is 6)", inline=False)
        embedH.add_field(name="!magic8ball", value="Ask the magic 8ball a question (will only respond if statement ends with a question mark)", inline=False)
    elif mod == 'misc':
        embedH.add_field(name="!theTime", value="Gets the time (you can use +- to specify GMT)", inline=False)
        embedH.add_field(name="!theDay", value="Gets the day", inline=False)
        embedH.add_field(name="!claim_waifu", value="Claim a Waifu to make sure no one else can have her", inline=False)
        embedH.add_field(name="!show_waifu", value="Show off your waifu", inline=False)

    await author.send(embed=embedH)

@client.command()
async def magic8ball(ctx):
    if "?" == str(ctx.message.content)[-1]:
        await ctx.send(f"```{ctx.author.name} The Magic 8-Ball has spoken: {m8ball()}```")
    else:
        await ctx.send("```A question for the Magic 8ball must end with a '?'```")

@client.command()
async def choose(ctx, *args):
    await ctx.send(random.choice(args))

@client.command()
async def kill619815(ctx):
    await client.close()
    sys.exit()

@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command()
async def report(ctx):
    G = ctx.guild
    on, of, idl = _community_report(G)
    await ctx.send(f"```py\nOnline: {on}\nOffline: {of}\nIdle: {idl}\nTotal: {on+of+idl}```")
    '''file = discord.File('online.png', filename='online.png')
    await ctx.send('Online Per Time', file=file)'''

@client.command()
async def theDay(ctx):
    await ctx.send(datetime.date.today().strftime('%d %b %Y'))

@client.command()
async def theTime(ctx, h=0, m=0):
    t = datetime.datetime.now() + datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)
    await ctx.send(t.strftime('%I:%M:%S  %p'))

@client.command()
async def time_since_join(ctx):
    mem = ctx.message.mentions[0]
    diff = ((datetime.datetime.now())-(mem.joined_at))
    await ctx.send(f"```{diff} (in dd:hh:mm:ss)```")

@client.command()
async def kick(ctx, mem:discord.Member, *, reason=None):
    await mem.kick(reason=reason)
    await ctx.send(f"{mem.name} has been banned {reason}")

@client.command()
async def ban(ctx, mem:discord.Member, *, reason=None):
    await mem.ban(reason=reason)
    await ctx.send(f"{mem.name} has been banned {reason}")

'''@client.command()
async def unban(ctx, mem : discord.User):
    banned = await ctx.guild.bans()
    for entry in banned:
        user = entry.user
        if user.id == mem:
            await ctx.guild.unban(user)
            #await ctx.send(f"{name}#{disc} has been unbanned")'''

@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@client.command()
async def make_deck(ctx):
    global deck
    li1, li2 = ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King'], ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    deck = [i + ' of ' + j for i in li1 for j in li2]
    random.shuffle(deck)
    await ctx.send("Deck ready")

@client.command()
async def draw(ctx, draws=1):
    global deck
    for _ in range(draws):
        await ctx.send(deck.pop())

@client.command()
async def flip_coin(ctx):
    await ctx.send(random.choice(['head', 'tail']))

@client.command()
async def roll_dice(ctx, sides=6):
    dice = [i for i in range(1, sides+1)]
    await ctx.send(random.choice(dice))

@client.command()
async def message_count(ctx):
    channel, count = ctx.channel, 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.send(f'This channel has {count} messages')

@client.command()
async def claim_waifu(ctx, waifu):
    with open('waifus', 'r') as f:
        WaifuIndex = eval(f.read())
    
    if waifu in WaifuIndex.values():
        await ctx.send(f'Sorry bud, but this waifu is already taken')
    else:
        WaifuIndex[ctx.author.name] = waifu
        await ctx.send('waifu claimed successfully')
    
    with open('waifus', 'w') as f:
        f.write(str(WaifuIndex))

@client.command()
async def show_waifu(ctx):
    with open('waifus', 'r') as f:
        WaifuIndex = eval(f.read())
    
    if ctx.author.name in WaifuIndex:
        await ctx.send(f'Your Waifu is {WaifuIndex[ctx.author.name]}')
    else:
        await ctx.send('You don\'t have a waifu :*/')

@client.command()
async def message_info(ctx, limit=None):
    channel, count = ctx.channel, {}

    async for msg in channel.history(limit=limit):
        if msg.author.name in count:
            count[msg.author.name] += 1
        else:
            count[msg.author.name] = 1
    
    info = ''
    for key, vaue in count.items():
        info += key + ': ' + str(vaue) + '\n'
    
    await ctx.send(f'```{info}```')

#client.loop.create_task(user_metrics_background_tasks())
client.run(token)