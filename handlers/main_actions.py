import telebot
from telebot import types
from config import bot, admin_ids
import json
import datetime

class Client:

    def __init__(self) -> None:
        pass

    name: str
    age: int
    phone: str
    target: str
    train_type: str
    date: str
    time: str


@bot.message_handler(commands=['start'])
def first_step(message):
    bot.delete_message(message.chat.id, message.id)

    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["start_step"]

    markup = types.ForceReply(input_field_placeholder="Введите имя")

    client = Client()

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")

    bot.register_next_step_handler(msg, age_step, client)


def age_step(message, client: Client):
    client.name = message.text

    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["age_step"]

    markup = types.ForceReply(input_field_placeholder="Введите возраст")

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")

    bot.register_next_step_handler(msg, phone_step, client)


def phone_step(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    try:
        age = int(message.text)
        if age < 0:
            msg_txt = steps["age_error_step"]
            markup = types.ForceReply(input_field_placeholder="Введите возраст")

            msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")

            bot.register_next_step_handler(msg, phone_step, client)
            return
    except:
        msg_txt = steps["age_error_step"]
        markup = types.ForceReply(input_field_placeholder="Введите возраст")

        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")

        bot.register_next_step_handler(msg, phone_step, client)
        return
    
    client.age = age

    msg_txt = steps["phone_step"]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="7 999 999 99 99")
    markup.add(types.KeyboardButton(text="Оставить номер", request_contact=True))

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, target_step, client)

def target_step(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    check_type = message.content_type
    """
    if check_type != "contact":
        msg_txt = steps["phone_step_error"]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Оставить номер", request_contact=True))
        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup)
        bot.register_next_step_handler(msg, target_step, client)
        return
    """
    if check_type == "contact":
        client.phone = str(message.contact.phone_number)
    else:
        client.phone = str(message.text)

    msg_txt = steps["target_step"]

    markup = types.ForceReply(input_field_placeholder="Цель занятия")

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, train_type, client)


def train_type(message, client: Client):
    client.target = message.text
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["choose_train_type_step"]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите тип", one_time_keyboard=True)
    markup.add(types.KeyboardButton(text="Персональная"))
    markup.add(types.KeyboardButton(text="Групповая"))

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, type_buffer, client)
    

def type_buffer(message, client: Client):
    client.train_type = message.text

    if message.text == "Персональная":
        personal_choose_date(message, client)
    elif message.text == "Групповая":
        group_choose_date(message, client)
    else:
        with open('steps.json', 'r', encoding="UTF-8") as json_file:
            steps = json.load(json_file)

        msg_txt = steps["error_choose_type"]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите тип", one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Персональная"))
        markup.add(types.KeyboardButton(text="Групповая"))

        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(msg, type_buffer, client)
        return



def group_choose_date(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["group_type_choose_date"]

    markup = types.ForceReply(input_field_placeholder="15.01.2023")

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, group_choose_time, client)

def group_choose_time(message, client: Client):

    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    try:
        date = message.text.split(".")[::-1]
        day = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
        weekday = day.weekday()
        if weekday == 6:
            msg_txt = steps["group_date_error"]

            markup = types.ForceReply(input_field_placeholder="15.01.2023")

            msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
            bot.register_next_step_handler(msg, group_choose_time, client)
            return
    except:
        msg_txt = steps["group_date_error"]

        markup = types.ForceReply(input_field_placeholder="15.01.2023")

        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(msg, group_choose_time, client)
        return

    client.date = message.text

    msg_txt = steps["group_time_choose"]

    if weekday == 5:
        markup = types.ForceReply(input_field_placeholder="12:00")
    else:
        markup = types.ForceReply(input_field_placeholder="18:00")

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, group_buffer, client)

def group_buffer(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    date = client.date.split(".")[::-1]
    day = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    weekday = day.weekday()

    try:
        if ":" in message.text:
            time = message.text.split(":")
        elif "." in message.text:
            time = message.text.split(".")
        elif " " in message.text:
            time = message.text.split(" ")
        else:
            time = [message.text[0]+message.text[1], message.text[2]+message.text[3]]

        if len(time) != 2 or len(time[0]) != 2 or len(time[1]) != 2:
            msg_txt = steps["group_time_error"]

            if weekday == 5:
                markup = types.ForceReply(input_field_placeholder="12:00")
            else:
                markup = types.ForceReply(input_field_placeholder="18:00")

            msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
            bot.register_next_step_handler(msg, group_buffer, client)
            return

        if weekday == 5:
            if int(time[0]) < 12 or int(time[0]) > 14:
                msg_txt = steps["group_time_error"]

                if weekday == 5:
                    markup = types.ForceReply(input_field_placeholder="12:00")
                else:
                    markup = types.ForceReply(input_field_placeholder="18:00")

                msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
                bot.register_next_step_handler(msg, group_buffer, client)
                return
        else:
            if int(time[0]) < 18 or int(time[0]) > 21:
                msg_txt = steps["group_time_error"]

                if weekday == 5:
                    markup = types.ForceReply(input_field_placeholder="12:00")
                else:
                    markup = types.ForceReply(input_field_placeholder="18:00")

                msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
                bot.register_next_step_handler(msg, group_buffer, client)
                return
    except:
        msg_txt = steps["group_time_error"]

        if weekday == 5:
            markup = types.ForceReply(input_field_placeholder="12:00")
        else:
            markup = types.ForceReply(input_field_placeholder="18:00")

        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(msg, group_buffer, client)
        return


    client.time = client.time = time[0]+":"+time[1]

    end_quiz_step(message, client)


def personal_choose_date(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["personal_type_choose_date"]

    markup = types.ForceReply(input_field_placeholder="15.01.2023")

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, personal_choose_time, client)

def personal_choose_time(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)
    try:
        date = message.text.split(".")
        if len(date) != 3 or len(date[0]) != 2 or len(date[1]) != 2 or len(date[2]) != 4:
            msg_txt = steps["personal_date_error"]

            markup = types.ForceReply(input_field_placeholder="15.01.2023")

            msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
            bot.register_next_step_handler(msg, personal_choose_time, client)
            return
    except:
        msg_txt = steps["personal_date_error"]

        markup = types.ForceReply(input_field_placeholder="15.01.2023")

        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(msg, personal_choose_time, client)
        return

    client.date = message.text

    msg_txt = steps["personal_time_choose"]

    markup = types.ForceReply(input_field_placeholder="14:00")

    msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
    bot.register_next_step_handler(msg, personal_buffer, client)


def personal_buffer(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    try:
        if ":" in message.text:
            time = message.text.split(":")
        elif "." in message.text:
            time = message.text.split(".")
        elif " " in message.text:
            time = message.text.split(" ")
        else:
            time = [message.text[0]+message.text[1], message.text[2]+message.text[3]]
            
        if len(time) != 2 or len(time[0]) != 2 or len(time[1]) != 2:
            msg_txt = steps["personal_time_error"]

            markup = types.ForceReply(input_field_placeholder="14:00")

            msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
            bot.register_next_step_handler(msg, personal_buffer, client)
            return
    except:
        msg_txt = steps["personal_time_error"]

        markup = types.ForceReply(input_field_placeholder="14:00")

        msg = bot.send_message(message.chat.id, msg_txt, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(msg, personal_buffer, client)
        return

    client.time = time[0]+":"+time[1]

    end_quiz_step(message, client)



def end_quiz_step(message, client: Client):
    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)
    msg_txt = steps["end_quiz_step"]

    markup = types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, msg_txt, parse_mode="HTML", reply_markup=markup)

    admin_msg_txt = f"""НОВАЯ ЗАПИСЬ!

Имя клиента: {client.name}
Возраст клиента: {client.age}

Телефон клиента: {client.phone}

Цель занятия: {client.target}

Вид тренировки: {client.train_type}
 
Желаемая дата: {client.date}
Желаемое время: {client.time}
"""

    for admin in admin_ids:
        bot.send_message(admin, admin_msg_txt, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=["price"])
def show_price_step(message):
    bot.delete_message(message.chat.id, message.id)

    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["show_price_step"]

    bot.send_message(message.chat.id, msg_txt, parse_mode="HTML")


@bot.message_handler(commands=["address"])
def show_adress_step(message):
    bot.delete_message(message.chat.id, message.id)

    with open('steps.json', 'r', encoding="UTF-8") as json_file:
        steps = json.load(json_file)

    msg_txt = steps["show_adress_step"]

    bot.send_message(message.chat.id, msg_txt, parse_mode="HTML")
