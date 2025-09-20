#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Bot using pyTelegramBotAPI
- Stores user data (username + unique ID) in keyword.json
- Works on Termux, local PC, and GitHub hosting
"""

import telebot
import json
import os

# ---------------- Configuration ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8293183951:AAHP0tqzjDrOXLiM4g4lZZvkiB_gMP2vQss")
DATA_FILE = "keyword.json"

bot = telebot.TeleBot(BOT_TOKEN)

# ---------------- Persistence Helpers ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Global in-memory cache
user_data = load_data()

# ---------------- Handlers ----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "Welcome to @easy_money_bux_bot!\n\n"
        "➤ Join our Telegram group: https://t.me/ArifurHackworld\n\n"
        "👉 Please send me a unique ID number for your username."
    )
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def save_unique_id(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    unique_id = message.text.strip()

    # Save in memory + persist
    user_data[user_id] = {
        "username": username,
        "unique_id": unique_id
    }
    save_data(user_data)

    bot.reply_to(
        message,
        f"✅ Saved!\n\nYour username: @{username}\nYour unique ID: {unique_id}"
    )

# ---------------- Runner ----------------
if __name__ == "__main__":
    print("Bot is running... Press Ctrl+C to stop.")
    bot.infinity_polling()
