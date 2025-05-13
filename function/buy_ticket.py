from data.db_session import global_init, create_session
from data.models.Movies import Movies
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# @hsdbjhbfsbot


async def movie_message(update, name, duration, data, price):
    button = [[InlineKeyboardButton("Купить билет", callback_data=f'{name}')]]
    reply_markup = InlineKeyboardMarkup(button)
    text = (f'Название фильма:  {name}\n'
            f'Длительность:  {duration}\n'
            f'Дата сеанса:  {data}\n'
            f'Цена билета:  {price}\n')
    await update.callback_query.message.reply_text(text, reply_markup=reply_markup)


async def show_cinema_list(update, context):
    global_init("database/database.db")
    sess = create_session()
    movies = sess.query(Movies).all()

    for movie in movies:
        await movie_message(update=update,
                            name=movie.name,
                            duration=movie.duration,
                            data=movie.data,
                            price=movie.price)
