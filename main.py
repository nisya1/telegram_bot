import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from function.buy_ticket import show_cinema_list, buy_tickets
from function.yandex_map import address_message, show_map, handle_address
from function.show_profile import show_profile
from function.admin import add_film, admin, film_info_write, add_film_message, delete_film, delete_film_from_base
from data.db_session import global_init, create_session
from data.models.Movies import Movies

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

NORMAL, INPUT, ADMIN = range(3)


async def start(update, _):
    keyboard = [
        [InlineKeyboardButton("Посмотреть список фильмов", callback_data='show_cinema_list')],
        [InlineKeyboardButton("Найти ближайший кинотеатр", callback_data='input_address')],
        [InlineKeyboardButton("Показать профиль", callback_data='show_profile')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)
    return NORMAL


async def button(update, context):
    query = update.callback_query
    variant = query.data
    await query.answer()

    global_init("database/database.db")
    sess = create_session()
    movies = [movie.name for movie in sess.query(Movies).all()]

    if variant in movies:
        await buy_tickets(update, context, variant)
        return NORMAL
    elif variant == "show_cinema_list":
        await show_cinema_list(update, context)
        return NORMAL
    elif variant == "input_address":
        await address_message(update, context)
        return INPUT
    elif variant == "find_cinema":
        await show_map(update, context)
        return NORMAL
    elif variant == "show_profile":
        await show_profile(update)
        return NORMAL
    elif variant == "add_film":
        await add_film_message(update, context)
        return ADMIN
    elif variant == "add_film_in_base":
        await add_film(update, context)
        return NORMAL
    elif variant == "delete_film":
        await delete_film(update, context)
        return NORMAL
    elif len(variant) > 7 and variant[7:] in movies:
        await delete_film_from_base(update, context, variant[7:])
        return NORMAL


async def help_command(update, _):
    await update.message.reply_text("Используйте `/admin` для тестирования.")


if __name__ == '__main__':
    app = Application.builder().token("7842458338:AAH-eLEPuDLiL8_NzQoQ0gElxSvAlAVCsdo").build()

    conversion = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NORMAL: [
                CommandHandler('start', start),
                CommandHandler('admin', admin),
                CallbackQueryHandler(button),
                CommandHandler('help', help_command)
            ],
            INPUT: [
                CommandHandler('start', start),
                CommandHandler('admin', admin),
                CallbackQueryHandler(button),
                CommandHandler('help', help_command),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address)
            ],
            ADMIN: [
                CommandHandler('start', start),
                CommandHandler('admin', admin),
                CallbackQueryHandler(button),
                CommandHandler('help', help_command),
                MessageHandler(filters.TEXT & ~filters.COMMAND, film_info_write)
            ]
        },
        fallbacks=[]
    )

    app.add_handler(conversion)

    app.run_polling()
