from time import sleep
import re

from telethon import TelegramClient, events
import jstyleson as json


# Get your credentials on https://my.telegram.org/apps and place them in `settings.json`
with open("settings.json") as file:
    settings = json.load(file)


TIMEOUT_SHMA = settings["timeout_shma"]
TIMEOUT_PEOPLE = settings["timeout_people"]

CHAT_ID = settings["chat_id"]
SHMA_ID = settings["shma_id"]

client = TelegramClient("session", settings["api_id"], settings["api_hash"])


# async def send_msg(msg: str):
#     message_entity = await client.send_message(entity=CHAT_ID, message=msg, silent=True)
#     print(f"Notify message [{message_entity.id}] send")
#     return message_entity


# async def delete_msg(message_entity):
#     await client.delete_messages(entity=CHAT_ID, message_ids=[message_entity.id])
#     print(f"Notify message [{message_entity.id}] deleted")


@client.on(events.NewMessage(chats=CHAT_ID))
async def my_event_handler(event):
    message_id = event.original_update.message.id
    message = event.original_update.message.message
    user_id = event.original_update.message.from_id.user_id

    if user_id == SHMA_ID:
        if message.split('\n')[0] == "🎣 [Рыбалка] 🎣":
            print(f"Deleting message from SHMALALA after {TIMEOUT_SHMA} seconds")
            sleep(TIMEOUT_SHMA)
            await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])
    else:
        if any((
            re.match(r"^(@shmalala_bot)?\s*Шма\s*.*рыбалка", message, re.IGNORECASE),
            re.match(r"^(?:@shmalala_bot)?\s*(?:Шма)?\s*.*Дуэль", message, re.IGNORECASE)
        )):
            username = (await event.get_sender()).username
            print(f"Deleting message from {username} after {TIMEOUT_PEOPLE} seconds")
            sleep(TIMEOUT_PEOPLE)
            await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])

client.start()
print("Starting...")
client.run_until_disconnected()
