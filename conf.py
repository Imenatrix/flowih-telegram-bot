from telegram import ReplyKeyboardMarkup
from dotenv import dotenv_values

config = dict(dotenv_values(".env"))

CHOOSING, TYPING_REPLY, TYPING_CHOICE,  TIMER = range(4)
REPLY_DEFAULT = config["REPLY_DEFAULT"]
url_filters = {}
reply_keyboard = [
    ["Modelo", "Direção"],
    ["Quilometragem", "Ano"],
    ["Tipo de Câmbio", "Tipo de Combustível"],
    ["Pronto"],
]
intervals = [["1 hora", "10 minutos", "1 minuto"]]


steering_wheel_types = [["Hidráulica", "Elétrica"], ["Mecânica", "Assistida"]]
gear_types = [["Manual", "Automático"], ["Semi-Automático"]]
gas_types = [["Gasolina", "Álcool"], [
    "Flex", "Diesel"], ["Híbrido", "Elétrico"]]

strwheel_markup = ReplyKeyboardMarkup(
    steering_wheel_types, one_time_keyboard=True, input_field_placeholder="Selecione a direção:")
gear_markup = ReplyKeyboardMarkup(
    gear_types, one_time_keyboard=True, input_field_placeholder="Selecione o câmbio:")
gas_markup = ReplyKeyboardMarkup(
    gas_types, one_time_keyboard=True, input_field_placeholder="Selecione o tipo de combustível:")
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
interval_markup = ReplyKeyboardMarkup(intervals,
                                      one_time_keyboard=True,
                                      input_field_placeholder="Selecione o intervalo:")
