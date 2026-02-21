import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask server (Render o'chib qolmasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Bot sozlamalari
TOKEN = "8599100876:AAGhk-U0gLCKNUAEf5Q1qThzsaAH-WHYmmA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kinolarni qidirish uchun kino nomini yozing.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Bu yerga kino bazasini ulasa bo'ladi, hozircha javob qaytaradi
    movie_name = update.message.text
    await update.message.reply_text(f"Tez orada '{movie_name}' kinosini topib beraman!")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    # Render portini eshitish uchun Flaskni vaqtinchalik chetga suramiz
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    main()
