import configparser
import os

def create_config():
    config = configparser.ConfigParser()

    if os.path.exists('private_data.ini'): 
        os.remove('private_data.ini')  

    config.add_section('Reddit')
    config.set('Reddit','user',input ('Enter your reddit username: '))
    config.set('Reddit','psw',input ('Enter your reddit password: '))
    config.set('Reddit','RCI',input ('Enter your reddit client id: '))
    config.set('Reddit','RST',input ('Enter your reddit secret token: '))
    config.add_section('Discord')
    config.set('Discord','token',input('Enter discord\'s bot token: '))
    with open('private_data.ini','w') as config_file:
        config.write(config_file)

    config_file.close()

    input ('File was updated/created. Press any button to close setup program.')

if __name__ == '__main__':
    create_config()