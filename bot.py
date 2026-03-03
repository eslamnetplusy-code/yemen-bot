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

# ==============================
# قراءة المتغيرات من Railway
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Add it in Railway Variables.")

# ==============================
# أمر /start
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل الرقم الذي تريد تعبئته")

# ==============================
# استقبال الرقم وتنفيذ العملية
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()

    await update.message.reply_text("جاري تنفيذ العملية... ⏳")

    data = {
        "username": API_USER,
        "password": API_PASS,
        "account": ACCOUNT_ID,
        "number": number,
        "amount": 100,          # عدل المبلغ إذا أردت
        "type": "almamon"       # مهم جداً حسب الصورة
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            API_URL,
            data=data,
            headers=headers,
            timeout=20
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 200:
            await update.message.reply_text("تم إرسال الطلب ✅")
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text(f"فشل الطلب ❌\nكود الخطأ: {response.status_code}")
            await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text("حدث خطأ في الاتصال بالمزود ❌")
        print("ERROR:", e)

# ==============================
# تشغيل البوت
# ==============================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
