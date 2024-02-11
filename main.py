import psycopg2
import telebot
from telebot import types
from admin import token, password


conn = psycopg2.connect(
    database="pro_it_bot",
    user="postgres",
    password=password,
    host="localhost",
    port="5432"
)


cursor = conn.cursor()

TOKEN = token
bot = telebot.TeleBot(TOKEN)
admin_id = 525820323

courses = {
    'Unity': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'JavaScript': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'Робототехника': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'Scratch': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'WEB': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'UI/UX': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'Illustrator': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'C#': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
    'ASP.NET': [
        'Урок 1: https://example.com/урок1',
        'Урок 2: https://example.com/урок2',
        'Урок 3: https://example.com/урок3'
    ],
}


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    sql = "SELECT user_id FROM users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        sql = "INSERT INTO users (user_id, first_name, last_name) VALUES (%s, %s, %s)"
        values = (user_id, first_name, last_name)
        cursor.execute(sql, values)
        conn.commit()

    markup = types.InlineKeyboardMarkup(row_width=2)

    course_btn = types.InlineKeyboardButton("Курсы", callback_data="courses")
    markup.add(course_btn)

    website_btn = types.InlineKeyboardButton("Наш сайт", url="https://pro-it.school/")
    social_media_btn = types.InlineKeyboardButton("Мы в соцсетях",
                                            url="https://www.instagram.com/pro_it.school?igsh=MXU0Z2JyNnowN3kyNw==")

    markup.add(website_btn, social_media_btn)

    bot.send_message(message.chat.id, 'Выберите опцию:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "courses")
def choose_course(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    course_btns = [types.InlineKeyboardButton(course, callback_data=course) for course in courses.keys()]
    markup.add(*course_btns)

    menu_btn = types.InlineKeyboardButton("Меню", callback_data="menu")
    markup.add(menu_btn)

    bot.send_message(call.message.chat.id, 'Выберите курс:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in courses.keys())
def send_course_materials(call):
    course = call.data
    materials = courses[course]
    response = f'Материалы по курсу "{course}":\n\n' + '\n'.join(materials)

    back_btn = types.InlineKeyboardButton("Назад", callback_data="courses")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(back_btn)

    bot.send_message(call.message.chat.id, response, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "back")
def go_back(call):
    welcome(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def go_to_menu(call):
    welcome(call.message)


@bot.message_handler(func=lambda message: message.from_user.id == admin_id)
def handle_admin_message(message):
    admin_message = message.text

    sql = "SELECT user_id FROM users"
    cursor.execute(sql)
    users = cursor.fetchall()

    for user in users:
        bot.send_message(user[0], admin_message)

    bot.reply_to(message, "Сообщение отправлено всем пользователям!")


bot.polling(non_stop=True)
