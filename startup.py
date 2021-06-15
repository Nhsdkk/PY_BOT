import json
import os
import configparser
import sys

def converter ():
    private = True
    user = True
    if (os.path.exists('private_data.ini')):
        privini = configparser.ConfigParser()
        privini.read('private_data.ini')

        data = {}
        data['Reddit']={}
        data['Reddit']['rci'] = privini['Reddit']['rci']
        data['Reddit']['rst'] = privini['Reddit']['rst']
        data['Reddit']['user'] = privini['Reddit']['user']
        data['Reddit']['psw'] = privini['Reddit']['psw']
        data['Distoken'] = privini['Discord']['token']
        try:
            data['GeniusToken'] = privini['GeniusToken']
        except:
            data['GeniusToken'] = input('Enter Genius API token: ')

        with open ('private_data.json','w') as privfile:
            json.dump(data,privfile)

        os.remove('private_data.ini')
        private = True
    
    if (os.path.exists('User_data.ini')):
        userini = configparser.ConfigParser()
        userini.read('User_data.ini')

        datasett = {}
        datasett['github'] = {}
        datasett['channel_start_message'] = userini['disstart']['channelmsg']
        datasett['github']['channel'] = userini['github']['channel']
        datasett['github']['repository'] = userini['github']['rep']
        datasett['github']['username'] = userini['github']['username']

        with open ('settings.json','w') as setfile:
            json.dump(datasett,setfile)
        
        datt = {}
        datt['lastsha'] = userini['Last_Sha']['sha']
        for param in userini:
            if param.find('#')!= -1:
                datt[param] = {}
                datt[param]['UserExp'] = userini[param]['userexp']
                datt[param]['UserLevel'] = userini[param]['userlevel']

        with open ('data.json','w') as datfile:
            json.dump(datt,datfile)

        os.remove('User_data.ini')
        user=True

    if not(user):
        if not(os.path.exists('settings.json')):
            data = {}
            data['channel_start_message'] = input ('Enter system(bot) channel id: ')
            data['github'] = {}
            data['github']['channel'] = ''
            data['github']['repository'] = ''
            data['github']['username'] = ''
        else:
            with open('settings.json','r') as setfile:
                data = json.load(setfile)
                data['channel_start_message'] = input ('Enter system(bot) channel id: ')

        with open ('settings.json','w') as setfile:
            json.dump(data,setfile)

        if not(os.path.exists('data.json')):
            data = {}
            data['lastsha']=''
        
            with open ('data.json','w') as datafile:
                json.dump(data,datafile)
    elif not(private):
        if not(os.path.exists('private_data.json')):
            data = {}
            data['Reddit']={}
            data['Reddit']['rci'] = input ('Enter your reddit client id: ')
            data['Reddit']['rst'] = input ('Enter your reddit secret token: ')
            data['Reddit']['user'] = input ('Enter your reddit username: ')
            data['Reddit']['psw'] = input ('Enter your reddit password: ')
            data['Distoken'] = input('Enter discord\'s bot token: ')
            data['GeniusToken'] = input('Enter Genius API token(press Enter to skip this parameter): ')
            with open ('private_data.json','w') as privatef:
                json.dump(data,privatef)    

        else:
            with open ('private_data.json','r') as privatef:
                data = json.load(privatef)
            rci = input ('Enter your reddit client id(press Enter to skip this parameter): ')
            rst = input ('Enter your reddit secret token(press Enter to skip this parameter): ')
            user = input ('Enter your reddit username(press Enter to skip this parameter): ')
            psw = input ('Enter your reddit password(press Enter to skip this parameter): ')
            distoken = input('Enter discord\'s bot token(press Enter to skip this parameter): ')
            gentoken = input('Enter Genius API token(press Enter to skip this parameter): ')
            if rci != '':
                data['Reddit']['rci'] = rci
            if rst!= '':
                data['Reddit']['rst'] = rst
            if user!= '':
                data['Reddit']['user'] = user
            if psw!= '':
                data['Reddit']['psw'] = psw
            if distoken!= '':
                data['Distoken'] = distoken
            if gentoken!= '':
                data['GeniusToken'] = gentoken

            with open ('private_data.json','w') as privatef:
                json.dump(data,privatef)    




if (os.path.exists('private_data.ini')) or (os.path.exists('User_data.ini')):
    print ('Old version\'s files detected. Converting them...')
    converter()
    input('File configuration successful. Press any button to close installation programm...')   
    sys.exit()

if not(os.path.exists('private_data.json')):
    data = {}
    data['Reddit']={}
    data['Reddit']['rci'] = input ('Enter your reddit client id: ')
    data['Reddit']['rst'] = input ('Enter your reddit secret token: ')
    data['Reddit']['user'] = input ('Enter your reddit username: ')
    data['Reddit']['psw'] = input ('Enter your reddit password: ')
    data['Distoken'] = input('Enter discord\'s bot token: ')
    data['GeniusToken'] = input('Enter Genius API token(press Enter to skip this parameter): ')

    with open ('private_data.json','w') as privatef:
        json.dump(data,privatef)    

else:
    with open ('private_data.json','r') as privatef:
        data = json.load(privatef)
    rci = input ('Enter your reddit client id(press Enter to skip this parameter): ')
    rst = input ('Enter your reddit secret token(press Enter to skip this parameter): ')
    user = input ('Enter your reddit username(press Enter to skip this parameter): ')
    psw = input ('Enter your reddit password(press Enter to skip this parameter): ')
    distoken = input('Enter discord\'s bot token(press Enter to skip this parameter): ')
    gentoken = input('Enter Genius API token(press Enter to skip this parameter): ')
    if rci != '':
        data['Reddit']['rci'] = rci
    if rst!= '':
        data['Reddit']['rst'] = rst
    if user!= '':
        data['Reddit']['user'] = user
    if psw!= '':
        data['Reddit']['psw'] = psw
    if distoken!= '':
        data['Distoken'] = distoken
    if gentoken!= '':
        data['GeniusToken'] = gentoken

    with open ('private_data.json','w') as privatef:
       json.dump(data,privatef)    

if not(os.path.exists('settings.json')):
    data = {}
    data['channel_start_message'] = input ('Enter system(bot) channel id: ')
    data['github'] = {}
    data['github']['channel'] = ''
    data['github']['repository'] = ''
    data['github']['username'] = ''

    with open ('settings.json','w') as setfile:
        json.dump(data,setfile)
else:
    with open('settings.json','r') as setfile:
        data = json.load(setfile)
    stmsg = input ('Enter system(bot) channel id(press Enter to skip this parameter): ')
    if stmsg!= '':
        data['channel_start_message'] = stmsg

    with open ('settings.json','w') as setfile:
        json.dump(data,setfile)

if not(os.path.exists('data.json')):
    data = {}
    data['lastsha']=''

    with open ('data.json','w') as datafile:
        json.dump(data,datafile)

input('Installation successful. Press any button to close installation programm...')
