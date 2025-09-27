from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CallbackQuery
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
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(
                text="📝 Account application",
                web_app=WebAppInfo(url=weburl)
            )
        ]],
        resize_keyboard=True
    )
    await message.answer("Click the button below to open the form", reply_markup=keyboard)
    print(f"Start command received from {message.from_user.id}")

@dp.message()
async def handle_all(message: types.Message):
    print(f"Received message type: {message.content_type}")
    
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
📧 Email: {data.get('email', 'Not provided')}
💬 Reason: {data.get('reason', 'Not provided')}
            """
            
            # Add admin control buttons
            admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="✅ Approve", 
                    callback_data=f"approve_{user.id}_{data.get('service', 'unknown')}"
                ),
                types.InlineKeyboardButton(
                    text="❌ Deny", 
                    callback_data=f"deny_{user.id}"
                )
            ]])
            
            await bot.send_message(
                admin, 
                ticket_text, 
                parse_mode="Markdown",
                reply_markup=admin_keyboard
            )
            await message.answer("Your request has been submitted!")
            
        except Exception as e:
            print(f"Error processing data: {e}")
            await message.answer("❌ Error processing your request")

@dp.callback_query(lambda c: c.data.startswith('approve_'))
async def approve_request(callback: types.CallbackQuery):
    try:
        parts = callback.data.split('_')
        user_id = int(parts[1])
        service = parts[2] if len(parts) > 2 else "the requested"
        
        # Notify the user
        await bot.send_message(
            user_id, 
            f"Your {service} account has been approved!"
        )
        
        # Update admin message to show it was approved
        new_text = callback.message.text + "\n\n✅ **APPROVED**"
        await callback.message.edit_text(new_text, parse_mode="Markdown")
        
        # Confirm to admin
        await callback.answer("Request approved! User has been notified.")
        
    except Exception as e:
        print(f"Error approving request: {e}")
        await callback.answer("Error processing approval", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith('deny_'))
async def deny_request(callback: types.CallbackQuery):
    try:
        _, user_id = callback.data.split('_')
        user_id = int(user_id)
        
        # Notify the user
        await bot.send_message(
            user_id, 
            "Unfortunately, your account request has been denied."
        )
        
        # Update admin message to show it was denied
        new_text = callback.message.text + "\n\n❌ **DENIED**"
        await callback.message.edit_text(new_text, parse_mode="Markdown")
        
        # Confirm to admin
        await callback.answer("Request denied. User has been notified.")
        
    except Exception as e:
        print(f"Error denying request: {e}")
        await callback.answer("Error processing denial", show_alert=True)

# this is stupid actually

async def main():
    print(f"Bot starting... Admin ID: {admin}, Web URL: {weburl}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
