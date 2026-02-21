import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Live!"

# --- SOZLAMALAR ---
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"
ADMIN_ID = 7257755738
TMDB_API_KEY = "6ecbd00310e0bb66d4686fae5567a93f"
video_db = {} # Vaqtinchalik baza

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men aqlli kino botman. Kino nomini yozing, men qidirib beraman!")

async def handle_admin_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID and update.message.video:
        movie_name = update.message.caption
        if movie_name:
            video_db[movie_name.lower()] = update.message.video.file_id
            await update.message.reply_text(f"✅ '{movie_name}' bazaga saqlandi!")
        else:
            await update.message.reply_text("⚠️ Videoni yuborganda izohiga (caption) kino nomini yozing!")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=uz-UZ"
    res = requests.get(url).json()

    if res.get('results'):
        movie = res['results'][0]
        title = movie['title']
        caption = f"🎬 **{title}**\n⭐️ Reyting: {movie['vote_average']}\n\n{movie['overview']}"
        poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None

        if poster: await update.message.reply_photo(photo=poster, caption=caption, parse_mode='Markdown')
        else: await update.message.reply_text(caption)

        if title.lower() in video_db:
            await update.message.reply_video(video=video_db[title.lower()], caption="Mana kino fayli!")
        else:
            await update.message.reply_text("📥 Ma'lumot topildi, lekin video fayli hali yuklanmagan.")
    else:
        await update.message.reply_text("🔍 Hech narsa topilmadi.")

def main():
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.VIDEO, handle_admin_video))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    app_bot.run_polling()

if __name__ == '__main__':
    main()
    
