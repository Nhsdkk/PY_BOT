from asyncio import tasks
import discord
from discord import activity
from discord.activity import Spotify
import requests
import configparser
from discord.ext import tasks
import datetime
import re

from Text import htextemb
from Text import Error_text
from Text import ee
from Text import Syntemb
from Text import settingsemb

config1 = configparser.ConfigParser()
config1.read('private_data.ini')
with open ('private_data.ini','r') as config_file1:
    Reddit_client_id = config1['Reddit']['rci']
    Reddit_secret_token = config1['Reddit']['rst']
    username = config1['Reddit']['user']
    password = config1['Reddit']['psw']
    DisToken = config1['Discord']['token']
config_file1.close()
color = 0x874aff

today = datetime.date.today()
tyear = today.year
year = ''
if tyear != 2021:
    year = '(flashback from 2021)'
intents = discord.Intents.all()
activity = discord.Activity(name = f'a new episode of \'Yes or no\'{year}',type =discord.ActivityType.watching)

client = discord.Client(intents=intents,activity=activity)

@client.event
async def on_ready():
    print('{0.user} is ready. Thank you for using this bot!'.format(client))
    config = configparser.ConfigParser()
    config.read('User_data.ini') 

async def AddSetting(setting,chname,rep,usrname,message):
    if setting == 'gitchannel':
        param = 'channel'
        variable = chname
        section = 'github'
    elif setting == 'gitrep':
        param = 'rep'
        variable = rep
        section = 'github'
    elif setting == 'gitusername':
        param = 'username'
        variable = usrname
        section = 'github'
    else:
        await message.channel.send('The command spelling is incorrect. Use #settinglist to see all settings')
        return
    
    config = configparser.ConfigParser()
    config.read('User_data.ini')
    try:
        section_name = config[section]        
    except Exception: # KeyError:
        config.add_section(section)

    config.set(section,param,variable)
    with open ('User_data.ini','w') as config_file:
        config.write(config_file)
    config_file.close()

    await message.channel.send('Setting applied.')

def GetMentions(message):
    usermenlist = message.mentions
    channelmenlist = message.channel_mentions
    return(usermenlist,channelmenlist)

async def WakeUp(message):
    usermenlist,channelmenlist = GetMentions(message)
    for user in usermenlist:
        await user.send (f'Wake up!\n{message.author} is waiting for you in {message.guild.name} in {channelmenlist[0]} channel')

def Get_Channel_Id(channel_name):
    chn_list = list(client.get_all_channels())
    for e in chn_list:
        if e.name == channel_name:
            channelid = e.id
            break
    return (channelid)

async def Get_Update(message):
    err_msg = {
        'channel':'No message channel assigned.',
        'rep': 'No repository assigned.',
        'username':'No username assigned.',
    }
    msg_use = 'Use #settings + \'=\' + setting (Use #settinglist to see all settings) + \'=\' + parameter to add/edit setting.'

    config = configparser.ConfigParser()

    config.read('User_data.ini')
    try:
        channelname = config['github']['channel']
    except Exception:
        await message.channel.send(err_msg['channel']+' '+msg_use)
        return
    try:
        repname = config['github']['rep']
    except Exception:
        await message.channel.send(err_msg['rep']+' '+msg_use)
        return

    try:
        usrname = config['github']['username']
    except Exception:
        await message.channel.send(err_msg['username']+' '+msg_use)
        return
    if channelname == '':
        await message.channel.send(err_msg['channel']+' '+msg_use)
        return
    elif repname == '':
        await message.channel.send(err_msg['rep']+' '+msg_use)
        return
    elif usrname == '':
        await message.channel.send(err_msg['username']+' '+msg_use)
        return
    channel = client.get_channel(Get_Channel_Id(channelname))

    try:
        lastsha = config['Last_Sha']['Sha']
    except KeyError:
        config.add_section('Last_Sha')
        config.set('Last_Sha','Sha','')    
    
    except Exception:
        config.set('Last_Sha','Sha','')
    lastsha = config['Last_Sha']['Sha']
    
    url = 'https://api.github.com/repos/'+ usrname+'/'+ repname + '/events'
    res = requests.get(url).json()

    global color

    sha = res[0]['payload']['commits'][0]['sha']
    if lastsha != sha:
        config.set('Last_Sha','Sha',sha)
        lastsha = sha
        await channel.send(message.guild.default_role)
        embmsg =discord.Embed(title = 'Repository update!',color = color)
        embmsg.add_field(name = f'{repname} repository was updated',value = f'{usrname} updated his program.',inline=False)
        embmsg.add_field(name = 'URL',value = 'https://github.com/'+ usrname + '/' + repname + '/commit/' + sha,inline=False)
        await channel.send (embed=embmsg)

    with open ('User_data.ini','w') as config_file:
        config.write(config_file)
    config_file.close()

async def reddit_API_usage(subreddit,section,message):
    global color
    auth = requests.auth.HTTPBasicAuth(Reddit_client_id, Reddit_secret_token)
    data = {
        'grant_type' : 'password',
        'username' : username,
        'password' : password
    }
    headers = {'User-Agent' : 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', data = data, auth=auth, headers=headers)
    Token = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {Token}"}}
    res = requests.get('https://oauth.reddit.com/r/' + subreddit + '/'+ section ,headers=headers,params = {'limit' : 25})
    for post in res.json()['data']['children']:
        title = post['data']['title']
        print(title)
        embmsg = discord.Embed(title = title,color = color)
        permalink = post['data']['permalink']
        embmsg.add_field(name = 'Link:',value = f'https://reddit.com{permalink}',inline = False)
        thumbnail=''
        thumbnail=post['data']['thumbnail']
        rethemb = re.match('http',thumbnail)
        if rethemb!=None:    
            embmsg.set_thumbnail(url=post['data']['thumbnail'])
        await message.channel.send(embed = embmsg)

def GetChannelType(message):
    chantype=list(message.channel.type)
    return(chantype[0])

# async def GetRole(message,roleid):
#     role = discord.guild.Guild.get_role(message.guild,role_id=int(roleid))
#     print(role)
#     await message.channel.send(role.color)

# async def GetMessage(messageid,message):
#     message_data = await message.channel.fetch_message(messageid)
#     await message.channel.send(message_data.reactions)

async def GetReferenceToPM(message):
    id = message.reference.message_id
    message_data = await message.channel.fetch_message(id)
    date = message.created_at
    datemessage = date.strftime('%d.%m.%Y %H:%M:%S')
    attachmentlist = []
    global color
    attachmentlist = message_data.attachments 

    newembmsg = discord.Embed(title = f'{message_data.author} said: ',color=color)
    newembmsg.add_field(name ='Text:',value = f'{message_data.content}',inline = False)
    extlist = [f'.jpeg',f'.jpg',f'.png',f'.webp',f'.gif']
    acceptable = False
    if len(attachmentlist) != 0:
        newembmsg.add_field(name ='Attachment:',value = 'The attachment of the message',inline = False)
        for attachment in attachmentlist:
            for ext in extlist:
                if re.search(ext,attachment.url)!= None:
                    acceptable =True 
                    break
            if acceptable: 
                newembmsg.set_image(url = attachment.url)
            else:
                newembmsg.add_field(name = 'Can\'t add this type of attachment to embed message',value = f'Url: {attachment.url}',inline=False)
    newembmsg.set_footer(text = f'The bookmark was added at {datemessage}')

    try:
        await message.author.send (embed = newembmsg)
    except:
        try:
            newembmsg.remove_field(1)
            newembmsg.remove_field(0)
            lastembeds = message_data.embeds
            newembmsg.description = lastembeds[0].title
            for embed in lastembeds[0].fields:
                newembmsg.add_field(name = embed.name,value = embed.value,inline=False)
            newembmsg.set_image(url = lastembeds[0].thumbnail.url)
            await message.author.send (embed = newembmsg)
        except:
            newembmsg.remove_field(0)
            newembmsg.add_field(name = 'Text',value = 'No text found. There are only attachments')
            for ext in extlist:
                if re.search(ext,attachment.url)!= None:
                    acceptable =True 
                    break
            if acceptable: 
                newembmsg.set_image(url = attachment.url)
            else:
                newembmsg.add_field(name = 'Can\'t add this type of attachment to embed message',value = f'Url: {attachment.url}',inline=False)
            await message.author.send (embed = newembmsg)

async def DeletePM(message):
    id = message.reference.message_id
    message_data = await message.channel.fetch_message(id)
    chantype = GetChannelType(message_data)
    if (message_data.author == client.user) and (chantype == 'private'):
        await message_data.delete()
    else:
        await message.channel.send ('Not enough permissions.')

async def GetCurrentTrack(message):
    activitylist = message.author.activities
    global color
    for activity in activitylist:
        if isinstance(activity,Spotify):
            embedmessage = discord.Embed(title='Spotify',color = color)
            embedmessage.set_thumbnail(url = activity.album_cover_url)
            embedmessage.add_field(name = f'{message.author.name}\'s currently plaing track:',value = f'{activity.title} by {activity.artist}',inline=False)
            embedmessage.add_field(name = 'URL',value = f'https://open.spotify.com/track/{activity.track_id}')
            await message.channel.send(embed = embedmessage)            

async def User_Level(message,function):
    config = configparser.ConfigParser()
    config.read('User_data.ini') 

    Username = str(message.author)

    k=3
    global color

    try:
        Expstr = config[Username]['UserExp']
        Expint = int(Expstr)

    except Exception:
        config.add_section(Username)
        config.set(Username,'UserExp','0')
        with open('User_data.ini', "w") as config_file:
            config.write(config_file)
        Expstr = config[Username]['UserExp']
        Expint = int(Expstr)

    User_Level = 0
    LevelExp = 1

    try:
        User_Level = config[username]['userlevel']
    except:
        while Expint > LevelExp:
            LevelExp = LevelExp + LevelExp * 2
            User_Level += 1
        config.set(Username,'userlevel',str(User_Level))    
    
    oldlevel = User_Level

    if function == 'GetLevel':
        embmsg = discord.Embed(title = 'Level',color =color)
        embmsg.add_field(name=message.author,value = str(User_Level),inline = False)
        embmsg.add_field(name = 'EXP until next level:',value = str(LevelExp-Expint)+' exp',inline = False)
        await message.channel.send(embed = embmsg) 

    elif function == 'Add Exp':
        Expint = Expint + k * len(message.content)
        config.set(Username,'UserExp',str(Expint))
        while Expint > LevelExp:
            LevelExp = LevelExp + LevelExp * 2
            User_Level += 1
        if oldlevel != User_Level:
            embmsg = discord.Embed(title = 'New level!', color = color)
            embmsg.add_field(name = f'{Username} leveled up',value = f'The user is now level {User_Level}. Congatulations!',inline=False)
            await message.channel.send(embed=embmsg) 
        with open ('User_data.ini','w') as config_file:
            config.write(config_file)
        config_file.close()

@tasks.loop(seconds = 300)
async def GetGitUpdates(message):
    try:
        await Get_Update(message)
    except Exception as e:
        await message.channel.send('Error: '+ str(e)) 

@client.event
async def on_message(message):
    if message.author == client.user:
        return          

    if message.content.startswith('#'):

            await User_Level(message,'Add Exp')

            if message.content.startswith('#lets-go'):
                await message.channel.send('Hello')               

            elif message.content.startswith('#help'):
                await message.channel.send(embed = htextemb)

            elif message.content.startswith('#LOGIN-SHEESH-PASSWORD-FAKER'):
                await message.channel.send(ee)

            elif message.content.startswith('#r/'):               
                data1=message.content.split('/')
                data2 = data1[1].split('=')
                Section = data2[1]
                Subreddit=data2[0]
                try:
                    await reddit_API_usage(str(Subreddit),str(Section),message)
                except Exception:
                    await message.channel.send('An error ocurred. Check the spelling of subreddit or section. Type #synt to see all reddit sections')

            elif message.content.startswith('#settinglist'):
                await message.channel.send(embed = settingsemb)

            elif message.content.startswith('#synt'):
                await message.channel.send(embed = Syntemb)
            
            elif message.content.startswith('#level'):
                await User_Level(message,'GetLevel')

            elif message.content.startswith('#gitupdates'):
                command = message.content.split('=')
                if command[1] == 'start':    
                    await GetGitUpdates.start(message)
                elif command[1] == 'stop':
                    GetGitUpdates.stop

            elif message.content.startswith('#settings'):
                channelname = message.content.split('=')
                text = client.get_all_channels()
                Channelexists = False
                if channelname[1] == 'gitchannel':
                    for i in text:
                         if i.name == channelname[2]:
                             Channelexists = True
                             break
                    if Channelexists:
                        await AddSetting(channelname[1],channelname[2],channelname[2],channelname[2],message)    
                    else:
                        await message.channel.send ('No channel named '+channelname[2])
                else:
                    await AddSetting(channelname[1],channelname[2],channelname[2],channelname[2],message)
            elif message.content.startswith('#wakeup'):
                await WakeUp(message)
            #    await GetMentions(message)
            #    await GetAllUsers(message)
            #     content = message.content.split('=')
            #     roleid = content[1]
            #     #await GetRole(message,roleid)
            #     await GetMessage(roleid,message) 
            
            elif message.content.startswith('#addbm'):
                await GetReferenceToPM(message)

            elif message.content.startswith('#currenttrack'):
                await GetCurrentTrack(message)

            elif message.content.startswith('#removebm'):
                await DeletePM(message)
                 
            else:
                await message.channel.send(Error_text)

client.run(DisToken)