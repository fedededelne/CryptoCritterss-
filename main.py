import os
import logging
from flask import Flask, request
import telegram

# Imposta il logging
logging.basicConfig(level=logging.INFO)

# Inizializza Flask app
app = Flask(__name__)

# Leggi il token del bot da variabile d'ambiente
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    if message_text == "/start":
        bot.sendMessage(chat_id=chat_id, text="Welcome to CryptoCritters! Get ready to hatch your digital pet.")
    else:
        bot.sendMessage(chat_id=chat_id, text="Use /start to begin your adventure!")

    return 'ok'

@app.route("/")
def index():
    return "CryptoCritters Bot is running!"

if __name__ == "__main__":
    app.run(threaded=True)
