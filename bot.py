from telethon import TelegramClient, events
from time import sleep
import json
import re


# Get your credentials from https://my.telegram.org/apps and place in `credentials.json`
with open("credentials.json") as file:
    credentials = json.load(file)


CHAT_ID = 1694246507
SHMA_ID = 200164142

TIMEOUT_SHMA = 10
TIMEOUT_PEOPLE = 3


api_id = credentials["api_id"]
api_hash = credentials["api_hash"]
client = TelegramClient("session", api_id, api_hash)


@client.on(events.NewMessage(chats=CHAT_ID))
async def my_event_handler(event):
    message_id = event.original_update.message.id
    message = event.original_update.message.message
    user_id = event.original_update.message.from_id.user_id

    if user_id == SHMA_ID and message.split('\n')[0] == "🎣 [Рыбалка] 🎣":
        # sleep(10)
        print(f"Deleting message from SHMALALA in {TIMEOUT_SHMA} seconds")
        sleep(TIMEOUT_SHMA)
        await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])

    elif re.fullmatch(r"Шма[,\.]?\s+рыбалка", message, re.IGNORECASE):
        print(f"Deletig message from {user_id} in {TIMEOUT_PEOPLE}")
        sleep(TIMEOUT_PEOPLE)
        await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])

client.start()
client.run_until_disconnected()
