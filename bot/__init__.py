from telegram import ReplyKeyboardMarkup, Update
from bot.utils import _show_help
from dotenv import dotenv_values
from bot.states import (
    entrypoint, 
    choosing_state,
    timer_state,
    typing_choice_state, 
    typing_reply_state,
    fallback_state
)
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
)


config = dict(dotenv_values(".env"))
CHOOSING, TYPING_REPLY, TYPING_CHOICE,  TIMER = range(4)
REPLY_DEFAULT=config["REPLY_DEFAULT"]  
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
gas_types = [["Gasolina", "Álcool"], ["Flex", "Diesel"], ["Híbrido", "Elétrico"]]

strwheel_markup = ReplyKeyboardMarkup(steering_wheel_types , one_time_keyboard=True, input_field_placeholder="Selecione a direção:")
gear_markup = ReplyKeyboardMarkup(gear_types , one_time_keyboard=True, input_field_placeholder="Selecione o câmbio:")
gas_markup = ReplyKeyboardMarkup(gas_types , one_time_keyboard=True, input_field_placeholder="Selecione o tipo de combustível:")
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
interval_markup = ReplyKeyboardMarkup(intervals,
                                      one_time_keyboard=True, 
                                      input_field_placeholder="Selecione o intervalo:")



def init(handlers=[]):
    app = Application.builder().token(config['TOKEN']).build()
        
    app.add_handler(CommandHandler("help", _show_help))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", entrypoint)],
        states={
            CHOOSING: choosing_state,
            TYPING_CHOICE: typing_choice_state,
            TYPING_REPLY: typing_reply_state,
            TIMER: timer_state
        },
        fallbacks=fallback_state,
    ))
        
    if len(handlers) > 0:
        for i in handlers:
            app.add_handler(i)

    # Run the bot until the user presses Ctrl-C
    app.run_polling()