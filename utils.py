import json
import os
import string
import random

from dotenv import load_dotenv

load_dotenv()


# generator id to verified user to using command
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def verified(user_id):
    with open("verified.json", "r") as file:
        data = json.load(file)
        if user_id in data.keys():
            return True
    return False


# get spreadsheet link
def get_spreadsheet_link():
    return os.getenv("SPREADSHEET_LINK")


# get spreadsheet id
def get_spreadsheet_id():
    return os.getenv("SPREADSHEET_ID")
