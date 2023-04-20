import time
import sched
from telegram import ReplyKeyboardMarkup
from dotenv import dotenv_values

'''
    Arquivo de confs globais
'''

config = dict(dotenv_values(".env"))


# globais do timer
current_process = None
current_interval = 0

CHOOSING, TYPING_REPLY, TYPING_CHOICE,  TIMER = range(4)
REPLY_DEFAULT = config["REPLY_DEFAULT"]


user_info = {
    "interval": 0
}


'''
    Types para markups
'''

menu_types = [
    ["Modelo", "Direção"],
    ["Quilometragem", "Ano"],
    ["Tipo de Câmbio", "Tipo de Combustível"],
    ["Pronto"],
]
gas_types = [
    ["Gasolina", "Álcool"],
    ["Flex", "Diesel"],
    ["Híbrido", "Elétrico"]
]
interval_types = [["1 hora", "10 minutos", "1 minuto"]]
strwheel_types = [["Hidráulica", "Elétrica"], ["Mecânica", "Assistida"]]
gear_types = [["Manual", "Automático"], ["Semi-Automático"]]


'''
    Markups
'''

markup = ReplyKeyboardMarkup(menu_types, one_time_keyboard=True)
interval_markup = ReplyKeyboardMarkup(interval_types, one_time_keyboard=True)
strwheel_markup = ReplyKeyboardMarkup(strwheel_types, one_time_keyboard=True)
gear_markup = ReplyKeyboardMarkup(gear_types, one_time_keyboard=True)
gas_markup = ReplyKeyboardMarkup(gas_types, one_time_keyboard=True)
