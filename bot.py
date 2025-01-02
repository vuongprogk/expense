from calendar import month
import datetime
import json
import os
import re
from dotenv import load_dotenv
import telebot
from sheetapi import append_value
from utils import *

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
MAX_TRY = 3


# greetting
@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = "Hello before we need some steps to verified.\nPlease input secret code"
    secret = id_generator()
    print("Use this code to verified: " + secret)
    sent_msg = bot.send_message(message.chat.id, text=text)
    bot.register_next_step_handler(sent_msg, authen_handler, 0, secret)


def authen_handler(message, count, secret):
    result = message.text
    if count > MAX_TRY:
        bot.reply_to("You exceed the max time try call the admin for support")
        return
    else:
        if result == secret:
            data = {message.chat.id: message.from_user.id}
            with open("verified.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=True)
            bot.send_message(chat_id=message.chat.id, text="You be verified")
        else:
            text = f"You try {count} time in {MAX_TRY} time try"
            sent_msg = bot.send_message(message.chat.id, text=text)
            bot.register_next_step_handler(sent_msg, authen_handler, ++count, secret)


@bot.message_handler(commands=["add"])
def add_handler(message):
    data: string = message.text
    user_id = message.from_user.id
    if not verified(f"{user_id}"):
        bot.send_message(
            message.chat.id, "You do not have permission to do this action!"
        )
        return
    data = data.split(" ")
    if len(data) < 3:
        bot.send_message(
            message.chat.id,
            "Make sure you input correct format\nAdd expense with format /add <amount> <purpose>",
        )
        return
    data = data[1:]
    amount = data[0]
    purpose = data[1:]
    if re.search("[kK]$", amount) != None:
        amount = re.sub("[kK]$", "000", amount)
    purpose = " ".join(purpose)
    if re.search("[^0-9]", amount):
        bot.send_message(message.chat.id, "You must input the amount of money first")
        return
    date = datetime.datetime.now().date()
    day = date.day
    month = date.month
    year = date.year
    result = append_value(
        [[amount, purpose, f"{day}", f"{month}", f"{year}"]],
        "Figure!a1:e1",
    )
    if type(result) != Exception:
        bot.send_message(message.chat.id, "Add expense successfully")


@bot.message_handler(commands=["getlink"])
def add_handler(message):
    user_id = message.from_user.id
    if not verified(f"{user_id}"):
        bot.send_message(
            message.chat.id, "You do not have permission to do this action!"
        )
        return
    bot.send_message(message.chat.id, get_spreadsheet_link())


bot.infinity_polling()
