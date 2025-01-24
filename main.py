import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Membaca token dari variabel lingkungan
TOKEN = os.getenv("BOT_API_TOKEN")

# Fungsi untuk mendownload video dengan kualitas HD
def download_video(url: str, filename: str) -> str:
    options = {
        'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]',  # Maksimal 720p
        'merge_output_format': 'mp4',
        'outtmpl': filename,  # Nama file output
        'quiet': True,
        'socket_timeout': 30,  # Timeout koneksi
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return filename

# Fungsi untuk perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to YouTube Video Downloader Bot!\n\n"
        "💡 Kirimkan link video YouTube, dan saya akan mendownloadkannya untuk Anda dalam kualitas HD.\n\n"
    )
    await update.message.reply_text(welcome_message)

# Fungsi untuk menangani pesan teks
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            await update.message.reply_text("📥 Downloading video in HD... Please wait.")
            file_name = 'video.mp4'  # Nama file video sementara
            download_video(url, file_name)
            with open(file_name, 'rb') as video_file:
                await update.message.reply_video(video_file)
            os.remove(file_name)  # Hapus file setelah dikirim
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("⚠️ Please send a valid YouTube URL.")

# Fungsi utama untuk menjalankan bot
def main():
    # Periksa apakah token tersedia
    if not TOKEN:
        print("Error: BOT_API_TOKEN tidak ditemukan. Tambahkan token di Environment Variables.")
        return

    # Membuat aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Menambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Menambahkan handler untuk menangani pesan teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Menjalankan bot
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
