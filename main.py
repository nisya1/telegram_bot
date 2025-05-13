import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from function.buy_ticket import show_cinema_list, buy_tickets
from function.yandex_map import adres_message, show_map, handle_address
from function.show_profile import show_profile
from data.db_session import global_init, create_session
from data.models.Movies import Movies

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, _):
    keyboard = [
        [InlineKeyboardButton("Посмотреть список фильмов", callback_data='show_cinema_list')],
        [InlineKeyboardButton("Найти ближайший кинотеатр", callback_data='input_addres')],
        [InlineKeyboardButton("Показать профиль", callback_data='show_profile')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)


async def button(update, context):
    query = update.callback_query
    variant = query.data
    await query.answer()

    global_init("database/database.db")
    sess = create_session()
    movies = [movie.name for movie in sess.query(Movies).all()]

    if variant in movies:
        await buy_tickets(update, context, variant)
    elif variant == "show_cinema_list":
        await show_cinema_list(update, context)
    elif variant == "input_addres":
        await adres_message(update, context)
    elif variant == "find_cinema":
        await show_map(update, context)
    elif variant == "show_profile":
        await show_profile(update)


async def help_command(update, _):
    await update.message.reply_text("Используйте `/start` для тестирования.")


if __name__ == '__main__':
    app = Application.builder().token("7842458338:AAH-eLEPuDLiL8_NzQoQ0gElxSvAlAVCsdo").build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address))

    app.run_polling()
