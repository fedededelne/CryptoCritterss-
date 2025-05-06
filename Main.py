from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import threading
import os

# === Flask setup for Render ===
app = Flask(__name__)

@app.route('/')
def home():
    return "CryptoCritters Bot is alive!"

# === Telegram Bot Setup ===
TOKEN = os.environ.get("TELEGRAM_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

# === Game Data ===
users = {}  # user_id -> {'creatures': [], 'level': 1, 'coins': 0}

creatures = [
    {"name": "Byteclaw", "rarity": "common"},
    {"name": "Cryphos", "rarity": "common"},
    {"name": "Glitcheel", "rarity": "rare"},
    {"name": "Cryptoflare", "rarity": "rare"},
    {"name": "Spectrabyte", "rarity": "legendary"},
]

rarity_weights = {
    "common": 0.7,
    "rare": 0.25,
    "legendary": 0.05
}

rarity_rewards = {
    "common": 10,
    "rare": 25,
    "legendary": 100
}

# === Game Logic ===

def get_random_creature():
    rarity = random.choices(
        population=["common", "rare", "legendary"],
        weights=[rarity_weights[r] for r in ["common", "rare", "legendary"]],
        k=1
    )[0]
    options = [c for c in creatures if c["rarity"] == rarity]
    return random.choice(options)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"creatures": [], "level": 1, "coins": 0}
    await update.message.reply_text("Welcome to CryptoCritters!\nUse /hunt to search for new creatures!")

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.setdefault(user_id, {"creatures": [], "level": 1, "coins": 0})

    creature = get_random_creature()
    user["creatures"].append(creature)
    user["coins"] += rarity_rewards[creature["rarity"]]

    await update.message.reply_text(
        f"You found a {creature['rarity'].capitalize()} creature: {creature['name']}!\n"
        f"You earned {rarity_rewards[creature['rarity']]} coins.\n"
        f"Use /inventory to view your collection."
    )

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users.get(update.effective_user.id)
    if not user or not user["creatures"]:
        await update.message.reply_text("You haven't found any creatures yet. Use /hunt!")
        return

    lines = ["Your CryptoCritters Collection:"]
    counts = {}
    for c in user["creatures"]:
        counts[c["name"]] = counts.get(c["name"], 0) + 1

    for name, qty in counts.items():
        lines.append(f"• {name} x{qty}")
    lines.append(f"Coins: {user['coins']}")

    await update.message.reply_text("\n".join(lines))

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users.get(update.effective_user.id)
    if not user:
        await update.message.reply_text("Start hunting first using /hunt!")
        return

    cost = user["level"] * 100
    if user["coins"] >= cost:
        user["coins"] -= cost
        user["level"] += 1
        rarity_weights["common"] -= 0.05
        rarity_weights["rare"] += 0.03
        rarity_weights["legendary"] += 0.02
        await update.message.reply_text(f"Upgrade successful! You're now level {user['level']}.")
    else:
        await update.message.reply_text(f"You need {cost} coins to upgrade! You have {user['coins']}.")

# === Command Handlers ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("hunt", hunt))
application.add_handler(CommandHandler("inventory", inventory))
application.add_handler(CommandHandler("upgrade", upgrade))

# === Launch Telegram bot in thread ===
def run_bot():
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
