import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from function.buy_ticket import show_cinema_list

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, _):
    keyboard = [
        [InlineKeyboardButton("Посмотреть список фильмов", callback_data='show_cinema_list')],
        [InlineKeyboardButton("Найти ближайший кинотеатр", callback_data='find_cinema')],
        [InlineKeyboardButton("Показать профиль", callback_data='show_profile')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)


async def button(update, context):
    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == "show_cinema_list":
        await show_cinema_list(update, context)


async def help_command(update, _):
    await update.message.reply_text("Используйте `/start` для тестирования.")


if __name__ == '__main__':
    app = Application.builder().token("7842458338:AAH-eLEPuDLiL8_NzQoQ0gElxSvAlAVCsdo").build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('help', help_command))

    app.run_polling()
