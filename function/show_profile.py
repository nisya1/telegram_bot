from data.db_session import global_init, create_session
from data.models.Users import Users
from data.models.Movies import Movies


async def show_profile(update):
    global_init("database/database.db")
    sess = create_session()
    all_movies = sess.query(Movies).all()
    bought_tickets = sess.query(Users).filter(Users.id == update.callback_query.from_user.id).first().tickets

    text = 'Ваш профиль:\n\n'

    if len(bought_tickets) != 0:
        text += 'Купленные Вами билеты: \n'

        for movie in all_movies:
            if movie.name in bought_tickets:
                text += f'{movie.name} - куплено {bought_tickets.count(movie.name)}\n'
    else:
        text += 'Вы не купили ещё ни одного фильма!'
    await update.callback_query.message.reply_text(text)
