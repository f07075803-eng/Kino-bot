import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask server
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!"

# --- SOZLAMALAR ---
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"
TMDB_API_KEY = "6ecbd00310e0bb66d4686fae5567a93f"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kino nomini yozing, qidirib beraman.")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=uz-UZ"
    
    try:
        res = requests.get(url).json()
        if res.get('results'):
            movie = res['results'][0]
            title = movie['title']
            desc = movie.get('overview', 'Ma'lumot yo'q')
            poster = movie.get('poster_path')
            
            caption = f"🎬 **{title}**\n\n📝 {desc}"
            
            if poster:
                await update.message.reply_photo(photo=f"https://image.tmdb.org/t/p/w500{poster}", caption=caption, parse_mode='Markdown')
            else:
                await update.message.reply_text(caption)
        else:
            await update.message.reply_text("🔍 Hech narsa topilmadi.")
    except Exception as e:
        await update.message.reply_text("⚠️ Qidiruvda xatolik yuz berdi.")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def main():
    # Botni qurish
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    
    # Flaskni alohida oqimda ishga tushirish
    Thread(target=run_flask).start()
    
    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
            
