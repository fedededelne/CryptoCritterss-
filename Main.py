from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import os

critters = [
    {"name": "Byteclaw", "rarity": "Common", "image": "https://i.imgur.com/NruCL9u.png"},
    {"name": "Cryphos", "rarity": "Rare", "image": "https://i.imgur.com/tHhL1wB.png"},
    {"name": "Neurofang", "rarity": "Epic", "image": "https://i.imgur.com/h8Se5uW.png"},
    {"name": "Shardscale", "rarity": "Legendary", "image": "https://i.imgur.com/ZwDoB1Y.png"},
    {"name": "Hexhorn", "rarity": "Mythic", "image": "https://i.imgur.com/wskTGgD.png"}
]

users = {}
app = Flask('')

@app.route('/')
def home():
    return """
    <html>
      <head>
        <title>CryptoCritterss</title>
        <style>
          body { font-family: sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 50px; }
          h1 { color: #ffcc00; }
          img { max-width: 200px; margin-top: 20px; }
          a { color: #00ffff; }
        </style>
      </head>
      <body>
        <h1>Welcome to CryptoCritterss!</h1>
        <p>Collect rare creatures, explore the world, and build your critter army on Telegram.</p>
        <p><strong>Start now:</strong> <a href="https://t.me/CryptoCritterssBot">@CryptoCritterssBot</a></p>
        <img src="https://i.imgur.com/NruCL9u.png" />
        <p>More features and NFT integrations coming soon!</p>
      </body>
    </html>
    """

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = random.choice(critters)
    await update.message.reply_text("Welcome to CryptoCritterss! Use /mycritter to view your creature.")

async def mycritter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = random.choice(critters)
    critter = users[user_id]
    await update.message.reply_photo(critter["image"],
        caption=f"Your Critter:\nName: {critter['name']}\nRarity: {critter['rarity']}")

async def explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_critter = random.choice(critters)
    users[update.effective_user.id] = new_critter
    await update.message.reply_photo(new_critter["image"],
        caption=f"You found a new Critter!\nName: {new_critter['name']}\nRarity: {new_critter['rarity']}")

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Shop!\n\n"
        "Upgrade Options:\n"
        "1. Level Boost - $0.99\n"
        "2. Unlock Rare Critter - $2.99\n"
        "3. Mythic Critter Pack - $5.99\n\n"
        "Payments coming soon. Stay tuned!"
    )

def main():
    keep_alive()
    application = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mycritter", mycritter))
    application.add_handler(CommandHandler("explore", explore))
    application.add_handler(CommandHandler("shop", shop))
    application.run_polling()

if __name__ == "__main__":
    main()
