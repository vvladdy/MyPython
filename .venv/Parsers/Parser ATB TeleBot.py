import datetime
from datetime import timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from Myinfo import yablonvlbot_token
from ParserATBAsync import collect_data, get_promo
from aiofiles import os



bot = Bot(token=yablonvlbot_token)
dp = Dispatcher(bot)

promo = get_promo()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = get_promo()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Please select sale ATB ', reply_markup=keyboard)

@dp.message_handler()
async def promo_1(message: types.Message):
    start_buttons = get_promo()
    await message.answer(f'Promo {message.text}')
    if message.text in start_buttons:
        await message.answer('Please waiting...')
        print(message.text)
        chat_id = message.chat.id
        await send_data(promo=message.text, chat_id=chat_id)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Not such promo... Please click /start')

async def send_data(promo='', chat_id=''):
    file = await collect_data(promo=promo)
    await bot.send_message(chat_id=chat_id,
                           text='Now you can download your file')

    # with open('Files/ATB/ids.txt', 'r') as file_id:
    #     file_id.read()
    with open('Files/ATB/ids.txt', 'a') as file_id:
        file_id.write(str(chat_id)+'\n')
    await bot.send_document(chat_id=chat_id, document=open(
        f'Files/ATB/{file}', 'rb'))
    # await os.remove(file)

if __name__ == '__main__':
    executor.start_polling(dp)








#
# @dp.message_handler(commands='start')
# async def start(message: types.Message):
#     start_buttons = get_promo()
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*start_buttons)
#
#     await message.answer('Please select sale ATB ', reply_markup=keyboard)
#
# @dp.message_handler(Text(equals='sim_dniv'))
# async def promo_1(message: types.Message):
#     await message.answer('Please waiting...')
#     chat_id = message.chat.id
#     await send_data(promo='sim_dniv', chat_id=chat_id)
#
# @dp.message_handler(Text(equals='new'))
# async def promo_1(message: types.Message):
#     await message.answer('Please waiting...')
#     chat_id = message.chat.id
#     await send_data(promo='new', chat_id=chat_id)
#
# @dp.message_handler(Text(equals='economy'))
# async def promo_1(message: types.Message):
#     await message.answer('Please waiting...')
#     chat_id = message.chat.id
#     await send_data(promo='economy', chat_id=chat_id)
#
# @dp.message_handler(Text(equals='novorichni_zini'))
# async def promo_2(message: types.Message):
#     await message.answer('Please waiting...')
#     chat_id = message.chat.id
#     await send_data(promo='novorichni_zini', chat_id=chat_id)

# async def send_data(promo='', chat_id=''):
#     file = await collect_data(promo=promo)
#     await bot.send_message(chat_id=chat_id,
#                            text='Now you can download your file')
#
#     # with open('Files/ATB/ids.txt', 'r') as file_id:
#     #     file_id.read()
#     with open('Files/ATB/ids.txt', 'a') as file_id:
#         file_id.write(str(chat_id)+'\n')
#     await bot.send_document(chat_id=chat_id, document=open(
#         f'Files/ATB/{file}', 'rb'))
#     # await os.remove(file)
#
# if __name__ == '__main__':
#     executor.start_polling(dp)
