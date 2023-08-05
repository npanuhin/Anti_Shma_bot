from time import sleep
import logging
import re

from telethon import TelegramClient, events
import jstyleson as json


# Get your credentials on https://my.telegram.org/apps and place them in `settings.json`
with open("settings.json") as file:
    settings = json.load(file)


assert settings["api_id"] != -1 and settings["chat_id"] != -1, "You haven't entered your credentials in settings.json"


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
    message = event.original_update.message.message.lower()
    user_id = event.original_update.message.from_id.user_id

    if user_id == SHMA_ID:
        if any((
            re.match(r"🎣\s*\[Рыбалка\]\s*🎣", message, re.IGNORECASE | re.DOTALL),
            re.match(r"🎣\s*\[Бар Шмы\]\s*🎣", message, re.IGNORECASE | re.DOTALL),
            message.startswith("от вашего врага давно не было вестей"),
            message.split('\n')[0].startswith("нападающий") and message.split('\n')[1].startswith("защищающийся"),
            re.match(r"^.+У вас больше не осталось сил для сражений", message, re.IGNORECASE | re.DOTALL)
        )):
            notification = f"Deleting message from SHMALALA after {TIMEOUT_SHMA} seconds"
            print(notification)
            logging.info(notification)
            sleep(TIMEOUT_SHMA)
            await delete_msg(message_id)
    else:
        if any((
            message.startswith("@shmalala_bot"),
            message.startswith("шма")
        )) and any((
            re.search(r"рыбалка", message, re.IGNORECASE | re.DOTALL),
            re.search(r"лови\s+рыбу", message, re.IGNORECASE | re.DOTALL),
            re.search(r"дуэль", message, re.IGNORECASE | re.DOTALL),
            re.search(r"топ\s+(богачей|богатых)", message, re.IGNORECASE | re.DOTALL),
            re.match(r"(мяу|гав)", message, re.IGNORECASE | re.DOTALL),
            re.search(r"покажи\s+(собаку|кота|кошку)", message, re.IGNORECASE | re.DOTALL),
            re.search(r"начинаем\s+пить", message, re.IGNORECASE | re.DOTALL),
            re.search(r"пьем\s+\w+", message, re.IGNORECASE | re.DOTALL)
        )):
            # username = (await event.get_sender()).username
            notification = f"Deleting message from {user_id} after {TIMEOUT_PEOPLE} seconds"
            print(notification)
            logging.info(notification)
            sleep(TIMEOUT_PEOPLE)
            await delete_msg(message_id)

client.start(phone=settings["phone"], password="fJZ2GtbqVdveaQuX")
print("Starting...")
client.run_until_disconnected()
