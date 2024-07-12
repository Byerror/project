from telethon import TelegramClient, events
import time
import re
import random
import asyncio

# Замените эти значения на свои API ID, API хеш и номер телефона
api_id = '20045757'
api_hash = '7d3ea0c0d4725498789bd51a9ee02421'
phone = '+79954748369'

client = TelegramClient('your_bot_session', api_id, api_hash)

# Получите свой ID пользователя
my_id = None

@client.on(events.NewMessage(pattern=r".*report\s+(\d+).*"))
async def handle_report(event):
    match = re.search(r"report\s+(\d+)", event.message.text)
    if match:
        total_report_count = int(match.group(1))
        success_count = random.randint(0, total_report_count)

        await event.message.edit(f"Отправка отчета...")
        time.sleep(2)  # Имитация задержки
        await event.message.edit(f"Успешно {success_count}/{total_report_count}\nSuccessfully")

@client.on(events.NewMessage(pattern=r".*emails\s+(\d+)\s+(.+)\s+(.+)"))
async def handle_emails(event):
    match = re.search(r"emails\s+(\d+)\s+(.+)\s+(.+)", event.message.text)
    if match:
        email_count = int(match.group(1))
        subject = match.group(2)
        text = match.group(3)

        success_count = random.randint(0, email_count)

        await event.message.edit(f"Отправка писем...")
        time.sleep(2)  # Имитация задержки
        await event.message.edit(f"Успешно отправлено {success_count}/{email_count} писем\nSuccessfully")

@client.on(events.NewMessage(pattern=r".*menu.*"))
async def handle_menu(event):
    await event.message.edit("**крч я юзер бот от богоподобного, который может отправлять жалобы круто а мне пофиг**.\n\n"
                     "```Используйте команду .report [количество] для отправки жалоб мде.```\n\n"
                     "```Используйте команду .emails [количество писем] [тема] [текст] для отправки писем.```")
                     
@client.on(events.NewMessage(pattern=r".*ping.*"))
async def handle_ping(event):
    ping = random.randint(14, 1000)
    await event.message.edit(f"Ваш телеграмм пинг: {ping} ms")

@client.on(events.NewMessage(pattern=r".*spam\s+(\d+)\s+(.+)\s+(\d+)"))
async def handle_spam(event):
    global my_id
    if event.sender_id == my_id:
        match = re.search(r"spam\s+(\d+)\s+(.+)\s+(\d+)", event.message.text)
        if match:
            count = int(match.group(1))
            text = match.group(2)
            delay = float(match.group(3))

            for _ in range(count):
                await event.message.respond(text)
                time.sleep(delay)
    else:
        await event.message.respond("Извини, ты не можешь использовать эту команду.")


async def main():
    global my_id  
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone) # Используем await для send_code_request
        client.sign_in(phone, input('Enter the code: '))
    my_id = (await client.get_me()).id
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())