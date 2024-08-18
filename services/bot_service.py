import logging
import io
from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from aiogram.exceptions import TelegramForbiddenError
from flask_sqlalchemy import SQLAlchemy
from staticmap import StaticMap, CircleMarker

from messages.message_ru import MESSAGE_RU
from admin_app.db_model import User, EarthQuake
from logger.logger import logger_wraps
from model.p_model import EarthQuakeP


@logger_wraps(level=logging.INFO)
async def delete_user(db: SQLAlchemy, user: User):
    print("delete {user=}")
    db.session.delete(user)
    db.session.commit()


@logger_wraps()
def make_map_pic_bytes(latitude, longitude) -> io.BytesIO:
    m = StaticMap(400, 400, url_template="http://a.tile.osm.org/{z}/{x}/{y}.png")
    # m = StaticMap(400, 400, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')
    # m = StaticMap(
    #     400, 400, url_template="https://tile1.maps.2gis.com/tiles?x={x}&y={y}&z={z}&v=2"
    # )

    marker_outline = CircleMarker((float(longitude), float(latitude)), "#ffa188", 22)
    marker = CircleMarker((float(longitude), float(latitude)), "#FF3600", 14)
    dark_marker = CircleMarker((float(longitude), float(latitude)), "#661600", 8)

    m.add_marker(marker_outline)
    m.add_marker(marker)
    m.add_marker(dark_marker)

    image = m.render(zoom=4)
    bytes_io = io.BytesIO()
    image.save(bytes_io, format="png")
    return bytes_io


@logger_wraps()
def check_fields_in_message(mq_message_json: dict, log: logging.Logger):
    field_list = ["description", "latitude", "longitude", "depth", "magnitude", "time"]
    for field in field_list:
        if field not in mq_message_json:
            log.warning(
                f'In message id={mq_message_json.get('publicID', 'UNKNOWN')} missed field "{field}"'
            )


@logger_wraps()
async def send_earthquake_message_to_user(
    bot: Bot, db: SQLAlchemy, user: User, mq_message_json: dict
):
    try:
        await bot.send_message(
            chat_id=user.chat_id,
            text=MESSAGE_RU["earhtqueqe_inform"].format(
                mq_message_json.get("description", "UNKNOWN"),
                mq_message_json.get("latitude", "UNKNOWN"),
                mq_message_json.get("longitude", "UNKNOWN"),
                mq_message_json.get("depth", "UNKNOWN"),
                mq_message_json.get("magnitude", "UNKNOWN"),
                mq_message_json.get("time", "UNKNOWN"),
            ),
        )

    except TelegramForbiddenError:
        await delete_user(db, user)


@logger_wraps()
async def send_earthquake_message_to_all_user(
    bot: Bot, db: SQLAlchemy, msg: dict, logger: logging.Logger
):
    try:
        io_bytes = make_map_pic_bytes(msg.get("latitude"), msg.get("longitude"))
        buffered_image = BufferedInputFile(io_bytes.getvalue(), "map.png")
        for user in db.session.query(User):
            await send_earthquake_message_to_user(bot, db, user, msg)
            await bot.send_photo(chat_id=user.chat_id, photo=buffered_image)
            logger.info(
                f'{user.user_id=} {user.user_name=} publicID={msg.get('publicID', 'UNKNOWN')} description={msg.get("description", 'UNKNOWN')}'
            )
    finally:
        io_bytes.close()


def save_earthquake_to_db(db:SQLAlchemy,eq_msg:EarthQuakeP):
    new_earthquake = EarthQuake(
        id=eq_msg.id,
        description = eq_msg.description,
        latitude=eq_msg.latitude,
        longitude=eq_msg.longitude,
        depth=eq_msg.depth,
        magnitude=eq_msg.magnitude,
        time=eq_msg.time
    )
    db.session.add(new_earthquake)
    db.session.commit()
