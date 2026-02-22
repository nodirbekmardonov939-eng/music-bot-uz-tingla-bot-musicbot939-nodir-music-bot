import telebot
from telebot import types
import os
import json

TOKEN = "8098573516:AAHaSibUAv9bMVf_uXXo9K4hdCTyLx2aj4E"
ADMIN_ID =6834394748  # o'zingizning telegram ID

bot = telebot.TeleBot(TOKEN)

if not os.path.exists("music"):
    os.makedirs("music")

if not os.path.exists("songs.json"):
    with open("songs.json", "w") as f:
        json.dump({}, f)

def load_songs():
    with open("songs.json", "r") as f:
        return json.load(f)

def save_songs(data):
    with open("songs.json", "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎵 Xit qoshiqlar")
    bot.send_message(message.chat.id, "Assalomu alaykum 🎶", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎵 Xit qoshiqlar")
def list_songs(message):
    songs = load_songs()

    if not songs:
        bot.send_message(message.chat.id, "Hozircha qo'shiq yo'q")
        return

    text = "🎵 Xit qoshiqlar:\n\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    buttons = []

    for number, name in songs.items():
        text += f"{number}. {name}\n"
        buttons.append(types.KeyboardButton(number))

    markup.add(*buttons)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(content_types=['audio'])
def add_song(message):
    if message.from_user.id != ADMIN_ID:
        return

    songs = load_songs()
    number = str(len(songs) + 1)

    file_info = bot.get_file(message.audio.file_id)
    downloaded = bot.download_file(file_info.file_path)

    file_path = f"music/{number}.mp3"
    with open(file_path, "wb") as f:
        f.write(downloaded)

    title = message.audio.title or f"Qo'shiq {number}"
    artist = message.audio.performer or ""

    full_name = f"{artist} - {title}" if artist else title

    songs[number] = full_name
    save_songs(songs)

    bot.send_message(message.chat.id, f"✅ {full_name} saqlandi")

@bot.message_handler(func=lambda message: message.text.isdigit())
def send_song(message):
    songs = load_songs()
    number = message.text

    if number not in songs:
        return

    file_path = f"music/{number}.mp3"

    with open(file_path, "rb") as audio:
        bot.send_audio(message.chat.id, audio)

bot.polling()
