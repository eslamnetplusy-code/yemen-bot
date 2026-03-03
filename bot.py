import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8057785864:AAEUPBg4OjCMVDNFEYjCArzP7PfyDY_1F5U")

API_URL = os.getenv("https://daizer.yemoney.net/api/yr/")
API_USER = os.getenv("aleslam")
API_PASS = os.getenv("asd123456")
ACCOUNT_ID = os.getenv("5445")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل الرقم الذي تريد تعبئته")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text

    data = {
        "username": API_USER,
        "password": API_PASS,
        "account": ACCOUNT_ID,
        "number": number,
        "amount": 100
    }

    try:
        response = requests.post(API_URL, json=data)
        await update.message.reply_text("تم إرسال الطلب للمزود")
        await update.message.reply_text(response.text)
    except:
        await update.message.reply_text("حدث خطأ في الاتصال بالمزود")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
