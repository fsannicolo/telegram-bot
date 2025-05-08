from typing import Final
from telegram import Update, ReactionTypeEmoji
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import configparser

import requests
import json 

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN: Final = config.get('AUTH', 'token', fallback=None)

BOT_USERNAME: Final = '@MyMarconiBot'

api_url = 'http://naas.isalman.dev/no'

# gestione dei comandi
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ciao! Sono il MarconiBot')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Digita qualcosa e vediamo che succede!')

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_text = update.message.text.replace('/echo', '').strip() 
    await update.message.reply_text(new_text, do_quote=True) 

# gestione API
async def no_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        risposta = requests.get(api_url, timeout=5)
        risposta.raise_for_status() 

        # tutto ok
        if risposta.status_code == 200:
            dati = risposta.json()
            print(dati) 

            # estraggo la risposta dai dati
            message = dati.get('reason')

            await update.message.reply_text(message)
        else:
            await update.message.reply_text('Non ho potuto recuperare una risposta')

    except requests.exceptions.RequestException as e:
        print(f'Si è verificato un errore: {e}')  

# gestione delle risposte
def handle_response(text: str) -> str:
    if 'ciao' in text.lower():
        return 'Ehilà!'
    elif 'adoro' in text.lower() or 'mi piace' in text.lower():
        return 'love'
    else:
        return 'Non ho capito cosa devo fare'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # recupera il tipo di chat in cui si trova il bot
    message_type = update.message.chat.type

    # testo del messaggio ricevuto
    text = update.message.text

    print(f'Utente {update.message.chat.id} in {message_type}: "{text}"')

    risposta = handle_response(text)
    print('Bot:', risposta)

    if risposta != 'love':
        await update.message.reply_text(risposta)
    else:
        await update.message.set_reaction(reaction=[ReactionTypeEmoji('❤️')])

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} causato errore {context.error}') 


if __name__ == '__main__':
    print('Bot avviato...')
    app = Application.builder().token(TOKEN).build()

    # gestione comandi
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('echo', echo_command))
    app.add_handler(CommandHandler('no', no_command))

    # gestione messaggi
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # gestione errori
    app.add_error_handler(error)

    # aspettare nuovi messaggi
    print('Polling...')
    app.run_polling(poll_interval=3)

