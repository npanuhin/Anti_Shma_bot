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


async def send_notify_msg_to_chat(msg: str):
    message_entity = await client.send_message(entity=CHAT_ID, message=msg, silent=True)
    print(f"Notify message [{message_entity.id}] send")
    return message_entity


async def delete_msg(message_entity):
    await client.delete_messages(entity=CHAT_ID, message_ids=[message_entity.id])
    print(f"Notify message [{message_entity.id}] deleted")


@client.on(events.NewMessage(chats=CHAT_ID))
async def my_event_handler(event):
    message_id = event.original_update.message.id
    message = event.original_update.message.message
    user_id = event.original_update.message.from_id.user_id

    if user_id == SHMA_ID and message.split('\n')[0] == "🎣 [Рыбалка] 🎣":
        msg_str = f"Deleting message from SHMALALA after {TIMEOUT_SHMA} seconds"
        msg_entity = await send_notify_msg_to_chat(msg_str)
        sleep(TIMEOUT_SHMA)
        await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])
        await delete_msg(msg_entity)

    elif re.fullmatch(r"Шма[,\.]?\s+рыбалка", message, re.IGNORECASE):
        username = (await event.get_sender()).username
        msg_str = f"Deleting message from {username} after {TIMEOUT_PEOPLE} seconds"
        msg_entity = await send_notify_msg_to_chat(msg_str)
        sleep(TIMEOUT_PEOPLE)
        await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])
        await delete_msg(msg_entity)

client.start()
client.run_until_disconnected()
