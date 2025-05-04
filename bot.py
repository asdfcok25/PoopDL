from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
BACKEND_URL = 'http://your-backend-url/mass_download'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirimkan URL PoopHD (pisahkan dengan spasi atau baris baru)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urls = update.message.text.strip().split()
    payload = {"urls": urls}
    
    try:
        response = requests.post(BACKEND_URL, json=payload)
        results = response.json()["results"]
        
        for result in results:
            if "error" in result:
                await update.message.reply_text(f"❌ Error: {result['url_input']}\n{result['error']}")
            else:
                await update.message.reply_text(
                    f"✅ Judul: {result['title']}\n"
                    f"🔗 Video: {result['video_url']}\n"
                    f"🔗 URL Asli: {result['url_input']}"
                )
    except Exception as e:
        await update.message.reply_text(f"❌ Error backend: {str(e)}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
