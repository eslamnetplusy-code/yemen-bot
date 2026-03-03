import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ====== قراءة المتغيرات من Railway ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# تأكد أن التوكن موجود
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Add it in Railway Variables.")

# ====== أمر /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل الرقم الذي تريد تعبئته")

# ====== استقبال الرقم ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()

    data = {
        "username": API_USER,
        "password": API_PASS,
        "account": ACCOUNT_ID,
        "number": number,
        "amount": 100
    }

    try:
        response = requests.post(API_URL, json=data, timeout=15)
        result = response.text
        await update.message.reply_text("تم إرسال الطلب للمزود ✅")
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text("حدث خطأ في الاتصال بالمزود ❌")
        print("ERROR:", e)

# ====== تشغيل البوت ======
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
