#!/home/adr/miniconda3/envs/botenv/bin/python3.10
import config
import requests
import schedule
import telebot
import threading
from time import sleep

from anketa.runner import send_my_profile_for
from customlog import LoggerFile
from telebot import types
from jobParser import JobParser, JobParserDB
from wakeonlan import send_magic_packet
from graph import build_hist_year


bot = telebot.TeleBot(config.token)


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        return message.chat.id in config.users


bot.add_custom_filter(IsAdmin())

@bot.message_handler(is_admin=True, commands=['help', 'start'])
def handle_help(message):

    markup = types.ReplyKeyboardMarkup()

    itembtn1 = types.KeyboardButton('wakeup')
    itembtn2 = types.KeyboardButton('shutdown')
    itembtn3 = types.KeyboardButton('hibernate')
    itembtn4 = types.KeyboardButton('status')

    markup.row(itembtn4, itembtn1)
    markup.row(itembtn2, itembtn3)

    bot.reply_to(message, "r2d2 is online!", reply_markup=markup)


@bot.message_handler(is_admin=True, func=lambda message: True)
def botfunc(message) -> str:

    if message.text.lower() == 'wakeup':
        send_magic_packet(config.zMAC)
        return bot.send_message(config.users[0], 'PC wakeup...')

    if message.text.lower() == 'status':
        try:
            requests.get("http://{}:8585/".format(config.host))
            staet_msg = "PC is online!"
        except:
            staet_msg = "PC is offline"

        return bot.send_message(config.users[0], staet_msg)

    if message.text.lower() == 'jobs':
        graph = build_hist_year()
        return bot.send_photo(config.users[0], graph)

    url = f"http://{config.host}:8585/?cmd={message.text.lower()}"

    try:
        resp_text = requests.get(url).text
        resp_msg = f'{message.text.lower()} - OK!\n Response {resp_text}'
    except Exception as e:
        resp_msg = str(e)

    return bot.send_message(config.users[0], resp_msg)


@bot.message_handler(commands=['help', 'start'])
def handle_help(message):
    bot.reply_to(message, "У вас нет прав для работы с этим ботом или его разделом.")


def fill_profile(job_name):
    msg = f"Заполняем анкету: {job_name}"
    shedule_log.logger.debug(msg)
    bot.send_message(config.users[0], msg)

    try:
        res_msg = send_my_profile_for(job_name)
    except Exception as e:
        res_msg = str(e)

    shedule_log.logger.debug(res_msg)
    bot.send_message(config.users[0], res_msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    city, id = call.data.split(":")

    db = JobParserDB(city)
    job_name = db.db_get_name_by_id(id)[0]

    bot.answer_callback_query(call.id,
            f'Отправляем анкету:"{job_name}"')

    t_profile = threading.Thread(target=fill_profile, args=(job_name,))
    t_profile.start()


def send_fmt(obj: JobParser):

    markup = types.InlineKeyboardMarkup()
    msg = f"{obj}. Заполнить анкету на вакансию:\n"
    cnt = 0
    button_list = list()

    for id, fmt_job in obj.get_fmt_jobs():
        cnt += 1
        msg += f"{cnt}. {fmt_job}\n"
        button = types.InlineKeyboardButton(
                            str(cnt),
                            callback_data=f"{obj.city}:{id}"
                            )
        button_list.append(button)

    markup.row(*button_list)
    bot.send_message(config.users[0], f"{msg}\n", reply_markup=markup, parse_mode="HTML")


def updater(parsers: list):
    for parser in parsers:
        parser: JobParser
        if parser.update(filter=config.keysIT):
            send_fmt(parser)


def shedule_ping():
    shedule_log.logger.debug("sheduller working")


def botScheduler():
    parsers = [JobParser(city) for city in ["ufa", "Sterlitamak"]]

    schedule.every(config.period).minutes.do(updater, parsers)
    schedule.every(config.period).minutes.do(shedule_ping)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    shedule_log = LoggerFile("sheduller")
    tbotScheduler = threading.Thread(target=botScheduler)
    tbotScheduler.start()
    bot.infinity_polling()
