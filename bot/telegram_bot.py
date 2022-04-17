"""Don't run this in anything production like. It was hacked in a rush to test an idea"""

import os
import asyncio
import datetime
import logging

import requests
from shazamio import Shazam
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logger = logging.getLogger("geosong_bot")

TOKEN = os.environ.get("TELEGRAM_BOT_GEOSONG_TOKEN")


def post_to_geosong(out, context, update):
    """ publish the Geolocated song to the GeoSong server"""
    song_metadata = [x for x in out["track"]["sections"] if x["type"] == "SONG"][0]
    released = int([x['text'] for x in song_metadata['metadata'] if x['title'] == 'Released'][0])
    lat, lon = context.user_data['location']
    payload = {
        "date": datetime.datetime.now().isoformat(),
        "song_metadata": {
            "title": out['track']['title'],
            "artist": out['track']['subtitle'],
            "year": released,
            "genre": out["track"]["genres"]["primary"]
        },
        "point": {
            "coordinates": [lon, lat],
            "type": "Point"
        },
        "bbox": [lon, lon, lat, lat],
        "username": update.message.chat.username,
    }
    logger.debug("Will post to the API: '%s'", payload)
    r = requests.post("http://192.168.0.108:8000/geosong/", json=payload)
    logger.info("Post to geosong %s", r.status_code)


def start(update: Update, context: CallbackContext):
    context.user_data["started"] = True
    help_msg = ("Welcome! This bot can listen to audio samples and post them to the "
                "GeoSong server to update the map: https://github.com/PyCampES/geosong/\n "
                "To start you have to share your location. To do it click in the "
                "📎 button and just send your current location. \n\n\n"
                "After that you can send audio samples and I'll reply with the song name "
                "(if I can guess it) and post the result to the GeoSong map")

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)


def print_locations(update: Update, context: CallbackContext):
    if update.message.chat.username == "Gilgamezh":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=context.user_data["locations"])
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="You don't have permissions")


def on_message(update: Update, context: CallbackContext):
    if not context.user_data.get("started", False):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Run /start to begin")
        return

    if "location" not in context.user_data:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Please share your location first")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You can send me an audio of a song sample now")


def on_audio(update: Update, context: CallbackContext):
    if not context.user_data.get("started", False):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Run /start to begin")
        return
    if "location" not in context.user_data:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Please share your location")
        return
    try:
        shazam = Shazam()
        to_download = update.message.voice.get_file()
        audio_bytearray = to_download.download_as_bytearray()
        loop = asyncio.new_event_loop()
        out = loop.run_until_complete(shazam.recognize_song(audio_bytearray))
    except Exception:
        logger.exception("Error getting info")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Perdón tuve un error 🧑‍🏭")
    else:
        logger.debug("from shazam: %s", out)
        if "track" in out:
            context.bot.send_message(chat_id=update.effective_chat.id, text="I Found it! 🎉")
            theme = f"{out['track']['title']} by {out['track']['subtitle']}"
            context.bot.send_message(chat_id=update.effective_chat.id, text=theme)
            img_link = out['track']['images']['coverarthq']
            context.bot.send_photo(update.effective_chat.id, img_link)
            post_to_geosong(out, context, update)

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No tengo idea 😔")


def on_location(update: Update, context: CallbackContext):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    context.user_data["location"] = [lat, lon]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Gracias! 🗺")


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    command_handler = CommandHandler("locations", print_locations)
    dispatcher.add_handler(command_handler)

    text_handler = MessageHandler(Filters.text, on_message)
    dispatcher.add_handler(text_handler)

    echo_handler = MessageHandler(Filters.voice, on_audio)
    dispatcher.add_handler(echo_handler)

    location_handler = MessageHandler(Filters.location, on_location)
    dispatcher.add_handler(location_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
