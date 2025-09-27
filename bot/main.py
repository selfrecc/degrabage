from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
weburl = os.getenv("WEB_URL")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text="Open",
            web_app=WebAppInfo(url=weburl)
        )
    ]])
    await message.answer("Open menu:", reply_markup=keyboard)


# this new "web app" shit is just straight up stupid


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

