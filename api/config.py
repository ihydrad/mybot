#!/usr/bin/env python
# @ihydradbot

import os
import sys

NEW = 2
CUR = 1
OLD = 0

host = '192.168.88.8'
work_dir = os.path.dirname(__file__)
token = os.getenv("API_TOKEN")
ufanet_user = os.getenv("UNAME") or None
ufanet_pass = os.getenv("UPASS") or None
DEBUG = True if os.getenv("DEBUG") == "True" else False
period = 30 if not DEBUG else 1  # period minutes for site parse
delay = 10
zMAC = '00:01:2E:A2:09:2B'
users = [285917182, ]
job_add_threshold = 10000  # ~ 3 hours
keysIT = ["системный",
          "сетев",
          "it",
          "программист",
          "разработчик"
          ]

cityes = {
          'ufa': 'Уфа',
          'sterlitamak': 'Стерлитамак'
          }

cmd = """
    hibernate
    process (Отображает запущенные процессы на компьютере)
    shutdown
    poweroff
    reboot
    forceifhung
    logoff
    monitor1 (переключает монитор, аналогично WIN+P)
    monitor2
    monitorclone (Дублировать)
"""


def addToPATH(folder):
    pathname, _ = os.path.split(os.path.abspath(__file__))     
    sys.path.append(os.path.join(pathname, folder))


#apihelper.proxy = {'https': 'socks5://127.0.0.1:9050'}


# @bot.message_handler(content_types=['document', 'audio'])
# def handle_docs_audio(message):
# 	pass

# @bot.message_handler(regexp="SOME_REGEXP")
# def handle_message(message):
# 	pass

# @bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
# def handle_text_doc(message):
# 	pass

