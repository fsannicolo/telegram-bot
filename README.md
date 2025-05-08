# Marconi Telegram Bot
A simple Telegram bot with custom commands that can recognize some words and emotions. 

## Requirements
Create your own Telegram bot with [BotFather](https://telegram.me/BotFather).

API token needs to be stored in a `config.ini` file:
```
[AUTH]
token = <your_token>
```

## Dependancies
This project requires some libraries: `python-telegram-bot` and `requests`  
    
    pip install -r requirements.txt

## Commands
- `/start`
- `/help` 
- `/echo` replies to the last message  quoting the user
- `/no` exploits a no-as-a-service API to get a random rejection response

## Credits
Thanks to [hotheadhacker](https://github.com/hotheadhacker/no-as-a-service) for providing this cool NaaS API.
