import asyncio# Модуль для работы с асинхронными операциями
import logging# Модуль для ведения логов (отслеживание и запись работы программы)

from aiogram import Bot, Dispatcher # Импорт классов для создания бота и диспетчера сообщений
from aiogram import types # Импортирует типы данных (например, для сообщений)
from aiogram.filters import CommandStart, Command #Импорт класса CommandStart из подмодуля filters библиотеки aiogram позволяет

import config


# фильтровать сообщения так, что проходить будет лишь команда /start Пример использования: @dp.message(CommandStart())
#BOT_TOKEN="получаем у бати ботов" ### Чтобы не спарсили ключ и от этого бота не рассылали спам уберем ключ в модуль config
dp = Dispatcher()
#bot = Bot(token=BOT_TOKEN)  # Создаем экземпляр bot перенесем в функцию main()

@dp.message(CommandStart())
async def handle_start(message: types.Message): #чтобы не засорять функцию echo_message создаем отдельную функцию на реагирования сообщения от пользователя /start
    await message.answer(text=f"Горячо приветствую {message.from_user.first_name}!") #message.from_user.username можно и .first_name и last_name b full_name

@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text= f" {message.from_user.first_name}! Я простой эхобот :(\n Отправь мне сообщение))"# можно и так усложнить переменной, а можно было как и start сразу написать
    await message.answer(text=text)

@dp.message()
async def echo_message(message: types.Message):  # создали ассинхронную функцию echo_message с типом параметра Меssage. функция папугай за пользователем
    await message.bot.send_message(
            # а это отправка сообщения через бота. если бота объявить в другой функции или мести, то вместо bot.send_message напишем message.bot.send_message
            chat_id=message.chat.id,
            # chat_id=  передаем сообщение в чат, message.chat.id узнаем в какой чат передовать сообщение
            text='Секундочку подожди')  # само сообщение, которое отправляет бот)
    await message.bot.send_message(
            chat_id=message.chat.id,
            text='Вижу Ваше сообщение',
            reply_to_message_id=message.message_id,)  # Ответ на то самое сообщение
    await message.answer(text='Думаю...')  # укороченный вариант await bot.send_message
    try:  # не все условия описаны в message.send_copy и потому можем словить ошибку. вводим исключение try
        await message.send_copy(
            chat_id=message.chat.id)  # все условия, которые написаны внизу реализовано в этом методе
    except TypeError:
        await message.reply(text='какой неповторимый объект :)')



     # if message.text: #эта штука не отвечает на стикеры и потому поставили условие ответа
     #    await message.answer(           # await типа ждать выполнения ассинхроной операции. Кароч приняли сообщение от пользователя и ему это вернули
     #        text=message.text
     #    )
     #
     #    await message.reply(text=message.text) #.reply отвечаем именно на то самое сообщение пользователя
     #
     #
     # elif message.sticker:  #если сообщение sticker ответим этим же стикером
     #     await bot.send_sticker(
     #          chat_id = message.chat.id,
     #          sticker = message.sticker.file_id
     #     )
     #     await message.reply_sticker(sticker=message.sticker.file_id) #делает то же самое, но запись короче
     # else:
     #     await message.reply(text='какой неповторимый объект :)'
     #     )

async def main():
    logging.basicConfig(level=logging.DEBUG) #все логи уровня Debug должны быть отражены
    bot = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(bot)    #.start_polling() (начинает опрос Telegram API на предмет новых обновлений для вашего бота.)
                                # ассинхронный метод и потому поставили await

if __name__ == "__main__":
    asyncio.run(main()) #так выполним запуск ассинхронной функции main