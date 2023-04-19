
from bot import CHOOSING, markup
from bot.utils import _done_fallback, _regular_choice, _regular_reply
from utils import set_timer
from utils import show_error
from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

async def entrypoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def choosing_state():
    return [
        MessageHandler(
            filters.Regex("^(Modelo|Direção|Quilometragem|Tipo de Câmbio|Tipo de Combustível|Ano)$"), _regular_choice,
        ),
    ]
    
async def typing_choice_state():
    return  [
        MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")), _regular_choice
        )
    ]

async def typing_reply_state():
    return  [
        MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")),
            _regular_reply,
        )
    ]
    
async def timer_state():
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, set_timer)
    ]
    
async def fallback_state():
    return [
        MessageHandler(
            filters.Regex("^(Modelo|Direção|Quilometragem|Tipo de Câmbio|Tipo de Combustível|Ano)$"), _done_fallback,
        ),
    ]