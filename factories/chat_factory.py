
import logging

from dotenv import dotenv_values
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,

)

from utils.str_util import facts_to_str
from utils.timer_util import set_timer
from utils.validate_util import show_error, validate_choices

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
config = dict(dotenv_values(".env"))
REPLY_DEFAULT=config["REPLY_DEFAULT"]  

url_filters = {}

reply_keyboard = [
    ["Modelo", "Direção"],
    ["Quilometragem", "Ano"],
    ["Tipo de Câmbio", "Tipo de Combustível"],
    ["Pronto"],
]
intervals = [
    ["1 hora", "10 minutos", "1 minuto"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
interval_markup = ReplyKeyboardMarkup(intervals,
                                      one_time_keyboard=True, 
                                      input_field_placeholder="Selecione o intervalo:")

CHOOSING, TYPING_REPLY, TYPING_CHOICE,  TIMER = range(4)

class ChatFactory():
    def __init__(self):
        pass
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Começa a conversa e mostra o menu
        """
        try:
            await update.message.reply_text(
                f"Olá {update.message.from_user.first_name}!\n"
                "Sou o Flowih bot, ficarei reponsável pela sua configuração de filtros!",
                reply_markup=markup,
            )
        except Exception as e:
            show_error(update,context)
            return ConversationHandler.END

        return CHOOSING

    async def regular_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Pede o input do usuario sobre o topico escolhido
        """
        text = update.message.text
        context.user_data["choice"] = text
        reply= REPLY_DEFAULT +  f" para {text.lower()}: "
        await validate_choices(reply, text, update, context)
        return TYPING_REPLY
        
        
    async def received_information(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Guarda a info e pergunta a proxima
        """
        user_data = context.user_data
        text = update.message.text
        category = user_data["choice"]
        user_data[category] = text
        del user_data["choice"]

        await update.message.reply_text(
            "Filtros escolhidos:"
            f"{facts_to_str(user_data)}",
            reply_markup=markup,
        )

        return CHOOSING


    async def done(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            Mostra os filtros escolhidos.
        """
        
        user_data = context.user_data
        if "choice" in user_data:
            del user_data["choice"]

        await update.message.reply_text(
            f"Esses foram seus filtros: {facts_to_str(user_data)}",
            reply_markup=ReplyKeyboardRemove(),
        )
        await update.message.reply_text(
            "Agora, escolha o intervalo para ser notificado:",
            reply_markup=interval_markup,
        )
        return TIMER

