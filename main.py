import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
API_TOKEN = '8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA'
ADMIN_ID = 7257755738

# --- UYG'OQ TUTUVCHI SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 holatda!"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# --- BOT ---
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Admin Tugmalari
def admin_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📊 Statistika", "✉️ Xabar yuborish")
    kb.row("🎬 Kinolar", "🔐 Kanallar")
    kb.row("👤 Adminlar", "⚙️ Sozlamalar")
    kb.add("⬅️ Orqaga")
    return kb

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=admin_kb())
    else:
        await message.answer("🎬 Salom! Kino kodini yuboring...")

@dp.message_handler(lambda m: m.text == "📊 Statistika")
async def stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👥 Foydalanuvchilar: 1\n🎬 Kinolar: 0")

@dp.message_handler(lambda m: m.text == "⬅️ Orqaga")
async def back(message: types.Message):
    await message.answer("Bosh menyu", reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
    
