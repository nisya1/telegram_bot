import math
from function.cinemas import SPB_CINEMAS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests

GEOCODE_API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'
STATIC_MAPS_API_KEY = '7a4bc255-548a-46bf-a0e0-d3cffbd8bb95'


def get_coordinates(address):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    geocoder_request = f'{server_address}apikey={GEOCODE_API_KEY}&geocode={address}&format=json'

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        if json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"][
            "found"] == "0":
            return None
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        return float(toponym_coodrinates[0]), float(toponym_coodrinates[1])
    return None


def find_nearest_cinema(user_coords: list[float]):
    if not user_coords or len(user_coords) != 2:
        return None

    cinemas_with_distances = []

    for cinema in SPB_CINEMAS:
        lat1, lon1 = math.radians(user_coords[1]), math.radians(user_coords[0])
        lat2, lon2 = math.radians(cinema["coords"][1]), math.radians(cinema["coords"][0])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        distance = 6371 * c * 1000

        cinemas_with_distances.append({
            **cinema,
            "distance": distance
        })

    if not cinemas_with_distances:
        return None

    return sorted(cinemas_with_distances, key=lambda x: x["distance"])[0]


async def handle_address(update, context):
    context.user_data['user_address'] = update.message.text
    await update.message.reply_text(
        f"Адрес сохранён: {update.message.text}\n"
        "Теперь нажмите кнопку 'Найти кинотеатр'",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Найти кинотеатр", callback_data="find_cinema")]
        ])
    )


async def show_map(update, context):
    address = context.user_data.get('user_address')
    print(address)

    if not address:
        await update.callback_query.message.reply_text("Сначала введите адрес!")
        return

    user_coords = get_coordinates(address)
    print(user_coords)
    if not user_coords:
        text = ("Не удалось найти ближайший кинотеатр.\n"
                "Проверьте корректность введённого вами адреса")
        await update.callback_query.message.reply_text(text)
        return

    cinema = find_nearest_cinema(user_coords)
    print(cinema)
    if not cinema:
        text = ("Не удалось найти ближайший кинотеатр.\n"
                "проверьте корректность введённого вами адреса")
        await update.callback_query.message.reply_text(text)
        return

    map_params = {
        'l': 'map',
        'pt': f"{cinema['coords'][0]},{cinema['coords'][1]}",
        'z': '17',
        'size': '650,450'
    }

    map_url = f"https://static-maps.yandex.ru/1.x/?{'&'.join([f'{k}={v}' for k, v in map_params.items()])}"
    response = requests.get(map_url)

    image = response.content
    await update.callback_query.message.reply_photo(
        photo=image,
        caption=f"Ближайший к вам кинотеатр это:\n"
                f"Название: {cinema['name']}\n"
                f"Адрес: {cinema['address']}"
    )


async def adres_message(update, context):
    text = "Пожалуйста. введите свой адрес, а потом нажмите на кнопку 'Найти кинотеатр'"

    await update.callback_query.message.reply_text(text)
