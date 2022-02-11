import json
import telebot
from telebot import types
from config import token, check_text
import requests
import speech_recognition as sr
import soundfile as sf
from pydub import AudioSegment
from backend import create_user, add_answer
import subprocess
import os



bot = telebot.TeleBot(token)

with open('text.json', encoding='utf-8') as f:
    text = json.load(f)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name}!\n' + text["text_1"], parse_mode="Markdown", reply_markup=menu_keyboard())
    create_user(message.from_user.username)


@bot.message_handler(content_types=["text"])
def step_0(message):
    if message.text == "Practice":
        step_1(message)

    elif message.text == "Theory":
        btn = types.InlineKeyboardButton(text='RAIN Group Sales Training', url='https://www.rainsalestraining.com/blog/4-steps-to-overcoming-sales-objections', callback_data='click1')
        markup = types.InlineKeyboardMarkup().add(btn)
        bot.send_message(message.chat.id, 'Let\'s study!', reply_markup=markup)
        bot.register_next_step_handler(message, step_0)

    elif message.text == "Help & settings":
        btn = types.InlineKeyboardButton(text='Start chat with support', url='https://t.me/techh_bot_support', callback_data='click2')
        markup = types.InlineKeyboardMarkup().add(btn)
        bot.send_message(message.chat.id, 'You can contact help via next link:', reply_markup=markup)
        bot.register_next_step_handler(message, step_0)

    else:
        pass
        #bot.register_next_step_handler(message, step_0)


def step_1(message):
    #bot.send_message(message.chat.id, text["text_2"], parse_mode="Markdown", reply_markup=scene_keyboard())
    bot.send_message(message.chat.id, text["text_2"], parse_mode="Markdown")
    bot.send_message(message.chat.id, "By clicking start you agree with our rules of data collection (GDPR).", parse_mode="Markdown", reply_markup=start_scene())
    bot.register_next_step_handler(message, step_3)



def step_3(message):
    if message.text == "Start":
        bot.send_message(message.chat.id, "_Starting conversation..._", parse_mode="Markdown")
        bot.send_message(message.chat.id, text["answer_1"], parse_mode="Markdown")
        bot.send_message(message.chat.id, text["prompt_1"], parse_mode="Markdown")
        bot.register_next_step_handler(message, step_4)

def step_4(message):
    t = message.content_type
    if t == "text":
        answer = check_text(message.text)
        bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        #bot.register_next_step_handler(message, step_5)
        add_answer(message.from_user.username, 1, message.text)
        step_5(message)

    if t == "voice":
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('voice_file.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        src_filename = 'voice_file.ogg'
        dest_filename = 'voice_file_1.wav'
        process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
        if process.returncode != 0:
            raise Exception("Something went wrong")
        
            
        voice_to_text_1(message)
        

def voice_to_text_1(message):

    #file_audio = sr.AudioFile("/Users/nymaxxx/Google Drive/Python Projects/Project Training Chat Bot ENG with ORM/voice_file_1.wav")
    file_audio = sr.AudioFile("voice_file_1.wav")

    r = sr.Recognizer()
    with file_audio as source:
        audio_text = r.record(source)

    text = r.recognize_google(audio_text)
    answer = check_text(text)
    repl = "_Text from voice:_\n\n" + text
    bot.send_message(message.chat.id, repl, parse_mode="Markdown")
    bot.send_message(message.chat.id, answer, parse_mode="Markdown")

    os.remove("voice_file.ogg")
    os.remove("voice_file_1.wav")

    add_answer(message.from_user.username, 1, text)
    step_5(message)


def step_5(message):
    bot.send_message(message.chat.id, text["answer_2"], parse_mode="Markdown")
    bot.send_message(message.chat.id, text["prompt_2"], parse_mode="Markdown")
    bot.register_next_step_handler(message, step_6)


def step_6(message):
    t = message.content_type
    if t == "text":
        answer = check_text(message.text)
        bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        add_answer(message.from_user.username, 2, message.text)
        step_7(message)

    if t == "voice":
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('voice_file.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        src_filename = 'voice_file.ogg'
        dest_filename = 'voice_file_2.wav'
        process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
        if process.returncode != 0:
            raise Exception("Something went wrong")

        voice_to_text_2(message)


def voice_to_text_2(message):

    #file_audio = sr.AudioFile("/Users/nymaxxx/Google Drive/Python Projects/Project Training Chat Bot ENG with ORM/voice_file_2.wav")
    file_audio = sr.AudioFile("voice_file_2.wav")

    r = sr.Recognizer()
    with file_audio as source:
        audio_text = r.record(source)

    text = r.recognize_google(audio_text)
    answer = check_text(text)
    repl = "_Text from voice:_\n\n" + text
    bot.send_message(message.chat.id, repl, parse_mode="Markdown")
    bot.send_message(message.chat.id, answer, parse_mode="Markdown")

    os.remove("voice_file.ogg")
    os.remove("voice_file_2.wav")

    add_answer(message.from_user.username, 2, text)
    step_7(message)


def step_7(message):
    bot.send_message(message.chat.id, text["prompt_3"], parse_mode="Markdown")
    bot.send_message(message.chat.id, text["answer_3"], parse_mode="Markdown")
    bot.register_next_step_handler(message, step_8)


def step_8(message):
    t = message.content_type
    if t == "text":
        answer = check_text(message.text)
        bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        add_answer(message.from_user.username, 3, message.text)
        step_9(message)

    if t == "voice":
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('voice_file.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        src_filename = 'voice_file.ogg'
        dest_filename = 'voice_file_3.wav'
        process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
        if process.returncode != 0:
            raise Exception("Something went wrong")

        #data, samplerate = sf.read('voice_file.ogg')
        #sf.write('voice_file_3.wav', data, samplerate)

        voice_to_text_3(message)


def voice_to_text_3(message):

    #file_audio = sr.AudioFile("/Users/nymaxxx/Google Drive/Python Projects/Project Training Chat Bot ENG with ORM/voice_file_3.wav")
    file_audio = sr.AudioFile("voice_file_3.wav")

    r = sr.Recognizer()
    with file_audio as source:
        audio_text = r.record(source)

    text = r.recognize_google(audio_text)
    answer = check_text(text)
    repl = "_Text from voice:_\n\n" + text
    bot.send_message(message.chat.id, repl, parse_mode="Markdown")
    bot.send_message(message.chat.id, answer, parse_mode="Markdown")

    os.remove("voice_file.ogg")
    os.remove("voice_file_3.wav")

    add_answer(message.from_user.username, 3, text)
    step_9(message)

def step_9(message):
    bot.send_message(message.chat.id, "Thanks for trying out our simulator! See you!", parse_mode="Markdown", reply_markup=menu_keyboard())
    bot.register_next_step_handler(message, step_0)




@bot.callback_query_handler(func=lambda message: True)
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Practice')
    btn2 = types.KeyboardButton('Theory')
    btn3 = types.KeyboardButton('Help & settings')
    markup.add(btn1).add(btn2).add(btn3)
    return markup

def scene_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Script №1')
    btn2 = types.KeyboardButton('Script №2')
    btn3 = types.KeyboardButton('Script №3')
    markup.add(btn1).add(btn2).add(btn3)
    return markup

def start_scene():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Start')
    markup.add(btn1)
    return markup

bot.infinity_polling()
