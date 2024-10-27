import telebot  
from telebot import types
import re
import random

# Токен для доступа к боту
TOKEN = '8106633598:AAFOzRyjhSHwlhcyW0tw_RRCyRuc3nxWZSI'
bot = telebot.TeleBot(TOKEN)

user_data = {}  # Словарь для временного хранения данных, которые вводит пользователь

# Функция для проверки правильности формата даты
def is_valid_date(date_text):
    # Формат должен быть ДД.ММ.ГГГГ
    return bool(re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_text))

# Функция для проверки правильности формата года
def is_valid_year(year_text):
    # Год должен быть в формате ГГГГ
    return bool(re.match(r"^\d{4}$", year_text))

# Функция заглушка
def make_prediction(data):
    # Случайный выбор результата
    prediction = random.choice(["Человек выйдет на пенсию досрочно", "Человек не выйдет на пенсию досрочно"])
    return prediction

# Старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет, я бот, команды 'ByteBusters' специально разработанный для ЦП. "
        "На основе ваших данных мы можем предсказать, выйдете ли вы на пенсию раньше срока, а также почему в частности.\n"
    )

    # Создаем кнопки для выбора формата ввода данных
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Загрузить CSV файл"), types.KeyboardButton("Ввести данные вручную"))
    bot.send_message(message.chat.id, "Выберите формат:", reply_markup=markup)

# Обработчик выбора формата (CSV или вручную)
@bot.message_handler(func=lambda message: message.text in ["Загрузить CSV файл", "Ввести данные вручную"])
def handle_format_selection(message):
    if message.text == "Загрузить CSV файл":

        bot.send_message(message.chat.id, "CSV файл пока не доступен.")
    else:
        # Если пользователь выбрал ввод данных вручную, очищаем данные и задаем вопросы
        user_data.clear()  # Очищаем данные, если это повторный ввод
        bot.send_message(message.chat.id, "Пожалуйста, ответьте на следующие вопросы.")
        ask_next_question(message.chat.id)

# Функция для поочередного задания вопросов пользователю
def ask_next_question(chat_id):


    if 'accnt_bgn_date' not in user_data:
        bot.send_message(chat_id, "Дата заключения договора (формат ответа: ДД.ММ.ГГГГ):")
    elif 'brth_yr' not in user_data:
        bot.send_message(chat_id, "Год рождения клиента (формат ответа: ГГГГ):")
    elif 'gndr' not in user_data:
        # Кнопки для выбора пола
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Мужской"), types.KeyboardButton("Женский"))
        bot.send_message(chat_id, "Пол клиента (формат ответа: Мужской/Женский):", reply_markup=markup)
    elif 'region' not in user_data:
        bot.send_message(chat_id, "Регион (формат ответа: Тюменская область):")
    elif 'city' not in user_data:
        bot.send_message(chat_id, "Город (формат ответа: Москва):")
    elif 'assgn_npo' not in user_data:
        # Кнопки для ответа "Да" или "Нет"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
        bot.send_message(chat_id, "Является ли клиент правопреемником по договору НПО? (формат ответа: Да/Нет)", reply_markup=markup)
    elif 'assgn_ops' not in user_data:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
        bot.send_message(chat_id, "Является ли клиент правопреемником по договору ОПС? (формат ответа: Да/Нет)", reply_markup=markup)
    elif 'lk' not in user_data:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
        bot.send_message(chat_id, "Зарегистрирован ли клиент в личном кабинете? (формат ответа: Да/Нет)", reply_markup=markup)
    else:

        confirm_data(chat_id)

# Обработчик текстовых ответов на вопросы
@bot.message_handler(func=lambda message: True)
def handle_answers(message):
    chat_id = message.chat.id
    text = message.text.strip().lower()

    # Проверяем каждый вопрос и сохраняем ответ, если формат правильный
    if 'accnt_bgn_date' not in user_data:
        if is_valid_date(text):
            user_data['accnt_bgn_date'] = text
        else:
            bot.send_message(chat_id, "Некорректный формат даты. Укажите дату в формате ДД.ММ.ГГГГ.")
            return
    elif 'brth_yr' not in user_data:
        if is_valid_year(text):
            user_data['brth_yr'] = text
        else:
            bot.send_message(chat_id, "Некорректный формат года. Введите год рождения клиента в формате ГГГГ.")
            return
    elif 'gndr' not in user_data:
        if text in ["мужской", "женский"]:
            user_data['gndr'] = text
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите пол клиента с помощью кнопок.")
            return
    elif 'region' not in user_data:
        user_data['region'] = text
    elif 'city' not in user_data:
        user_data['city'] = text
    elif 'assgn_npo' not in user_data:
        if text in ["да", "нет"]:
            user_data['assgn_npo'] = text
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите ответ с помощью кнопок 'Да' или 'Нет'.")
            return
    elif 'assgn_ops' not in user_data:
        if text in ["да", "нет"]:
            user_data['assgn_ops'] = text
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите ответ с помощью кнопок 'Да' или 'Нет'.")
            return
    elif 'lk' not in user_data:
        if text in ["да", "нет"]:
            user_data['lk'] = text
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите ответ с помощью кнопок 'Да' или 'Нет'.")
            return


    ask_next_question(chat_id)

# Функция для подтверждения введенных данных
def confirm_data(chat_id):

    confirmation_text = (
        "Вы ввели следующие данные:\n"
        f"Дата заключения договора: {user_data.get('accnt_bgn_date')}\n"
        f"Год рождения клиента: {user_data.get('brth_yr')}\n"
        f"Пол клиента: {user_data.get('gndr')}\n"
        f"Регион: {user_data.get('region')}\n"
        f"Город: {user_data.get('city')}\n"
        f"Правопреемник по договору НПО: {user_data.get('assgn_npo')}\n"
        f"Правопреемник по договору ОПС: {user_data.get('assgn_ops')}\n"
        f"Зарегистрирован в личном кабинете: {user_data.get('lk')}\n\n"
        "Все ли верно?"
    )

    # Кнопки для подтверждения или отказа
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Да", callback_data="confirm_yes"))
    markup.add(types.InlineKeyboardButton("Нет", callback_data="confirm_no"))

    # Отправляем сообщение с подтверждением
    bot.send_message(chat_id, confirmation_text, reply_markup=markup)

# Обработчик для подтверждения данных
@bot.callback_query_handler(func=lambda call: call.data in ["confirm_yes", "confirm_no"])
def handle_confirmation(call):
    if call.data == "confirm_yes":
        # Генерация случайного предсказания
        prediction = make_prediction(user_data)
        bot.send_message(call.message.chat.id, f"Предсказание: {prediction}")
    else:
        bot.send_message(call.message.chat.id, "Пожалуйста, введите данные заново.")
        user_data.clear()
        ask_next_question(call.message.chat.id)

# Запуск бота
bot.polling()
