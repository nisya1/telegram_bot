from data.db_session import global_init, create_session
from data.models.Movies import Movies
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def admin(update, context):
    print(10)
    keyboard = [
        [InlineKeyboardButton("Добавить фильм", callback_data='add_film')],
        [InlineKeyboardButton("Удалить фильм", callback_data='delete_film')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Что вы хотите сделать?', reply_markup=reply_markup)


async def add_film_message(update, context):
    text = ("Пожалуйста через запятую с пробелом (, ) введите название фильма,"
            " его длительность, дату проведения сеанса и цену на билет")

    await update.callback_query.message.reply_text(text)


async def film_info_write(update, context):
    user_message = update.message.text.split(", ")
    context.user_data['name'] = user_message[0]
    context.user_data['duration'] = user_message[1]
    context.user_data['data'] = user_message[2]
    context.user_data['price'] = user_message[3]
    text = (f"Название: {user_message[0]}\n"
            f"Длительность: {user_message[1]}\n"
            f"Дата сеанса: {user_message[2]}\n"
            f"Цена билета: {user_message[3]}\n")
    await update.message.reply_text(text,
                                    reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton("Добавить фильм", callback_data="add_film_in_base")]
                                    ])
                                    )


async def add_film(update, context):
    try:
        global_init("database/database.db")
        sess = create_session()

        movie = Movies(
            name=context.user_data['name'],
            duration=context.user_data['duration'],
            data=context.user_data['data'],
            price=context.user_data['price']
        )
        sess.add(movie)

        sess.commit()
        await add_film_complete_message(update, context)
    except:
        await add_film_error_message(update, context)


async def add_film_complete_message(update, context):
    text = "Фильм успешно добавлен"
    await update.callback_query.message.reply_text(text)


async def add_film_error_message(update, context):
    text = "Не удалось доюавить фильм"
    await update.callback_query.message.reply_text(text)


async def movie_message(update, name, duration, data, price):
    button = [[InlineKeyboardButton("Удалить фильм", callback_data=f'delete {name}')]]
    reply_markup = InlineKeyboardMarkup(button)
    text = (f'Название фильма:  {name}\n'
            f'Длительность:  {duration}\n'
            f'Дата сеанса:  {data}\n'
            f'Цена билета:  {price}\n')
    await update.callback_query.message.reply_text(text, reply_markup=reply_markup)


async def delete_film(update, context):
    global_init("database/database.db")
    sess = create_session()
    movies = sess.query(Movies).all()

    for movie in movies:
        await movie_message(update=update,
                            name=movie.name,
                            duration=movie.duration,
                            data=movie.data,
                            price=movie.price)


async def delete_film_from_base(update, context, movie_name):
    global_init(f"database/database.db")
    sess = create_session()
    movies = [movie.name for movie in sess.query(Movies).all()]
    if movie_name in movies:
        film = sess.query(Movies).filter(Movies.name == movie_name).first()

        sess.delete(film)
        sess.commit()
        await delete_film_complete_message(update, context)
    else:
        await film_deleted(update, context)


async def delete_film_complete_message(update, context):
    text = "Фильм успешно удалён"
    await update.callback_query.message.reply_text(text)


async def film_deleted(update, context):
    text = "Фильм уже удалён"
    await update.callback_query.message.reply_text(text)
