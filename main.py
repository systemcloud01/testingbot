import os
from fastapi import FastAPI
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
import yt_dlp

# Baca token dan URL dari variabel lingkungan
TOKEN = os.getenv("BOT_API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Inisialisasi FastAPI
app = FastAPI()

# Endpoint root untuk memberikan pesan respons
@app.get("/")
async def root():
    return {
        "response": {
            "status": "true",
            "message": "Bot Successfully Activated!",
            "author": "SATRIADEV"
        }
    }

# Fungsi untuk mendownload video
def download_video(url: str, filename: str) -> str:
    options = {
        'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
        'merge_output_format': 'mp4',
        'outtmpl': filename,
        'quiet': True,
        'socket_timeout': 30,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return filename

# Fungsi untuk perintah /start
async def start(update: Update, context):
    welcome_message = (
        "👋 Welcome to YouTube Video Downloader SatriaDev!\n\n"
        "💡 Kirimkan link video YouTube, dan saya akan mendownloadkannya untuk Anda dalam kualitas HD.\n\n"
    )
    await update.message.reply_text(welcome_message)

# Fungsi untuk menangani pesan teks
async def handle_message(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            await update.message.reply_text("📥 Downloading video in HD... Please wait.")
            file_name = 'video.mp4'
            download_video(url, file_name)
            with open(file_name, 'rb') as video_file:
                await update.message.reply_video(video_file)
            os.remove(file_name)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("⚠️ Please send a valid YouTube URL.")

# Fungsi utama untuk menjalankan bot dengan webhook
async def main():
    if not TOKEN or not WEBHOOK_URL:
        print("Error: BOT_API_TOKEN atau WEBHOOK_URL tidak ditemukan.")
        return

    # Inisialisasi aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Konfigurasikan webhook
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

    # Jalankan aplikasi bot (non-blocking)
    app.state.bot_app = application
    print("Bot is running...")

# Menambahkan startup event untuk FastAPI
@app.on_event("startup")
async def startup():
    await main()
