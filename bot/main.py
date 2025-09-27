from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
admin = os.getenv("ADMIN_ID")
weburl = os.getenv("ADMIN_URL")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text="Open",
            web_app=WebAppInfo(url=weburl)
        )
    ]])
    await message.answer("Launch telegram webapp", reply_markup=keyboard)


@dp.message(lambda message: message.web_app_data is not None)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    # Get user info
    user = message.from_user
    username = f"@{user.username}" if user.username else "No username"
    
    # Create ticket message
    ticket_text = f"""
🎫 **New Account Request**
👤 From: {user.full_name} ({username})
🆔 User ID: {user.id}
📱 Service: {data.get('service', 'Unknown')}
📝 Desired Username: {data.get('username', 'Not specified')}
    """
    
    # Send to admin
    await bot.send_message(
        admin, 
        ticket_text,
        parse_mode="Markdown"
    )
    
    # Confirm to user
    await message.answer("✅ Your request has been submitted!")


# this new "web app" shit is just straight up stupid

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

