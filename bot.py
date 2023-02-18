from time import sleep
import logging
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

logging.basicConfig(
    filename="log.txt",
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)


# async def send_msg(msg: str):
#     message_entity = await client.send_message(entity=CHAT_ID, message=msg, silent=True)
#     print(f"Notify message [{message_entity.id}] send")
#     return message_entity


async def delete_msg(message_id):
    for _ in range(5):
        try:
            await client.delete_messages(entity=CHAT_ID, message_ids=[message_id])
            break
        except Exception as e:
            print(e)
            client.get_dialogs()
            sleep(3)


@client.on(events.NewMessage(chats=CHAT_ID))
async def my_event_handler(event):
    message_id = event.original_update.message.id
    message = event.original_update.message.message
    user_id = event.original_update.message.from_id.user_id

    if user_id == SHMA_ID:
        if any((
            message.startswith("🎣 [Рыбалка] 🎣"),
            message.startswith("От вашего врага давно не было вестей"),
            message.split('\n')[0].startswith("Нападающий") and message.split('\n')[1].startswith("Защищающийся"),
            re.match(r"^.+У вас больше не осталось сил для сражений", message, re.IGNORECASE | re.DOTALL)
        )):
            notification = f"Deleting message from SHMALALA after {TIMEOUT_SHMA} seconds"
            print(notification)
            logging.info(notification)
            sleep(TIMEOUT_SHMA)
            await delete_msg(message_id)
    else:
        if any((
            re.match(r"^(?:@shmalala_bot)?\s*Шма\s*.*рыбалка", message, re.IGNORECASE | re.DOTALL),
            re.match(r"^(?:@shmalala_bot)?\s*Шма\s*.*лови\s*рыбу", message, re.IGNORECASE | re.DOTALL),
            re.match(r"^(?:@shmalala_bot)?\s*(?:Шма)?\s*.*Дуэль", message, re.IGNORECASE | re.DOTALL),
            re.match(r"^(?:@shmalala_bot)?\s*(?:Шма)?\s*.*топ\s+(богачей|богатых)", message, re.IGNORECASE | re.DOTALL),
            re.match(r"^(?:@shmalala_bot)?\s*(?:Шма)?\s*(мяу|гав)", message, re.IGNORECASE | re.DOTALL),
            re.match(r"^(?:@shmalala_bot)?\s*Шма\s*.*покажи\s*(собаку|кота|кошку)", message, re.IGNORECASE | re.DOTALL)
        )):
            # username = (await event.get_sender()).username
            notification = f"Deleting message from {user_id} after {TIMEOUT_PEOPLE} seconds"
            print(notification)
            logging.info(notification)
            sleep(TIMEOUT_PEOPLE)
            await delete_msg(message_id)

client.start()
print("Starting...")
client.run_until_disconnected()
