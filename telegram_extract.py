import pytz
from classification_model import classify_message
from telethon import TelegramClient
import nest_asyncio
import asyncio
import pandas as pd
from datetime import datetime, timezone
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os

load_dotenv()

# Apply the nest_asyncio patch to allow nested event loops
nest_asyncio.apply()

# Use your own values from my.telegram.org
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
session_string = os.getenv('SESSION_STRING')
# Create the client with the saved session string
client = TelegramClient(StringSession(session_string), api_id, api_hash)

def merge_replies(row, df):
    if row['Reply_to'] != -1:
        # Find the main message by 'ID' of the row's 'Reply_to'
        main_message = df[df['ID'] == row['Reply_to']]['Message'].values
        if main_message.size > 0:
            # Concatenate the main message with the current message (reply)
            return main_message[0] + " " + row['Message']
    return row['Message']

async def fetch_messages():
    await client.start(phone_number)

    # Getting information about yourself
    me = await client.get_me()

    username = me.username
    output = []
    async for message in client.iter_messages(-1001957076600):
        print(message)
        output.append(message)
        if len(output) > 20:
            break

    return output

def merge_replies_df(output):
    data = {}
    data['Date'] = list(map(lambda x: x.date.astimezone(pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S'), output))
    data['Message'] = list(map(lambda x: x.message, output))
    data['ID'] = list(map(lambda x: x.id, output))
    data["Reply_to"] = list(map(lambda x: -1 if not x.reply_to else x.reply_to.reply_to_msg_id, output))
    df = pd.DataFrame(data)
    # Apply the merge function to each row
    df['Merged_Message'] = df.apply(lambda row: merge_replies(row, df), axis=1)

    return df

async def main():
    output = await fetch_messages()
    df = merge_replies_df(output)
    dir_path = r'combined_data'

    df["Classification"] = df['Message'].map(classify_message)
    df.to_csv(os.path.join(dir_path, 'telegram_messages.csv'), index=False)

if __name__ == '__main__':
    asyncio.run(main())