# -*- coding: utf-8 -*-

import telebot
from telebot import types
import os
from PIL import Image
from io import BytesIO
import database_func
import hashlib

TOKEN_FILE_PATH = "token.txt"
USERS_FILE_PATH = "users.txt"
LESSONS_FILE_PATH = "C:/Users/andre/OneDrive/Desktop/schoolbot/photos/lessons.jpeg"
RINGS_FILE_PATH = "C:/Users/andre/OneDrive/Desktop/schoolbot/photos/rings.jpeg"
CHANGES_FILE_PATH = "changes.txt"
PASSWORD_FILE_PATH = "password.txt"

login_user = False

with open(TOKEN_FILE_PATH, 'r') as file:
    TOKEN = file.read()
bot = telebot.TeleBot(token=TOKEN)


def correct_user(user_id, chat_id):
    usernames = database_func.allnick()
    chat_ids = database_func.allids()
    if (user_id in usernames) and (chat_id in chat_ids):
        return False
    return True


@bot.message_handler(commands=['start'])
def hi_message(message):
    user_nickname = str(message.from_user.username)
    chat_id = str(message.chat.id)

    if correct_user(user_nickname, chat_id):
        database_func.newuser(user_nickname, chat_id)

    keyboard = types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
    )
    functions_button = types.KeyboardButton(text="Функции\u2699")
    keyboard.add(functions_button)
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Это бот Школы №1 города Шимановска.",
        reply_markup=keyboard,
    )


@bot.message_handler(func=lambda message: message.text == 'Функции\u2699')
def functions(message):
    func_keyboard = types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True
    )

    buttons = [
        types.KeyboardButton(text="Расписание уроков \U0001F4C5"),
        types.KeyboardButton(text="Расписание звонков \U0001F514"),
        types.KeyboardButton(text="Изменения в расписании \U0001F504"),
        types.KeyboardButton(text="Информация о школе \U00002139"),
        types.KeyboardButton(text="Оставить отзыв \U0001F4AC"),
        types.KeyboardButton(text="Для учителей \U0001F469\u200D\U0001F3EB\u200C \U0001F468\u200D\U0001F3EB"),
    ]
    for but in buttons:
        func_keyboard.add(but)
    bot.send_message(
        message.chat.id,
        "Выберите функцию",
        reply_markup=func_keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_button(message):
    global login_user
    functions(message)
    login_user = False


@bot.message_handler(func=lambda message: message.text == "Расписание уроков \U0001F4C5")
def lesson_schedule(message):
    with open(LESSONS_FILE_PATH, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: message.text == "Расписание звонков \U0001F514")
def ring_schedule(message):
    with open(RINGS_FILE_PATH, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: message.text == "Изменения в расписании \U0001F504")
def schedule(message):
    with open(CHANGES_FILE_PATH, 'r', encoding='windows-1251') as changes_file:
        changes = ""
        for el in changes_file:
            changes += el
    bot.send_message(message.chat.id, changes)


@bot.message_handler(func=lambda message: message.text == "Информация о школе \U00002139")
def school_info(message):
    info_keyboard = types.InlineKeyboardMarkup()
    keyboards = {
        'Телеграм канал школы': 'https://t.me/shkola1shimanovska',
        'Сайт школы': 'https://shimsosh1.obramur.ru/',
        'Группа Вконтакте': 'https://vk.com/public217462602'
    }
    for key, value in keyboards.items():
        info_keyboard.add(types.InlineKeyboardButton(text=key, url=value))
    bot.send_message(
        message.chat.id,
        text="Список социальных сетей школы, где Вы можете узнать о ней более подробно и получить свежие новости.",
        reply_markup=info_keyboard
    )


@bot.message_handler(func=lambda message: message.text == "Оставить отзыв \U0001F4AC")
def form(message):
    stop_keyboard = types.ReplyKeyboardMarkup()
    stop_keyboard.add(types.KeyboardButton(text="Отмена"))
    sent = bot.send_message(message.chat.id, text="Напишите отзыв", reply_markup=stop_keyboard)
    bot.register_next_step_handler(sent, review)


def review(message):
    user_review = message.text
    if user_review != 'Отмена':
        bot.send_message(
            879423418,
            text=f"Оставлен отзыв пользователем @{message.from_user.username}:\n {user_review}"
        )
        bot.send_message(message.chat.id, text="Спасибо за отзыв!")
        functions(message)
    else:
        functions(message)


@bot.message_handler(
    func=lambda message: message.text == "Для учителей \U0001F469\u200D\U0001F3EB\u200C \U0001F468\u200D\U0001F3EB")
def start(message):
    sent = bot.send_message(message.chat.id, text="Введите пароль")
    bot.register_next_step_handler(sent, user)


def user(message):
    teacher_password = message.text
    hash_object = hashlib.sha256()
    hash_object.update(teacher_password.encode())
    hash_value = hash_object.hexdigest()
    global login_user
    try:
        with open(PASSWORD_FILE_PATH, 'r') as password_file:
            currect_password = str(password_file.read())
    except FileNotFoundError:
        bot.send_message(message.chat.id, text="Не найден файл пароля")

    if hash_value == currect_password:
        bot.send_message(message.chat.id, text="Успешный вход!")

        login_user = True

        t_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        t_buttons = [
            types.KeyboardButton(text="Добавить изменения в расписании"),
            types.KeyboardButton(text="Написать объявление"),
            types.KeyboardButton(text="Изменить расписание"),
            types.KeyboardButton(text="Изменить расписание звонков"),
            types.KeyboardButton(text="Изменить пароль"),
            types.KeyboardButton(text="Назад"),
        ]

        for but in t_buttons:
            t_keyboard.add(but)

        bot.send_message(
            message.chat.id,
            text="Функции для сотрудников",
            reply_markup=t_keyboard
        )

    else:
        bot.send_message(message.chat.id, text="Неверный пароль")


@bot.message_handler(func=lambda message: message.text == "Добавить изменения в расписании")
def c_changes(message):
    if not login_user:
        bot.send_message(message.chat.id, text="Вы не вошли в систему!")
    else:
        sent = bot.send_message(message.chat.id, text="Отправьте изменения")
        bot.register_next_step_handler(sent, file_changes)


def file_changes(message):
    with open(CHANGES_FILE_PATH, 'w') as changes_file:
        changes_file.write(str(message.text))
        bot.send_message(message.chat.id, text="Успешно!")
        chatids = database_func.allids()
        for c_id in chatids:
            bot.send_message(c_id, text="Добавлены новые изменения в расписании!")


@bot.message_handler(func=lambda message: message.text == "Изменить пароль")
def change_password(message):
    if not login_user:
        bot.send_message(message.chat.id, text="Вы не вошли в систему!")
    else:
        sent = bot.send_message(message.chat.id, text="Введите текущий пароль")
        bot.register_next_step_handler(sent, verify_password)


@bot.message_handler(func=lambda message: message.text == "Написать объявление")
def hi(message):
    if not login_user:
        bot.send_message(message.chat.id, text="Вы не вошли в систему!")
    else:
        sent = bot.send_message(message.chat.id, text=f"Отправьте объявление")
        bot.register_next_step_handler(sent, go)


def go(message):
    chat_ids = database_func.allids()
    announcement = message.text
    for chatid in chat_ids:
        bot.send_message(chatid, announcement)


def verify_password(message):
    with open(PASSWORD_FILE_PATH, 'r') as password_file:
        current_password = password_file.read().strip()
    password = message.text
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_value = hash_object.hexdigest()
    if hash_value == current_password:
        sent = bot.send_message(message.chat.id, "Введите новый пароль")
        bot.register_next_step_handler(sent, file_password_changes)
    else:
        bot.send_message(message.chat.id, "Неправильный пароль")


def file_password_changes(message):
    hash_object = hashlib.sha256()
    password = message.text
    hash_object.update(password.encode())
    hash_value = hash_object.hexdigest()
    with open(PASSWORD_FILE_PATH, 'w') as password_file:
        password_file.write(str(hash_value))
        bot.send_message(message.chat.id, text="Пароль успешно изменен!")


@bot.message_handler(func=lambda message: message.text and message.text == 'Изменить расписание')
def request_schedule_lessons(message):
    if not login_user:
        bot.send_message(message.chat.id, text="Вы не вошли в систему!")
    else:
        bot.send_message(message.chat.id, 'Отправьте фото нового расписания.')
        bot.register_next_step_handler(message, handle_photo_lessons)


def handle_photo_lessons(message):
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path

            old_photo_path = os.path.join('photos', 'lessons.jpeg')
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)

            downloaded_file = bot.download_file(file_path)

            image = Image.open(BytesIO(downloaded_file))
            image_path = os.path.join('photos', 'lessons.jpeg')
            image.save(image_path, 'JPEG', quality=100)

            bot.send_message(message.chat.id, 'Фото расписания успешно сохранено!')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, отправьте фото.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')


@bot.message_handler(func=lambda message: message.text and message.text == 'Изменить расписание звонков')
def request_schedule_rings(message):
    if not login_user:
        bot.send_message(message.chat.id, text="Вы не вошли в систему!")
    else:
        bot.send_message(message.chat.id, 'Отправьте фото нового расписания звонков.')
        bot.register_next_step_handler(message, handle_photo_rings)


def handle_photo_rings(message):
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path

            old_photo_path = os.path.join('photos', 'rings.jpeg')
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)

            downloaded_file = bot.download_file(file_path)

            image = Image.open(BytesIO(downloaded_file))
            image_path = os.path.join('photos', 'rings.jpeg')
            image.save(image_path, 'JPEG', quality=100)

            bot.send_message(message.chat.id, 'Расписание звонков успешно сохранено!')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, отправьте фото.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')


if __name__ == '__main__':
    bot.infinity_polling()
