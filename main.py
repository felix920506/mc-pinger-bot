# import modules
import discord, datetime, discord.ext, json
from discord.ext import commands
from mcstatus import MinecraftServer

#load servers
with open('servers.json','r',encoding='utf8') as serverlist:
    servers = json.load(serverlist)
    print('servers loaded')

with open('settings.json','r',encoding='utf8') as config:
    settings = json.load(config)
    token = settings['token']
    title = settings['title']
    errormsg = settings['errormsg']
    prefix = settings['prefix']

# clock function
def clock():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# get status function
def mcping(ip):
    server = MinecraftServer.lookup(ip)
    try:
        mcstatus = server.status()
        ping = mcstatus.latency
        return round(ping)
    except:
        return False

# send result function
def genemb(id):
    name = servers[str(id)]['name']
    ip = servers[str(id)]['ip']
    color = int(servers[str(id)]['color'],0)
    ping = mcping(ip)
    if ping == False:
        ping = errormsg
    else:
        ping = f'{ping} ms'

    embed=discord.Embed(title=title, color=color)
    embed.add_field(name=f'{name} ( {ip} ):', value=f'{ping}', inline=False)
    return embed

# setup
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.command()
async def ping(ctx,id=None):
    if id == None:
        for i in range(len(servers)):
            await ctx.send(embed=genemb(i))
    
    else:
        i = int(id)-1
        await ctx.send(embed=genemb(i))

# run
bot.run(token)
