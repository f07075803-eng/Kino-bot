import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Admin Boshqaruvi bilan Faol!"

# --- SOZLAMALAR ---
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"
TMDB_API_KEY = "6ecbd00310e0bb66d4686fae5567a93f"
CHANNEL_ID = -1003873626925
OWNER_ID = 7257755738  # Sening ID raqaming (Asosiy Admin)

# Adminlar ro'yxati (Boshida faqat OWNER)
admins = {OWNER_ID}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kino nomini yozing yoki admin buyruqlaridan foydalaning.")

# --- ADMINLARNI BOSHQARISH ---

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == OWNER_ID:
        try:
            new_admin_id = int(context.args[0])
            admins.add(new_admin_id)
            await update.message.reply_text(f"✅ ID: {new_admin_id} admin sifatida qo'shildi.")
        except (IndexError, ValueError):
            await update.message.reply_text("⚠️ To'g'ri foydalanish: /add_admin ID_RAQAM")
    else:
        await update.message.reply_text("🚫 Bu buyruq faqat asosiy admin uchun!")

async def del_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == OWNER_ID:
        try:
            admin_id = int(context.args[0])
            if admin_id in admins:
                admins.remove(admin_id)
                await update.message.reply_text(f"🗑 ID: {admin_id} adminlikdan chiqarildi.")
            else:
                await update.message.reply_text("❌ Bunday ID adminlar ro'yxatida yo'q.")
        except (IndexError, ValueError):
            await update.message.reply_text("⚠️ To'g'ri foydalanish: /del_admin ID_RAQAM")

async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id in admins:
        text = "👥 **Adminlar ro'yxati:**\n\n" + "\n".join([f"• `{a}`" for a in admins])
        await update.message.reply_text(text, parse_mode='Markdown')

# --- QIDIRUV ---

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=uz-UZ"
    
    try:
        res = requests.get(url).json()
        if res.get('results'):
            movie = res['results'][0]
            title = movie['title']
            poster = movie.get('poster_path')
            caption = f"🎬 **Nomi:** {title}\n⭐️ **Reyting:** {movie['vote_average']}\n\n📝 {movie.get('overview', '')}"
            
            if poster:
                await update.message.reply_photo(photo=f"https://image.tmdb.org/t/p/w500{poster}", caption=caption, parse_mode='Markdown')
            else:
                await update.message.reply_text(caption)

            clean_id = str(CHANNEL_ID).replace("-100", "")
            search_url = f"https://t.me/c/{clean_id}/1?q={query.replace(' ', '%20')}"
            await update.message.reply_text(f"📥 [KINO FAYLINI KO'RISH]({search_url})", parse_mode='Markdown')
    except:
        await update.message.reply_text("⚠️ Xatolik.")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_admin", add_admin))
    application.add_handler(CommandHandler("del_admin", del_admin))
    application.add_handler(CommandHandler("admins", list_admins))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    application.run_polling()

if __name__ == '__main__':
    main()
    
