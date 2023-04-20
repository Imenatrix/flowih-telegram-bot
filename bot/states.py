
from conf import (
    CHOOSING,
    markup
)
from bot.utils import done_fallback, regular_choice, regular_reply, set_timer, show_error
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
        show_error(update, context)
        return ConversationHandler.END

    return CHOOSING


def choosing_state():
    return [
        MessageHandler(
            filters.Regex(
                "^(Modelo|Direção|Quilometragem|Tipo de Câmbio|Tipo de Combustível|Ano)$"), regular_choice,
        ),
    ]


def typing_choice_state():
    return [
        MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex(
                "^Pronto$")), regular_choice
        )
    ]


def typing_reply_state():
    return [
        MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")),
            regular_reply,
        )
    ]


def timer_state():
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, set_timer)
    ]


def fallback_state():
    return [
        MessageHandler(
            filters.Regex("^Pronto$"), done_fallback,
        ),
    ]
