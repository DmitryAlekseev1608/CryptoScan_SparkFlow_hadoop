import telebot
import pandas as pd
from dotenv import load_dotenv
import logging
import os

bot_api_token = os.getenv('TELEGRAM_BOT_API_TOKEN')
bot = telebot.TeleBot(bot_api_token)
chat_ids = os.getenv('TELEGRAM_CHAT_IDS')


def send_dataframe_to_telegram(dataframe):
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id, dataframe.to_string())
        except Exception as e:
            logging.error(f'Failed to send dataframe to {chat_id}\nError:{e}')
