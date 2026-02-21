import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Active"

# --- SOZLAMALAR ---
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"
TMDB_API_KEY = "6ecbd00310e0bb66d4686fae5567a93f"
CHANNEL_ID = -1003873626925
OWNER_ID = 7257755738

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboards = [['🔍 Kino qidirish']]
    if update.effective_user.id == OWNER_ID:
        keyboards.append(['🗄 Boshqaruv'])
    
    reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
    await update.message.reply_text("Xush kelibsiz! Kino nomini yozing:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🗄 Boshqaruv" and update.effective_user.id == OWNER_ID:
        await update.message.reply_text("🛠 Admin panel: Hozircha faqat siz admin ekansiz.")
        return

    # Kino qidirish qismi
    query = text.strip()
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=uz-UZ"
    
    try:
        res = requests.get(url).json()
        if res.get('results'):
            movie = res['results'][0]
            title = movie['title']
            clean_id = str(CHANNEL_ID).replace("-100", "")
            search_url = f"https://t.me/c/{clean_id}/1?q={query.replace(' ', '%20')}"
            
            button = [[InlineKeyboardButton("📥 KINONI KO'RISH", url=search_url)]]
            markup = InlineKeyboardMarkup(button)

            await update.message.reply_text(f"🎬 **{title}**\n\nKino topildi! Uni kanaldan ko'rish uchun pastdagi tugmani bosing:", 
                                         reply_markup=markup, parse_mode='Markdown')
        else:
            await update.message.reply_text("🔍 Kechirasiz, hech narsa topilmadi.")
    except:
        await update.message.reply_text("⚠️ Xatolik yuz berdi.")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    Thread(target=run_flask).start()
    application.run_polling()

if __name__ == '__main__':
    main()
