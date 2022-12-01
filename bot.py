
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import os
import logging

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Goodbye {update.effective_user.first_name}')

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_to_download = await update.message.document.get_file()
    file_path = await file_to_download.download_to_drive()

    os.system(f'python {file_path} > {str(file_path)}.out 2>{str(file_path)}.error')
    
    text_message = None
    with open(str(file_path) + '.out') as f:
        text_message = f.read()
    
    if text_message == '':
        with open(str(file_path) + '.error') as f:
            text_message = f.read()

    if text_message == '':
        text_message = 'Nothing to output'
   
    await update.message.reply_text(text_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Facebook", callback_data="https://facebook.com"),
            InlineKeyboardButton("VKontakte", callback_data="https://vk.com"),
        ],
        [InlineKeyboardButton("Yandex", callback_data="https://yandex.ru")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


app = ApplicationBuilder().token("5810368499:AAFsVF_ScmKP9eKPNvPW2WkiD59Xsve1Zpw").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("help", help_command))


app.add_handler(MessageHandler(filters.Document.FileExtension('py'), msg))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("goodbye", goodbye))


app.run_polling()

# Done! Congratulations on your new bot. You will find it at t.me/vanneste_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 5810368499:AAFsVF_ScmKP9eKPNvPW2WkiD59Xsve1Zpw
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api