import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
API_TOKEN = '8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA'
ADMIN_ID = 7257755738

# Bazani simulyatsiya qilish (Vaqtinchalik xotira)
# Real loyihada buni MongoDB yoki SQLite ga ulash tavsiya etiladi
movies_db = {} 
users = set()

# --- UYG'OQ SAQLASH (RENDER UCHUN) ---
app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 holatda ishlamoqda!"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOTNI SOZLASH ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Tugmalar
admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.row("📊 Statistika", "✉️ Xabar yuborish")
admin_menu.row("🎬 Kinolar", "🔐 Kanallar")
admin_menu.row("👤 Adminlar", "⚙️ Sozlamalar")
admin_menu.row("⬅️ Orqaga")

@dp.message_handler(commands=['start', 'admin'])
async def start_command(message: types.Message):
    users.add(message.from_user.id)
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=admin_menu)
    else:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n\n🍿 Kino ko'rish uchun uning kodini yuboring...")

@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def show_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"👥 Bot a'zolari soni: {len(users)}\n🎬 Yuklangan kinolar: {len(movies_db)}")

@dp.message_handler(content_types=['video'])
async def get_video(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        file_id = message.video.file_id
        await message.answer(f"Kino qabul qilindi. Kod bering:\n(Masalan: 12)")
        
        @dp.message_handler(content_types=['text'])
        async def set_movie_code(msg: types.Message):
            if msg.from_user.id == ADMIN_ID and msg.text.isdigit():
                movies_db[msg.text] = file_id
                await msg.answer(f"✅ Tayyor! Kod: {msg.text}")
            dp.message_handlers.unregister(set_movie_code) # Jarayonni to'xtatish

@dp.message_handler()
async def find_movie(message: types.Message):
    if message.text in movies_db:
        await bot.send_video(message.chat.id, movies_db[message.text], caption=f"🎬 Kino kodi: {message.text}")
    elif message.text == "⬅️ Orqaga":
        await message.answer("Bosh sahifa", reply_markup=types.ReplyKeyboardRemove())
    elif message.from_user.id != ADMIN_ID:
        await message.answer("❌ Bunday kodli kino topilmadi.")

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
    
