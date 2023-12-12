import logging

import pandas as pd
import telebot
from dotenv import load_dotenv

YOUR_TELEGRAM_BOT_API_TOKEN = "6461265385:AAFR2e6PC6xHL4luokHiL9mBn4LTyoeXVL8"
YOUR_TELEGRAM_CHAT_IDS = [562928180]

bot_api_token = YOUR_TELEGRAM_BOT_API_TOKEN
bot = telebot.TeleBot(bot_api_token)
chat_ids = YOUR_TELEGRAM_CHAT_IDS


def send_dataframe_to_telegram(dataframe):
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id, dataframe.to_string())
        except Exception as e:
            logging.error(f"Failed to send dataframe to {chat_id}\nError:{e}")
