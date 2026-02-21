import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"

# --- SOZLAMALAR ---
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"
TMDB_API_KEY = "6ecbd00310e0bb66d4686fae5567a93f"
CHANNEL_ID = -1003873626925
OWNER_ID = 7257755738

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Foydalanuvchi uchun menyu
    reply_markup = ReplyKeyboardMarkup([['🔍 Kino qidirish']], resize_keyboard=True)
    
    # Faqat admin uchun Boshqaruv tugmasi
    if update.message.from_user.id == OWNER_ID:
        reply_markup = ReplyKeyboardMarkup([['🔍 Kino qidirish'], ['🗄 Boshqaruv']], resize_keyboard=True)
        
    await update.message.reply_text(
        f"Assalomu alaykum {update.message.from_user.first_name}!\nKino nomini yozing yoki menyudan foydalaning.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🗄 Boshqaruv" and update.message.from_user.id == OWNER_ID:
        await update.message.reply_text("🎛 Admin paneliga xush kelibsiz!\nBu yerda bot statistikasi va adminlarni boshqarish mumkin (Tez kunda...).")
        return

    if text == "🔍 Kino qidirish":
        await update.message.reply_text("Kino nomini yuboring...")
        return

    # Kino qidirish (TMDB + Kanal havolasi)
    query = text.strip()
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=uz-UZ"
    
    try:
        res = requests.get(url).json()
        if res.get('results'):
            movie = res['results'][0]
            title = movie['title']
            poster = movie.get('poster_path')
            caption = f"🎬 **Nomi:** {title}\n⭐️ **Reyting:** {movie['vote_average']}\n\n📝 {movie.get('overview', 'Ma\\'lumot yo\\'q.')}"
            
            clean_id = str(CHANNEL_ID).replace("-100", "")
            search_url = f"https://t.me/c/{clean_id}/1?q={query.replace(' ', '%20')}"
            
            # Havola tugmasi
            keyboard = [[InlineKeyboardButton("📥 KINONI KO'RISH", url=search_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if poster:
                await update.message.reply_photo(photo=f"https://image.tmdb.org/t/p/w500{poster}", caption=caption, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text("🔍 Kechirasiz, bunday kino topilmadi.")
    except:
        await update.message.reply_text("⚠️ Qidiruvda xatolik!")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    application.run_polling()

if __name__ == '__main__':
    main()
            
