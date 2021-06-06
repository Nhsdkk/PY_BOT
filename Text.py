import discord

color = 0x874aff

Error_text = 'Unknown command. Type \'#help\' for all bot commands.'
ee='Q09OR1JBVFMhIFlvdSBmb3VuZCB0aGUgZWFzdGVyIGVnZywgYnV0IGF0IHdoYXQgY29zdC4gQW55d2F5IHRoaXMgaXMgRWFzdGVyIEVnZyA6IFRoZSBkZXZlbG9wZXIgcXVpdGVkIGxlYWd1ZSB0aGUgc2FtZSBkYXkgaGUgc3RhcnRlZCB0aGlzIHByb2plY3Q= (BASE 64 System)'

dic_help = {
    '#lets-go':'command for sending \'Hello\'',
    '#Level':'command, which shows you your level',
    '#r/ + \'subreddit\' + \'=\' + \'section (hot,new,etc.)\'':'command for getting 25 reddit posts from the subreddit you requested',
    '#gitupdates=start':'starts sending github repository updates to a channel',
    '#gitupdates=stop':'stops sending github repository updates to a channel',
    '#settings=\'setting(use #settinglist to see all settings)\'=\'value\'':'adding or updating a setting',
    '#addbm':'sends the message you replied to in pm',
    '#removebm':'deletes bot\'s message, that replied to in private message',
    '#curtrack':'sends an information about a track that you are listening to at this moment',
    '#wakeup+\'person mention\' +\'channel mention\'': 'sends a wake up message to the person you mentioned'    
} 

htextemb = discord.Embed(title = 'Bot commands',color = color)
for k,v in dic_help.items():
    htextemb.add_field(name = k,value = v,inline=False)

settingsemb = discord.Embed(title = 'Settings',color = color)
settingsemb.add_field(name = 'gitchannel',value = 'channel where gits will be send',inline=False)
settingsemb.add_field(name = 'gitrep',value = 'repository you are tracking',inline=False)
settingsemb.add_field(name = 'gitusername',value = 'username of the owner of the repository you are tracking',inline=False)
settingsemb.set_thumbnail(url = 'https://img.icons8.com/ios/452/settings--v2.png')

Syntemb = discord.Embed(title = 'All subreddit sections',color=color)
Syntemb.add_field(name='hot',value = 'hot subreddit posts',inline=False)
Syntemb.add_field(name='new',value = 'new subreddit posts',inline=False)
Syntemb.add_field(name='best',value = 'best subreddit posts',inline=False)
Syntemb.add_field(name='top',value = 'top subreddit posts',inline=False)
Syntemb.add_field(name='rising',value = 'rising subreddit posts',inline=False)
Syntemb.set_thumbnail(url = 'https://cdn0.iconfinder.com/data/icons/social-flat-rounded-rects/512/reddit-512.png')
