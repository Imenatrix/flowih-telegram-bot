from dotenv import dotenv_values
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,

)
config = dict(dotenv_values(".env"))
REPLY_DEFAULT =  config["REPLY_DEFAULT"]  
    

steering_wheel_types = [["Hidráulica", "Elétrica"], ["Mecânica", "Assistida"]]
gear_types = [["Manual", "Automático"], ["Semi-Automático"]]
gas_types = [["Gasolina", "Álcool"], ["Flex", "Diesel"], ["Híbrido", "Elétrico"]]

strwheel_markup = ReplyKeyboardMarkup(steering_wheel_types , one_time_keyboard=True, input_field_placeholder="Selecione a direção:")
gear_markup = ReplyKeyboardMarkup(gear_types , one_time_keyboard=True, input_field_placeholder="Selecione o câmbio:")
gas_markup = ReplyKeyboardMarkup(gas_types , one_time_keyboard=True, input_field_placeholder="Selecione o tipo de combustível:")



async def validate_choices(reply:str, text:str,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Valida qual dos textos exibir, mostrando escolhas 
        pré-definas, ou liberando a escrita
    """
    if text.lower() == "ano" or text.lower() == "quilometragem" :
        new_reply = REPLY_DEFAULT + f" para {text.lower()} (números apenas): "
        try:
            await update.message.reply_text(new_reply)
        except Exception as e:
            show_error(update,context)
            return ConversationHandler.END
    elif text.lower() == "direção":
        try:
            await update.message.reply_text(reply,reply_markup=strwheel_markup)
        except Exception as e:
            show_error(update,context)
            return ConversationHandler.END
    elif "combustível" in text.lower():
        try:
            await update.message.reply_text(reply,reply_markup=gear_markup)
        except Exception as e:
            show_error(update,context)
            return ConversationHandler.END
    elif "câmbio" in text.lower():
        try:
            await update.message.reply_text(reply,reply_markup=gear_markup)
        except Exception as e:
            show_error(update,context)
            return ConversationHandler.END
    else:
        try:
            await update.message.reply_text(reply)    
        except Exception as e:
            show_error(update,context)
            return ConversationHandler.END
        
        

async def show_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ocorreu um erro inesperado!\n" +
        "Por favor, tente novamente com o comando /start \n" +
        "ou veja a lista de comandos com o comando /help.\n"
    )