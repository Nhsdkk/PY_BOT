from asyncio import tasks
import discord
from discord import activity
from discord.activity import Spotify
import requests
from discord.ext import tasks
import datetime
import re
import random
import sys
import os
import json
import lyricsgenius
from lyricsgenius import Genius

from Text import htextemb
from Text import Error_text
from Text import ee
from Text import Syntemb
from Text import settingsemb

if not(os.path.exists('private_data.json')):
    print('An error ocurred. private_data.json does not exist. Please read the installation instructions and use startup.py before using bot.')
    sys.exit()
with open ('private_data.json','r') as private:
    data = json.load(private)

Reddit_client_id = data['Reddit']['rci']
Reddit_secret_token = data['Reddit']['rst']
username = data['Reddit']['user']
password = data['Reddit']['psw']
DisToken = data['Distoken']
try:
    gentoken = data['GeniusToken']
except:
    print('An error ocurred. There is no Genius API token. Please read the installation instructions and use startup.py before using bot.')
    sys.exit()

if not(os.path.exists('settings.json')):
    print('An error ocurred. settings.json file does not exists. Use startup.py to create this file')
    sys.exit()
with open ('settings.json') as settingf:
    data = json.load(settingf)

chnstartid = data['channel_start_message']
if chnstartid == '':
    print('An error ocurred. System channel is not assigned. Use startup.py to assign a channel by id')
    sys.exit()    
chngitname = data['github']['channel']
repname = data['github']['repository']
usrname = data['github']['username']

if not(os.path.exists('data.json')):
    print('An error ocurred. data.json file does not exists. Use startup.py to create this file')
    sys.exit()

with open ('data.json','r') as datfile:
    data = json.load(datfile)

lastsha = data['lastsha']

color = 0x874aff

Beginer = [0,1,2,3,4]
Intermed = [5,6,7,8,9]
Senior = [10,11,12,13,14]
Pro = [15,16,17,18,19]
Genius = [20,21,22,23,24]
Sheesh = 25

today = datetime.date.today()
tyear = today.year
year = ''
if tyear != 2021:
    year = '(flashback from 2021)'
intents = discord.Intents.all()
activity = discord.Activity(name = f'a new episode of \'Yes or no\'{year}',type =discord.ActivityType.watching)
roles = []

client = discord.Client(intents=intents,activity=activity)

@client.event
async def on_ready():
    global chnstartid
    chnid = chnstartid
    for channel in client.get_all_channels():
        if channel.id == int(chnid):
            chn = channel
            break

    msg = await chn.send('msg')
    await RoleChecker(msg)
    await msg.delete()
    print (f'{client.user.name} is now working')

async def rndfact(message):
    global color
    res = requests.get('http://numbersapi.com/random/math?json')
    msg = discord.Embed(title = 'Random number fact',color = color)
    text = res.json()['text']
    words = text.split(' ')
    i = True

    fact = ''
    for word in words:
        if i:
            i = False
            pass 
        else:
            fact= fact+' '+word
    msg.add_field(name = words[0],value = fact,inline = False)
    await message.channel.send(embed = msg)

def Admcheck(message):
    return (message.author.guild_permissions.administrator)

def Genusage(name,artist):
    global gentoken
    genius = lyricsgenius.Genius(gentoken,skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
    song = genius.search_song(name,artist)
    return(song.lyrics)

async def AddSetting(setting,variable,message):
    if not(Admcheck(message)):
        await message.channel.send ('Not  permissions to use this command. User should be administrator.')
        return
    with open ('settings.json','r') as stgfile:
        data = json.load(stgfile)
    
    if setting == 'gitchannel':
        param = 'channel'
        section = 'github'
    elif setting == 'gitrep':
        param = 'repository'
        section = 'github'
    elif setting == 'gitusername':
        param = 'username'
        section = 'github'
    else:
        await message.channel.send('The command spelling is incorrect. Use #settinglist to see all settings')
        return
    
    data[section][param] = variable

    with open ('settings.json','w') as stgfile:
        json.dump(data,stgfile)

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

    global chngitname, repname,usrname
    channelname = chngitname
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

    global lastsha
    
    url = 'https://api.github.com/repos/'+ usrname+'/'+ repname + '/events'
    res = requests.get(url).json()

    global color

    sha = res[0]['payload']['commits'][0]['sha']
    if lastsha != sha:
        with open('data.json','r') as datfile:
            data = json.load(datfile)
        data['lastsha'] = sha
        with open ('data.json','w') as datfile:
            json.dump(data,datfile)
        lastsha = sha
        await channel.send(message.guild.default_role)
        embmsg =discord.Embed(title = 'Repository update!',color = color)
        embmsg.add_field(name = f'{repname} repository was updated',value = f'{usrname} updated his program.',inline=False)
        embmsg.add_field(name = 'URL',value = 'https://github.com/'+ usrname + '/' + repname + '/commit/' + sha,inline=False)
        await channel.send (embed=embmsg)

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

def GetRNDColor():
    rndcolor = [0,0,0]
    rndcolor[0]=random.randint(0,255)
    rndcolor[1]=random.randint(0,255)
    rndcolor[2]=random.randint(0,255)
    return (rndcolor)

async def RoleChecker(message):
    rolenames = ['Beginner','Intermediate','Senior','Pro','Genius','Sheeesh']
    cluserid = client.user.id
    cluser = discord.utils.get(client.get_all_members(),id = cluserid)
    global roles
    for rolename in rolenames:
        role=discord.utils.get(cluser.roles,name = rolename)
        if not (role in cluser.roles):
            rndcolormass = GetRNDColor()
            rndcolor = discord.Color.from_rgb(rndcolormass[0],rndcolormass[1],rndcolormass[2])
            role = await message.guild.create_role(name = rolename,color = rndcolor,hoist = False,mentionable = False)
            await cluser.add_roles(role,reason = '')       
        roles.append(role)

# asymessage.guildsage(messageid,message):
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

async def GetCurrentTrack(message,function):
    activitylist = message.author.activities
    global color
    for activity in activitylist:
        if isinstance(activity,Spotify):
            if function == 'track':
                embedmessage = discord.Embed(title='Spotify',color = color)
                embedmessage.set_thumbnail(url = activity.album_cover_url)
                embedmessage.add_field(name = f'{message.author.name}\'s currently plaing track:',value = f'{activity.title} by {activity.artist}',inline=False)
                embedmessage.add_field(name = 'URL',value = f'https://open.spotify.com/track/{activity.track_id}')
            elif function == 'lyrics':
                artist = activity.artist.split('; ')
                lyrics = Genusage(activity.title,artist[0])
                stroki = lyrics.split('\n')
                i=0
                lengh = 0
                parags = []
                for z in range(len(stroki)):
                    parags.append('')
                for stroka in stroki:
                    if lengh+len(stroka) <= 1024:
                        parags[i] = parags[i]+'\n'+stroka
                        lengh = lengh + len(stroka)+1
                    else:
                        lengh=len(stroka)
                        i+=1
                        parags[i]= parags[i]+stroka

                a = 1                    
                embedmessage = discord.Embed(title='Spotify',color = color)
                embedmessage.set_thumbnail(url = activity.album_cover_url)
                embedmessage.add_field(name = 'Song:',value = f'{activity.title} by {activity.artist}',inline = False)
                for parag in range(i+1):
                    embedmessage.add_field(name = f'Lyrics(part {a}): ',value = parags[parag],inline = False)
                    a+=1
            await message.channel.send(embed = embedmessage)

async def levelrole (message,role,rolelist):
    for usrrole in message.author.roles:
        for roll in rolelist:
            if roll != role:
                if usrrole == roll:
                    await message.author.remove_roles(roll)
    await message.author.add_roles(role)    

async def User_Level(message,function): 

    Username = str(message.author)

    k=2
    global color,Beginer,Intermed,Senior,Pro,Genius,Sheesh,roles


    with open('data.json','r') as datfile:
        data = json.load(datfile) 

    try:
        Expstr = data[Username]['UserExp']
    except:
        Expint = 0
        User_Level = 0
        data[Username] = {}
        data[Username]['UserExp'] = '0'
        data[Username]['UserLevel'] = '0'
        await message.author.add_roles(roles[0])
    Expint = int(Expstr)
    User_Level = 0
    LevelExp = 75

    try:
        User_Level = int(data[Username]['UserLevel'])
        while Expint > LevelExp:
            LevelExp = round(LevelExp + LevelExp * 1.5)
    except:
        while Expint > LevelExp:
            LevelExp = round(LevelExp + LevelExp * 1.5)
            User_Level += 1
        data[Username]['UserLevel'] = str(User_Level)   
    
    oldlevel = User_Level

    if function == 'GetLevel':
        embmsg = discord.Embed(title = 'Level',color =color)
        embmsg.add_field(name=message.author,value = str(User_Level),inline = False)
        embmsg.add_field(name = 'EXP until next level:',value = str(round(LevelExp-Expint))+' exp',inline = False)
        await message.channel.send(embed = embmsg)

    elif function == 'Add Exp':
        data[Username]['UserExp'] = int(Expint)
        Expint = Expint + k * len(message.content)
        while Expint > LevelExp:
            LevelExp = LevelExp + LevelExp * 1.5
            User_Level += 1
        if oldlevel != User_Level:
            data[Username]['UserLevel'] = str(User_Level)
            embmsg = discord.Embed(title = 'New level!', color = color)
            embmsg.add_field(name = f'{Username} leveled up',value = f'The user is now level {User_Level}. Congatulations!',inline=False)
            await message.channel.send(embed=embmsg)
        with open ('data.json','w') as datfile:
            json.dump(data,datfile)
        if User_Level in Beginer:
            await levelrole(message,roles[0],roles)
        elif User_Level in Intermed:
            await levelrole(message,roles[1],roles)
        elif User_Level in Senior:
            await levelrole(message,roles[2],roles)
        elif User_Level in Pro:
            await levelrole(message,roles[3],roles)
        elif User_Level in Genius:
            await levelrole(message,roles[4],roles)
        elif User_Level >= Sheesh:
            await levelrole(message,roles[5],roles)

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

    if message.content.startswith('#lets-go'):
        await message.channel.send('Hello')               
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#help'):
        await message.channel.send(embed = htextemb)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#LOGIN-SHEESH-PASSWORD-FAKER'):
        await message.channel.send(ee)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#r/'):               
        data1=message.content.split('/')
        data2 = data1[1].split('=')
        Section = data2[1]
        Subreddit=data2[0]
        try:
            await reddit_API_usage(str(Subreddit),str(Section),message)
        except Exception:
            await message.channel.send('An error ocurred. Check the spelling of subreddit or section. Type #synt to see all reddit sections')
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#settinglist'):
        await message.channel.send(embed = settingsemb)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#synt'):
        await message.channel.send(embed = Syntemb)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#level'):
        await User_Level(message,'GetLevel')
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#gitupdates'):
        if not(Admcheck(message)):
            await message.channel.send ('Not  permissions to use this command. User should be administrator.')
            return
        command = message.content.split('=')
        if command[1] == 'start':    
            await GetGitUpdates.start(message)
        elif command[1] == 'stop':
            GetGitUpdates.stop
        await User_Level(message,'Add Exp')

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
                await AddSetting(channelname[1],channelname[2],message)    
            else:
                await message.channel.send ('No channel named '+channelname[2])
        else:
            await AddSetting(channelname[1],channelname[2],message)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#wakeup'):
        await WakeUp(message)
        await User_Level(message,'Add Exp') 
    
    elif message.content.startswith('#addbm'):
        await GetReferenceToPM(message)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#curtrack'):
        await GetCurrentTrack(message,'track')
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#removebm'):
        await DeletePM(message)
        await User_Level(message,'Add Exp')

    elif message.content.startswith('#lyrics'):
        try:
            await GetCurrentTrack(message,'lyrics')
            await User_Level(message,'Add Exp')
        except:
            await message.channel.send('An error ocurred. There is no lyrics on Genius for this song.')

    elif message.content.startswith('#fact'):
        await rndfact(message)
        await User_Level(message,'Add Exp')
        
    else:
        await message.channel.send(Error_text)

client.run(DisToken)