import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# --- MA'LUMOTLAR ---
API_TOKEN = '8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA'
ADMIN_ID = 7257755738

# --- UYG'OQ SAQLASH ---
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Tugmalar (Skrinshotingizdagidek)
def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("📊 Statistika"), KeyboardButton("✉️ Xabar yuborish"))
    keyboard.row(KeyboardButton("🎬 Kinolar"), KeyboardButton("🔐 Kanallar"))
    keyboard.row(KeyboardButton("👤 Adminlar"), KeyboardButton("⚙️ Sozlamalar"))
    keyboard.row(KeyboardButton("⬅️ Orqaga"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=get_admin_keyboard())
    else:
        await message.answer("👋 Assalomu alaykum!\n✍️ Kino kodini yuboring...")

@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("📊 Bot statistikasi:\n\nA'zolar: 1ta (Siz)")

@dp.message_handler(lambda message: message.text == "⬅️ Orqaga")
async def back(message: types.Message):
    await message.answer("Bosh menyu", reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
    
