from asyncio import tasks
import discord
import requests
import configparser
from discord.ext import tasks


from Text import help_text
from Text import Error_text
from Text import ee
from Text import Synt
from Text import settinglist

config1 = configparser.ConfigParser()
config1.read('private_data.ini')
with open ('private_data.ini','r') as config_file1:
    Reddit_client_id = config1['Reddit']['rci']
    Reddit_secret_token = config1['Reddit']['rst']
    username = config1['Reddit']['user']
    password = config1['Reddit']['psw']
    DisToken = config1['Discord']['token']
config_file1.close()

client = discord.Client()

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

    sha = res[0]['payload']['commits'][0]['sha']
    if lastsha != sha:
        config.set('Last_Sha','Sha',sha)
        lastsha = sha
        await channel.send (usrname+'updated his program. Watch whats new now: '+'https://github.com/'+ usrname + '/' + repname + '/commit/' + sha)

    with open ('User_data.ini','w') as config_file:
        config.write(config_file)
    config_file.close()

def Reddit_Subreddit_Section(message):
    index1=3
    Bol1=True
    Reddit_Subreddit=''
    Section=''
    while (not(index1 == len(message.content))and(Bol1)):
        if message.content[index1] == '-':
            Bol1=False
            index1+=1
            break
        else:
            Reddit_Subreddit+=message.content[index1]
            index1+=1
    
    for index2 in range (index1,len(message.content)):
        Section+=message.content[index2]

    return(str(Section),str(Reddit_Subreddit))

async def reddit_API_usage(subreddit,section,message):
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
       await message.channel.send(post['data']['url'])

async def User_Level(message,function):
    config = configparser.ConfigParser()
    config.read('User_data.ini') 

    Username = str(message.author)

    k=3

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

    level = 0
    LevelExp = 1

    if function == 'GetLevel':
        while Expint > LevelExp:
            LevelExp = LevelExp + LevelExp * 2
            level += 1
        await message.channel.send('Your level is: '+ str(level) +'\n' + 'EXP until next level: ' + str(LevelExp-Expint)+' exp') 

    elif function == 'Add Exp':
        Expint = Expint + k * len(message.content)
        config.set(Username,'UserExp',str(Expint))
        with open ('User_data.ini','w') as config_file:
            config.write(config_file)

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
                await message.channel.send(help_text)

            elif message.content.startswith('#LOGIN-SHEESH-PASSWORD-FAKER'):
                await message.channel.send(ee)

            elif message.content.startswith('#r/'):               
                Section,Subreddit = Reddit_Subreddit_Section(message)

                try:
                    await reddit_API_usage(str(Subreddit),str(Section),message)
                except Exception:
                   await message.channel.send('An error ocurred. Check the spelling of subreddit or section. Type #synt to see all reddit sections')

            elif message.content.startswith('#settinglist'):
                await message.channel.send(settinglist)

            elif message.content.startswith('#synt'):
                await message.channel.send(Synt)
            
            elif message.content.startswith('#level'):
                await User_Level(message,'GetLevel')

            elif message.content.startswith('#gitupdates'):
                command = message.content.split('=')
                if command[1] == 'start':    
                    await GetGitUpdates.start(message)
                elif command[1] == 'stop':
                    GetGitUpdates.stop
                    #print('stop ')

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
                 
            else:
                await message.channel.send(Error_text)

client.run(DisToken)