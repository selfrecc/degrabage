from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, MenuButtonWebApp
import asyncio
import json
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
admin = int(os.getenv("ADMIN_ID"))
weburl = os.getenv("WEB_URL")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Try using a ReplyKeyboardMarkup instead
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(
                text="📝 Request Account",
                web_app=WebAppInfo(url=weburl)
            )
        ]],
        resize_keyboard=True
    )
    await message.answer("Click the button below to open the form:", reply_markup=keyboard)
    
    # Also log to confirm the command worked
    print(f"Start command received from {message.from_user.id}")

@dp.message()
async def handle_all(message: types.Message):
    print(f"Received message type: {message.content_type}")
    print(f"Message object: {message}")
    
    if message.web_app_data:
        print(f"WEB APP DATA RECEIVED: {message.web_app_data.data}")
        
        try:
            data = json.loads(message.web_app_data.data)
            
            user = message.from_user
            username = f"@{user.username}" if user.username else "No username"
            
            ticket_text = f"""
🎫 **New Account Request**
👤 From: {user.full_name} ({username})
🆔 User ID: {user.id}
📱 Service: {data.get('service', 'Unknown')}
📝 Desired Username: {data.get('username', 'Not specified')}
            """
            
            await bot.send_message(admin, ticket_text, parse_mode="Markdown")
            await message.answer("✅ Your request has been submitted!")
        except Exception as e:
            print(f"Error processing data: {e}")
            await message.answer("❌ Error processing your request")

async def main():
    print(f"Bot starting... Admin ID: {admin}, Web URL: {weburl}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

