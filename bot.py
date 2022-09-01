import asyncio
from asyncore import dispatcher
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from auth_data import token
from site_data_getter import get_records, get_free_records

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot)

def records_to_string(date, records):
    string = f"<b>{date}</b>\n"
    for record in records:
        string += f"Время: {record['time']}\n" \
                  f"Дата: {record['date']}\n" \
                  f"Запись: <u>{'есть места' if record['isFree'] else 'мест нет'}</u>\n\n"
    return string

@dispatcher.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все записи", "Свободные записи", "Следить за обновлениями"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Посмотреть записи для медосмотра в общежитие:", reply_markup=keyboard)

@dispatcher.message_handler(Text(equals="Все записи"))
async def send_all_records(message: types.Message):
    records = get_records()
    for key, value in records.items():
        await message.answer(records_to_string(key, value))

@dispatcher.message_handler(Text(equals="Свободные записи"))
async def send_free_records(message: types.Message):
    free_records = get_free_records()
    if len(free_records) == 0:
        await message.answer("<b>Нет свободных записей</b>")
    else:
        for key, value in free_records.items():
            await message.answer(records_to_string(key, value))

async def check_free_records(user_id):
    while True:
        free_records = get_free_records()
        if len(free_records) != 0:
            for key, value in free_records.items():
                await bot.send_message(user_id, records_to_string(key, value))
        await asyncio.sleep(1800)

@dispatcher.message_handler(Text(equals="Следить за обновлениями"))
async def monitor_free_records(message: types.Message):
    loop = asyncio.get_event_loop()
    loop.create_task(check_free_records(message.from_id))

if __name__ == "__main__":
    executor.start_polling(dispatcher)