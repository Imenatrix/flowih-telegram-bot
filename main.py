
import logging
from typing import Dict
from dotenv import dotenv_values
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE,  TIMER = range(4)

reply_keyboard = [
    ["Modelo", "Preço"],
    ["Quilometragem", "Ano"],
    ["Tipo de Câmbio", "Tipo de Combustível"],
    ["Pronto"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """
        Formata as escolhas em formato de lista.
    """
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
        Começa a conversa e mostra o menu
    """
    await update.message.reply_text(
        f"Olá {update.message.from_user.first_name}!\n"
        "Sou o Flowih bot, ficarei reponsável pela sua configuração de filtros!",
        reply_markup=markup,
    )

    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
        Pede o input do usuario sobre o topico escolhido
    """
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Por favor, digite a sua preferêmcia para {text.lower()}: ")

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    interval = [
        ["1 hora", "10 minutos", "1 minuto"]
    ]
    await update.message.reply_text(
        "Agora, escolha o intervalo para ser notificado:",
        reply_markup=ReplyKeyboardMarkup(
            interval, one_time_keyboard=True, input_field_placeholder="Selecione o intervalo:"
        ),
    )
    return TIMER


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Cria uma job na fila
    """
    
    interval = 60
    if "hora" in update.message.text:
        interval = float(str(update.message.text).split(" ")[0]) * 60 * 60
    elif "minuto" in update.message.text:
        interval = float(str(update.message.text).split(" ")[0]) * 60
        
    chat_id = update.effective_message.chat_id
    try:
        if interval < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, interval, chat_id=chat_id, name=str(chat_id), data=interval)

        text = "Alarme salvo!"
        if job_removed:
            text += " Alarme antigo removido."
        await update.effective_message.reply_text(text)
        return ConversationHandler.END

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Ops! houve um erro, tente novamente!")

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Manda a notificação."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove a job e diz se foi removida."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a job a partir da escolha do user."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Comandos aceitos:\n"+
        "- /start: Começa o fluxo\n" +
        "- /help: Mostra comandos\n" +
        "- /unset: Remove notificações\n"
        )


def main() -> None:
    """Roda o bot"""
    config = dict(dotenv_values(".env"))
    
    # Cria o app com o token.
    application = Application.builder().token(config['TOKEN']).build()
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Modelo|Preço|Quilometragem|Tipo de Câmbio|Tipo de Combustível|Ano)$"), regular_choice
                ),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Pronto$")),
                    received_information,
                )
            ],
            TIMER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_timer)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Pronto$"), done)],
    )
    application.add_handler(CommandHandler("help", show_help))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()