import telebot
from telebot import types

with open("C:/token.txt", 'r') as file:
    TOKEN = file.read()
bot = telebot.TeleBot(token=TOKEN)


def corect_user(user_id, chat_id):
    with open("users.txt", 'r') as file:
        for ides in file:
            uid, cid = ides.strip().split()
            if user_id == uid and str(chat_id) == cid:
                return False
    return True


@bot.message_handler(commands=['start'])
def hi_message(message):
    nickname = message.from_user.username
    chat_id = message.chat.id
    if corect_user(nickname, chat_id):
        with open('users.txt', 'a') as file:
            file.write(f"{nickname} {chat_id}\n")

    keyboard = types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
    )
    functions_button = types.KeyboardButton(text="Функции")
    keyboard.add(functions_button)
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Это бот Школы №1 города Шимановска.",
        reply_markup=keyboard,
    )


@bot.message_handler(func=lambda message: message.text == 'Функции')
def functions(message):
    func_keyboard = types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True
    )

    buttons = [
        types.KeyboardButton(text="Расписание уроков"),
        types.KeyboardButton(text="Расписание звонков"),
        types.KeyboardButton(text="Изменения в расписании"),
        types.KeyboardButton(text="Информация о школе"),
        types.KeyboardButton(text="Для учителей"),
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
    functions(message)


@bot.message_handler(func=lambda message: message.text == "Расписание звонков")
def ring_schedule(message):
    with open('C:/Users/andre/OneDrive/Desktop/schoolbot/photoes/rings.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: message.text == "Расписание уроков")
def lessons_schedule(message):
    lessons_keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
    )
    lessons_keyboard.add(types.KeyboardButton(text='Назад'))
    for i in range(5, 12):
        lessons_keyboard.add(types.KeyboardButton(text=f"{i}-е классы"))
    bot.send_message(message.chat.id, text="Выберите класс", reply_markup=lessons_keyboard)


@bot.message_handler(func=lambda message: message.text == "5-е классы")
def schedule_5(message):
    pass


@bot.message_handler(func=lambda message: message.text == "6-е классы")
def schedule_6(message):
    pass


@bot.message_handler(func=lambda message: message.text == "7-е классы")
def schedule_7(message):
    pass


@bot.message_handler(func=lambda message: message.text in ["8-е классы",
                                                           "9-е классы",
                                                           "10-е классы",
                                                           "11-е классы"])
def schedule(message):
    class_to_photo = {
        "8-е классы": "8class.jpg",
        "9-е классы": "9class.jpg",
        "10-е классы": "10class.jpg",
        "11-е классы": "11class.jpg"
    }

    photo_filename = class_to_photo.get(message.text)
    if photo_filename:
        photo_path = f"C:/Users/andre/OneDrive/Desktop/schoolbot/photoes/{photo_filename}"
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.reply_to(message, "Расписание для этого класса не найдено.")


@bot.message_handler(func=lambda message: message.text == "11-е классы")
def schedule_11(message):
    with open("C:/Users/andre/OneDrive/Desktop/schoolbot/photoes/11class.jpg", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: message.text == "Информация о школе")
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


@bot.message_handler(func=lambda message: message.text == "Для учителей")
def teacher_login(message):
    bot.send_message(message.chat.id, text="Введите пароль")


@bot.message_handler(func=lambda message: message.text == "Изменения в расписании")
def schedule(message):
    with open('changes.txt', 'r', encoding='windows-1251') as file:
        changes = ""
        for el in file:
            changes += el
    bot.send_message(message.chat.id, changes)


@bot.message_handler(func=lambda message: message.text == "Добавить изменения в расписании")
def c_changes(message):
    sent = bot.send_message(message.chat.id, text="Отправьте изменения")
    bot.register_next_step_handler(sent, file_changes)
    with open('users.txt', 'r') as file:
        for elements in file:
            login = elements.strip().split()[1]
            bot.send_message(login, "Новые изменения добавлены")


def file_changes(message):
    with open('changes.txt', 'w') as file:
        file.write(str(message.text))
        bot.send_message(message.chat.id, text="Успешно!")


@bot.message_handler(func=lambda message: message.text == "Изменить пароль")
def change_password(message):
    sent = bot.send_message(message.chat.id, text="Введите текущий пароль")
    bot.register_next_step_handler(sent, verify_password)


def verify_password(message):
    try:
        with open('password.txt', 'r') as file:
            current_password = file.read().strip()
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл пароля не найден.")
        return

    if message.text == current_password:
        sent = bot.send_message(message.chat.id, "Введите новый пароль")
        bot.register_next_step_handler(sent, file_password_changes)
    else:
        bot.send_message(message.chat.id, "Неправильный пароль")


def file_password_changes(message):
    with open('password.txt', 'w') as file:
        file.write(str(message.text))
        bot.send_message(message.chat.id, text="Пароль успешно изменен!")


@bot.message_handler(func=lambda message: True)
def handle_login(message):
    t_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    t_buttons = [
        types.KeyboardButton(text="Изменить расписание(pass)"),
        types.KeyboardButton(text="Добавить изменения в расписании"),
        types.KeyboardButton(text="Изменить расписание звонков(pass)"),
        types.KeyboardButton(text="Изменить пароль"),
        types.KeyboardButton(text="Назад"),
    ]
    for but in t_buttons:
        t_keyboard.add(but)

    ACCOUNTS = []
    with open('password.txt', 'r') as file:
        for line in file:
            password = line
            ACCOUNTS.append(str(password))

    try:
        password = message.text
        if password in ACCOUNTS:
            bot.send_message(
                message.chat.id,
                text="Функции для сотрудников",
                reply_markup=t_keyboard
            )
        else:
            bot.send_message(message.chat.id, text="Неверный пароль")
    except ValueError:
        bot.send_message(message.chat.id, text="Введите логин и пароль в правильном формате")
    except Exception as e:
        bot.send_message(message.chat.id, text=f"Произошла ошибка: {e}")


if __name__ == '__main__':
    bot.infinity_polling()
