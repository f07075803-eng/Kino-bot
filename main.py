import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot ishlayapti!"

# --- SOZLAMALAR ---
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"
TMDB_API_KEY = "6ecbd00310e0bb66d4686fae5567a93f"
CHANNEL_ID = -1003873626925  # Sizning kanal ID
OWNER_ID = 7257755738        # Sizning ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Asosiy menyu tugmalari
    buttons = [['🔍 Kino qidirish']]
    if update.effective_user.id == OWNER_ID:
        buttons.append(['⚙️ Boshqaruv'])
    
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz! Kino nomini yozing yoki menyudan foydalaning:",
        reply_markup=reply_markup
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "⚙️ Boshqaruv" and user_id == OWNER_ID:
        await update.message.reply_text("🛠 Admin panel: Bu yerda adminlarni boshqarish mumkin.")
        return

    if text == "🔍 Kino qidirish":
        await update.message.reply_text("Kino nomini kiriting...")
        return

    # Kino qidirish jarayoni
    query = text.strip()
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=uz-UZ"
    
    try:
        res = requests.get(url).json()
        if res.get('results'):
            movie = res['results'][0]
            title = movie['title']
            desc = movie.get('overview', 'Ma\'lumot yo\'q')
            poster = movie.get('poster_path')
            
            # Kanal ichidan qidirish havolasi
            clean_id = str(CHANNEL_ID).replace("-100", "")
            search_url = f"https://t.me/c/{clean_id}/1?q={query.replace(' ', '%20')}"
            
            keyboard = [[InlineKeyboardButton("📥 KINONI KO'RISH", url=search_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            caption = f"🎬 **{title}**\n\n📝 {desc[:300]}..."
            
            if poster:
                await update.message.reply_photo(
                    photo=f"https://image.tmdb.org/t/p/w500{poster}",
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text("🔍 Kechirasiz, hech narsa topilmadi.")
    except Exception as e:
        await update.message.reply_text("⚠️ Qidiruvda xatolik yuz berdi.")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    Thread(target=run_flask).start()
    application.run_polling()

if __name__ == '__main__':
    main()
    
