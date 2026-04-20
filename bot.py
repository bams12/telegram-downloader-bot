import re
import os
from telegram import *
from telegram.ext import *
from config import *
from database import *
from downloader import *
from keep_alive import keep_alive

keep_alive()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Bot Downloader PRO\nKirim link!")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    url = re.search(r'(https?://\S+)', text)
    if not url:
        return await update.message.reply_text("Link tidak valid")

    limit_count, premium = get_user(user_id, FREE_LIMIT)

    if limit_count <= 0 and premium == 0:
        return await update.message.reply_text("Limit habis 😅 upgrade premium")

    context.user_data["url"] = url.group(0)

    kb = [
        [InlineKeyboardButton("360p", callback_data="360"),
         InlineKeyboardButton("720p", callback_data="720")],
        [InlineKeyboardButton("Audio", callback_data="audio")]
    ]

    await update.message.reply_text("Pilih kualitas:", reply_markup=InlineKeyboardMarkup(kb))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    url = context.user_data.get("url")

    if not url:
        return await query.edit_message_text("Session expired")

    choice = query.data

    fmt = "bestaudio" if choice == "audio" else f"best[height<={choice}]"

    await query.edit_message_text("Downloading... ⏳")

    try:
        file = download(url, fmt)

        if choice == "audio":
            await query.message.reply_audio(open(file, "rb"))
        else:
            await query.message.reply_video(open(file, "rb"))

        os.remove(file)

        limit_count, premium = get_user(user_id, FREE_LIMIT)
        if premium == 0:
            reduce_limit(user_id)

    except Exception as e:
        await query.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.add_handler(CallbackQueryHandler(button))

print("Bot jalan 🔥")
app.run_polling()
