import telebot
from telebot import types

import datos
from datos import *



bot = telebot.TeleBot(token)


bot.send_message(master, '🤖 El bot se ha actualizado correctamente: '+act_mss,disable_notification= True )




