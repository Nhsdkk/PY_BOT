from asyncio.windows_events import SelectorEventLoop
from typing import List
import discord
import requests
import configparser
#import argparse

config = configparser.ConfigParser()
config.read('private_data.ini')
Reddit_client_id = config['Reddit']['rci']
Reddit_secret_token = config['Reddit']['rst']
username = config['Reddit']['user']
password = config['Reddit']['psw']
DisToken = config['Discord']['token']

client = discord.Client()

from Text import help_text
from Text import Error_text
from Text import ee
from Text import Synt

@client.event
async def on_ready():
    print('ready for {0.user}'.format(client))
#    is_ = False

def Reddit_Subreddit_Section(message):
    index1 = 3
    Bol1=True
    Reddit_Subreddit = ''
    Section = ''
    while (not(index1 == len(message.content))and(Bol1)):
        if message.content[index1] == '-':
            Bol1=False
            index1+=1
            break
        else:
            Reddit_Subreddit += message.content[index1]
            index1 += 1
    
    for index2 in range (index1,len(message.content)):
        Section += message.content[index2]
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

    except:
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


@client.event
async def on_message(message):
    if message.author == client.user:
        return      

    if message.content.startswith('#'):
            await User_Level(message,'Add Exp')
            if message.content.startswith('#lets-go'):
                await message.channel.send('DABABY')               

            elif message.content.startswith('#help'):
                await message.channel.send(help_text)

            elif message.content.startswith('#LOGIN-SHEESH-PASSWORD-FAKER'):
                await message.channel.send(ee)

            elif message.content.startswith('#r/'):               
                Section,Subreddit = Reddit_Subreddit_Section(message)

                try:
                    await reddit_API_usage(str(Subreddit),str(Section),message)
                except:
                    await message.channel.send('An error ocurred. Check the spelling of subreddit or section. Type #Synt to see all reddit sections')

            elif message.content.startswith('#Synt'):
                await message.channel.send(Synt)
            
            elif message.content.startswith('#Level'):
                await User_Level(message,'GetLevel')

            else:
                await message.channel.send(Error_text)

client.run(DisToken)