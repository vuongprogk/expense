from datetime import datetime
import json
import os.path
from unittest import result

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import get_spreadsheet_id

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]
SPREADSHEET_ID = get_spreadsheet_id()


# get service to interact with sheet
def get_service():
    service = None
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print(err)
    return service


# append value to the end of the sheet
def append_value(expense, range_name):
    try:
        service = get_service()
        body = {"values": expense}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# get the total of expense in current month
def get_total():
    try:
        service = get_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=SPREADSHEET_ID, range="summary!b5")
            .execute()
        )
        rows = result.get("values", [])
        return rows[0][0]
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
